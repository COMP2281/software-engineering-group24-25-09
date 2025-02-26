from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from data.urls import urls
from fastapi.templating import Jinja2Templates
from backend.engagements.engagement_manager import EngagementManager
from backend.engagements.llm.llm import LLM
from dotenv import load_dotenv, find_dotenv
import os
from contextlib import asynccontextmanager
import subprocess
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
for url in urls:
    engagement_manager.create_engagement_from_url(str(url))


@asynccontextmanager
async def lifespan(app: FastAPI):
    subprocess.Popen(["npm", "start"], cwd="./frontend")
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")


@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    engagements = [
        {"slug": engagement.get_slug()}
        for engagement in engagement_manager.get_engagements().values()
    ]

    return templates.TemplateResponse(
        request=request, name="index.html", context={"engagements": engagements}
    )


if __name__ == "__main__":
    uvicorn.run(app)
