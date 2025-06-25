import asyncio
from team.dsa_solver_team import get_team
from agent.problem_solver import get_problem_solver
from agent.code_executer import get_code_executor
from config.docker_utils import get_docker_executor, start_docker_executor, stop_docker_executor
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import TextMessage

async def get_team_and_docker():
    docker_executor = get_docker_executor()

   

    
    team = get_team()

    return team, docker_executor


async def main():
    team, docker = await get_team_and_docker()

    try:
        await start_docker_executor(docker)
        task = "Write a Python code to check whether a number is prime or not"

        async for message in team.run_stream(task = task):
        
            print('='*200)
            if isinstance(message, TextMessage):
                print("Message from:", message.source)
                print("Content:", message.content)
            elif isinstance(message, TaskResult):
                print (message.stop_reason)
            print('='*200)


    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        await stop_docker_executor(docker)
        print("🛑 Docker stopped")


if __name__ == "__main__":
    asyncio.run(main())
    print("✅ Code execution completed.")