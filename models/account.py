from datetime import datetime
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from .db import Base,DBSession

from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship


session = DBSession()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(50),unique=True,nullable=False)
    password = Column(String(50),nullable=False)
    created = Column(DateTime,default=datetime.now)

    def __repr__(self):
        return '<User(#{}:{})>'.format(self.id,self.name)

    @classmethod
    def add_user(cls,username,password):
        user = User(name=username,password=password)
        session.add(user)
        session.commit()

    @classmethod
    def is_exists(cls,username):
        tf = session.query(exists().where(User.name==username)).scalar()
        return tf

    @classmethod
    def get_password(cls,uername):
        u = session.query(User).filter_by(name=uername).first()
        print(u)
        if u:
            return u.password
        else:
            return None

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key=True,autoincrement=True)
    image_url = Column(String(150))
    thumb_url = Column(String(150))

    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship('User',backref='posts',uselist=False,cascade='all')

    def __repr__(self):
        return "Post(id:{})".format(self.id)


class Like(Base):
    __tablename__ = 'likes'
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False,primary_key=True)
    post_id = Column(Integer,ForeignKey('posts.id'),nullable=False,primary_key=True)
