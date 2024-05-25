import json
from typing import Annotated

from fastapi import Depends, FastAPI
from openai import AsyncOpenAI

from src.constants import FEEDBACK_SYSTEM_CHAT, INITIAL_QUESTION, QUESTION_SYSTEM_CHAT
from src.dependency import Conversation, client, context, user_input
from src.schemas import Chat, Question


app = FastAPI()


@app.post(
    "/start",
    description="""
    Notify that the interview has started.
    User starts the interview with this endpoint.
    This request will reset and initialize the interview.
    """,
    response_model=Question,
    response_description="Initial question, which is always same.",
)
async def start_interview(
    conversation: Annotated[Conversation, Depends(context)],
) -> Question:
    conversation.clear()
    conversation.append(QUESTION_SYSTEM_CHAT.model_dump())
    conversation.append(INITIAL_QUESTION.to_chat().model_dump())

    return INITIAL_QUESTION


@app.get(
    "/question",
    description="Request for interviewer's next question.",
    response_model=Question,
    response_description="Intervier's next question.",
)
async def feed_forward(
    client: Annotated[AsyncOpenAI, Depends(client)],
    conversation: Annotated[Conversation, Depends(context)],
) -> Question:
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.1,
    )
    question = Question(**json.loads(response.choices[0].message.content))
    conversation.append(question.to_chat().model_dump())

    return question


@app.post(
    "/answer",
    description="Request for the feedback of interviewee's answer.",
    response_model=str,
    response_description="Feedback of the answer.",
)
async def feedback_answer(
    client: Annotated[AsyncOpenAI, Depends(client)],
    conversation: Annotated[Conversation, Depends(context)],
    answer: Annotated[Chat, Depends(user_input)],
) -> str:
    conversation.append(answer.model_dump())

    # Log
    for chat in conversation:
        print(chat)

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            FEEDBACK_SYSTEM_CHAT.model_dump(),
            answer.model_dump(),
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content
