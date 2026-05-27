import inspect
import signal as _signal
import socket
import threading

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


class CallToolRequest(BaseModel):
    arguments: dict = {}


class ToolServer:
    """HTTP server on host that code_sandbox proxies call back to.

    Routes tool calls to registered local functions.
    """

    def __init__(self):
        self.app = FastAPI()
        self._toolname_func: dict[str, callable] = {}
        self._port: int | None = None
        self._server: uvicorn.Server | None = None
        self._thread: threading.Thread | None = None

        @self.app.post("/call/{tool_name}")
        async def call_tool(tool_name: str, body: CallToolRequest):
            print(f'==TOOL SERVER: {tool_name}, {body}==')
            if tool_name in self._toolname_func:
                try:
                    result = self._toolname_func[tool_name](**body.arguments)
                    print(result)
                    resp = {
                        "content": [
                            {"type": b.type, "text": b.text}
                            for b in result.content
                            if hasattr(b, "text")
                        ],
                    }
                    if result.metadata is not None:
                        resp["metadata"] = result.metadata
                    return resp
                except Exception as e:
                    print(f"---------[{tool_name}] args={body.arguments}\nError: {e}--------")
                    return {"content": [{"type": "text", "text": f"[{tool_name}] args={body.arguments}\nError: {e}"}], "isError": True}
            print(f'------{tool_name} NOT FOUND')
            return {"content": [{"type": "text", "text": f"Error: Tool '{tool_name}' not found"}], "isError": True}

    def register(self, func: callable):
        """Register a tool function that can be called from the sandbox."""
        self._toolname_func[func.__name__] = func

    def start(self):
        # IPython internally uses signal.signal() / signal.alarm() which only
        # work in the main thread. Since the ToolServer runs in a background
        # thread, patch them to no-ops to avoid "signal only works in main
        # thread" errors.
        self._orig_signal = _signal.signal
        self._orig_alarm = _signal.alarm

        def _no_op_signal(*_, **__):
            return None

        _signal.signal = _no_op_signal
        _signal.alarm = _no_op_signal

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", 0))
        self._port = sock.getsockname()[1]
        sock.close()

        config = uvicorn.Config(
            self.app,
            host="0.0.0.0",
            port=self._port,
            log_level="warning",
        )
        self._server = uvicorn.Server(config)
        self._thread = threading.Thread(
            target=self._server.run, daemon=True,
        )
        self._thread.start()

    def stop(self):
        _signal.signal = self._orig_signal
        _signal.alarm = self._orig_alarm
        if self._server:
            self._server.should_exit = True

    @property
    def port(self) -> int:
        return self._port
