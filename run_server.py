import os
os.environ.setdefault('DEFAULT_VIEW', 'rightside')
#!/usr/bin/env python
"""
run_server.py - RightSideAlpha Unified Production Server Runner
Starts the FastAPI application serving both the REST APIs (/api/...)
and the frontend single-page application at /
"""
import os
import sys
import argparse
from pathlib import Path
import uvicorn

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main():
    parser = argparse.ArgumentParser(description="RightSideAlpha Production Server")
    parser.add_argument("--host", type=str, default=os.getenv("HOST", "0.0.0.0"), help="Bind host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8000")), help="Bind port (default: 8000)")
    parser.add_argument("--reload", action="store_true", default=False, help="Enable auto-reload for development")
    args = parser.parse_args()

    print("=" * 70)
    print(f" [RIGHTSIDEALPHA] Launching Unified Web Server on {args.host}:{args.port}")
    print(f"  - REST API Documentation: http://{args.host if args.host != '0.0.0.0' else '127.0.0.1'}:{args.port}/docs")
    print(f"  - Web Application:       http://{args.host if args.host != '0.0.0.0' else '127.0.0.1'}:{args.port}/")
    print("=" * 70)

    uvicorn.run(
        "backend.app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info",
    )


if __name__ == "__main__":
    main()
