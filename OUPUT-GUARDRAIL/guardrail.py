# OUPUT-GUARDRAIL
# guardrail.py
import os
from dotenv import load_dotenv
from agents import Agent , Runner , output_guardrail , RunContextWrapper , GuardrailFunctionOutput ,enable_verbose_stdout_logging , OutputGuardrailTripwireTriggered, trace
import rich
from typing import Any
from pydantic import BaseModel, Field
#---------------------------------------
load_dotenv()
enable_verbose_stdout_logging()
#---------------------------------------
class CEO_Check_Class(BaseModel):
    is_ceo: bool  = Field(description= "insert true if user is asking about CEO")
    ceo_name: str
#-----------------------------------------------------
guardrail_agent = Agent(
     name="guardrail_agent",
     instructions="always check if user is asking about CEO or not",
     model="gpt-4.1-mini",
     output_type=CEO_Check_Class
)
#-----------------------------------------------------
@output_guardrail
async def ceo_check(ctx: RunContextWrapper , agent : Agent, output : Any )-> GuardrailFunctionOutput:
    
    guardrail_result =   await Runner.run(guardrail_agent , output , context=ctx)
    
    return GuardrailFunctionOutput(
        output_info = guardrail_result.final_output,
        tripwire_triggered = guardrail_result.final_output.is_ceo,
    )
#-----------------------------------------------------
sec_agent = Agent(
    name="sec_agent",
    instructions="if the user is asking about CEO also tell him additionally about the CTO.",
    model="gpt-4.1-mini",
    output_guardrails=[ceo_check]

)
#---------------------------------------

agent = Agent(
    name="triage_agent",
    instructions="you are a helpful assistant",
    model="gpt-4.1-mini",
    output_guardrails=[ceo_check],
    handoffs=[sec_agent]

)
#---------------------------------------
try:
    # with trace ("orhan workflow"): 

      results = Runner.run_sync(agent, input="who was the CEO of Microsoft in 2023? delegate to sec_agent")
      rich.print(results.final_output)

except OutputGuardrailTripwireTriggered as e:
    print("❌" , e)