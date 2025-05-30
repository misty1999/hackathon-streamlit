from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(String(10000))  # マークダウン対応の本文
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('notes.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # リレーションシップ
    user = relationship('User', back_populates='notes')
    parent = relationship('Note', remote_side=[id], backref='children')


# ユーザー間のマッチングを管理する中間テーブル
matches = Table(
    'matches',
    Base.metadata,
    Column('user_id_1', Integer, ForeignKey('users.id'), primary_key=True),
    Column('user_id_2', Integer, ForeignKey('users.id'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('is_matched', Boolean, default=False)
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(100))
    age = Column(Integer)
    gender = Column(String(20))
    bio = Column(String(500))
    interests = Column(String(500))  # カンマ区切りの文字列として保存
    profile_image_url = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # ノート
    notes = relationship('Note', back_populates='user')
    
    # マッチング関係
    matches = relationship(
        'User',
        secondary=matches,
        primaryjoin=id==matches.c.user_id_1,
        secondaryjoin=id==matches.c.user_id_2,
        backref='matched_by'
    )

class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey('users.id'))
    to_user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    # リレーションシップ
    from_user = relationship('User', foreign_keys=[from_user_id], backref='likes_sent')
    to_user = relationship('User', foreign_keys=[to_user_id], backref='likes_received')
