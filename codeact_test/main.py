import os
import asyncio

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from appworld import AppWorld
import world as _world_mod

from agentscope.agent import ReActAgent
from agentscope.model import DashScopeChatModel
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit
from agentscope.message import Msg
from codeact_env import CodeActEnv
from instructions import CODEACT_SYSTEM_PROMPT

# Import all AppWorld tools
from api_docs_show_app_descriptions import show_app_descriptions, AppDescriptionsOutput
from api_docs_show_api_descriptions import show_api_descriptions, ApiDescriptionsOutput
from api_docs_show_api_doc import show_api_doc, ApiDocOutput
from show_account_passwords import show_account_passwords, AccountPasswordsOutput
from spotify_login import login, LoginOutput
from spotify_show_playlist_library import show_playlist_library, PlaylistLibraryOutput
from spotify_show_song import show_song, SongOutput
from supervisor_complete_task import complete_task, CompleteTaskOutput


async def main():
    # Create and inject the AppWorld instance

    codebox = CodeActEnv()

    # Register tools callable in the codebox
    # codebox.register_callable_tool(show_app_descriptions, output_model=AppDescriptionsOutput)
    # codebox.register_callable_tool(show_api_descriptions, output_model=ApiDescriptionsOutput)
    # codebox.register_callable_tool(show_api_doc, output_model=ApiDocOutput)
    codebox.register_callable_tool(show_account_passwords, output_model=AccountPasswordsOutput)
    codebox.register_callable_tool(login, output_model=LoginOutput)
    codebox.register_callable_tool(show_playlist_library, output_model=PlaylistLibraryOutput)
    codebox.register_callable_tool(show_song, output_model=SongOutput)
    codebox.register_callable_tool(complete_task, output_model=CompleteTaskOutput)

    # Start sandbox + tool server + inject proxies
    await codebox.start()
    task_id = "692c77d_1" # "82e2fac_1"
    _world_mod.world = AppWorld(task_id=task_id, experiment_name="codeact_test")
    print("_world_mod.world")

    try:
        toolkit = Toolkit()

        # Register code execution tools (from sandbox)
        toolkit.register_tool_function(
            codebox.run_python_code,
            func_description=codebox.run_python_code_description,
        )
        print(codebox.run_python_code_description)

        # Register host tools directly (agent can call them without sandbox)
        toolkit.register_tool_function(show_app_descriptions)
        toolkit.register_tool_function(show_api_descriptions)
        toolkit.register_tool_function(show_api_doc)
        # toolkit.register_tool_function(show_account_passwords)
        # toolkit.register_tool_function(login)
        # toolkit.register_tool_function(show_playlist_library)
        # toolkit.register_tool_function(show_song)
        toolkit.register_tool_function(complete_task)

        agent = ReActAgent(
            name="Friday",
            sys_prompt=CODEACT_SYSTEM_PROMPT,
            model=DashScopeChatModel(
                model_name="qwen-max",
                api_key=os.environ["DASHSCOPE_API_KEY"],
                stream=True,
            ),
            memory=InMemoryMemory(),
            formatter=DashScopeChatFormatter(),
            toolkit=toolkit,
        )

        world = _world_mod.world

        print(f"\n{'='*60}")
        print(f"Task ID: {task_id}")
        sup = world.task.supervisor
        print(f"Supervisor: {sup['first_name']} {sup['last_name']}")
        print(f"Instruction: {world.task.instruction}")
        print(f"{'='*60}\n")

        msg = Msg(
            name="user",
            content="""
1. The email addresses, access tokens and variables in the example above were only for demonstration. Obtain the correct information by calling relevant APIs yourself.
2. Only generate valid code blocks, i.e., do not put them in ```...``` or add any extra formatting. Any thoughts should be put as code comments.
3. You can use the variables from the previous code blocks in the subsequent code blocks.
4. Write small chunks of code and only one chunk of code in every step. Make sure everything is working correctly before making any irreversible change.
5. The provided Python environment has access to its standard library. But modules and functions that have a risk of affecting the underlying OS, file system or process are disabled.
6. Any reference to a file system in the task instructions means the file system *app*, operable via given APIs, and not the actual file system the code is running on.
7. To interact with apps, only use the provided APIs, and not the corresponding Python packages. E.g., do NOT use `spotipy` for spotify.
8. The provided API documentation has both the input arguments and the output JSON schemas. All calls to APIs and parsing its outputs must be as per this documentation.
9. For APIs that return results in "pages", make sure to consider all pages.
10. To obtain current date or time, use Python functions like `datetime.now()` or obtain it from the phone app. Do not rely on your existing knowledge of what the current date or time is.
11. For all temporal requests, use proper time boundaries, e.g., if I ask for something that happened yesterday, make sure to consider the time between 00:00:00 and 23:59:59.
12. Any reference to friends, family or any other person or relation refers to the people in the phone's contacts list.
13. All personal information, and information about app account credentials, physical addresses and owned payment cards are stored in APIs. Access them via the APIs.
14. Once you have completed the task, call `complete_task()`. If the task asks for some information, return it as the answer argument, i.e. call `complete_task(answer=<answer>)`. For tasks that do not require an answer, just skip the answer argument or pass it as None.
15. The answers, when given, should be just entity or number, not full sentences, e.g., `answer=10` for "How many songs are in the spotify queue?". When an answer is a number, it should be in numbers, not in words, e.g., "10" and not "ten".
16. You can also pass `status="fail"` in the complete_task API if you are sure you cannot solve it and want to exit.
17. You must make all decisions completely autonomously and not ask for any clarifications or confirmations.

for Spotify use lower case spotify
Using these APIs, now generate code and call run_python_code solve the actual task:

"""
            f"My name is: {sup['first_name']} {sup['last_name']}. My personal email is {sup['email']} and phone number is {sup['phone_number']}.\n\nTask:\n\n{world.task.instruction}",
            role="user",
        )
        while True:
            msg = await agent(msg)
            if world.task_completed():
                print("\nTask completed!")
                break
            msg = Msg(name="user", content="continue", role="user")

        report = world.evaluate().report()
        print(f"\n--- Evaluation Report ---")
        print(report)

    finally:
        await codebox.stop()
        _world_mod.world.close()


asyncio.run(main())
