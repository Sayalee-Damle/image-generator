from pathlib import Path
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI


load_dotenv()


class Config:
    model_name = os.getenv("OPENAI_MODEL")
    llm_cache = os.getenv("LLM_CACHE") == "True"
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model=model_name,
        temperature=0,
        request_timeout=os.getenv("REQUEST_TIMEOUT"),
        cache=llm_cache,
        streaming=True,
    )
    verbose_llm = os.getenv("VERBOSE_LLM") == "True"
    python_executor = Path(os.getenv("PYTHON_SCRIPT"))

    
    path_json = Path(os.getenv("JSON_PATH_DISC"))
    path_csv = Path(os.getenv("CSV_FILES"))
    
    if not path_json.exists():
        path_json.mkdir(exist_ok=True, parents=True)

    if not path_csv.exists():
        path_csv.mkdir(exist_ok=True, parents=True)

    ui_timeout = os.getenv("REQUEST_TIMEOUT")

cfg = Config()


if __name__ == "__main__":
    print("llm: ", cfg.llm)
