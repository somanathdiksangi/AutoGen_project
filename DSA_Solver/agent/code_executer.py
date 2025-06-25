from autogen_ext.agents import CodeExecutorAgent
from config.docker_utils import get_docker_executor

def get_code_executor(docer_executor):
    """
    Returns a CodeExecutorAgent instance configured to execute code in a Docker container.
    
    :return: CodeExecutorAgent instance
    """

    docker_executor = get_docker_executor()

    code_executer=CodeExecutorAgent(
    name="CodeExecuterCode",
    description="An agent that executes code in a docker container.",
    code_executor=docker_executor
    )


    
    return code_executer