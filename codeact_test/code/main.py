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
from spotify_login import spotify_login, SpotifyLoginOutput
from spotify_show_playlist_library import show_playlist_library, PlaylistLibraryOutput
from spotify_show_song import show_song, SongOutput
from spotify_show_liked_songs import show_liked_songs, LikedSongsOutput
from spotify_search_songs import search_songs, SearchSongsOutput
from spotify_show_playlist import show_playlist, PlaylistOutput
from spotify_add_song_to_playlist import add_song_to_playlist, MessageOutput as AddSongOutput
from spotify_remove_song_from_playlist import remove_song_from_playlist, MessageOutput as RemoveSongOutput
from spotify_review_song import review_song, ReviewSongOutput
from spotify_update_song_review import update_song_review, UpdateSongReviewOutput
from spotify_show_song_review import show_song_review, SongReviewOutput
from spotify_show_song_reviews import show_song_reviews, SongReviewsOutput
from spotify_delete_song_review import delete_song_review, DeleteSongReviewOutput
from phone_login import phone_login, PhoneLoginOutput
from phone_search_text_messages import search_text_messages, TextMessagesOutput
from supervisor_complete_task import complete_task, CompleteTaskOutput
from supervisor_show_profile import show_profile, SupervisorProfileOutput

async def run_one_case(task_id):
    # Create and inject the AppWorld instance

    codebox = CodeActEnv()

    # Register tools callable in the codebox
    codebox.register_callable_tool(show_account_passwords, output_model=AccountPasswordsOutput)
    codebox.register_callable_tool(spotify_login, output_model=SpotifyLoginOutput)
    codebox.register_callable_tool(show_playlist_library, output_model=PlaylistLibraryOutput)
    codebox.register_callable_tool(show_song, output_model=SongOutput)
    codebox.register_callable_tool(show_liked_songs, output_model=LikedSongsOutput)
    codebox.register_callable_tool(search_songs, output_model=SearchSongsOutput)
    codebox.register_callable_tool(show_playlist, output_model=PlaylistOutput)
    codebox.register_callable_tool(add_song_to_playlist, output_model=AddSongOutput)
    codebox.register_callable_tool(remove_song_from_playlist, output_model=RemoveSongOutput)
    codebox.register_callable_tool(review_song, output_model=ReviewSongOutput)
    codebox.register_callable_tool(update_song_review, output_model=UpdateSongReviewOutput)
    codebox.register_callable_tool(show_song_review, output_model=SongReviewOutput)
    codebox.register_callable_tool(show_song_reviews, output_model=SongReviewsOutput)
    codebox.register_callable_tool(delete_song_review, output_model=DeleteSongReviewOutput)
    codebox.register_callable_tool(phone_login, output_model=PhoneLoginOutput)
    codebox.register_callable_tool(search_text_messages, output_model=TextMessagesOutput)
    codebox.register_callable_tool(show_profile, output_model=SupervisorProfileOutput)
    codebox.register_callable_tool(complete_task, output_model=CompleteTaskOutput)

    # Start sandbox + tool server + inject proxies
    await codebox.start()
    _world_mod.world = AppWorld(task_id=task_id, experiment_name="codeact_test")

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
        print(f"Supervisor: {sup}")
        print(f"Instruction: {world.task.instruction}")
        print(f"{'='*60}\n")

        msg = Msg(
            name="user",
            content=f"""
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

for Spotify use lower case spotify
Now, call `run_python_code` tool with your code to solve the actual task:

{world.task.instruction}

In case of tool_call_error, read the failed API's schema AGAIN.
"""
            f"My name is: {sup['first_name']} {sup['last_name']}. My personal email is {sup['email']} and phone number is {sup['phone_number']}.",
            role="user",
        )
        while True:
            msg = await agent(msg)
            if world.task_completed():
                print("\nTask completed!")
                break
            # msg = Msg(name="user", content="continue", role="user")
            break

        report = world.evaluate().report()
        print(f"\n--- Evaluation Report ---")
        print(report)

    finally:
        await codebox.stop()
        _world_mod.world.close()

async def main():
    await run_one_case(task_id='82e2fac_1') #'042a9fc_1') #'82e2fac_1')

asyncio.run(main())
