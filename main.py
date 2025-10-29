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


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_connection.connect()

    async def handle_message(msg: dict[str, Any]):
        logger.info(f"Message received: {msg}")

    asyncio.create_task(consumer.consume(EXCHANGE_NAME, ROUTING_KEY_TASK, handle_message))
    asyncio.create_task(consumer.consume(EXCHANGE_NAME, ROUTING_KEY_STATUS, handle_message))

    yield

    await rabbit_connection.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
