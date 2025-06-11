import json
import os
from typing import Optional

api_path = os.path.expanduser("auth/api.json")
with open(api_path, "r") as f:
    apis = json.load(f)
os.environ["GOOGLE_API_KEY"] = apis.get("GCP")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = apis.get("HUGGINGFACE")


def get_model(provider: str, model: Optional[str] = None, **kwargs):
    if provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
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
    model = get_model("huggingface", "mistralai/Mistral-7B-Instruct-v0.3")
    print(model.invoke("Hello, how are you?"))
