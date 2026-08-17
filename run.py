#!/usr/bin/env python3
"""
COOUCodeGuard - Offline Source Code Plagiarism Detection System
Launcher Script
Chukwuemeka Odumegwu Ojukwu University (COOU), Uli Campus
"""

import sys
import os
import time
import socket
import webbrowser
import threading
import uvicorn

def is_port_available(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) != 0

def find_available_port(host: str, preferred_port: int) -> int:
    port = preferred_port
    while port < preferred_port + 50:
        if is_port_available(host, port):
            return port
        port += 1
    return preferred_port

def open_browser(url: str, delay: float = 1.2):
    time.sleep(delay)
    print(f"\n[COOUCodeGuard] Launching browser at: {url}")
    webbrowser.open(url)

def main():
    host = os.getenv("HOST", "127.0.0.1")
    preferred_port = int(os.getenv("PORT", "8000"))
    port = find_available_port(host, preferred_port)
    url = f"http://{host}:{port}"

    print("=" * 70)
    print("  COOUCodeGuard - Offline Source Code Plagiarism Detection System")
    print("  Chukwuemeka Odumegwu Ojukwu University (COOU), Uli Campus")
    print("  Department of Computer Science")
    print("=" * 70)
    print(f"[*] Offline Mode: ENABLED (Zero external API / cloud requirements)")
    print(f"[*] Database: SQLite Local Engine")
    print(f"[*] Server Starting on: {url}")
    print("=" * 70)

    # Launch browser in background thread
    threading.Thread(target=open_browser, args=(url,), daemon=True).start()

    # Run Uvicorn Server
    uvicorn.run(
        "backend.main:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
