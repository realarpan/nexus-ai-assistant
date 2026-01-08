"""Document management endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.document import Document
from app.schemas.document import DocumentResponse, DocumentCreate

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a document to knowledge base"""
    content = await file.read()
    
    # Create document
    document = Document(
        user_id=current_user.id,
        title=file.filename,
        content=content.decode('utf-8', errors='ignore'),
        file_type=file.content_type,
        file_size=len(content)
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return document

@router.get("/", response_model=List[DocumentResponse])
async def get_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all user documents"""
    documents = db.query(Document).filter(
        Document.user_id == current_user.id
    ).order_by(Document.created_at.desc()).all()
    
    return documents