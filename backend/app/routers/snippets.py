from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models import Comment, Snippet, User
from app.schemas import CommentCreate, CommentOut, SnippetCreate, SnippetOut

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


@router.get("/{snippet_id}/comments", response_model=list[CommentOut])
async def list_comments(
    snippet_id: int,
    payload: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    snippet = await db.get(Snippet, snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")

    result = await db.scalars(
        select(Comment)
        .where(Comment.snippet_id == snippet_id)
        .order_by(Comment.created_at)
    )

    return list(result)


@router.post(
    "/{snippet_id}/comments",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    snippet_id: int,
    payload: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    snippet = await db.get(Snippet, snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")

    comment = Comment(
        snippet_id=snippet_id,
        author_id=current_user.id,
        line_number=payload.line_number,
        body=payload.body,
    )

    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment
