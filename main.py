import asyncio
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from src.api import router
from src.config import Settings
from src.logger import logger
from src.queue import (
    RabbitMQConnection,
    RabbitMQConsumer,
    RabbitMQProducer,
)

settings = Settings()  # type: ignore[call-arg]


rabbit_connection = RabbitMQConnection()
producer = RabbitMQProducer(rabbit_connection)
consumer = RabbitMQConsumer(rabbit_connection)

last_status_message: dict[str, Any] = {}

ROUTING_KEYS_STATUS = [
    settings.ROUTING_KEY_STATUS_CREATED,
    settings.ROUTING_KEY_STATUS_VALIDATED,
    settings.ROUTING_KEY_STATUS_REJECTED,
    settings.ROUTING_KEY_STATUS_DONE,
    settings.ROUTING_KEY_STATUS_UNPROCESSABLE,
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_connection.connect()
    logger.info("Connected to RabbitMQ")

    async def handle_message(message: dict[str, Any], routing_key: str):
        request_id = message["request_id"]
        last_status_message[request_id] = message
        logger.info(f" IN: request_id={request_id}, routing_key={routing_key}")

    for routing_key in ROUTING_KEYS_STATUS:
        asyncio.create_task(
            consumer.consume(settings.EXCHANGE_NAME, routing_key, lambda msg, rk=routing_key: handle_message(msg, rk))
        )

    yield

    await rabbit_connection.close()
    logger.info("Disconnected from RabbitMQ")


app = FastAPI(lifespan=lifespan)
app.include_router(router)

app.state.last_status_message = lambda: last_status_message
