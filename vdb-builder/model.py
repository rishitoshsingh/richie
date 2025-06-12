import logging
import time
from typing import Any, ClassVar, Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class TokenRateChatGoogleGenerativeAI(ChatGoogleGenerativeAI, BaseModel):
    current_token_usage: int = 0
    TOKEN_RATE_LIMIT: ClassVar[int] = 1000000

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def _generate(
        self,
        messages,
        stop=None,
        run_manager=None,
        *,
        tools=None,
        functions=None,
        safety_settings=None,
        tool_config=None,
        generation_config=None,
        cached_content=None,
        tool_choice=None,
        **kwargs,
    ):
        # Count tokens
        token_count = self.get_num_tokens("".join([mess.content for mess in messages]))
        if self.current_token_usage + token_count > self.TOKEN_RATE_LIMIT:
            # If token limit exceeded, wait for a while
            print(
                f"Token limit exceeded: {self.current_token_usage + token_count} > {self.TOKEN_RATE_LIMIT}. Waiting for 60 seconds."
            )
            time.sleep(60)
            self.current_token_usage = 0
        self.current_token_usage += token_count

        return super()._generate(
            messages=messages,
            stop=stop,
            run_manager=run_manager,
            tools=tools,
            functions=functions,
            safety_settings=safety_settings,
            tool_config=tool_config,
            generation_config=generation_config,
            cached_content=cached_content,
            tool_choice=tool_choice,
            **kwargs,
        )


def get_model(provider: str, model: Optional[str] = None, **kwargs):
    if provider == "google":
        from langchain_core.rate_limiters import InMemoryRateLimiter
        from langchain_google_genai import ChatGoogleGenerativeAI

        PERMINUTE_RATE = 15
        google_rate_limiter = InMemoryRateLimiter(
            requests_per_second=PERMINUTE_RATE / 60,
            check_every_n_seconds=0.1,  # Wake up every 100 ms to check whether allowed to make a request,
            max_bucket_size=1,
        )
        # return ChatGoogleGenerativeAI(
        return TokenRateChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            rate_limiter=google_rate_limiter,
        )
    elif provider == "huggingface":
        from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

        return ChatHuggingFace(
            llm=HuggingFaceEndpoint(
                repo_id=model,
                task="text-generation",
                do_sample=False,
                repetition_penalty=1.03,
            )
        )

    else:
        raise ValueError(f"Unsupported model provider: {provider}")


if __name__ == "__main__":
    import json
    import os

    api_path = os.path.expanduser("auth/api.json")
    with open(api_path, "r") as f:
        apis = json.load(f)
    os.environ["GOOGLE_API_KEY"] = apis.get("GCP")
    # model = get_model("huggingface", "mistralai/Mistral-7B-Instruct-v0.3")
    model = get_model("google")
    print(model.invoke("Hello, how are you?"))
