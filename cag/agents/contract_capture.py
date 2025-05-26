from langsmith import traceable
from cag.schemas import ContractState
import json
import os

@traceable(name="Contract Capture")
def contract_capture(state: ContractState) -> ContractState:
    print("[IN][contract_capture] Starting contract capture validation...")
    
    # Cargar el archivo de campos requeridos
    contract_types_path = os.path.join(os.path.dirname(__file__), '../contract_types/contract_required_fields.json')
    with open(contract_types_path, 'r', encoding='utf-8') as f:
        contract_types = json.load(f)
    
    # Obtener el tipo de contrato del input_data
    contract_type = state.input_data.get("contract_type")
    if not contract_type:
        state.format_valid = False
        state.final_contract = "Error: No se especificó el tipo de contrato en los datos de entrada."
        print(f"[OUT][contract_capture] Validation failed: Tipo de contrato no especificado")
        return state
    
    # Obtener los campos requeridos para el tipo de contrato
    if contract_type not in contract_types:
        state.format_valid = False
        state.final_contract = f"Error: Tipo de contrato '{contract_type}' no encontrado en la lista de tipos disponibles."
        print(f"[OUT][contract_capture] Validation failed: Tipo de contrato no encontrado")
        return state
    
    required_fields = contract_types[contract_type]["datos_requeridos"]
    
    errors = []
    data = state.input_data
    for section, fields in required_fields.items():
        if section not in data or not isinstance(data[section], dict):
            errors.append(f"Falta la sección obligatoria: {section}")
            continue
        for field in fields:
            if field not in data[section]:
                errors.append(f"Falta el campo obligatorio: {section}.{field}")
    
    if errors:
        state.format_valid = False
        state.final_contract = "Error de captura de contrato:\n" + "\n".join(errors)
        print(f"[OUT][contract_capture] Validation failed: {errors}")
    else:
        state.format_valid = True
        print("[OUT][contract_capture] Validation passed.")
    
    return state 