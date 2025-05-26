import os
import sys
import json
from dotenv import load_dotenv
from cag.schemas import ContractState
from cag.agents.graph import app
import uuid

# Load environment variables from .env if present
load_dotenv()

def make_json_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(v) for v in obj]
    elif isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    else:
        # Fallback: represent the object as a string
        return str(obj)

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_contract_graph.py <input_data.json>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}")
        sys.exit(1)
    
    with open(input_path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    
    if "contract_type" not in input_data:
        print("Error: El archivo de entrada debe contener el campo 'contract_type'")
        sys.exit(1)

    # ContractState expects input_data as a dict
    state = ContractState(input_data=input_data)
    print("Running contract graph...")
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    final_state = app.invoke(state, config=config)
    print("\n--- FINAL CONTRACT ---\n")
    print(final_state.get("final_contract") or "No contract generated.")
    print("\n--- FULL CONTRACT STATE ---\n")
    if hasattr(final_state, "model_dump"):
        serializable_state = final_state.model_dump()
    elif hasattr(final_state, "dict"):
        serializable_state = final_state.dict()
    else:
        serializable_state = final_state  # fallback, may still fail
    serializable_state = make_json_serializable(serializable_state)
    print(json.dumps(serializable_state, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main() 