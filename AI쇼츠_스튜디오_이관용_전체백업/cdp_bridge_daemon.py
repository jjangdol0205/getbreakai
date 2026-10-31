# -*- coding: utf-8 -*-
"""
Persistent Chrome CDP Bridge Daemon (Port 9333)
Keeps a SINGLE WebSocket connection open to Chrome so the user never has to click
'Allow debugging connection' more than once!
"""
import asyncio
import json
import os
import sys
from aiohttp import web
import websockets

sys.stdout.reconfigure(encoding="utf-8")

STATE = {
    "ws": None,
    "sid": None,
    "tid": None,
    "msg_id": 10,
    "lock": asyncio.Lock(),
}


async def send_cdp(method: str, params: dict = None, use_sid: bool = True):
    async with STATE["lock"]:
        ws = STATE["ws"]
        STATE["msg_id"] += 1
        mid = STATE["msg_id"]
        payload = {"id": mid, "method": method}
        if params:
            payload["params"] = params
        if use_sid and STATE["sid"]:
            payload["sessionId"] = STATE["sid"]
        await ws.send(json.dumps(payload))
        while True:
            raw = await ws.recv()
            resp = json.loads(raw)
            if resp.get("id") == mid:
                return resp


async def ensure_connected():
    if STATE["ws"] is not None:
        return
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\DevToolsActivePort")
    lines = open(port_file).read().strip().splitlines()
    ws_url = f"ws://127.0.0.1:{lines[0]}{lines[1]}"
    print("Connecting to Chrome WebSocket:", ws_url, flush=True)
    ws = await websockets.connect(ws_url, open_timeout=120, max_size=100 * 1024 * 1024, ping_interval=None)
    STATE["ws"] = ws

    r = await send_cdp("Target.getTargets", use_sid=False)
    tid = None
    for t in r.get("result", {}).get("targetInfos", []):
        if t.get("type") == "page" and ("flow.google" in t.get("url", "") or "labs.google" in t.get("url", "")):
            tid = t["targetId"]
            print("Attached to Flow tab:", t.get("url"), flush=True)
            break
    if not tid:
        for t in r.get("result", {}).get("targetInfos", []):
            if t.get("type") == "page":
                tid = t["targetId"]
                break
    STATE["tid"] = tid
    r_att = await send_cdp("Target.attachToTarget", {"targetId": tid, "flatten": True}, use_sid=False)
    STATE["sid"] = r_att["result"]["sessionId"]
    await send_cdp("Page.enable")
    await send_cdp("DOM.enable")
    await send_cdp("Runtime.enable")
    print("CDP Bridge Ready! SessionId:", STATE["sid"], flush=True)


async def handle_cmd(request):
    await ensure_connected()
    body = await request.json()
    method = body.get("method")
    params = body.get("params", {})
    use_sid = body.get("use_sid", True)
    resp = await send_cdp(method, params, use_sid=use_sid)
    return web.json_response(resp)


async def init_app():
    app = web.Application(client_max_size=50 * 1024 * 1024)
    app.router.add_post("/cmd", handle_cmd)
    return app


if __name__ == "__main__":
    web.run_app(init_app(), host="127.0.0.1", port=9333)
