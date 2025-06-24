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

docker=DockerCommandLineCodeExecutor(
    work_dir='tmp',
    timeout=120
)

code_executer=CodeExecutorAgent(
    name="CodeExecuterCode",
    code_executor=docker

)


task = TextMessage(
    content='''Here is some code:\n```python\nprint("hello")\n```''',
    source="user"
)


async def run_code():
    try:
        await docker.start()
        result=await code_executer.run(
            task=task,
            cancellation_token=CancellationToken()
        )
        print(result)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await docker.stop()
        print("Docker stopped")

if __name__ == "__main__":
    asyncio.run(run_code())
    print("Code execution completed")