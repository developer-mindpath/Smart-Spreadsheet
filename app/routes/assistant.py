from typing import Annotated

from fastapi import APIRouter, File, Query, UploadFile

from app.common.constants.messages import UPLOAD_FILE_MESSAGE
from app.common.types.user_request import UserRequest
from app.contexts.assistant import AssistantContext
from app.contexts.files import FilesContext
from app.utils.local_cache import LocalCache

router = APIRouter(prefix="/api")


@router.post("/files/upload", tags=["Files"])
async def upload_file(files: Annotated[list[UploadFile], File()]) -> str:
    assistant_id = LocalCache.get_value("assistant_id")
    files = await FilesContext().file_controller.upload_files(assistant_id=assistant_id, files=files)
    LocalCache.set_value(key="file_ids", value=files)
    return "Files uploaded successfully"

@router.post("/assistant/ask", tags=["Assistant"])
async def ask_question(question: str = Query()) -> str:
    assistant_id = LocalCache.get_value("assistant_id")
    thread_id = LocalCache.get_value("thread_id")
    files = LocalCache.get_value("file_ids")
    if not files:
        return UPLOAD_FILE_MESSAGE
    user_request = UserRequest(query=question, assistant_id=assistant_id, thread_id=thread_id)
    response = await AssistantContext().assistant_controller.handle_request(user_request=user_request)
    return response
