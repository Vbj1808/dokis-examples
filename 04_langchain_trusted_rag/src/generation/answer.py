from langchain_openai import ChatOpenAI

from src.config import load_settings
from src.generation.prompts import SYSTEM_PROMPT, build_answer_prompt


def generate_answer(question: str, docs:list) -> str:
    settings = load_settings()

    llm = ChatOpenAI(
        api_key = settings.openai_api_key,
        model = settings.openai_model,
        temperature = 0,
    )

    prompt = build_answer_prompt(question, docs)

    response = llm.invoke(
        [
            ("system", SYSTEM_PROMPT),
            ("user", prompt),
        ]
    )

    return response.content.strip()

