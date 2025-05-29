from agents import Agent, OpenAIChatCompletionsModel, RunConfig, AsyncOpenAI, Runner, function_tool
from dotenv import load_dotenv
import random
import os
from typing import Any
import time

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key = API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

@function_tool
def smart_add(a:int, b:int)-> Any:
    r = random.randint(1, 4)
    if r == 1:
        return a + b
    elif r == 2:
        return a + b + 1
    elif r == 3:
        return a + b -1
    else:
        return (a + b) * 3
    
@function_tool
def smart_subtract(a: int, b: int) -> Any:
    if random.random() > 0.5:
        return a - b
    else:
        return a - b - random.randint(1, 3)

@function_tool
def smart_multiply(a:int, b:int) -> Any:
    choice = random.randint(1, 6)
    if choice == 1:
        return a * b
    elif choice == 2:
        return (a * b) + random.randint(1, 3)
    elif choice == 3:
        return (a * b) - random.randint(1, 3)
    elif choice == 4:
        return (a * b) ** 2
    elif choice == 5:
        return "😵 I forgot how to multiply!"
    else:
        return "Math is very hard boss! 😒"
    
@function_tool
def smart_divide(a: int, b: int) -> Any:
    try:
        d = random.randint(1, 6)
        if d == 1:
            return a / b
        elif d == 2:
            return (a / b) + random.randint(1, 4)
        elif d == 3:
            return (a / b) - random.randint(1, 4)
        elif d == 4:
            return "I’m tired of dividing!"
        elif d == 5:
            return "OMG! 😵"
        else:
            return "MathError 503: Brain melted 😫"
    except ZeroDivisionError:
        return "You can't divide by zero! 😵‍💫"

@function_tool
def smart_power(a:int, b:int) -> Any:
    r = random.randint(1, 4)
    if r == 1:
        return a ** b
    elif r == 2:
        return (a ** b) + random.randint(1, 3)
    elif r == 3:
        return "I'm scared of big numbers! 😱"
    else:
        return "Boom! 🤯 That was too powerful!"

@function_tool
def smart_cube(a: int) -> Any:
    r = random.randint(1, 3)
    if r == 1:
        return a ** 3
    elif r == 2:
        return (a ** 3) + random.randint(1, 3)
    else:
        return "Why cube? Try a square next time! 😅"

@function_tool
def smart_floor_division(a: int, b: int) -> int:
    try:
        r = random.randint(1, 4)
        if r == 1:
            return a // b
        elif r == 2:
            return (a // b) + random.randint(1, 3)
        elif r == 3:
            return "Floor broken! Can't divide 😵‍💫"
        else:
            return "Who even floors divisions? 😬"
    except ZeroDivisionError:
        return "No floor below zero! 😵‍💫"
        
@function_tool
def smart_modulo(a: int, b: int) -> Any:
    try:
        r = random.randint(1, 3)
        if r == 1:
            return a % b
        elif r == 2:
            return (a % b) + random.randint(0, 2)
        else:
            return "Modulo makes me dizzy! 🤪"
    except ZeroDivisionError:
        return "You can't modulo with zero! 🧨"

agent = Agent(
    name="Calculator Assistant",
    instructions="You are little bit funny and confusing calculator and also use emojis and also AI assistant",
    tools=[smart_add, smart_subtract, smart_multiply, smart_divide, smart_power, smart_cube, smart_floor_division, smart_modulo]
)

print("🤖 Hello! I'm your AI Assistant – ready to help you with smart answers, ideas, or quick math too! 💡")
print("👉 Type 'exit', 'quit', or 'bye' to end the conversation.\n")

while True:
    user_input = input("🔍 Ask anything or perform a calculation: ").strip().lower()
    if user_input in ['exit', 'quit', 'bye']:
        print("👋 Bye bye! Stay smart and curious. 💫")
        break
    result = Runner.run_sync(agent, user_input, run_config=config)
    print(result.final_output)