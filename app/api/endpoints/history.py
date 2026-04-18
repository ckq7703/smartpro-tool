from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
import os
from app.db.session import get_db
from app.db.models import ReportHistory, User
from app.api.deps import get_current_user
from app.core.config import EXPORTS_DIR

router = APIRouter()

@router.get("/history")
async def get_history(
    page: int = 1, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skip = (page - 1) * limit
    
    # Base query
    query = db.query(ReportHistory)
    
    # Filter by user_id ONLY IF user is NOT admin
    if current_user.role != "admin":
        query = query.filter(ReportHistory.user_id == current_user.id)
    
    total = query.with_entities(func.count(ReportHistory.id)).scalar()
    items = query.order_by(ReportHistory.created_at.desc()).offset(skip).limit(limit).all()
    total_pages = (total + limit - 1) // limit
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "pages": total_pages,
        "limit": limit
    }

@router.get("/download/{filename}")
async def download_file(filename: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check ownership OR role
    report = db.query(ReportHistory).filter(ReportHistory.filename == filename).first()
    if not report: raise HTTPException(status_code=404)
    
    if current_user.role != "admin" and report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền tải file này")
        
    file_path = os.path.join(EXPORTS_DIR, filename)
    if not os.path.exists(file_path): raise HTTPException(status_code=404)
    return FileResponse(file_path, filename=filename)
