from sqlalchemy import Boolean, Column, ForeignKey, Integer, Table, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from . import Base


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = Column(UUID, primary_key=True,
                server_default=text("uuid_generate_v1()"))
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    score = Column(Integer, server_default=text("0"))

    parents = relationship(
        'User',
        secondary='friend',
        primaryjoin='User.id == friend.c.fromFriendId',
        secondaryjoin='User.id == friend.c.toFriendId'
    )


# Friendship association table
t_friend = Table(
    'friend', Base.metadata,
    Column('fromFriendId', ForeignKey('user.id'),
           primary_key=True, nullable=False),
    Column('toFriendId', ForeignKey('user.id'),
           primary_key=True, nullable=False)
)


class Snap(Base):
    __tablename__ = 'snap'

    id = Column(UUID, primary_key=True,
                server_default=text("uuid_generate_v1()"))
    fromUserId = Column(ForeignKey('user.id'))
    toUserId = Column(ForeignKey('user.id'))
    read = Column(Boolean, server_default=text("false"))

    user = relationship('User', primaryjoin='Snap.fromUserId == User.id')
    user1 = relationship('User', primaryjoin='Snap.toUserId == User.id')


class LoginToken(Base):
    __tablename__ = "loginToken"

    token = Column(UUID, primary_key=True,
                   server_default=text("uuid_generate_v1()"))
    userId = Column(ForeignKey('user.id'))
    valid = Column(Boolean, server_default=text("true"))

    user = relationship('User', primaryjoin='LoginToken.userId == User.id')
