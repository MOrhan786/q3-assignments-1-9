
from agents import Agent, GuardrailFunctionOutput, RunContextWrapper , Runner, output_guardrail
from pydantic import BaseModel , Field
from typing import Any
#------------------------------------------------
class Check_Res_Class(BaseModel):
   is_not_banking_related: bool = Field(description="if the LLM response is not relate to banking related topic set the value True in this field.")
   reasoning: str = Field(description="what is the reason behind it .")
#--------------------------------------------------------------------
o_guardrail_agent = Agent(
    name="output Guardrail Agent" ,
    instructions="always check  the LLM response should be only related to banking response.if response is related to hollywood topic keep is_not_banking_related value to True ",
    model="gpt-4.1-mini",
    output_type=Check_Res_Class  
    )
#----------------------------------------------------------
@output_guardrail
async def res_check(ctx: RunContextWrapper, agent: Agent, output: Any)-> GuardrailFunctionOutput:
   
   result = await Runner.run(o_guardrail_agent, output , context=ctx)

   return GuardrailFunctionOutput(
      output_info = result.final_output,
    tripwire_triggered =result.final_output.is_not_banking_related
   ) 


      
