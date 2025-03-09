from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas


async def get_author_list(db: AsyncSession):
    result = await db.execute(
        select(models.Author).options(selectinload(models.Author.books))
    )
    authors = result.scalars().all()
    return authors


async def get_author(db: AsyncSession, author_id: int):
    result = await db.execute(
        select(models.Author).options(selectinload(models.Author.books)).where(models.Author.id == author_id)
    )
    author = result.scalar_one_or_none()
    return author


async def add_author(db: AsyncSession, author: schemas.AuthorCreate):
    new_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(new_author)
    await db.commit()
    await db.refresh(new_author)
    return new_author
