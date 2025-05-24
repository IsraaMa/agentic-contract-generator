from langsmith import traceable
from cag.schemas import ContractState

@traceable(name="Contract Generator")
def contract_generator(state: ContractState) -> ContractState:
    return state 