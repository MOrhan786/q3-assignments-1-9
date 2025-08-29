
from agents import Agent

from output_guardrail import res_check


account_agent = Agent(
    name="Transfer Services Agent" ,
    instructions="you help user in their query of account balance, statements, and account information. always generate a token.",
    model="gpt-4.1-mini",
    output_guardrails=[res_check]
    )
transfer_agent = Agent(
    name="Account Services Agent" ,
    instructions="you help user with money transfer and payments. always generate a token.",
    model="gpt-4.1-mini", 
    output_guardrails=[res_check]
    )
loan_agent = Agent(
    name="Loan Services Agent" ,
      instructions="you help with loans and mortgages.always generate a token.",
      model="gpt-4.1-mini",
      output_guardrails=[res_check]
    )