from langsmith import traceable
from cag.schemas import ContractState

@traceable(name="Contract Capture")
def contract_capture(state: ContractState) -> ContractState:
    required_fields = {
        "datos_trabajador": [
            "nombre_completo", "nacionalidad", "edad", "sexo", "estado_civil", "curp", "rfc", "domicilio"
        ],
        "datos_patron": [
            "razon_social", "rfc", "domicilio", "representante_legal"
        ],
        "condiciones_trabajo": [
            "tipo_contrato", "puesto", "funciones", "lugar_trabajo", "jornada_laboral", "horario", "salario_mensual", "forma_pago", "dia_lugar_pago", "periodo_prueba_dias", "capacitacion"
        ]
    }
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
    else:
        state.format_valid = True
    return state 