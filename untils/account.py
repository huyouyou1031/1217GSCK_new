from models.account import User, Post, Like,session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

import hashlib


def hashMD5(test):
    return hashlib.md5(test.encode('utf8')).hexdigest()

# USER_DATA = {
#     'username':'tudo',
#     'password':'123'
# }

def authenticate(username,password):
    if hashMD5(password) == User.get_password(username):
        return True
    else:
        return False

def register(username,password):
    if User.is_exists(username):
        return '已存在用户名'
    else:
        User.add_user(username, hashMD5(password))
        return 'ok'

class handlerORM():

    def __init__(self,db_session):
        self.db = db_session

    def add_post_for(self,username,image_url,thumb_url):
        user = self.db.query(User).filter_by(name=username).first()
        print(user)
        post = Post(image_url=image_url,thumb_url=thumb_url,user = user)
        self.db.add(post)
        self.db.commit()
        return post

    def get_post_for(self,username):
        user = self.db.query(User).filter_by(name=username).first()
        if user:
            print(user.posts)
            return user.posts
        else:
            return []

    def get_post(self,post_id):
        post = self.db.query(Post).filter_by(id=post_id).scalar()
        return post

    def get_all_posts(self):
        posts = self.db.query(Post).order_by(Post.id.desc()).all()
        return posts

    def get_user(self,username):
        user = self.db.query(User).filter_by(name=username).first()
        return user

    def get_like_posts(self,user):
        if user:
            posts = self.db.query(Post).filter(Post.id==Like.post_id,user.id==Like.user_id).all()
        else:
            posts = []
        return posts

    def get_like_count(self,post):
        count = self.db.query(Like).filter_by(post_id=post.id).count()
        return count