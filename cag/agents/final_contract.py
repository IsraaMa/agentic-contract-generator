from langsmith import traceable
from cag.schemas import ContractState

@traceable(name="Final Contract")
def final_contract(state: ContractState) -> ContractState:
    print("[IN][final_contract] Finalizing contract...")
    state.final_contract = "Contract approved and finalized."
    print("[OUT][final_contract] Contract finalized.")
    return state 