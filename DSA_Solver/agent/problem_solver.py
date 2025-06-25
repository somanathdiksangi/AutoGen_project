from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from config.model_clint import model_client

def get_problem_solver():
    """
    Returns an AssistantAgent instance configured to solve DSA problems.
    
    :return: AssistantAgent instance
    """
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
    return problem_solver
    