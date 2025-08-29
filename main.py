from dotenv import load_dotenv
from agents import Agent, Runner ,FileSearchTool
import chainlit as cl

load_dotenv()
#--------------------------------------

agent = Agent(
    model="gpt-4.1-mini",
    name="my_agent",
    instructions="you are a helpfull assistant, always search in file for information",
     tools=[
        # WebSearchTool()
        FileSearchTool(
        max_num_results=3,
      #   vector_store_ids=["vs_682f21a9eccc8191a5cf6198681860ec"],
     )]
)
#--------------------------------------

@cl.on_message
async def main(msg: cl.Message):
  user_input = msg.content
    
  result = Runner.run_sync(agent, user_input )
  await cl.Message(content = result.final_output).send()