from contextlib import asynccontextmanager
from importlib.metadata import version

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from app.common.constants.common import ALLOWED_METHODS, SELECTED_ALL
from app.common.helpers.logger import logger
from app.contexts.assistant import AssistantContext
from app.routes import assistant
from app.utils.local_cache import LocalCache


@asynccontextmanager
async def lifespan(app: FastAPI):
    assistant = await AssistantContext().assistant_service.create_assistant()
    thread = await AssistantContext().assistant_service.create_session()
    LocalCache.set_value(key="assistant_id", value=assistant.id)
    LocalCache.set_value(key="thread_id", value=thread.id)
    logger.info("FastAPI server is up and running.")
    yield
    logger.info("Server is shutting down...")

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=SELECTED_ALL,
    allow_credentials=True,
    allow_methods=ALLOWED_METHODS,
    allow_headers=SELECTED_ALL,
)

@app.get('/', tags=["Health Check"], response_class=PlainTextResponse)
async def health_check() -> str:
    return f"Hello from FastAPI: {version('fastapi')}"

app.include_router(assistant.router)
