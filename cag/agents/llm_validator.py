from langchain_openai import ChatOpenAI
from cag.schemas import ContractState
import json

llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

def llm_validator(state: ContractState, stage: str) -> ContractState:
    """
    Generic LLM-based validator for any stage.
    - stage: one of 'format', 'legal', 'structure', 'quality'
    """
    if stage == "quality":
        field = "quality_approved"
        prompt = (
            f"You are acting as the optimal validator for the 'quality' stage of a contract review process.\n"
            f"Given the following contract state, evaluate whether it meets the requirements for this stage.\n"
            f"Respond ONLY with a JSON object: {{\"quality_approved\": true or false}}.\n"
            f"Contract State: {state}"
        )
    else:
        field = f"{stage}_valid"
        prompt = (
            f"You are acting as the optimal validator for the '{stage}' stage of a contract review process.\n"
            f"Given the following contract state, evaluate whether it meets the requirements for this stage.\n"
            f"Respond ONLY with a JSON object: {{\"{field}\": true or false}}.\n"
            f"Contract State: {state}"
        )
    response = llm.invoke(prompt)
    result = json.loads(response.content)
    setattr(state, field, result.get(field, False))
    return state 