from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.session import WritingSession
from app.services import writer

router = APIRouter(tags=["write"])


class TextIn(BaseModel):
    text: str = Field(min_length=1, max_length=20000)


class ToneIn(BaseModel):
    text: str = Field(min_length=1, max_length=20000)
    tone: str = "professional"


class EmailIn(BaseModel):
    intent: str = Field(min_length=1, max_length=5000)
    recipient: str | None = None
    tone: str = "professional"


class TransformIn(BaseModel):
    text: str = Field(min_length=1, max_length=20000)
    mode: str  # expand | shorten


class WriteOut(BaseModel):
    output: str
    session_id: int | None = None


class SessionOut(BaseModel):
    id: int
    mode: str
    input_text: str
    output_text: str
    meta: str | None
    created_at: datetime

    class Config:
        from_attributes = True


def _save_session(
    db: Session,
    user_id: int,
    mode: str,
    input_text: str,
    output_text: str,
    meta: str | None = None,
) -> WritingSession:
    row = WritingSession(
        owner_id=user_id,
        mode=mode,
        input_text=input_text,
        output_text=output_text,
        meta=meta,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def _run_ai(fn, *args, **kwargs) -> str:
    try:
        return fn(*args, **kwargs)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/write/rewrite", response_model=WriteOut)
def rewrite(
    body: TextIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    output = _run_ai(writer.rewrite, body.text)
    session = _save_session(db, current_user.id, "rewrite", body.text, output)
    return WriteOut(output=output, session_id=session.id)


@router.post("/write/tone", response_model=WriteOut)
def change_tone(
    body: ToneIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    output = _run_ai(writer.change_tone, body.text, body.tone)
    session = _save_session(db, current_user.id, "tone", body.text, output, meta=body.tone)
    return WriteOut(output=output, session_id=session.id)


@router.post("/write/email", response_model=WriteOut)
def draft_email(
    body: EmailIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    output = _run_ai(writer.draft_email, body.intent, body.recipient, body.tone)
    session = _save_session(
        db, current_user.id, "email", body.intent, output, meta=body.tone
    )
    return WriteOut(output=output, session_id=session.id)


@router.post("/write/transform", response_model=WriteOut)
def transform(
    body: TransformIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    output = _run_ai(writer.transform, body.text, body.mode)
    session = _save_session(db, current_user.id, body.mode, body.text, output)
    return WriteOut(output=output, session_id=session.id)


@router.get("/sessions/", response_model=list[SessionOut])
def list_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(WritingSession)
        .filter(WritingSession.owner_id == current_user.id)
        .order_by(WritingSession.created_at.desc())
        .limit(50)
        .all()
    )


@router.get("/sessions/{session_id}", response_model=SessionOut)
def get_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = (
        db.query(WritingSession)
        .filter(WritingSession.id == session_id, WritingSession.owner_id == current_user.id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Session not found")
    return row


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = (
        db.query(WritingSession)
        .filter(WritingSession.id == session_id, WritingSession.owner_id == current_user.id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(row)
    db.commit()
