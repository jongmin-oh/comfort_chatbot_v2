import json
import http.client

from app.config import paths
from app.config import clova_settings as cs


class CompletionExecutor:
    def __init__(self):
        self.prompt: str = open(
            paths.PROMPT_DIR.joinpath("clova.txt"), encoding="utf-8"
        ).read()

    def _send_request(self, completion_request):
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "X-NCP-CLOVASTUDIO-API-KEY": cs.CLOVA_API_KEY,
            "X-NCP-APIGW-API-KEY": cs.CLOVA_API_PRIVATE_KEY,
            "X-NCP-CLOVASTUDIO-REQUEST-ID": cs.CLOVA_REQUEST_ID,
        }

        conn = http.client.HTTPSConnection(cs.CLOVA_HOST)
        conn.request(
            "POST",
            "/testapp/v1/completions/LK-D2",
            json.dumps(completion_request),
            headers,
        )
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding="utf-8"))
        conn.close()
        return result

    def _execute(self, completion_request):
        res = self._send_request(completion_request)
        if res["status"]["code"] == "20000":
            return res["result"]["text"]
        else:
            return "Error"

    def reply(self, query):
        preset_text = self.prompt + query
        request_data = {
            "text": preset_text,
            "maxTokens": 128,
            "temperature": 0.2,
            "topK": 0,
            "topP": 0.8,
            "repeatPenalty": 5.0,
            "start": "\n오복이:",
            "restart": "",
            "stopBefore": ["\n", "오복이", "내담자"],
            "includeTokens": False,
            "includeAiFilters": True,
            "includeProbs": True,
        }
        response_text = self._execute(request_data)
        answer = response_text.split("\n오복이:")[-1]
        answer = answer.replace("당신", "선생님")
        answer = answer.replace("내가", "제가")
        answer = answer.replace("내담자님", "선생님")
        return answer.strip()


clova = CompletionExecutor()

if __name__ == "__main__":
    completion_executor = CompletionExecutor()
    completion_executor.reply("안녕하세요")
