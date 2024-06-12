from typing import Any, Optional

from openai import AsyncOpenAI, NotGiven
from openai.types.beta.assistant import Assistant
from openai.types.beta.assistant_tool_param import AssistantToolParam
from openai.types.beta.thread import Thread
from openai.types.beta.thread_update_params import ToolResources
from openai.types.beta.threads import Message, Run
from openai.types.beta.threads.message_create_params import Attachment
from openai.types.beta.threads.run_create_params import TruncationStrategy
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput


class AssistantRepository:

    def __init__(self, client: AsyncOpenAI) -> None:
        self.client = client

    async def create_assistant(self, model: str, instructions: str, name: str, temperature: float, tools: list[AssistantToolParam], tool_resources: Optional[list[dict[str, Any]]] = None) -> Assistant:
        return await self.client.beta.assistants.create(
            model=model,
            instructions=instructions,
            name=name,
            temperature=temperature,
            tools=tools,
            tool_resources=tool_resources
        )

    async def update_assistant(self, assistant_id: str, model: str, instructions: str, name: str, temperature: float, tools: list[AssistantToolParam], tool_resources: Optional[list[dict[str, Any]]] = None) -> Assistant:
        return await self.client.beta.assistants.update(
            assistant_id=assistant_id,
            model=model,
            instructions=instructions,
            temperature=temperature,
            name=name,
            tools=tools,
            tool_resources=tool_resources
        )

    async def list_assistants(self) -> list[Assistant]:
        assistants = await self.client.beta.assistants.list()
        return assistants.data

    async def create_thread(self) -> Thread:
        return await self.client.beta.threads.create()

    async def modify_thread(self, thread_id: str, tool_resources: ToolResources) -> Thread:
        return await self.client.beta.threads.update(thread_id=thread_id, tool_resources=tool_resources)

    async def create_run(self, assistant_id: str, thread_id: str, instructions: str, truncation_strategy: TruncationStrategy) -> Run:
        run = await self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            truncation_strategy=truncation_strategy,
            instructions=instructions
        )
        return run

    async def retrieve_run(self, thread_id: str, run_id: str) -> Run:
        return await self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

    async def cancel_run(self, thread_id: str, run_id: str) -> Run:
        return await self.client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)

    async def create_message(self, user_message: str, thread_id: str, attachments: list[Attachment] | NotGiven) -> Message:
        message = await self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role='user',
            content=user_message,
            attachments=attachments
        )
        return message

    async def submit_tool_outputs_and_poll(self, run_id: str, thread_id: str, tool_outputs: list[ToolOutput] = None) -> Run:
        return await self.client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs
        )
