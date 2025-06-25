from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from config.constants import DOCKER_TIMEOUT, DOCKER_WORK_DIR
import asyncio

def get_docker_executor():
    """
    Returns a DockerCommandLineCodeExecutor instance configured with the specified work directory, timeout, and image.
    """
    docker_executor = DockerCommandLineCodeExecutor(
        work_dir=DOCKER_WORK_DIR,
        timeout=DOCKER_TIMEOUT,
        image="python:3.11" 
    )
    return docker_executor


async def start_docker_executor(docker_executor):
    try:
        await docker_executor.start()
        print("✅ Docker executor started successfully.")

        # Check and print container status
        if hasattr(docker_executor, "_container") and docker_executor._container:
            print("🚀 Docker container is running.")
        else:
            print("⚠️ Docker container failed to start.")
    except Exception as e:
        print(f"❌ Error starting Docker executor: {e}")


async def stop_docker_executor(docker_executor):
    """
    Stops the DockerCommandLineCodeExecutor instance asynchronously.
    
    :param docker_executor: DockerCommandLineCodeExecutor instance
    """
    try:
        await docker_executor.stop()
        print("Docker executor stopped successfully.")
    except Exception as e:
        print(f"Error stopping Docker executor: {e}")
