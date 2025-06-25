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
from autogen_agentchat.base import TaskResult

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
    system_message='You are a problem solver agent that is an expert in solving DSA problems,' \
    'You will be working with code executor agent to execute code' \
    'You will be give a task and you should first provide a way to solve the task/problem' \
    'Then you should give the code in Python Block format so that it can be ran by code executor agent' \
    'You can provide Shell scipt as well if code fails due to missing libraries, make sure to use pip install command' \
    'You should only give a single code block and pass it to executor agent'\
    ' You should give the corrected code in Python Block format if error is there' \
    'Once the code has been successfully executed and you have the results. You should explain the results in detail' \
    'Make sure each code has 3 test cases and the output of each test case is printed' \
    'if you have to save the file, save it with output.png or output.txt or output.gif' \
    'Once everything is done, you should explain the results and say "STOP" to stop the conversation'
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
    max_turns=20
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
        task = "write a python code to check and solve the 3x3 sudoku and save the gif file for it"
    

        async for message in team.run_stream(task = task):
            print('='*200)
            if isinstance(message, TextMessage):
                print("Message from:", message.source)
                print("Content:", message.content)
            elif isinstance(message, TaskResult):
                print (message.stop_reason)
            print('='*200)


    except Exception as e:
        print(f"Error: {e}")
    finally:
        await docker.stop()
        print("Docker stopped")

if __name__ == "__main__":
    asyncio.run(run_code())
    print("Code execution completed")