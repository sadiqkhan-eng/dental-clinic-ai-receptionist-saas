from fastapi import APIRouter
from pydantic import BaseModel

from app.services.training_service import simulate_conversation, evaluate_conversation

router = APIRouter()


class TrainingRequest(BaseModel):
    clinic_name: str
    scenario: str = "General booking and FAQ"
    turns: int = 10


@router.post("/simulate")
async def run_simulation(data: TrainingRequest):
    conversation = await simulate_conversation(
        clinic_name=data.clinic_name,
        scenario=data.scenario,
        turns=data.turns,
    )
    return {"conversation": conversation}


@router.post("/evaluate")
async def evaluate(data: TrainingRequest):
    conversation = await simulate_conversation(
        clinic_name=data.clinic_name,
        scenario=data.scenario,
        turns=data.turns,
    )
    evaluation = await evaluate_conversation(conversation)
    return {
        "conversation": conversation,
        "evaluation": evaluation,
    }
