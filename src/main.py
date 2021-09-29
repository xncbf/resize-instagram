import os
from typing import List

from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mangum import Mangum

from utils import upload_white_space_image

stage = os.environ.get('STAGE', None)

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/{ratio}", status_code=201)
async def main_post(image: UploadFile = File(...), ratio: str="1"):
    return upload_white_space_image(image, ratio)


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots(request: Request):
    return templates.TemplateResponse("robots.txt", {"request": request})

handler = Mangum(app)