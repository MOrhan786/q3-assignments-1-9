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

@function_tool
def get_weather(city: str) -> str:
    """Return mock weather information for the given city."""
    return f'The current temperature in {city} is 34°C with clear sky'

def main():
    print("Welcome to Weather  Info Agents")
    print("Ask me about the weather in any city.Type 'exit' to quit.\n")
    agent = Agent(
        name="WeatherBot",
        instructions="You are a weather assistant. Use the weather tool to provide information when asked about the weather in any city.",
        model=model,
        tools=[get_weather]
    )
    while True:
        user_input = input("✅Write your question here! :")
        if user_input.lower() in ["exit", "quit"]:
            print("😎 Goodbye!")
            break
        result = Runner.run_sync(agent, user_input, run_config=config)
        rich.print("Bot:", result.final_output)

if __name__ == "__main__":
    main()