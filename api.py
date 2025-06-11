from fastapi import APIRouter, HTTPException
from qa_engine import answer_question
from schemas import AskRequest, AskResponse, Link


router = APIRouter()


@router.post("/api/", response_model=AskResponse)
def ask_question(request: AskRequest):
    if not request.question or not isinstance(request.question, str):
        raise HTTPException(status_code=400, detail="'question' is required and must be a string.")
    new_links = []
    answer = answer_question(request.question, request.image)
    new_links.extend([Link(url='/'.join(link.url.split('/')[:-1]), text=link.text) for link in answer.links])
    answer.links.extend(new_links)
    return answer
