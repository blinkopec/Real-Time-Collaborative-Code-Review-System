from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models import Snippet, User
from app.schemas import SnippetCreate, SnippetOut

router = APIRouter(prefix="/api/snippets", tags=["snippets"])


@router.get("", response_model=list[SnippetOut])
async def list_snippets(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.scalars(select(Snippet).order_by(Snippet.created_at.desc()))
    return list(result)


@router.post("", response_model=SnippetOut, status_code=status.HTTP_201_CREATED)
async def create_snippet(
    payload: SnippetCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    snippet = Snippet(
        title=payload.title,
        language=payload.language,
        code=payload.code,
        author_id=current_user.id,
    )
    db.add(snippet)
    await db.commit()
    await db.refresh(snippet)
    return snippet
