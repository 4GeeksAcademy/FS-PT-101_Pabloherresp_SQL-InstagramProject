import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    posts: Mapped[list["Posts"]] = relationship(back_populates="user")
    comments: Mapped[list["Comments"]] = relationship(back_populates="user")

    # followers: Mapped[list["Follower"]] = relationship("follower", foreign_keys="[Follower.user_to_id]", back_populates="user_to")
    # followed: Mapped[list["Follower"]] = relationship("follower", foreign_keys="[Follower.user_from_id", back_populates="user_from")
    followers: Mapped[list["Follower"]] = relationship(back_populates="followed", foreign_keys="[Follower.user_to_id]")
    followed: Mapped[list["Follower"]] = relationship(back_populates="follower", foreign_keys="[Follower.user_from_id]")

class Follower(db.Model):
    __tablename__ = "follower"
    user_from_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    follower: Mapped["Users"] = relationship("Users", back_populates="followed", foreign_keys=[user_from_id])
    followed: Mapped["Users"] = relationship("Users", back_populates="followers", foreign_keys=[user_to_id])

class Posts(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="posts")
    media: Mapped[list["Media"]] = relationship(back_populates="post")
    comments: Mapped[list["Comments"]] = relationship(back_populates="post")

class Comments(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    user: Mapped["Users"] = relationship(back_populates="comments")
    post: Mapped["Posts"] = relationship(back_populates="comments")

class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"

class Media(db.Model):
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType),nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    post: Mapped["Posts"] = relationship(back_populates="media")