from fastapi import HTTPException

from app.common.constants.messages import ERROR_ENCOUNTERED_MSG
from app.common.helpers.logger import logger
from app.common.types.user_request import UserRequest
from app.services.assistant import AssistantService


class AssistantController:

    def __init__(self, assistant_service: AssistantService) -> None:
        self.__assistant_service = assistant_service

    async def handle_request(self, user_request: UserRequest) -> str:
        try:
            response = await self.__assistant_service.get_response(user_request=user_request)
            return response
        except Exception as ex:
            logger.exception(ex)
            raise HTTPException(status_code=500, detail=ERROR_ENCOUNTERED_MSG)

