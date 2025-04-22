from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from app.services.concept_map import generate_concept_map
from app.core.templates import templates
from app.services.concept_map import to_mermaid

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request, "data": None})


@router.post("/render", response_class=HTMLResponse)
async def render(request: Request, user_text: str = Form(...)):
    result = await generate_concept_map(user_text)
    mermaid_code = to_mermaid(result) if "nodes" in result else ""
    return templates.TemplateResponse("base.html", {
        "request": request,
        "data": result,
        "mermaid_code": mermaid_code
    })