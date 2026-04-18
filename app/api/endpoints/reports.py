from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import os
import uuid
import shutil
from datetime import datetime
from app.db.session import get_db
from app.db.models import ReportHistory, User
from app.api.deps import get_current_user
from app.services.word_service import get_template_path, reformat_docx_smart
from app.core.config import UPLOADS_DIR, EXPORTS_DIR

router = APIRouter()

@router.post("/reformat")
async def reformat_report(
    title: str = Form(...),
    version: str = Form("1.0"),
    template_id: int = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    draft_path = os.path.join(UPLOADS_DIR, f"Draft_{uuid.uuid4()}_{file.filename}")
    with open(draft_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    tpl_path = get_template_path(db, template_id)
    out_name = f"Reformatted_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.docx"
    output_path = os.path.join(EXPORTS_DIR, out_name)

    try:
        reformat_docx_smart(tpl_path, draft_path, output_path, {"title": title, "version": version})
        
        # Save history linked to USER
        db.add(ReportHistory(
            title=title + " (S.Ref)", 
            version=version, 
            filename=out_name,
            user_id=current_user.id
        ))
        db.commit()
        
        if os.path.exists(draft_path):
            os.remove(draft_path)
        return {"status": "success", "filename": out_name}
    except Exception as e:
        db.rollback()
        if os.path.exists(draft_path):
            os.remove(draft_path)
        raise HTTPException(status_code=500, detail=str(e))
