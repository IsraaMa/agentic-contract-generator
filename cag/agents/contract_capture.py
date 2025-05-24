from langsmith import traceable
from cag.schemas import ContractState

@traceable(name="Contract Capture")
def contract_capture(state: ContractState) -> ContractState:
    return state 