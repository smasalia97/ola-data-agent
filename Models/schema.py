from pydantic import BaseModel,Field
from typing import Annotated, Literal
from operator import add


class AgentSchema(BaseModel):
    messages: Annotated[list,add] = Field(..., description="List of messages to be processed")
    user_question: str = Field(..., description="The original question from the user")
    curated_question: str = Field(..., description="Curated user questions for the agent")
    prompt_query_context: str = Field(..., description="A detailed prompt with SQL DB context that will agent to generate SQL Query")
    is_safe: Literal["Yes", "No"] = Field(..., description="Flag indicating if the request is safe")
    generated_sql_query: str = Field(..., description="The generated SQL query based on the user's request")
    sql_query_result: str = Field(..., description="The result of the executed SQL query")
    final_answer: str = Field(..., description="The final answer to be returned to the user")