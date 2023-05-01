import pytest

from httpx import AsyncClient

host = "http://localhost:8100/"


@pytest.mark.asyncio
async def test_chatbot():
    async with AsyncClient(base_url=host) as ac:
        body = {"query": "안녕"}
        response = await ac.post("/chatbot/comfort", json=body)
        assert response.status_code == 200
        # assert response.json() == {"Q": "테스트", "A": "성공", "idx": 11}
