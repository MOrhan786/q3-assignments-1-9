# main_agent.py
from dotenv import load_dotenv
from agents import Agent , Runner,  enable_verbose_stdout_logging , InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
import rich
from input_guardrail import check_slangs
from my_tools import generate_customer_token, identify_banking_purpose
from handoff_agents import account_agent, transfer_agent, loan_agent

#-----------------------------------------------
load_dotenv()
# enable_verbose_stdout_logging()
#-----------------------------------------------
agent = Agent(
    name="Bank Greeting Agent",
    instructions="""
      you are a friendly bank greeting agent.

      1.welcome the user to the bank.
      2.use identify_banking_purpose to understand user need.
      3.if confidence > 0.8, send user to the right specialist.
      4.always use generate_customer_token tool to generate token for the customer. 
      
         #Example: argument for the  generate_customer_token can only be (service_type = "general" or
         service_type = "account_service" or service_type = "transfer_service"  or service_type = "loan_service")
      

      Always me helpful and friendly.
      """,
    model="gpt-4.1-mini",
    handoffs=[account_agent, transfer_agent, loan_agent],
     tools=[generate_customer_token, identify_banking_purpose],
     input_guardrails=[check_slangs]
   )
#-----------------------------------------------
while True:
   try:
         user_input = input("\n🤖Enter your query: ")
         if user_input.lower() in ['quit', 'exit']: break

         result = Runner.run_sync(agent, user_input)
         rich.print(result.final_output)
   except InputGuardrailTripwireTriggered as e :  
      print("✖️ input Guardrail", e)   
   except OutputGuardrailTripwireTriggered  as e :  
      print("✖️ output Guardrail", e)  

      
