import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mangum import Mangum

stage = os.environ.get('STAGE', None)

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("item.html", {"request": request})


@app.get("/robots.txt", response_class=PlainTextResponse)
async def main(request: Request):
    return templates.TemplateResponse("robots.txt")

handler = Mangum(app)