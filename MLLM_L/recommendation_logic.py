from flask import request, session, jsonify, render_template, redirect, url_for
from sqlalchemy.exc import IntegrityError

from MLLM_L.database import User, UserFavoriteProject, HeritageProject, SimilarProject, UserFavoriteWork, Work, \
    SimilarWork, ViewProject, ViewWork
from MLLM_L.database_all import db
from MLLM_L.neo4j_utils import like_project_2, like_project_3


# 根据用户的收藏项目,调用对应的推荐算法，将与用户收藏项目相似的其他项目写入数据库表（SimilarProject）
def recommend2():
    current_username = session.get('username')

    if current_username:
        user = User.query.filter_by(username=current_username).first()
        if user:
            user_id = user.id

            favorite_projects = UserFavoriteProject.query.filter_by(user_id=user_id).all()
            print(favorite_projects)
            project_ids = [fav.project_id for fav in favorite_projects]
            print(project_ids)

            recommended_projects = HeritageProject.query.filter(HeritageProject.id.in_(project_ids)).all()
            print(recommended_projects)
            recommended_project_names = [project.project_name for project in recommended_projects]
            print(recommended_project_names)

            result = like_project_2({'project_names': recommended_project_names})
            print("ok1")
            print(result)

            if 'similar_projects_all' in result:
                print("ok2")
                for recommendation in result['similar_projects_all']:
                    project_name = recommendation['project_name']
                    print("ok3:", project_name)
                    similar_project_names = recommendation['similar_projects']
                    print("ok4:", similar_project_names)

                    current_project = HeritageProject.query.filter_by(project_name=project_name).first()
                    print("ok5:", current_project)

                    if current_project:
                        project_id = current_project.id

                        for similar_project_name in similar_project_names:
                            similar_project = HeritageProject.query.filter_by(project_name=similar_project_name).first()
                            if similar_project:
                                similar_project_id = similar_project.id

                                try:
                                    # 检查是否已存在相同的记录
                                    existing_record = SimilarProject.query.filter_by(user_id=user_id,
                                                                                     similar_project_id=similar_project_id).first()

                                    if not existing_record:
                                        print("ok6")
                                        # 创建 SimilarProject 实例并添加到数据库
                                        similar_project_instance = SimilarProject(user_id=user_id,
                                                                                  project_id=project_id,
                                                                                  similar_project_id=similar_project_id)
                                        print(similar_project_instance)
                                        db.session.add(similar_project_instance)

                                except IntegrityError:
                                    # 如果存在唯一性约束冲突，忽略该记录并继续处理下一个记录
                                    db.session.rollback()
                                    continue

                        # 提交会话，将对象写入数据库
                        db.session.commit()

            # 去除重复的项目详情
            seen_project_names = set()
            unique_project_details = []
            for project_detail in result['similar_projects_all']:
                project_name = project_detail['project_name']
                if project_name not in seen_project_names:
                    seen_project_names.add(project_name)
                    unique_project_details.append(project_detail)

            result['similar_projects_all'] = unique_project_details

            print(result)  # 打印最终的推荐结果

            return result
        else:
            return jsonify({'error': '用户不存在'}), 404
    else:
        return jsonify({'error': '未登录用户'}), 401


# 根据用户的收藏文创,调用对应的推荐算法，将与用户收藏文创相似的其他文创写入数据库表（SimilarWork）
def recommend3():
    current_username = session.get('username')

    if current_username:
        user = User.query.filter_by(username=current_username).first()
        if user:
            user_id = user.id

            favorite_projects = UserFavoriteWork.query.filter_by(user_id=user_id).all()
            print(favorite_projects)
            project_ids = [fav.work_id for fav in favorite_projects]
            print(project_ids)

            recommended_projects = Work.query.filter(Work.id.in_(project_ids)).all()
            print(recommended_projects)
            recommended_project_names = [project.work_name for project in recommended_projects]
            print(recommended_project_names)

            result = like_project_3({'project_names': recommended_project_names})
            print("Result from like_project_3:", result)

            if 'similar_projects_all' in result:
                print("ok2")
                for recommendation in result['similar_projects_all']:
                    project_name = recommendation['project_name']
                    print("ok3:", project_name)
                    similar_project_names = recommendation['similar_projects']
                    print("ok4:", similar_project_names)

                    current_project = Work.query.filter_by(work_name=project_name).first()
                    print("ok5:", current_project)

                    if current_project:
                        project_id = current_project.id

                        for similar_project_name in similar_project_names:
                            similar_project = Work.query.filter_by(work_name=similar_project_name).first()
                            if similar_project:
                                similar_project_id = similar_project.id

                                try:
                                    # 检查是否已存在相同的记录
                                    existing_record = SimilarWork.query.filter_by(user_id=user_id,
                                                                                  similar_work_id=similar_project_id).first()

                                    if not existing_record:
                                        print("ok6")
                                        # 创建 SimilarProject 实例并添加到数据库
                                        similar_project_instance = SimilarWork(user_id=user_id,
                                                                               work_id=project_id,
                                                                               similar_work_id=similar_project_id)
                                        print(similar_project_instance)
                                        db.session.add(similar_project_instance)

                                except IntegrityError:
                                    # 如果存在唯一性约束冲突，忽略该记录并继续处理下一个记录
                                    db.session.rollback()
                                    continue

                        # 提交会话，将对象写入数据库
                        db.session.commit()

            # 去除重复的项目详情
            seen_project_names = set()
            unique_project_details = []
            for project_detail in result['similar_projects_all']:
                project_name = project_detail['project_name']
                if project_name not in seen_project_names:
                    seen_project_names.add(project_name)
                    unique_project_details.append(project_detail)

            result['similar_projects_all'] = unique_project_details

            print(result)  # 打印最终的推荐结果

            return result
        else:
            return jsonify({'error': '用户不存在'}), 404
    else:
        return jsonify({'error': '未登录用户'}), 401


# 从数据库中获取当前用户对应的相似非遗项目和相似文创信息，并根据用户请求的分页信息进行查询和展示，以便在前端页面中显示用户获得的推荐项目和文创结果
def get_user_projects():
    current_username = session.get('username')

    if current_username:
        user = User.query.filter_by(username=current_username).first()

        if user:
            similar_projects = user.similar_projects
            similar_project_ids = [similar.similar_project_id for similar in similar_projects]

            similar_works = user.similar_works
            similar_work_ids = [similar.similar_work_id for similar in similar_works]

            # 获取项目分页
            page_projects = request.args.get('page_projects', 1, type=int)
            per_page_projects = 3
            user_projects = HeritageProject.query.filter(
                HeritageProject.id.in_(similar_project_ids)).distinct().paginate(page=page_projects,
                                                                                 per_page=per_page_projects)

            # 获取作品分页
            page_works = request.args.get('page_works', 1, type=int)
            per_page_works = 8
            user_works = Work.query.filter(
                Work.id.in_(similar_work_ids)).distinct().paginate(page=page_works, per_page=per_page_works)

            return render_template('heartpp.html', user_projects=user_projects, user_works=user_works)

    empty_projects = HeritageProject.query.filter_by(id=0).paginate()
    empty_works = Work.query.filter_by(id=0).paginate()
    return render_template('heartpp.html', user_projects=empty_projects, user_works=empty_works)


def get_user_fav():
    current_username = session.get('username')

    if current_username:
        user = User.query.filter_by(username=current_username).first()

        if user:
            user_favorite_projects = user.favorite_projects
            user_favorite_project_ids = [fav_project.project_id for fav_project in user_favorite_projects]

            user_favorite_works = user.favorite_works
            user_favorite_work_ids = [fav_work.work_id for fav_work in user_favorite_works]

            # 获取项目分页
            page_projects = request.args.get('page_projects', 1, type=int)
            per_page_projects = 3
            user_projects = HeritageProject.query.filter(
                HeritageProject.id.in_(user_favorite_project_ids)).paginate(page=page_projects,
                                                                            per_page=per_page_projects)

            # 获取作品分页
            page_works = request.args.get('page_works', 1, type=int)
            per_page_works = 4
            user_works = Work.query.filter(
                Work.id.in_(user_favorite_work_ids)).paginate(page=page_works, per_page=per_page_works)

            return render_template('mycollectp.html', user_projects=user_projects, user_works=user_works)

    # 处理未找到用户或用户收藏为空的情况
    # 返回空的分页对象或其他默认值
    empty_projects = HeritageProject.query.filter_by(id=0).paginate()
    empty_works = Work.query.filter_by(id=0).paginate()
    return render_template('mycollectp.html', user_projects=empty_projects, user_works=empty_works)


def display_heartpp_recommend():
    current_username = session.get('username')

    if current_username:
        # 根据用户名获取当前用户
        user = User.query.filter_by(username=current_username).first()

        if user:
            user_id = user.id  # 获取当前用户的ID

            # 检查用户收藏的项目记录
            if UserFavoriteProject.query.filter_by(user_id=user_id).first():
                recommend2()  # 调用 recommend2() 函数
            else:
                return redirect(url_for('select_recommend'))

            # 检查用户收藏的作品记录
            if UserFavoriteWork.query.filter_by(user_id=user_id).first():
                recommend3()  # 调用 recommend3() 函数
            else:
                return redirect(url_for('select_recommend_work'))

            return get_user_projects()  # 显示用户项目页面

    # 如果用户未登录或其他情况，返回登录页面或其他处理
    return render_template('login.html')


def log_project_interaction_project():
    data = request.json
    project_id = data.get('project_id')

    # 获取当前登录用户的 ID（假设会话中存储的是用户的用户名）
    current_username = session.get('username')

    if current_username:
        # 查询当前登录用户的 ID
        user = User.query.filter_by(username=current_username).first()
        print(user)

        if user:
            user_id = user.id

            # 查询是否存在该用户对该项目的浏览记录
            existing_interaction = ViewProject.query.filter_by(user_id=user_id, project_id=project_id).first()
            print(existing_interaction)

            if existing_interaction:
                # 如果存在，增加浏览次数
                existing_interaction.view_count += 1
            else:
                # 如果不存在，创建新的浏览记录
                new_interaction = ViewProject(user_id=user_id, project_id=project_id, view_count=1)
                print(new_interaction)
                db.session.add(new_interaction)

            # 提交数据库修改
            db.session.commit()

            return jsonify({'message': 'Project interaction logged successfully.'}), 200
        else:
            return jsonify({'error': 'User not found.'}), 404
    else:
        return jsonify({'error': 'User not authenticated.'}), 401


def log_work_interaction_work():
    data = request.json
    work_id = data.get('work_id')
    print("work_id:", work_id)

    # 获取当前登录用户的 ID（假设会话中存储的是用户的用户名）
    current_username = session.get('username')

    if current_username:
        # 查询当前登录用户的 ID
        user = User.query.filter_by(username=current_username).first()
        print(user)

        if user:
            user_id = user.id

            # 查询是否存在该用户对该项目的浏览记录
            existing_interaction = ViewWork.query.filter_by(user_id=user_id, work_id=work_id).first()
            print(existing_interaction)

            if existing_interaction:
                # 如果存在，增加浏览次数
                existing_interaction.view_count += 1
            else:
                # 如果不存在，创建新的浏览记录
                new_interaction = ViewWork(user_id=user_id, work_id=work_id, view_count=1)
                print(new_interaction)
                db.session.add(new_interaction)

            # 提交数据库修改
            db.session.commit()

            return jsonify({'message': 'Work interaction logged successfully.'}), 200
        else:
            return jsonify({'error': 'User not found.'}), 404
    else:
        return jsonify({'error': 'User not authenticated.'}), 401
