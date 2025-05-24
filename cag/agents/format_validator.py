from langsmith import traceable
from cag.schemas import ContractState

@traceable(name="Format Validator")
def format_validator(state: ContractState) -> dict:
    condition = "success" if state.format_valid else "failure"
    return {"__condition__": condition} 