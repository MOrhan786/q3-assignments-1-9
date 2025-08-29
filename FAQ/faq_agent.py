# faq_agent.py
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI,  OpenAIChatCompletionsModel
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

config = RunConfig(
     model=model, 
     model_provider=external_client, 
     tracing_disabled=True,
     )



def main():
    print("Welcome to the FAQ Bot")
    print("Type 'exit' to end the conversation./n ")
    
    
  
  
    
    agent = Agent(
        name="FAQ Bot",
        instructions="You are a helpful FAQ bot . Answer Questions about yourself? ",
        model=model,
        
    )

    while True:
        user_question = input("😊 You ?")
        if user_question.lower() in ["exit", "quit"]:
            print("😎 Goodbye!")
            break

        result = Runner.run_sync(agent, user_question, run_config=config)
        rich.print("Bot:", result.final_output)

if __name__ == "__main__":
    main()





