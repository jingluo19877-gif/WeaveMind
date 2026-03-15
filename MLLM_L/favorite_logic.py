from flask import session, redirect, url_for, render_template, request, jsonify
from MLLM_L.database import User, UserFavoriteProject, UserFavoriteWork
from MLLM_L.database_all import db


def delete_favorite_project(project_id):
    username = session.get('username')

    if username:
        user = User.query.filter_by(username=username).first()

        if user:
            # 查找要删除的收藏项目
            favorite_project = UserFavoriteProject.query.filter_by(user_id=user.id, project_id=project_id).first()

            if favorite_project:
                # 删除收藏项目
                db.session.delete(favorite_project)
                db.session.commit()
                return redirect(url_for('show_collection'))
            else:
                # 收藏项目不存在或不属于当前用户
                return render_template('收藏项目不存在或无权删除')
        else:
            # 用户不存在
            return render_template('用户不存在')
    else:
        # 用户未登录
        return render_template('login.html', message='请先登录')


def delete_favorite_work(work_id):
    username = session.get('username')

    if username:
        user = User.query.filter_by(username=username).first()

        if user:
            # 查找要删除的收藏项目
            favorite_work = UserFavoriteWork.query.filter_by(user_id=user.id, work_id=work_id).first()
            print(favorite_work)

            if favorite_work:
                # 删除收藏项目
                db.session.delete(favorite_work)
                db.session.commit()
                print("ok")
                return redirect(url_for('show_collection'))
            else:
                # 收藏项目不存在或不属于当前用户
                return render_template('收藏项目不存在或无权删除')
        else:
            # 用户不存在
            return render_template('用户不存在')
    else:
        # 用户未登录
        return render_template('login.html', message='请先登录')



def add_favorite_select_project():
    # 检查用户是否已登录
    if 'username' in session:
        username = session['username']

        # 查询用户信息，获取 user_id
        user = User.query.filter_by(username=username).first()
        if user:
            user_id = user.id

            # 从前端获取 project_id
            data = request.get_json()
            project_id_str = data.get('projectId')
            try:
                project_id = int(project_id_str)
            except ValueError:
                return jsonify({'message': '无效的 project_id！'}), 400

            # 创建 UserFavoriteProject 对象并添加到数据库
            favorite_project = UserFavoriteProject(user_id=user_id, project_id=project_id)
            db.session.add(favorite_project)
            db.session.commit()
            print("Before redirection")


            return jsonify({'message': '收藏成功！'})
        else:
            return jsonify({'message': '用户不存在！'}), 404
    else:
        return jsonify({'message': '用户未登录！'}), 401


def add_favorite_select_work():
    # 检查用户是否已登录
    if 'username' in session:
        username = session['username']

        # 查询用户信息，获取 user_id
        user = User.query.filter_by(username=username).first()
        if user:
            user_id = user.id

            # 从前端获取 project_id
            data = request.get_json()
            work_id_str = data.get('workId')
            print(work_id_str)
            try:
                work_id = int(work_id_str)
            except ValueError:
                return jsonify({'message': '无效的 work_id！'}), 400

            # 创建 UserFavoriteProject 对象并添加到数据库
            favorite_work = UserFavoriteWork(user_id=user_id, work_id=work_id)
            print("2",favorite_work)
            db.session.add(favorite_work)
            db.session.commit()


            return jsonify({'message': '收藏成功！'})
        else:
            return jsonify({'message': '用户不存在！'}), 404
    else:
        return jsonify({'message': '用户未登录！'}), 401