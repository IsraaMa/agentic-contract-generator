import os

from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langsmith import traceable  # For LangSmith tracing
from cag.schemas import ContractState
from functools import partial

from cag.agents.contract_capture import contract_capture
from cag.agents.format_validator import format_validator
from cag.agents.contract_generator import contract_generator
from cag.agents.legal_validator import legal_validator
from cag.agents.structure_validator import structure_validator
from cag.agents.quality_evaluator import quality_evaluator
from cag.agents.final_contract import final_contract
from cag.agents.human_in_the_loop import human_in_the_loop_review

# Language model initialization
llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

# Graph construction
graph = StateGraph(ContractState)

# Add nodes
graph.add_node("contract_capture", contract_capture)
graph.add_node("format_validator", format_validator)
graph.add_node("contract_generator", contract_generator)
graph.add_node("legal_validator", legal_validator)
graph.add_node("structure_validator", structure_validator)
graph.add_node("quality_evaluator", quality_evaluator)
graph.add_node("final_contract", final_contract)

# Human review nodes using the generic HIL module
graph.add_node("human_review_format", partial(human_in_the_loop_review, review_type="format"))
graph.add_node("human_review_legal", partial(human_in_the_loop_review, review_type="legal"))
graph.add_node("human_review_structure", partial(human_in_the_loop_review, review_type="structure"))
graph.add_node("human_review_quality", partial(human_in_the_loop_review, review_type="quality"))

# Define edges
graph.set_entry_point("contract_capture")
graph.add_edge("contract_capture", "format_validator")

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
    "format_validator",
    {
        "success": contract_generator,
        "failure": "human_review_format"
    },
    condition=format_validator_gate
)
graph.add_edge("human_review_format", "format_validator")

graph.add_edge("contract_generator", "legal_validator")
graph.add_conditional_edges(
    "legal_validator",
    {
        "success": structure_validator,
        "failure": "human_review_legal"
    },
    condition=legal_validator_gate
)
graph.add_edge("human_review_legal", "contract_generator")

graph.add_conditional_edges(
    "structure_validator",
    {
        "success": quality_evaluator,
        "failure": "human_review_structure"
    },
    condition=structure_validator_gate
)
graph.add_edge("human_review_structure", "contract_generator")

graph.add_conditional_edges(
    "quality_evaluator",
    {
        "approved": final_contract,
        "rejected": "human_review_quality"
    },
    condition=quality_evaluator_gate
)
graph.add_edge("human_review_quality", "contract_generator")

graph.add_edge("final_contract", END)

# Compile the graph
app = graph.compile()