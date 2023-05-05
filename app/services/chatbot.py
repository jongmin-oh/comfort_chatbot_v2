from typing import List, Tuple, Final
import numpy as np
import pandas as pd

from sqlalchemy import select
from app.config import paths
from app.utility.utils import mean_pooling, top_k_sampling, clean
from app.services.pingpong_api import ping_pong_reply
from app.services.clova_api import CompletionExecutor
from app.db.save import save_reply_log
from app.db.models import Answer
from app.connections import postgres
from app.services import Singleton

import faiss
from onnxruntime import InferenceSession
from transformers import AutoTokenizer


class ComfortBot(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.base_model = "snunlp/KR-SBERT-V40K-klueNLI-augSTS"
        self.faiss_path = paths.FAISS_DIR.joinpath("faiss_onnx_uint8.index")
        self.onnx_path = paths.MODEL_DIR.joinpath("sbert-model_uint8.onnx")
        self.faiss_index = faiss.read_index(str(self.faiss_path))
        self.sess = InferenceSession(
            str(self.onnx_path), providers=["CPUExecutionProvider"]
        )

        self.tokenizer = AutoTokenizer.from_pretrained(self.base_model)
        self.clova = CompletionExecutor()
        self._THREADHOLD: Final[int] = 0.8

    def embedding_query(self, query: str, normalize_embeddings=False) -> np.ndarray:
        # user turn sequence to query embedding
        model_inputs = self.tokenizer(query, return_tensors="pt")
        inputs_onnx = {k: v.cpu().detach().numpy() for k, v in model_inputs.items()}
        sequence = self.sess.run(None, inputs_onnx)
        query_embedding = mean_pooling(sequence, inputs_onnx["attention_mask"])[0][0]

        if normalize_embeddings:
            query_embedding = query_embedding / np.linalg.norm(query_embedding)

        return query_embedding.numpy()

    def semantic_search(
        self, query_embedding: np.ndarray, top_k: int = 5
    ) -> Tuple[List, List]:
        distance, index = self.faiss_index.search(query_embedding, top_k)

        _sorted = sorted(
            zip(index[0].tolist(), distance[0].tolist()), key=lambda x: x[0]
        )
        index = [x[0] for x in _sorted]
        distance = [x[1] for x in _sorted]

        return index, distance

    def fetch_data(self, index: List[int]) -> Tuple[str, str]:
        index = [i + 1 for i in index]
        with postgres.engine.connect() as conn:
            table = Answer.__table__
            query = select(table.c.user, table.c.system).where(table.c.id.in_(index))
            res = conn.execute(query)
            return res.fetchall()

    def reply(self, query: str) -> str:
        cleaned = clean(query)
        if cleaned == "":
            return "헤헤..."

        query_embedding = self.embedding_query(query, normalize_embeddings=True)
        query_embedding = query_embedding.reshape(1, -1)
        I, D = self.semantic_search(query_embedding)

        fetchd: Tuple = self.fetch_data(I)
        user, system = zip(*fetchd)

        result = pd.DataFrame({"question": user, "answers": system, "distance": D})
        result = result[result["distance"] > self._THREADHOLD]

        if result.empty:  # ping-pong
            if len(cleaned) < 8:
                response = ping_pong_reply(query)
                save_reply_log(query, response, "2")
                return response
            else:  # clova
                response = self.clova.reply(query)
                save_reply_log(query, response, "3")
                return response
        else:  # semantic search
            pick_idx = top_k_sampling(result["distance"].tolist(), weight=3)
            response = result.iloc[pick_idx]["answers"]
            response = response.replace("00님", "선생님")
            save_reply_log(query, response, "1")
            return response


if __name__ == "__main__":
    bot = ComfortBot()
    print(bot.reply("너 누구야??"))
