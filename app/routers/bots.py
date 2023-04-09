from fastapi import APIRouter

from pydantic import BaseModel
import logging
from app.services.chatbot import ComfortBot
from app.services.kakao_api import skillTemplate

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s:%(message)s",
    level=logging.INFO,
    filename="logs/log.log",
    filemode="w",
)
logger = logging.getLogger(__name__)

class ComfortBotRequest(BaseModel):
    query: str

comfort_bot = ComfortBot()

@router.post("/comfort")
async def comfort(request: ComfortBotRequest):
    answer = comfort_bot.reply(request.query)
    return {"A": answer}

@router.post("/kakao")
async def chatbotAPI(request: ComfortBotRequest):
    try:
        result = comfort_bot.reply(request.query)
        return skillTemplate.send_response(result)

    except Exception as e:
        result = f"에러 : {e}"
        logger.info(result)
        return skillTemplate.send_response(result)