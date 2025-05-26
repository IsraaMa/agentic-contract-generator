from langsmith import traceable
from cag.schemas import ContractState
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import os
import json

@traceable(name="Contract Generator")
def contract_generator(state: ContractState) -> ContractState:
    print("[IN][contract_generator] Generating contract with retrieved data...")
    
    # Cargar el archivo de tipos de contrato
    contract_types_path = os.path.join(os.path.dirname(__file__), '../contract_types/contract_required_fields.json')
    with open(contract_types_path, 'r', encoding='utf-8') as f:
        contract_types = json.load(f)
    
    # Obtener el tipo de contrato del input_data
    contract_type = state.input_data.get("contract_type")
    if not contract_type:
        state.final_contract = "Error: No se especificó el tipo de contrato en los datos de entrada."
        print("[OUT][contract_generator] Error: Tipo de contrato no especificado")
        return state
    
    # Obtener la descripción del tipo de contrato
    if contract_type not in contract_types:
        state.final_contract = f"Error: Tipo de contrato '{contract_type}' no encontrado en la lista de tipos disponibles."
        print("[OUT][contract_generator] Error: Tipo de contrato no encontrado")
        return state
    
    contract_description = contract_types[contract_type]["descripción"]
    
    # Load vectorstore
    VECTORSTORE_DIR = os.path.join(os.path.dirname(__file__), '../../vectorstore/faiss_index')
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(VECTORSTORE_DIR, embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()

    # LLM
    llm = ChatOpenAI(model=os.getenv("LLM_MODEL", "gpt-4o"), temperature=float(os.getenv("MODEL_TEMP", "0.3")))

    # RetrievalQA chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False,
        chain_type="stuff"
    )

    datos = state.input_data
    prompt = f"""
    Genera un contrato de tipo '{contract_type}' con base en los siguientes datos:

    Descripción del tipo de contrato:
    {contract_description}

    Datos del contrato:
    {datos}

    Asegúrate de utilizar ejemplos de estilo legal y formal, incluyendo cláusulas relevantes para este tipo de contrato.
    El contrato debe seguir las mejores prácticas legales y ser claro y conciso.
    """
    result = chain.invoke({"query": prompt})
    state.final_contract = result["result"]
    print("[OUT][contract_generator] Contract generated.")
    return state 