from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
import asyncio
from autogen_agentchat.agents import CodeExecutorAgent
from autogen_agentchat.base import TaskResult
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.constants import MODEL 

from dotenv import load_dotenv
load_dotenv()
import os


api_key=os.getenv("GAMINI_API_KEY")
model_client = OpenAIChatCompletionClient(
    model="gemini-1.5-flash-8b",
    api_key=api_key,
)