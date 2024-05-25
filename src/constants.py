import os

import dotenv
from openai import AsyncOpenAI

from src.schemas import Chat, GPTRole, Question, QuestionRole


dotenv.load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
CLIENT = AsyncOpenAI(api_key=OPENAI_KEY)


QUESTION_SYSTEM_CHAT = Chat(
    role=GPTRole.SYSTEM,
    content="""Below are interview conversation. Your output format should be same as {"role": "", "content": ""}. In role, you can choose one of moderator, warm, and cold, which means the type of interviewer. You need to randomly choose a role from moderator, cold, and warm, with probabilities of 20%, 40%, and 40% respectively, ensuring that the moderator role is not chosen consecutively. In content, you should write proper dialogue for the interviewer. When the role is moderator, the dialogue is a general interview question, which is not related to my previous message. When the role is cold, the dialogue is a critical and aggresive question about my previous message. When the role is warm, the dialogue is a temperate and soft question about my previous message.""",
)
FEEDBACK_SYSTEM_CHAT = Chat(
    role=GPTRole.SYSTEM,
    content="The following is interviewee's answer. Modify the answer so that the intend of the interviewee might be well conveyed. Do not add any sarcasm. Only print the modified version.",
)
INITIAL_QUESTION = Question(
    role=QuestionRole.MODERATOR,
    content="안녕하세요, 면접에 지원해주셔서 감사합니다. 간단한 자기소개 부탁드립니다.",
)
