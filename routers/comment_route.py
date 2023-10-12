from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from repository import comment_repo
from schemas.commentbase import CommentBase, CommentCreate
from schemas.user import TokenData
from service import oauth2

router: APIRouter = APIRouter(
    tags=['Comment']
)


@router.get('/comments/{id}', response_model=list[CommentBase])
def get_comments(id: int, db: Session = Depends(get_db)):
    return comment_repo.get_idbook(id, db)


@router.post('/comment/{id}')
def add_comment(request: CommentCreate, id: int, current_user: TokenData = Depends(oauth2.get_current_user),
                db: Session = Depends(get_db)):
    return comment_repo.create(request, id, current_user.username, db)
