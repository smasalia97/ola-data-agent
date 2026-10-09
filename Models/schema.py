from pydantic import BaseModel,Field
from typing import Annotated, Literal
from operator import add


class AgentSchema(BaseModel):
    messages: Annotated[list,add] = Field(..., description="List of messages to be processed")
    user_question: str = Field(..., description="The original question from the user")
    curated_question: str = Field(..., description="Curated user questions for the agent")
    prompt_query_context: str = Field(..., description="A detailed prompt with SQL DB context that will agent to generate SQL Query")
    is_safe: Literal["Yes", "No"] = Field(..., description="Flag indicating if the request is safe")
    comments: str = Field(..., description="Comments or feedback regarding the safety of the SQL query")
    generated_sql_query: str = Field(..., description="The generated SQL query based on the user's request")
    sql_query_execution_result: str = Field(..., description="The result of the executed SQL query")
    final_answer: str = Field(..., description="The final answer to be returned to the user")

class JudgeSchema(BaseModel):
    answer: Literal["Yes", "No"] = Field(..., description="Indicates whether the generated SQL Query is safe to execute or not")
    comments: str = Field(..., description="Additional comments or feedback from the judge regarding the SQL query")
    