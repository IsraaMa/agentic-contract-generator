from langsmith import traceable
from cag.schemas import ContractState

@traceable(name="Quality Evaluator")
def quality_evaluator(state: ContractState) -> dict:
    condition = "approved" if state.quality_approved else "rejected"
    return {"__condition__": condition} 