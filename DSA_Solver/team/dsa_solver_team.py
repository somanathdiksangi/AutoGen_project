from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMessageTermination
from config.constants import MAX_TURNS
from agent.problem_solver import get_problem_solver
from agent.code_executer import get_code_executor
from config.docker_utils import get_docker_executor


def get_team():
    """
    Returns a RoundRobinGroupChat instance configured with the problem solver and code executor agents.
    
    :return: RoundRobinGroupChat instance
    """
    
    termination_condition = TextMessageTermination('STOP')

    team = RoundRobinGroupChat(
        participants=[get_problem_solver(), get_code_executor()],
        termination_condition=termination_condition,
        max_turns=12
    )
    
    return team


