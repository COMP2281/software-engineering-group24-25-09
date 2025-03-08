from fastapi import FastAPI, Request, Form
import sys
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
from config import ollama_host, ollama_port, ollama_model

frontend_dir = sys.argv[1]

llm = LLM(ollama_host, ollama_port, ollama_model)
engagement_manager = EngagementManager(llm, "./data")
for url in urls:
    print(f"Adding {url}")
    try:
        engagement_manager.create_engagement_from_url(URL(url))
    except CannotCrawlException as e:
        print(e)
    except GetPageException as e:
        print(e)

app = FastAPI()
app.mount("/static", StaticFiles(directory=frontend_dir + "/static"), name="static")
templates = Jinja2Templates(directory=frontend_dir + "/templates")


@app.get("/")
async def read_index():
    return FileResponse(frontend_dir + "/index.html")


def fuzzy_search(query, dataset, keys, limit=None, threshold=0.6):
    if query == "":
        return dataset

    if not limit:
        limit = len(query)

    results = []

    highest_score = 0
    for item in dataset:
        best_key_score = 0
        best_key = None

        for key in keys:
            if key in item and isinstance(item[key], str):
                score = fuzz.partial_ratio(query, item[key])
                if score > best_key_score:
                    best_key_score = score
                    best_key = key

        results.append((item, best_key_score, best_key))

        if best_key_score >= highest_score:
            highest_score = best_key_score

    results = [x for x in results if x[1] > threshold * highest_score]
    results.sort(key=lambda x: x[1], reverse=True)

    return [item[0] for item in results[:limit]]


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
        {"title": engagement.get_title()}
        for engagement in engagement_manager.get_engagements().values()
    ]

    searched = fuzzy_search(search_text, engagements, keys=["title"])

    return templates.TemplateResponse(
        request=request,
        name="slide_previews.html",
        context={"engagements": searched},
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
    ]

    searched = fuzzy_search(engagement_search_text, engagements, keys=["title"])

    return templates.TemplateResponse(
        request=request,
        name="engagement_list.html",
        context={"slugs": searched},
    )


if __name__ == "__main__":
    uvicorn.run(app, port=int(sys.argv[2]))
