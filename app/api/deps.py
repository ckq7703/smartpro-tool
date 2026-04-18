from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.core import security

async def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Bạn cần đăng nhập để thực hiện tính năng này")
    
    try:
        payload = security.jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token không hợp lệ")
        
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Người dùng không tồn tại")
        
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Phiên làm việc hết hạn")
