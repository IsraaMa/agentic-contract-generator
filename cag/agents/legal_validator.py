from langsmith import traceable
from cag.schemas import ContractState

@traceable(name="Legal Validator")
def legal_validator(state: ContractState) -> dict:
    condition = "success" if state.legal_valid else "failure"
    return {"__condition__": condition} 