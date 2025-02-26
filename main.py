from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.engagements import EngagementManager
from backend.engagements.llm import LLM
from dotenv import load_dotenv, find_dotenv
import os
from urllib.parse import urlunparse


def URL(scheme: str, netloc: str, url="", path="", query="", fragment=""):
    # https://stackoverflow.com/a/15799706
    return str(urlunparse((scheme, netloc, url, path, query, fragment)))


def load_config():
    load_dotenv(find_dotenv())


def get_llm_config() -> tuple[str, str]:
    return (
        URL(
            scheme="http",
            netloc=f'{os.getenv("OLLAMA_HOST")}:{os.getenv("OLLAMA_PORT")}',
        ),
        os.getenv("OLLAMA_MODEL"),
    )


def get_search_config() -> tuple[str, str]:
    return os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_CSE_ID")


load_config()
ollama_url, ollama_model_name = get_llm_config()
llm = LLM(ollama_url, ollama_model_name)
engagement_manager = EngagementManager(llm, "./data")

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")


@app.get("/index.html", response_class=HTMLResponse)
async def serve_index(request: Request):
    engagements = [
        {"slug": engagement.get_slug()}
        for engagement in engagement_manager.get_engagements()
    ]

    return templates.TemplateResponse(
        request=request, name="index.html", context={"engagements": engagements}
    )
