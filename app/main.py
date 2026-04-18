from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.api.router import api_router
from app.core.config import STATIC_DIR, TEMPLATES_UI_DIR, ADMIN_USER, ADMIN_PASSWORD, ADMIN_EMAIL, GOOGLE_CLIENT_ID
from app.db.session import SessionLocal
from app.db.models import User
from app.core import security

def create_default_admin():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        if not admin:
            hashed_pwd = security.get_password_hash(ADMIN_PASSWORD)
            new_admin = User(
                full_name=ADMIN_USER, 
                email=ADMIN_EMAIL, 
                hashed_password=hashed_pwd, 
                role="admin"
            )
            db.add(new_admin)
            db.commit()
            print(f"--- Default Admin Created: {ADMIN_USER} ---")
    finally:
        db.close()

def create_app() -> FastAPI:
    app = FastAPI(title="SmartPro Tools SaaS")

    # Initialize Admin
    create_default_admin()

    # Static files and Templates
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    templates_ui = Jinja2Templates(directory=TEMPLATES_UI_DIR)

    # Base Route
    @app.get("/")
    async def home(request: Request):
        if not request.cookies.get("access_token"):
            return RedirectResponse(url="/login")
        return templates_ui.TemplateResponse("index.html", {"request": request})

    # Login Route
    @app.get("/login")
    async def login_page(request: Request):
        if request.cookies.get("access_token"):
            return RedirectResponse(url="/")
        return templates_ui.TemplateResponse("login.html", {
            "request": request, 
            "google_client_id": GOOGLE_CLIENT_ID
        })

    # Include API Routers
    app.include_router(api_router, prefix="/api")

    return app
