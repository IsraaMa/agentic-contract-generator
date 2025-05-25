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
    print(f"[IN][human_in_the_loop_review] Human review requested for: {review_type}")
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
        print(f"[OUT][human_in_the_loop_review] Review accepted for: {review_type}")
    elif response["type"] in ("ignore", "response"):
        setattr(state, field, False)
        print(f"[OUT][human_in_the_loop_review] Review ignored or responded for: {review_type}")
    elif response["type"] == "edit":
        for k, v in response["args"]["args"].items():
            setattr(state, k, v)
        setattr(state, field, True)
        print(f"[OUT][human_in_the_loop_review] Review edited for: {review_type}")
    else:
        setattr(state, field, None)
        print(f"[OUT][human_in_the_loop_review] Review result unknown for: {review_type}")
    return state 