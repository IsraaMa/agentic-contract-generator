import os
from typing import Optional, Dict, Any

from pydantic import BaseModel


# Definición del estado compartido
class ContractState(BaseModel):
    input_data: Dict[str, Any]
    format_valid: Optional[bool] = None
    legal_valid: Optional[bool] = None
    structure_valid: Optional[bool] = None
    quality_approved: Optional[bool] = None
    final_contract: Optional[str] = None
