from typing import Annotated

from fastapi import Body
from openai import AsyncOpenAI

from src.constants import CLIENT
from src.schemas import Chat, GPTRole


Conversation = list[dict[str, str]]
storage: Conversation = []


def client() -> AsyncOpenAI:
    return CLIENT


def context() -> Conversation:
    return storage


def user_input(user_input: Annotated[str, Body()]) -> Chat:
    return Chat(role=GPTRole.USER, content=user_input)
