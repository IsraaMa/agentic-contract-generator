from langsmith import traceable
from langgraph.types import interrupt
from cag.schemas import ContractState

REVIEW_FIELD_MAP = {
    'format': 'format_valid',
    'legal': 'legal_valid',
    'structure': 'structure_valid',
    'quality': 'quality_approved',
}

@traceable(name="Human In The Loop Review")
def human_in_the_loop_review(state: ContractState, review_type: str, config=None, store=None) -> ContractState:
    if review_type not in REVIEW_FIELD_MAP:
        raise ValueError(f"Invalid review_type: {review_type}")
    field = REVIEW_FIELD_MAP[review_type]
    context = f"Please review the contract {review_type} validation below. Accept, edit, or reject as needed."
    request = {
        "action_request": {"action": f"review_{review_type}", "args": state.dict()},
        "config": {
            "allow_ignore": True,
            "allow_respond": True,
            "allow_edit": True,
            "allow_accept": True,
        },
        "description": context,
    }
    response = interrupt([request])[0]
    if response["type"] == "accept":
        setattr(state, field, True)
    elif response["type"] in ("ignore", "response"):
        setattr(state, field, False)
    elif response["type"] == "edit":
        for k, v in response["args"]["args"].items():
            setattr(state, k, v)
        setattr(state, field, True)
    else:
        setattr(state, field, None)
    return state 