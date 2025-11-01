import asyncio
from contextlib import asynccontextmanager
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI

from src.api import router
from src.logger import logger
from src.queue import (
    EXCHANGE_NAME,
    ROUTING_KEY_STATUS,
    ROUTING_KEY_TASK,
    RabbitMQConnection,
    RabbitMQConsumer,
    RabbitMQProducer,
)

load_dotenv()


rabbit_connection = RabbitMQConnection()
producer = RabbitMQProducer(rabbit_connection)
consumer = RabbitMQConsumer(rabbit_connection)

last_status_message: dict[str, Any] | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_connection.connect()

    async def handle_message(message: dict[str, Any], routing_key: str):
        if routing_key == ROUTING_KEY_TASK:
            logger.info(
                f"Message received: routing_key={routing_key},   request_id={message['request_id']}, type={message['request_type']}"
            )
        elif routing_key == ROUTING_KEY_STATUS:
            logger.info(
                f"Message received: routing_key={routing_key}, request_id={message['request_id']}, status={message['request_status']}"
            )

    asyncio.create_task(
        consumer.consume(EXCHANGE_NAME, ROUTING_KEY_TASK, lambda msg: handle_message(msg, ROUTING_KEY_TASK))
    )
    asyncio.create_task(
        consumer.consume(EXCHANGE_NAME, ROUTING_KEY_STATUS, lambda msg: handle_message(msg, ROUTING_KEY_STATUS))
    )

    yield

    await rabbit_connection.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router)

app.state.last_status_message = lambda: last_status_message
