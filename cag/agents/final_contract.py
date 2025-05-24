from langsmith import traceable
from cag.schemas import ContractState

@traceable(name="Final Contract")
def final_contract(state: ContractState) -> ContractState:
    state.final_contract = "Contract approved and finalized."
    return state 