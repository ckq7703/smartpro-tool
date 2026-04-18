from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.core import security
from app.core.config import GOOGLE_CLIENT_ID
from pydantic import BaseModel, EmailStr
from google.oauth2 import id_token
from google.auth.transport import requests

router = APIRouter()

class UserRegister(BaseModel):
    name: str
    email: str # Changed to str to support non-email usernames like 'smartproadmin'
    password: str

class UserLogin(BaseModel):
    email: str 
    password: str

class GoogleLoginRequest(BaseModel):
    token: str

@router.post("/register")
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Tài khoản/Email đã được đăng ký")
    
    hashed_pwd = security.get_password_hash(user_data.password)
    # Force default role to 'user' for safety
    new_user = User(
        full_name=user_data.name, 
        email=user_data.email, 
        hashed_password=hashed_pwd, 
        role="user" 
    )
    db.add(new_user)
    db.commit()
    return {"status": "success", "message": "Đăng ký thành công"}

@router.post("/login")
async def login(response: Response, login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not user.hashed_password or not security.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Tài khoản hoặc mật khẩu không đúng")
    
    token = security.create_access_token(data={"sub": str(user.id)})
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=3600*24)
    return {"status": "success", "user": {"name": user.full_name, "email": user.email, "role": user.role}}

@router.post("/google-login")
async def google_login(response: Response, data: GoogleLoginRequest, db: Session = Depends(get_db)):
    try:
        idinfo = id_token.verify_oauth2_token(data.token, requests.Request(), GOOGLE_CLIENT_ID)
        email = idinfo['email']
        name = idinfo.get('name', email.split('@')[0])
        google_id = idinfo['sub']

        user = db.query(User).filter(User.email == email).first()
        if not user:
            # Auto-register as 'user'
            user = User(full_name=name, email=email, google_id=google_id, role="user")
            db.add(user)
            db.commit()
            db.refresh(user)
        
        token = security.create_access_token(data={"sub": str(user.id)})
        response.set_cookie(key="access_token", value=token, httponly=True, max_age=3600*24)
        return {"status": "success", "user": {"name": user.full_name, "email": user.email, "role": user.role}}
    except ValueError:
        raise HTTPException(status_code=400, detail="Google Token không hợp lệ")

@router.get("/me")
async def get_me(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Chưa đăng nhập")
    try:
        payload = security.jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user: raise HTTPException(status_code=401)
        return {"name": user.full_name, "email": user.email, "role": user.role}
    except:
        raise HTTPException(status_code=401)

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "success"}
