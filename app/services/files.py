import os

import pandas as pd
from fastapi import HTTPException, UploadFile

from app.common.constants.messages import ASSISTANT_INSTRUCTIONS
from app.common.helpers.extractor import ExcelDataWizard
from app.repositories.assistant import AssistantRepository
from app.repositories.files import FilesRepository


class FilesService:

    def __init__(self, files_repository: FilesRepository, assistant_repository: AssistantRepository) -> None:
        self._files_repository = files_repository
        self.__assistant_repository = assistant_repository

    async def upload_files(self, assistant_id: str, files: list[UploadFile]) -> list[str]:
        file_ids = await self._get_file_ids(files=files)
        await self.__assistant_repository.update_assistant(
            assistant_id=assistant_id,
            model="gpt-4o",
            name="ExcelGenie",
            temperature=0.2,
            instructions=ASSISTANT_INSTRUCTIONS,
            tools=[{"type": "code_interpreter"}],
            tool_resources={"code_interpreter": {"file_ids": file_ids}})
        return file_ids

    async def _get_file_ids(self, files: list[UploadFile]) -> list[str]:
        file_ids = []
        for file in files:
            filename = file.filename
            if not filename.endswith(".xlsx"):
                raise HTTPException(detail=f"{filename} is not an excel file", status_code=400)
            file_path = f"./app/data/{filename.replace(' ', '_')}"
            with open(file_path, "wb") as buffer:
                buffer.write(file.file.read())
            extractor = ExcelDataWizard(file_path)
            extractor.retrieve_tables()
            dfs = extractor.convert_to_dfs()
            with pd.ExcelWriter(file_path) as writer:
                sheet_names = [f'Table_{count}' for count in range(1, len(dfs)+1)]
                for df, sheet_name in zip(dfs, sheet_names):
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            uploaded_file = await self._files_repository.upload_file(file=open(file_path, "rb"))
            file_ids.append(uploaded_file.id)
            if os.path.exists(file_path):
                os.remove(file_path)
        return file_ids
