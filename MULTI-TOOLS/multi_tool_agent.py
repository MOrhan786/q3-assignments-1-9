# multi_tool_agent.
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, function_tool, OpenAIChatCompletionsModel
from agents.run import RunConfig
import rich

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in .env!")

external_client = AsyncOpenAI(
    api_key=openai_api_key,
    base_url="https://api.openai.com/v1/"
)

model = OpenAIChatCompletionsModel(
    model="gpt-4.1-mini",
    openai_client=external_client
)

config = RunConfig(model=model, tracing_disabled=True)
# Tool 1: mah function
@function_tool
def add(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b
#-----------------

# Tool 2
def sub(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a - b
#---------------------
# Tool 3
@function_tool
def multiply(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a * b
# ---------------------
# Tool 4
@function_tool
def divided(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a / b

# Tool 5 weather function
@function_tool
def get_weather(city: str) -> str:
    """Return mock weather information for the given city."""
    return f'The current temperature in {city} is 34°C with clear sky'
# main cli
def main():
    print("====Welcome to Multi-Tool Agents=====")
    print("====Type 'exit' to quit./n=====")


    agent = Agent(
        name="Multi Tool",
        instructions="You are a smart assistant. Use the tools to answer math and weather questions .",
        model=model,
        tools=[add, sub, multiply, divided ,get_weather] #both tools call here
    )
    while True:
        user_input = input("✅ You:")
        if user_input.lower() in ["exit", "quit"]:
            print("😎 Goodbye!")
            break
        result = Runner.run_sync(agent, user_input, run_config=config)
        rich.print("Bot:", result.final_output)

if __name__ == "__main__":
    main()