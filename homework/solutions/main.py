from typing import Annotated
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, ConfigDict, Field
from errors import install_handlers, ERROR_RESPONSES

app = FastAPI(title="Movie guessing game")
install_handlers(app)
ROUNDS = {1: {"clue": "A shark threatens a seaside town", "answer": "Jaws"},
          2: {"clue": "Toys have a secret life", "answer": "Toy Story"}}

class Guess(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    movie_title: str = Field(min_length=1, max_length=100)
    attempt_number: int = Field(ge=1, le=5, strict=True)

class GuessResult(BaseModel):
    round_id: int
    correct: bool

@app.post("/rounds/{round_id}/guess", response_model=GuessResult,
          responses=ERROR_RESPONSES)
def guess_movie(round_id: Annotated[int, Path(ge=1)], guess: Guess):
    if round_id not in ROUNDS:
        raise HTTPException(status_code=404, detail={
            "code": "ROUND_NOT_FOUND", "message": "Round not found"})
    return {"round_id": round_id,
            "correct": guess.movie_title.casefold() == ROUNDS[round_id]["answer"].casefold()}
