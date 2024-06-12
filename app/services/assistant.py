import time

from openai import NOT_GIVEN, AsyncOpenAI
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads import Run

from app.common.constants.common import RUN_STATUSES, TRUNCATION_STRATEGY
from app.common.constants.messages import ASSISTANT_INSTRUCTIONS, NO_DATA_FOUND_MSG
from app.common.enums.content_type import ContentTypeEnum
from app.common.enums.run_status import RunStatusEnum
from app.common.types.user_request import UserRequest
from app.repositories.assistant import AssistantRepository


class AssistantService:

    def __init__(self, client: AsyncOpenAI, assistant_repository: AssistantRepository) -> None:
        self.client = client
        self.__assistant_repository = assistant_repository

    async def create_assistant(self) -> Assistant:
        assistant = await self.__assistant_repository.create_assistant(
            name="ExcelGenie",
            instructions=ASSISTANT_INSTRUCTIONS,
            temperature=0.2,
            model="gpt-4o",
            tools=[{"type": "code_interpreter"}]
        )
        return assistant

    async def create_session(self) -> Thread:
        session_thread = await self.__assistant_repository.create_thread()
        return session_thread

    async def get_response(self, user_request: UserRequest) -> str:
        thread_id = user_request.thread_id
        attachments = NOT_GIVEN
        await self.__assistant_repository.create_message(user_message=user_request.query, thread_id=thread_id, attachments=attachments)
        run = await self.__assistant_repository.create_run(
            assistant_id=user_request.assistant_id,
            thread_id=thread_id,
            truncation_strategy=TRUNCATION_STRATEGY,
            instructions=ASSISTANT_INSTRUCTIONS
        )
        while run.status not in RUN_STATUSES:
            time.sleep(1)
            run = await self.__assistant_repository.retrieve_run(thread_id=thread_id,run_id=run.id)
        return await self.get_run_response(run=run, thread_id=thread_id)

    async def get_run_response(self, run: Run, thread_id: str) -> str:
        match run.status:
            case RunStatusEnum.COMPLETED:
                messages = await self.client.beta.threads.messages.list(thread_id=thread_id)
                message_contents = messages.data[0].content
                for content in message_contents:
                    content_type = content.type
                    match content_type:
                        case ContentTypeEnum.TEXT:
                            response = content.text.value
                        case _:
                            continue
                return response
            case _:
                return NO_DATA_FOUND_MSG
