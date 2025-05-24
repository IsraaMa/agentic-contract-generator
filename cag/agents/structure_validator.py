from langsmith import traceable
from cag.schemas import ContractState

@traceable(name="Structure Validator")
def structure_validator(state: ContractState) -> dict:
    condition = "success" if state.structure_valid else "failure"
    return {"__condition__": condition} 