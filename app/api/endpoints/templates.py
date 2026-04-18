from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
import uuid
import os
import shutil
from app.db.session import get_db
from app.db.models import TemplateDoc, User
from app.api.deps import get_current_user
from app.core.config import TEMPLATES_WORD_DIR

router = APIRouter()

@router.get("/templates")
async def list_templates(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Admin sees ALL templates
    if current_user.role == "admin":
        return db.query(TemplateDoc).order_by(TemplateDoc.is_master.desc(), TemplateDoc.created_at.desc()).all()
    
    # User sees Master OR their own
    return db.query(TemplateDoc).filter(
        or_(TemplateDoc.is_master == True, TemplateDoc.user_id == current_user.id)
    ).order_by(TemplateDoc.is_master.desc(), TemplateDoc.created_at.desc()).all()

@router.post("/templates")
async def upload_template(
    name: str = Form(...), 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are allowed")
    
    filename = f"Tpl_{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(TEMPLATES_WORD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    new_tpl = TemplateDoc(name=name, filename=filename, is_master=False, user_id=current_user.id)
    db.add(new_tpl)
    db.commit()
    return {"status": "success", "id": new_tpl.id}

@router.delete("/templates/{tid}")
async def delete_template(tid: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tpl = db.query(TemplateDoc).filter(TemplateDoc.id == tid).first()
    if not tpl: raise HTTPException(status_code=404)
    if tpl.is_master: raise HTTPException(status_code=400, detail="Cannot delete Master Template")
    
    # Permission check: Admin can delete anything, User can only delete their own
    if current_user.role != "admin" and tpl.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền xóa mẫu này")
    
    file_path = os.path.join(TEMPLATES_WORD_DIR, tpl.filename)
    if os.path.exists(file_path): os.remove(file_path)
    
    db.delete(tpl)
    db.commit()
    return {"status": "success"}

@router.get("/templates/preview/{tid}")
async def preview_template(tid: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tpl = db.query(TemplateDoc).filter(TemplateDoc.id == tid).first()
    if not tpl: raise HTTPException(status_code=404)
    
    # Permission check: Admin OR Master OR owned by user
    if current_user.role != "admin" and not tpl.is_master and tpl.user_id != current_user.id:
         raise HTTPException(status_code=403, detail="Permission denied")

    file_path = os.path.join(TEMPLATES_WORD_DIR, tpl.filename)
    if not os.path.exists(file_path): raise HTTPException(status_code=404)
    return FileResponse(file_path, filename=f"Preview_{tpl.name}.docx")
