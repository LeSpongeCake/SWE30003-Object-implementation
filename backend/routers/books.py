from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["books"])  # Tags for documentation

# Example endpoint
@router.get("/{book_id}")
def get_book(book_id: int):
  return {book_id}