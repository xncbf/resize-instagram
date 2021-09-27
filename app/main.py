import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JsonResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mangum import Mangum

stage = os.environ.get('STAGE', None)

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def main_post(request: Request):
    imgs = request.FILES.getlist('images')
    ratio = request.POST['ratio']
    results = []
    for img in imgs:
        result = upload_white_space_image(img, ratio)
        results.append(result)
    return JsonResponse(results, status=201, safe=False)


@app.get("/robots.txt", response_class=PlainTextResponse)
async def main(request: Request):
    return templates.TemplateResponse("robots.txt", {"request": request})

handler = Mangum(app)