"""
backend/app/main.py - FastAPI application entry point
"""
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.services.quant_engine import quant_engine
from backend.app.services.semi_engine import semi_engine
from backend.app.api.stocks import router as stocks_router
from backend.app.api.backtest import router as backtest_router
from backend.app.api.research import router as research_router
from backend.app.api.auth import router as auth_router
from backend.app.api.pro import router as pro_router, evaluate_position_doctor
from backend.app.api.referral import router as referral_router
from backend.app.api.semi import router as semi_router
from backend.app.api.telegram import router as telegram_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load datasets into quant & semi engine memory
    quant_engine.initialize()
    semi_engine.initialize()
    print(f"[RightSideAlpha] QuantEngine initialized: {len(quant_engine.stocks)} US stocks loaded.")
    print(f"[SemiFearGreed] SemiEngine initialized: {len(semi_engine.rows)} daily observations loaded.")
    yield
    print("[RightSideAlpha & SemiFearGreed] Server shutting down.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Core Routers (Milestones 1, 2, 3 & SemiFearGreed)
app.include_router(stocks_router, prefix="/api/stocks", tags=["stocks"])
app.include_router(backtest_router, prefix="/api/backtest", tags=["backtest"])
app.include_router(research_router, prefix="/api/research", tags=["research"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(pro_router, prefix="/api/pro", tags=["pro"])
app.include_router(referral_router, prefix="/api/referral", tags=["referral"])
app.include_router(semi_router, prefix="/api/semi", tags=["semi"])
app.include_router(telegram_router, prefix="/api/telegram", tags=["telegram"])

# Alias route for position doctor
app.post("/api/position-doctor", include_in_schema=False)(evaluate_position_doctor)


# Health Check Endpoints
@app.api_route("/health", methods=["GET", "HEAD"], tags=["system"])
@app.api_route("/api/health", methods=["GET", "HEAD"], tags=["system"])
def health_check():
    return {
        "status": "ok",
        "service": "RightSideAlpha & SemiFearGreed Quant Engine",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": settings.APP_VERSION,
        "env": settings.ENV,
        "engine_loaded": quant_engine.is_loaded,
        "stocks_loaded": len(quant_engine.stocks),
        "stock_count": len(quant_engine.stocks),
        "backtest_loaded": quant_engine.backtest_data is not None,
        "backtest_trades": len(quant_engine.trade_logs),
        "semi_engine_loaded": semi_engine.is_loaded,
        "semi_history_days": len(semi_engine.rows),
    }


# Unified static mounting (Milestone 4)
# Mounts production build (frontend/dist) or frontend source directory if index.html exists
_static_candidates = [
    settings.STATIC_DIR,
    settings.BASE_DIR / "frontend" / "dist",
    settings.BASE_DIR / "frontend",
]
_static_dir = next((p for p in _static_candidates if p.exists() and (p / "index.html").exists()), None)

if _static_dir:
    @app.get("/semi", include_in_schema=False)
    def semi_spa_entry():
        return FileResponse(str(_static_dir / "index.html"))

    app.mount("/", StaticFiles(directory=str(_static_dir), html=True), name="static")
else:
    @app.get("/", tags=["system"])
    def root_endpoint():
        return {
            "app": settings.APP_NAME,
            "status": "online",
            "version": settings.APP_VERSION,
        }


