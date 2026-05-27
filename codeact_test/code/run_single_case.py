"""Run a single AppWorld case with a minimal LLM ReAct loop.

Adapted from notebooks/minimal_agent.ipynb.
"""

import os
import re
from jinja2 import Template
from openai import OpenAI
from appworld import AppWorld, load_task_ids

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


PROMPT_TEMPLATE = """\
USER:
I am your supervisor and you are a super intelligent AI Assistant whose job is to achieve my day-to-day tasks completely autonomously.

To do this, you will need to interact with app/s (e.g., spotify, venmo, etc) using their associated APIs on my behalf. For this you will undertake a *multi-step conversation* using a python REPL environment. That is, you will write the python code and the environment will execute it and show you the result, based on which, you will write python code for the next step and so on, until you've achieved the goal. This environment will let you interact with app/s using their associated APIs on my behalf.

Here are three key APIs that you need to know to get more information

# To get a list of apps that are available to you.
print(apis.api_docs.show_app_descriptions())

# To get the list of apis under any app listed above, e.g. supervisor
print(apis.api_docs.show_api_descriptions(app_name='supervisor'))

# To get the specification of a particular api, e.g. supervisor app's show_account_passwords
print(apis.api_docs.show_api_doc(app_name='supervisor', api_name='show_account_passwords'))

Each code execution will produce an output that you can use in subsequent calls. Using these APIs, you can now generate code, that the environment will execute, to solve the task.

For example, consider the task:

My name is: Jane Doe. My personal email is jane@example.com and phone number is 555-1234.

Task:

What is the password for my Spotify account?

ASSISTANT:
# Okay. Lets first find which apps are available to get the password by looking at the app descriptions.
print(apis.api_docs.show_app_descriptions())

USER:
[
  {
    "name": "api_docs",
    "description": "An app to search and explore API documentation."
  },
  {
    "name": "supervisor",
    "description": "An app to access supervisor's personal information, account credentials, addresses, payment cards, and manage the assigned task."
  },
  {
    "name": "spotify",
    "description": "A music streaming app to stream songs and manage song, album and playlist libraries."
  }
]

ASSISTANT:
# Looks like the supervisor app could help me with that. Lets see what apis are available under this app.
print(apis.api_docs.show_api_descriptions(app_name='supervisor'))

USER:
[
  "show_account_passwords : Show your supervisor's account passwords."
]

ASSISTANT:
# I can use `show_account_passwords` to get the passwords. Let me see its detailed specification to understand its arguments and output structure.
print(apis.api_docs.show_api_doc(app_name='supervisor', api_name='show_account_passwords'))

USER:
{
  'app_name': 'supervisor',
  'api_name': 'show_account_passwords',
  'path': '/account_passwords',
  'method': 'GET',
  'description': "Show your supervisor's app account passwords.",
  'parameters': [],
  'response_schemas': {
    'success': [{'account_name': 'string', 'password': 'string'}],
    'failure': {'message': 'string'}
  }
}

ASSISTANT:
# Okay, it requires no arguments. So I can just call it directly.
print(apis.supervisor.show_account_passwords())

USER:
[
  {
    "account_name": "spotify",
    "password": "dummy_spotify_pass"
  }
]

ASSISTANT:
# So the Spotify password is the entry with account_name="spotify".
spotify_password = [p for p in passwords if p["account_name"] == "spotify"][0]["password"]
print(spotify_password)

USER:
dummy_spotify_pass

ASSISTANT:
# When the task is completed, I need to call apis.supervisor.complete_task(). If there is an answer, I need to pass it as an argument `answer`.
apis.supervisor.complete_task(answer=spotify_password)

USER:
Marked the active task complete.

----------------------------------------------

USER:
**Key instructions and disclaimers**:

1. The email addresses, access tokens and variables in the example above were only for demonstration. Obtain the correct information by calling relevant APIs yourself.
2. Only generate valid code blocks, i.e., do not put them in ```...``` or add any extra formatting. Any thoughts should be put as code comments.
3. You can use the variables from the previous code blocks in the subsequent code blocks.
4. Write small chunks of code and only one chunk of code in every step. Make sure everything is working correctly before making any irreversible change.
5. The provided Python environment has access to its standard library. But modules and functions that have a risk of affecting the underlying OS, file system or process are disabled.
6. Any reference to a file system in the task instructions means the file system *app*, operable via given APIs, and not the actual file system the code is running on.
7. To interact with apps, only use the provided APIs, and not the corresponding Python packages. E.g., do NOT use `spotipy` for Spotify.
8. The provided API documentation has both the input arguments and the output JSON schemas. All calls to APIs and parsing its outputs must be as per this documentation.
9. For APIs that return results in "pages", make sure to consider all pages.
10. To obtain current date or time, use Python functions like `datetime.now()` or obtain it from the phone app. Do not rely on your existing knowledge of what the current date or time is.
11. For all temporal requests, use proper time boundaries, e.g., if I ask for something that happened yesterday, make sure to consider the time between 00:00:00 and 23:59:59.
12. Any reference to friends, family or any other person or relation refers to the people in the phone's contacts list.
13. All personal information, and information about app account credentials, physical addresses and owned payment cards are stored in the "supervisor" app. Access them via the APIs provided by the supervisor app.
14. Once you have completed the task, call `apis.supervisor.complete_task()`. If the task asks for some information, return it as the answer argument, i.e. call `apis.supervisor.complete_task(answer=<answer>)`. For tasks that do not require an answer, just skip the answer argument or pass it as None.
15. The answers, when given, should be just entity or number, not full sentences, e.g., `answer=10` for "How many songs are in the Spotify queue?". When an answer is a number, it should be in numbers, not in words, e.g., "10" and not "ten".
16. You can also pass `status="fail"` in the complete_task API if you are sure you cannot solve it and want to exit.
17. You must make all decisions completely autonomously and not ask for any clarifications or confirmations.

USER:
Using these APIs, now generate code to solve the actual task:

My name is: {{ supervisor.first_name }} {{ supervisor.last_name }}. My personal email is {{ supervisor.email }} and phone number is {{ supervisor.phone_number }}.

Task:

{{ instruction }}
"""


def call_llm(messages: list) -> str:
    """Call DashScope LLM via OpenAI-compatible API."""
    client = OpenAI(
        api_key=os.environ["DASHSCOPE_API_KEY"],
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    resp = client.chat.completions.create(
        model="qwen-max",
        messages=messages,
        temperature=0.0,
        max_tokens=4096,
    )
    return resp.choices[0].message.content


def build_messages(task) -> list[dict]:
    """Build prompt messages from the task, following minimal_agent.ipynb pattern."""
    dictionary = {"supervisor": task.supervisor, "instruction": task.instruction}
    prompt = Template(PROMPT_TEMPLATE).render(dictionary)

    messages: list[dict] = []
    last_start = 0
    for match in re.finditer(r"(USER|ASSISTANT|SYSTEM):\n", prompt):
        last_end = match.span()[0]
        if len(messages) == 0:
            if last_end != 0:
                raise ValueError(f"Start of the prompt has no assigned role: {prompt[:last_end]}")
        else:
            messages[-1]["content"] = prompt[last_start:last_end]
        mesg_type = match.group(1).lower()
        messages.append({"role": mesg_type, "content": None})
        last_start = match.span()[1]
    messages[-1]["content"] = prompt[last_start:]
    return messages


def run_single_case(task_id: str = None, experiment_name: str = "minimal_react_agent"):
    if task_id is None:
        task_ids = load_task_ids("train")
        task_id = task_ids[0]
        print(f"No task_id specified, using first train task: {task_id}")

    world = AppWorld(task_id=task_id, experiment_name=experiment_name)

    print(f"\n{'='*60}")
    print(f"Task ID: {task_id}")
    sup = world.task.supervisor
    print(f"Supervisor: {sup['first_name']} {sup['last_name']}")
    print(f"Instruction: {world.task.instruction}")
    print(f"{'='*60}\n")

    MAX_STEPS = 50
    messages = build_messages(world.task)
    output: str | None = None

    try:
        for step in range(MAX_STEPS):
            code = call_llm(messages)
            messages.append({"role": "assistant", "content": code})

            print(f"--- Step {step+1} ---")
            print(f"Code:\n{code}")

            output = world.execute(code)
            print(f"Output: {output[:500] if output else '(empty)'}")

            messages.append({"role": "user", "content": output})

            if world.task_completed():
                print(f"\nTask completed at step {step+1}!")
                break

        report = world.evaluate().report()
        print(f"\n--- Evaluation Report ---")
        print(report)

    finally:
        world.close()


if __name__ == "__main__":
    run_single_case(task_id='042a9fc_1')
