from fastapi import UploadFile

from app.common.helpers.logger import logger
from app.services.files import FilesService


class FilesController:

    def __init__(self, files_service: FilesService) -> None:
        self.__files_service = files_service

    async def upload_files(self, assistant_id: str, files: list[UploadFile]) -> list[str]:
        try:
            file_ids = await self.__files_service.upload_files(assistant_id=assistant_id, files=files)
            return file_ids
        except Exception as ex:
            logger.exception(ex)
            raise Exception(detail=ex.__str__(), status_code=400)
