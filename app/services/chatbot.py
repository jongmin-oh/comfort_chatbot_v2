from typing import List, Tuple
import numpy as np
import pandas as pd

from sqlalchemy import select
from app.config import paths
from app.utility.utils import mean_pooling, top_k_sampling, clean
from app.services.pingpong_api import ping_pong_reply
from app.db.save import save_reply_log
from app.db.models import Answer
from app.connections import postgres

import faiss
from onnxruntime import InferenceSession
from transformers import AutoTokenizer

class ComfortBot:
    def __init__(self):
        self.base_model = "snunlp/KR-SBERT-V40K-klueNLI-augSTS"
        self.faiss_path = paths.FAISS_DIR.joinpath("faiss_onnx_uint8.index")
        self.onnx_path = paths.MODEL_DIR.joinpath("sbert-model_uint8.onnx")
        self.faiss_index = faiss.read_index(str(self.faiss_path))
        self.sess = InferenceSession(str(self.onnx_path),
                            providers=["CPUExecutionProvider"])
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.base_model)
        
    def embedding_query(self, query: str, normalize_embeddings=False) -> np.ndarray:
        # user turn sequence to query embedding
        model_inputs = self.tokenizer(query, return_tensors="pt")
        inputs_onnx = {k: v.cpu().detach().numpy()
                    for k, v in model_inputs.items()}
        sequence = self.sess.run(None, inputs_onnx)
        query_embedding = mean_pooling(
            sequence, inputs_onnx["attention_mask"])[0][0]

        if normalize_embeddings:
            query_embedding = query_embedding / \
                np.linalg.norm(query_embedding)

        return query_embedding.numpy()
    
    def semantic_search(self, query_embedding: np.ndarray, top_k: int = 5) -> Tuple[List, List]:
        # query embedding to semantic search
        D, I = self.faiss_index.search(query_embedding, top_k)
        
        # sort for db fetch
        _sorted = sorted(zip(I[0].tolist() , D[0].tolist()), key=lambda x: x[0])
        I = [x[0] for x in _sorted]
        D = [x[1] for x in _sorted]
        
        return I, D
    
    def db_fetch(self, index: List[int]) -> Tuple[str, str]:
        index = [i+1 for i in index]
        with postgres.engine.connect() as conn:
            table = Answer.__table__
            query = select(table.c.user, table.c.system).where(table.c.id.in_(index))
            res = conn.execute(query)
            return res.fetchall()
    
    def reply(self, query: str, threshold: float = 0.75) -> str:
        
        cleaned = clean(query)
        if cleaned == "":
            return "무슨 뜻이에요? 이해 못한게 아니라 진짜 궁금해서 물어보는 거예요."
        
        query_embedding = self.embedding_query(query, normalize_embeddings=True)
        query_embedding = query_embedding.reshape(1, -1)
        I, D = self.semantic_search(query_embedding)
        
        fetchd: Tuple = self.db_fetch(I)
        user, system = zip(*fetchd)
        
        result = pd.DataFrame({"question": user ,"answers": system, "distance": D})
        result = result[result['distance'] > threshold]
        
        if result.empty: # ping-pong
            response = ping_pong_reply(query)
            save_reply_log(query, response, "2")
            return response
        else: # semantic search
            pick_idx = top_k_sampling(result['distance'].tolist(), weight=3)
            response = result.iloc[pick_idx]['answers']
            # response = result.iloc[pick_idx]['system']
            response = response.replace("00님", "선생님")
            save_reply_log(query, response, "1")
            return response

if __name__ == "__main__":
    bot = ComfortBot()
    print(bot.reply("너 누구야??"))
    