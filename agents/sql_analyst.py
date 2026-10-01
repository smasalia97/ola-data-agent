import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.llm_pick import pick_llm
from Models.schema import AgentSchema

# ----------------------------------------- AI Agent Code -----------------------------------------

def curate_question(state: AgentSchema) -> AgentSchema:

    user_question = state.user_question # Coz this is a Pydantic model Object

    llm = pick_llm("low")

    response = llm.invoke(f"Curate the following question: {user_question}")

    state.curated_question = response
    return state

def prompt_query_context(state: AgentSchema) -> AgentSchema:

    curated_question = state.curated_question # Coz this is a Pydantic model Object

