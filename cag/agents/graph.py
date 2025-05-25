import os

from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langsmith import traceable  # For LangSmith tracing
from cag.schemas import ContractState
from functools import partial
from langgraph.checkpoint.memory import InMemorySaver

from cag.agents.contract_capture import contract_capture
from cag.agents.contract_generator import contract_generator
from cag.agents.final_contract import final_contract
from cag.agents.human_in_the_loop import human_in_the_loop_review
from cag.agents.llm_validator import llm_validator

# Language model initialization
llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

# Graph construction
graph = StateGraph(ContractState)

# Add nodes
graph.add_node("contract_capture", contract_capture)
graph.add_node("contract_generator", contract_generator)

# Human review nodes using the generic HIL module
graph.add_node("human_review_format", partial(human_in_the_loop_review, review_type="format"))
graph.add_node("human_review_legal", partial(human_in_the_loop_review, review_type="legal"))
graph.add_node("human_review_structure", partial(human_in_the_loop_review, review_type="structure"))
graph.add_node("human_review_quality", partial(human_in_the_loop_review, review_type="quality"))

# Define edges
graph.set_entry_point("contract_capture")
graph.add_edge("contract_capture", "contract_generator")

# Logic gate functions for conditional edges
def format_validator_gate(state: ContractState) -> str:
    return "success" if state.format_valid else "failure"

def legal_validator_gate(state: ContractState) -> str:
    return "success" if state.legal_valid else "failure"

def structure_validator_gate(state: ContractState) -> str:
    return "success" if state.structure_valid else "failure"

def quality_evaluator_gate(state: ContractState) -> str:
    return "approved" if state.quality_approved else "rejected"

graph.add_conditional_edges(
    source="contract_generator",
    path=format_validator_gate,
    path_map={
        "success": "human_review_format",
        "failure": END
    }
)
graph.add_edge("human_review_format", "contract_generator")

graph.add_conditional_edges(
    source="contract_generator",
    path=legal_validator_gate,
    path_map={
        "success": "human_review_legal",
        "failure": END
    }
)
graph.add_edge("human_review_legal", "contract_generator")

graph.add_conditional_edges(
    source="contract_generator",
    path=structure_validator_gate,
    path_map={
        "success": "human_review_structure",
        "failure": END
    }
)
graph.add_edge("human_review_structure", "contract_generator")

graph.add_conditional_edges(
    source="contract_generator",
    path=quality_evaluator_gate,
    path_map={
        "approved": "human_review_quality",
        "rejected": END
    }
)
graph.add_edge("human_review_quality", "contract_generator")

graph.add_edge("contract_generator", END)

# Compile the graph
checkpointer = InMemorySaver()
app = graph.compile(checkpointer=checkpointer)