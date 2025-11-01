import asyncio
from contextlib import asynccontextmanager
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI

from src.api import router
from src.logger import logger
from src.queue import (
    EXCHANGE_NAME,
    ROUTING_KEY_STATUS_CREATED,
    ROUTING_KEY_STATUS_DONE,
    ROUTING_KEY_STATUS_REJECTED,
    ROUTING_KEY_STATUS_UNPROCESSABLE,
    ROUTING_KEY_STATUS_VALIDATED,
    ROUTING_KEY_TASK,
    RabbitMQConnection,
    RabbitMQConsumer,
    RabbitMQProducer,
)

load_dotenv()

rabbit_connection = RabbitMQConnection()
producer = RabbitMQProducer(rabbit_connection)
consumer = RabbitMQConsumer(rabbit_connection)

last_status_message: dict[str, Any] = {}

ROUTING_KEYS_STATUS = [
    ROUTING_KEY_STATUS_CREATED,
    ROUTING_KEY_STATUS_VALIDATED,
    ROUTING_KEY_STATUS_REJECTED,
    ROUTING_KEY_STATUS_DONE,
    ROUTING_KEY_STATUS_UNPROCESSABLE,
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_connection.connect()
    logger.info("Connected to RabbitMQ")

    async def handle_message(message: dict[str, Any], routing_key: str):
        if routing_key in (ROUTING_KEY_TASK, *ROUTING_KEYS_STATUS):
            logger.info(f" IN: request_id={message['request_id']}, routing_key={routing_key}")
        if routing_key in ROUTING_KEYS_STATUS:
            request_id = message["request_id"]
            last_status_message[request_id] = message

    async def start_consumer(routing_key: str):
        await consumer.consume(EXCHANGE_NAME, routing_key, lambda msg: handle_message(msg, routing_key))

    for routing_key in [ROUTING_KEY_TASK, *ROUTING_KEYS_STATUS]:
        asyncio.create_task(start_consumer(routing_key))

    yield

    await rabbit_connection.close()
    logger.info("Disconnected from RabbitMQ")


app = FastAPI(lifespan=lifespan)
app.include_router(router)

app.state.last_status_message = lambda: last_status_message
