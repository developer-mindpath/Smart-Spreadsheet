from openai import AsyncOpenAI
from openai._types import FileTypes
from openai.types.file_deleted import FileDeleted
from openai.types.file_object import FileObject


class FilesRepository:

    def __init__(self, client: AsyncOpenAI) -> None:
        self.client = client

    async def upload_file(self, file: FileTypes) -> FileObject:
        upload_file = await self.client.files.create(file=file, purpose="assistants")
        return upload_file

    async def retrieve_file_content(self, file_id: str) -> bytes:
        file_content = await self.client.files.content(file_id=file_id)
        return file_content.content

    async def retrieve_file(self, file_id: str) -> FileObject:
        file_content = await self.client.files.retrieve(file_id=file_id)
        return file_content

    async def delete_file(self, file_id: str) -> FileDeleted:
        delete_file = await self.client.files.delete(file_id=file_id)
        return delete_file

    async def list_files(self) -> list[FileObject]:
        delete_file = await self.client.files.list()
        return delete_file.data
