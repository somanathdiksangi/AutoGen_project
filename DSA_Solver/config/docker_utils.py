from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from config.constants import DOCKER_TIMEOUT, DOCKER_WORK_DIR


def get_docker_executor():
    """
    Returns a DockerCommandLineCodeExecutor instance configured with the specified work directory and timeout.
    
    :return: DockerCommandLineCodeExecutor instance
    """
    return DockerCommandLineCodeExecutor(
        work_dir=DOCKER_WORK_DIR,
        timeout=DOCKER_TIMEOUT
    )

def start_docker_executor(docter_executor):
    """
    Starts the DockerCommandLineCodeExecutor instance.
    
    :return: None
    """
    docker_executor = get_docker_executor()
    try:
        docker_executor.start()
        print("Docker executor started successfully.")
    except Exception as e:
        print(f"Error starting Docker executor: {e}")

def stop_docker_executor(docker_executor):
    """
    Stops the DockerCommandLineCodeExecutor instance.
    
    :return: None
    """
    try:
        docker_executor.stop()
        print("Docker executor stopped successfully.")
    except Exception as e:
        print(f"Error stopping Docker executor: {e}")