from sqlalchemy.orm import relationship
from MLLM_L.database_all import db
from sqlalchemy import or_, Table, Column, Integer, ForeignKey


# 用户注册
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    address = db.Column(db.String(100))
    gender = db.Column(db.String(10))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


def add_user_to_db(name, email, username, password, address, gender):
    new_user = User(name=name, email=email, username=username, password=password, address=address, gender=gender)
    db.session.add(new_user)
    db.session.commit()


def get_user_by_username(username):
    # 查询数据库以获取特定用户名的用户信息
    user = User.query.filter_by(username=username).first()
    return user


def check_username_exist(username):
    user = get_user_by_username(username)
    return user is not None


class HeritageProject(db.Model):
    __tablename__ = 'heritage_projects'
    id = db.Column(db.Integer, primary_key=True)
    category_big = db.Column(db.String(255))
    category_small = db.Column(db.String(255))
    project_name = db.Column(db.String(255))
    specific_number = db.Column(db.String(255))
    description = db.Column(db.Text)


# 定义 UserFavoriteProject 模型，表示用户收藏项目的关系
class UserFavoriteProject(db.Model):
    __tablename__ = 'user_favorite_projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    project_id = db.Column(db.Integer, ForeignKey('heritage_projects.id'))

    # 定义与 User 和 HeritageProject 的关联关系
    user = relationship('User', backref='favorite_projects')
    project = relationship('HeritageProject', backref='favorited_by')

    def __repr__(self):
        return f'<UserFavoriteProject id={self.id} user_id={self.user_id} project_id={self.project_id}>'


class SimilarProject(db.Model):
    __tablename__ = 'similar_projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    project_id = Column(Integer, ForeignKey('heritage_projects.id'), nullable=False)
    similar_project_id = Column(Integer, ForeignKey('heritage_projects.id'), nullable=False)

    # 定义与 User 表的关联关系
    user = relationship('User', backref='similar_projects')

    # 定义与 HeritageProject 表的关联关系
    project = relationship('HeritageProject', foreign_keys=[project_id])
    similar_project = relationship('HeritageProject', foreign_keys=[similar_project_id])

    def __repr__(self):
        return f'<SimilarProject id={self.id} user_id={self.user_id} project_id={self.project_id} similar_project_id={self.similar_project_id}>'


class ViewProject(db.Model):
    __tablename__ = 'view_projects'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('heritage_projects.id'))
    view_count = db.Column(db.Integer)
    user = db.relationship('User', backref='view_projects')
    project = db.relationship('HeritageProject', backref='view_projects')

    def __repr__(self):
        return f'<ViewProject(id={self.id}, user_id={self.user_id}, project_id={self.project_id})>'


# 定义工作表的模型类
class Work(db.Model):
    __tablename__ = 'work'

    id = db.Column(db.Integer, primary_key=True)
    category_big = db.Column(db.String(255))
    category_small = db.Column(db.String(255))
    work_name = db.Column(db.String(255))
    specific_number = db.Column(db.String(255))
    price = db.Column(db.String(255))

    def __repr__(self):
        return f'<Work id={self.id} work_name={self.work_name}>'


class UserFavoriteWork(db.Model):
    __tablename__ = 'user_favorite_works'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), nullable=False)

    # 定义与 User 模型的关联关系
    user = relationship('User', backref='favorite_works')

    # 定义与 Work 模型的关联关系
    work = relationship('Work', backref='favorited_by_users')

    def __repr__(self):
        return f'<UserFavoriteWork id={self.id} user_id={self.user_id} work_id={self.work_id}>'


class SimilarWork(db.Model):
    __tablename__ = 'similar_works'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), nullable=False)
    similar_work_id = db.Column(db.Integer, db.ForeignKey('work.id'), nullable=False)

    # 定义与 User 模型的关联关系
    user = relationship('User', backref='similar_works')

    # 定义与 Work 模型的关联关系
    work = relationship('Work', foreign_keys=[work_id], backref='related_similar_works')
    similar_work = relationship('Work', foreign_keys=[similar_work_id], backref='similar_to_works')

    def __repr__(self):
        return f'<SimilarWork id={self.id} user_id={self.user_id} work_id={self.work_id} similar_work_id={self.similar_work_id}>'


class ViewWork(db.Model):
    __tablename__ = 'view_works'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), nullable=False)
    view_count = db.Column(db.Integer, default=0)

    # 定义与 User 模型的关联关系
    user = relationship('User', backref='viewed_works')
    # 定义与 Work 模型的关联关系
    work = relationship('Work', backref='viewed_by_users')

    def __repr__(self):
        return f'<ViewWork id={self.id} user_id={self.user_id} work_id={self.work_id} view_count={self.view_count}>'


class SelectProject(db.Model):
    __tablename__ = 'select_project'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey('heritage_projects.id'))

    # 定义与 HeritageProject 模型的关联关系
    project = db.relationship('HeritageProject', backref='selected_projects')

    def __repr__(self):
        return f'<SelectProject id={self.id} project_id={self.project_id}>'


class SelectWork(db.Model):
    __tablename__ = 'select_work'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picture_id = db.Column(db.Integer)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'))

    # 定义与 HeritageProject 模型的关联关系
    work = db.relationship('Work', backref='selected_works')

    def __repr__(self):
        return f'<SelectWork id={self.id} work_id={self.work_id}>'
