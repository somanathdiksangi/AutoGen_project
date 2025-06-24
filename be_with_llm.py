from autogen_agentchat.agents import AssistantAgent,UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import TextMessageTermination,MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
import asyncio
from autogen_agentchat.agents import CodeExecutorAgent

from dotenv import load_dotenv
load_dotenv()
import os


api_key=os.getenv("GAMINI_API_KEY")
model_client = OpenAIChatCompletionClient(
    model="gemini-1.5-flash-8b",
    api_key=api_key,
)
problem_solver = AssistantAgent(
    name="ProblemSolver",
    model_client=model_client,
    description="An agent that solves problems by executing code.",
    system_message=(
        "You are a problem solver agent that solves DSA (Data Structures and Algorithms) problems. "
        "You will be given a task. First, you should explain the approach to solve the task/problem. "
        "Then, you should provide the code in a Python code block format so that it can be run by the code executor agent. "
        "You should only give a single code block and pass it to the code executor agent. "
        "In case there is an error in the code, you should explain how to fix it, "
        "and then provide the corrected code again in a Python code block. "
        "Once the code has been successfully executed and you have the result, you should explain the result in detail. "
        "Make sure each code block has 3 test cases and the output of each test case is printed. "
        "Once everything is done, you should explain the result and say 'STOP' to stop the conversation."
    )
)


docker=DockerCommandLineCodeExecutor(
    work_dir='tmp',
    timeout=120
)

code_executer=CodeExecutorAgent(
    name="CodeExecuterCode",
    description="An agent that executes code in a docker container.",
    code_executor=docker

)

termination_condition=TextMessageTermination('STOP')

team=RoundRobinGroupChat(
    participants=[problem_solver,code_executer],
    termination_condition=termination_condition,
    max_turns=10
)

# docker=DockerCommandLineCodeExecutor(
#     work_dir='tmp',
#     timeout=120
# )

# code_executer=CodeExecutorAgent(
#     name="CodeExecuterCode",
#     description="An agent that executes code in a docker container.",
#     code_executor=docker

# )


# task = TextMessage(
#     content='''Here is some code:\n```python\nprint("hello")\n```''',
#     source="user"
# )


async def run_code():
    try:
        await docker.start()
        task = ""
    

        async for message in team.run_stream(task=task):
            print('='*20)
            print(message.source,":",message)
            print("="*20)


    except Exception as e:
        print(f"Error: {e}")
    finally:
        await docker.stop()
        print("Docker stopped")

if __name__ == "__main__":
    asyncio.run(run_code())
    print("Code execution completed")