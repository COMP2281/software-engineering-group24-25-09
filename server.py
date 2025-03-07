from fastapi import FastAPI, Request, Form
from rapidfuzz import fuzz
from typing import Annotated
from starlette.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from backend.engagements.pages.page import GetPageException
from backend.search.url import URL
from data.urls import urls
from fastapi.templating import Jinja2Templates
from backend.engagements.engagement_manager import (
    EngagementManager,
    CannotCrawlException,
)
from backend.engagements.llm.llm import LLM
from backend.config import (
    get_llm_config,
    get_search_config,
    get_engagement_manager_config,
)
from contextlib import asynccontextmanager
import subprocess


ollama_url, ollama_model_name = get_llm_config()
llm = LLM(ollama_url, ollama_model_name)
engagement_manager = EngagementManager(llm, "./data")
for url in urls:
    print(f"Adding {url}")
    try:
        engagement_manager.create_engagement_from_url(URL(url))
    except CannotCrawlException as e:
        print(e)
    except GetPageException as e:
        print(e)


@asynccontextmanager
async def lifespan(app: FastAPI):
    subprocess.Popen(["npm", "start"], cwd="./frontend", shell=True)
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")


@app.get("/")
async def read_index():
    return FileResponse("frontend/index.html")


# @app.get("/slides", response_class=HTMLResponse)
# async def get_slides(request: Request):
#     engagements = [
#         {"slug": engagement.get_slug()}
#         for engagement in engagement_manager.get_engagements().values()
#     ]
#
#     return templates.TemplateResponse(
#         request=request,
#         name="slide_previews.html",
#         context={"engagements": engagements},
#     )


def printr(input):
    print(input)
    return input


@app.get("/slides", response_class=HTMLResponse)
@app.post("/search_slides", response_class=HTMLResponse)
async def search_slides(request: Request, search_text: Annotated[str, Form()] = ""):
    engagements = [
        {"slug": engagement.get_title()}
        for engagement in engagement_manager.get_engagements().values()
        if fuzz.partial_ratio(engagement.get_title(), search_text) > 50
        or search_text == ""
    ]
    print(search_text)

    return templates.TemplateResponse(
        request=request,
        name="slide_previews.html",
        context={"engagements": engagements},
    )


@app.get("/engagements", response_class=HTMLResponse)
@app.post("/search_engagements", response_class=HTMLResponse)
async def serve_engagement_list(
    request: Request, engagement_search_text: Annotated[str, Form()] = ""
):
    print(engagement_search_text)
    engagements = [
        engagement.get_title()
        for engagement in engagement_manager.get_engagements().values()
        if printr(fuzz.partial_ratio(engagement.get_title(), engagement_search_text))
        > 50
        or engagement_search_text == ""
    ]

    return templates.TemplateResponse(
        request=request,
        name="engagement_list.html",
        context={"slugs": engagements},
    )


if __name__ == "__main__":
    uvicorn.run(app)
