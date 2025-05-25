import os
import sys
import json
from dotenv import load_dotenv
from cag.schemas import ContractState
from cag.agents.graph import app

# Load environment variables from .env if present
load_dotenv()

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

    # ContractState expects input_data as a dict
    state = ContractState(input_data=input_data)
    print("Running contract graph...")
    final_state = app.invoke(state)
    print("\n--- FINAL CONTRACT ---\n")
    print(final_state.get("final_contract") or "No contract generated.")

if __name__ == "__main__":
    main() 