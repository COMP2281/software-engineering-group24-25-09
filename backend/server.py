from fastapi import FastAPI, Request, Form
import sys
from rapidfuzz import fuzz
from typing import Annotated
from starlette.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from data.urls import urls
from fastapi.templating import Jinja2Templates
from engagements import (
    LLM,
    URL,
    EngagementManager,
    GetPageException,
    CannotCrawlException,
)
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


slides = []
selectedSlideIndices = []
selectionCount = 1


class SlideData:
    def __init__(self, title):
        global selectionCount
        self.title = title
        self.selected = selectionCount
        selectionCount += 1

    def asDict(self):
        return dict(
            (name, getattr(self, name))
            for name in dir(self)
            if not name.startswith("__")
        )


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


def printr(input):
    print(input)
    return input


@app.get("/slides", response_class=HTMLResponse)
@app.post("/search_slides", response_class=HTMLResponse)
async def search_slides(request: Request, search_text: Annotated[str, Form()] = ""):
    slide_dicts = [slide.asDict() for slide in slides]
    for i, slide in enumerate(slide_dicts):
        slide["selected"] = (
            selectedSlideIndices.index(i) if i in selectedSlideIndices else False
        )
    searched = fuzzy_search(search_text, slide_dicts, keys=["title"])

    return templates.TemplateResponse(
        request=request,
        name="slide_previews.html",
        context={"slides": searched, "export_visible": len(selectedSlideIndices) != 0},
    )


@app.get("/engagements", response_class=HTMLResponse)
@app.post("/search_engagements", response_class=HTMLResponse)
async def serve_engagement_list(
    request: Request, engagement_search_text: Annotated[str, Form()] = ""
):
    print(engagement_search_text)
    engagements = [
        {"title": engagement.get_title(), "slug": engagement.get_slug()}
        for engagement in engagement_manager.get_engagements().values()
    ]

    searched = fuzzy_search(engagement_search_text, engagements, keys=["title"])
    print(searched)

    return templates.TemplateResponse(
        request=request,
        name="engagement_list.html",
        context={"engagements": searched},
    )


@app.post("/new_engagement/{slug}")
async def create_engagement(request: Request, slug: str):
    slides.append(SlideData(engagement_manager.get_engagement(slug).get_title()))


@app.post("/select_slide/{index}")
async def select_slide(request: Request, index: int):
    if index in selectedSlideIndices:
        selectedSlideIndices.remove(index)
    else:
        selectedSlideIndices.append(index)


@app.post("/export", response_class=FileResponse)
async def export(request: Request):
    pass


if __name__ == "__main__":
    uvicorn.run(app, port=int(sys.argv[2]))
