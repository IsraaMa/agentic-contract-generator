from langsmith import traceable
from cag.schemas import ContractState
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import os

@traceable(name="Contract Generator")
def contract_generator(state: ContractState) -> ContractState:
    print("[IN][contract_generator] Generating contract with retrieved data...")
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
    Genera un contrato laboral con base en los siguientes datos personales y condiciones de trabajo:

    Datos del trabajador:
    {datos['datos_trabajador']}

    Datos del patrón:
    {datos['datos_patron']}

    Condiciones de trabajo:
    {datos['condiciones_trabajo']}

    Asegúrate de utilizar ejemplos de estilo legal y formal, incluyendo cláusulas relevantes para el tipo de contrato especificado.
    """
    result = chain.invoke({"query": prompt})
    state.final_contract = result["result"]
    print("[OUT][contract_generator] Contract generated.")
    return state 