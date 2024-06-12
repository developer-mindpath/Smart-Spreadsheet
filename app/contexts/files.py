from openai import AsyncOpenAI

from app.common.constants.common import DEFAULT_TIMEOUT
from app.configs.dotenv import Config
from app.controllers.files import FilesController
from app.repositories.assistant import AssistantRepository
from app.repositories.files import FilesRepository
from app.services.files import FilesService


class FilesContext:

    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key= Config.OPENAI_API_KEY, timeout=DEFAULT_TIMEOUT)
        self.assistant_repository = AssistantRepository(self.client)
        self.files_repository = FilesRepository(self.client)
        self.files_service = FilesService(self.files_repository, self.assistant_repository)
        self.file_controller = FilesController(self.files_service)
