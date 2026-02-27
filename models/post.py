
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.user import User
from models.base import Base


class Post(Base):
    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(Text, default="",server_default="",)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] =relationship(back_populates="posts")

    def __str__(self):
        return f"{self.__class__.__name__}(title = {self.title!r}, author_id = {self.author_id!r}, post_id = {self.id!r})"

    def __repr__(self):
        return self.__str__()
