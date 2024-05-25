from enum import Enum
from pydantic import BaseModel


class GPTRole(Enum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"


class QuestionRole(Enum):
    MODERATOR = "moderator"
    COLD = "cold"
    WARM = "warm"


class Chat(BaseModel):
    role: GPTRole
    content: str

    class Config:
        use_enum_values = True


class Question(BaseModel):
    role: QuestionRole
    content: str

    class Config:
        use_enum_values = True

    def to_chat(self) -> Chat:
        return Chat(role=GPTRole.ASSISTANT, content=self.model_dump_json())
