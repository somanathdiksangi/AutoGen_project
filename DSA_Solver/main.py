import asyncio
from team.dsa_solver_team import get_team
from agent.problem_solver import get_problem_solver
from agent.code_executer import get_code_executor
from config.docker_utils import get_docker_executor ,start_docker_executor, stop_docker_executor
from 


async def main():
    docker=get_docker_executor()
    model_clind=
