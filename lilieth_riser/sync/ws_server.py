#!/usr/bin/env python3
"""
LILIETH_RISER — WebSocket Sync Server
Sovereign Sampling Engine | Kernel v1.0.47

Runs on the PROCESSOR (laptop) and accepts connections from the CONTROLLER
(phone).  Relays LiliethMessage packets between peers and handles
heavy audio rendering requests.

Usage:
    python3 ws_server.py [--host 0.0.0.0] [--port 8765]

Requirements:
    pip install websockets
"""

import argparse
import asyncio
import json
import logging
import time
from typing import Dict, Optional, Set

try:
    import websockets
    from websockets.server import WebSocketServerProtocol
except ImportError:
    raise SystemExit(
        "websockets package not found. Install with: pip install websockets"
    )

# ──────────────────────────────────────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("LiliethWS")

# ──────────────────────────────────────────────────────────────────────────────
# Server state
# ──────────────────────────────────────────────────────────────────────────────

class ServerState:
    """Shared mutable state for all connected peers."""

    def __init__(self) -> None:
        self.peers: Set[WebSocketServerProtocol] = set()
        self.ledger_entries: list = []
        self.active_apple: Optional[int] = None
        self.riser_running: bool = False

    def add_peer(self, ws: WebSocketServerProtocol) -> None:
        self.peers.add(ws)
        log.info("Peer connected: %s  (total: %d)", ws.remote_address, len(self.peers))

    def remove_peer(self, ws: WebSocketServerProtocol) -> None:
        self.peers.discard(ws)
        log.info("Peer disconnected (total: %d)", len(self.peers))

    async def broadcast(
        self, msg: dict, exclude: Optional[WebSocketServerProtocol] = None
    ) -> None:
        payload = json.dumps(msg)
        targets = [p for p in self.peers if p is not exclude]
        if targets:
            await asyncio.gather(*(p.send(payload) for p in targets))

# ──────────────────────────────────────────────────────────────────────────────
# Message handlers
# ──────────────────────────────────────────────────────────────────────────────

async def handle_pad_trigger(
    ws: WebSocketServerProtocol,
    msg: dict,
    state: ServerState,
) -> None:
    pad_index = msg.get("pad_index", 0)
    velocity  = msg.get("velocity", 1.0)
    log.info("PAD TRIGGER  pad=%d  velocity=%.3f", pad_index, velocity)
    state.active_apple = pad_index
    # Relay to all other peers (e.g. a display / mirror device)
    await state.broadcast(msg, exclude=ws)


async def handle_riser_arm(
    ws: WebSocketServerProtocol,
    msg: dict,
    state: ServerState,
) -> None:
    start_st    = msg.get("start_st",    -24.0)
    end_st      = msg.get("end_st",       12.0)
    duration_ms = msg.get("duration_ms", 2000.0)
    log.info(
        "RISER ARM  start=%.1f st  end=%.1f st  dur=%.0f ms",
        start_st, end_st, duration_ms,
    )
    state.riser_running = True
    # On the laptop processor, this would kick off actual audio rendering.
    # Here we simulate a progress stream.
    asyncio.ensure_future(_stream_riser_progress(ws, state, duration_ms))
    await state.broadcast(msg, exclude=ws)


async def _stream_riser_progress(
    ws: WebSocketServerProtocol,
    state: ServerState,
    duration_ms: float,
) -> None:
    """Stream riser progress updates back to the controller at ~60 fps."""
    interval_s = 1.0 / 60.0
    steps = int(duration_ms / 1000.0 / interval_s)
    for i in range(steps + 1):
        if not state.riser_running:
            break
        progress = i / steps if steps else 1.0
        try:
            await ws.send(json.dumps({"type": "riserProgress", "progress": progress}))
        except Exception:
            break
        await asyncio.sleep(interval_s)
    state.riser_running = False


async def handle_riser_stop(
    ws: WebSocketServerProtocol,
    msg: dict,
    state: ServerState,
) -> None:
    log.info("RISER STOP")
    state.riser_running = False
    await state.broadcast(msg, exclude=ws)


async def handle_cut(
    ws: WebSocketServerProtocol,
    msg: dict,
    state: ServerState,
) -> None:
    position = msg.get("position", 0.0)
    log.info("BLADE CUT  position=%.4f", position)
    await state.broadcast(msg, exclude=ws)


async def handle_load_apple(
    ws: WebSocketServerProtocol,
    msg: dict,
    state: ServerState,
) -> None:
    label = msg.get("label", "Apple")
    log.info("LOAD APPLE  '%s'", label)
    await state.broadcast(msg, exclude=ws)


async def handle_ledger_entry(
    ws: WebSocketServerProtocol,
    msg: dict,
    state: ServerState,
) -> None:
    entry = msg.get("entry", {})
    state.ledger_entries.append(entry)
    log.info(
        "LEDGER ENTRY  id=%s  source=%s",
        entry.get("id", "?"), entry.get("source", "?"),
    )


# ──────────────────────────────────────────────────────────────────────────────
# Dispatch table
# ──────────────────────────────────────────────────────────────────────────────

HANDLERS: Dict[str, object] = {
    "padTrigger":  handle_pad_trigger,
    "riserArm":    handle_riser_arm,
    "riserStop":   handle_riser_stop,
    "cut":         handle_cut,
    "loadApple":   handle_load_apple,
    "ledgerEntry": handle_ledger_entry,
}

# ──────────────────────────────────────────────────────────────────────────────
# Connection handler
# ──────────────────────────────────────────────────────────────────────────────

async def connection_handler(
    ws: WebSocketServerProtocol,
    state: ServerState,
) -> None:
    state.add_peer(ws)
    try:
        async for raw in ws:
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                log.warning("Invalid JSON from %s: %r", ws.remote_address, raw)
                continue

            msg_type = msg.get("type", "")

            if msg_type == "ping":
                await ws.send(json.dumps({"type": "pong", "ts": time.time()}))
                continue

            handler = HANDLERS.get(msg_type)
            if handler:
                await handler(ws, msg, state)
            else:
                log.warning("Unknown message type: %s", msg_type)

    except websockets.exceptions.ConnectionClosedOK:
        pass
    except websockets.exceptions.ConnectionClosedError as e:
        log.warning("Connection closed with error: %s", e)
    finally:
        state.remove_peer(ws)


# ──────────────────────────────────────────────────────────────────────────────
# Entrypoint
# ──────────────────────────────────────────────────────────────────────────────

async def main(host: str = "0.0.0.0", port: int = 8765) -> None:
    state = ServerState()

    log.info("═══════════════════════════════════════════")
    log.info("  LILIETH_RISER WebSocket Sync Server")
    log.info("  Kernel v1.0.47  |  Sovereign Protocol")
    log.info("  Listening on ws://%s:%d", host, port)
    log.info("═══════════════════════════════════════════")

    async with websockets.serve(
        lambda ws: connection_handler(ws, state),
        host, port,
        ping_interval=20,
        ping_timeout=10,
    ):
        await asyncio.Future()   # run forever


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LILIETH_RISER WebSocket Sync Server")
    parser.add_argument("--host", default="0.0.0.0", help="Bind address")
    parser.add_argument("--port", type=int, default=8765, help="Port number")
    args = parser.parse_args()

    try:
        asyncio.run(main(args.host, args.port))
    except KeyboardInterrupt:
        log.info("Server stopped.")
