from flask import render_template, session
from py2neo import Graph, Node, Relationship

from MLLM_L.database import UserFavoriteProject, ViewProject, User, UserFavoriteWork, ViewWork

# Neo4j数据库连接配置
uri = "bolt://localhost:7687"
username = "neo4j"
password = "0000"
graph = Graph(uri, auth=(username, password))


def execute_neo4j_query(selected_province):
    try:
        query = f"""
            MATCH (p1)-[:BELONGS_TO_6]->(p2 {{name: "{selected_province}"}})
            RETURN p1.name AS source, p2.name AS target LIMIT 4000
        """

        result = graph.run(query)
        records = [record for record in result]

        links = [{"source": record["source"], "target": record["target"]} for record in records]

        return links

    except Exception as e:
        print("Error occurred during query execution:", str(e))
        return {"error": str(e)}


def execute_node_detail_query(search_keyword):
    try:
        query = f"""
            MATCH (n:Project3)
            WHERE n.name CONTAINS "{search_keyword}"  // 使用CONTAINS进行模糊匹配
            RETURN n.name AS name, n.CategoryCN AS category, n.Proj_num AS proj_num,
                   n.ProvinceCN AS province, n.Region7CN AS region, n.Unit_CN AS unit
            """
        print(query)

        result = graph.run(query)
        node_detail = [{"name": record["name"], "category": record["category"],
                        "proj_num": record["proj_num"], "province": record["province"],
                        "region": record["region"], "unit": record["unit"]} for record in result]

        # 将查询结果转换为前端期望的格式
        formatted_data = node_detail
        print(formatted_data)

        return formatted_data

    except Exception as e:
        print("Error occurred during query execution:", str(e))
        return {"error": str(e)}


def browse_project(data, session_username):
    project_name = data['project_name']
    category_big = data['category_big']

    # 查找用户节点（假设用户节点已经在登录时创建）
    user_node = graph.nodes.match("User", username=session_username).first()
    print(user_node)

    if not user_node:
        return {'error': '用户节点未找到'}

    # 创建或获取非遗类别节点
    category_node = graph.nodes.match("Category7", name=category_big).first()
    print(category_node)
    if not category_node:
        category_node = Node("Category7", name=category_big)
        graph.create(category_node)

    # 创建用户与非遗类别的关系（View 关系）
    contains_rel = Relationship(user_node, "View", category_node)
    print(contains_rel)
    contains_rel["weight"] = 5
    graph.create(contains_rel)

    # 查找非遗类别包含的非遗项目并打印
    query = (
        f"MATCH (c:Category7 {{name: '{category_big}'}})-[:CONTAINS]->(p:IntangibleHeritage3 {{project_name: '{project_name}'}}) "
        "RETURN p"
    )
    print(query)
    result = graph.run(query).evaluate()

    if result:
        print(f"找到非遗项目：{project_name}")
        query_2 = (
            f"MATCH (c:Category7 {{name: '{category_big}'}})-[:CONTAINS]->(p1:IntangibleHeritage3 {{project_name: '{project_name}'}}) "
            "MATCH (c)-[:CONTAINS]->(p2:IntangibleHeritage3)-[r:SIMILARITY3]->(p1) "
            "WHERE p2.project_name <> p1.project_name "  # 排除自身项目
            "RETURN p2, r.score AS similarity_score "
            "ORDER BY r.score DESC "
            "LIMIT 3"
        )
        print(query_2)
        result = graph.run(query_2)
        print(result)

        similar_projects = []
        for record in result:
            project_node = record['p2']
            similarity_score = record['similarity_score']
            similar_projects.append(
                {'project_name': project_node['project_name'], 'similarity_score': similarity_score})

        print("找到相似项目：", similar_projects)

    return {'message': '浏览成功'}


def like_project_2(data):
    project_names = data.get('project_names', [])  # 获取多个项目名称列表

    if not project_names:
        return {'error': '未提供项目名称列表'}

    similar_projects_all = []

    for project_name in project_names:
        # 使用 DFS 查找与用户感兴趣项目相关的其他项目
        similar_projects = find_similar_projects_2(project_name)
        similar_projects_all.append({
            'project_name': project_name,
            'similar_projects': similar_projects
        })

    return {'similar_projects_all': similar_projects_all, 'message': '推荐成功'}


def find_similar_projects_2(project_name):
    similar_projects = []
    stack = [(project_name, 1.0)]  # 初始节点和初始权重
    visited = set()

    username2 = session.get('username')

    # 根据用户名查询对应的用户
    user = User.query.filter_by(username=username2).first()
    if not user:
        return similar_projects  # 如果找不到对应的用户，返回空列表或其他处理方式

    # 获取用户的 user_id
    user_id = user.id
    # 查询用户收藏记录
    user_favorites = UserFavoriteProject.query.filter_by(user_id=user_id).all()
    favorite_projects = {fav.project_id for fav in user_favorites}

    # 查询用户浏览记录
    user_views = ViewProject.query.filter_by(user_id=user_id).all()
    view_counts = {view.project_id: view.view_count for view in user_views}

    while stack:
        current_project, current_weight = stack.pop()
        if current_project in visited:
            continue
        visited.add(current_project)

        # 查询当前项目的相邻项目以及相似度权重（根据 SIMILARITY6 关系）
        query = (
            f"MATCH (p1:IntangibleHeritage5 {{project_name: '{current_project}'}})-[rel:SIMILARITY6]->(p2:IntangibleHeritage5) "
            "RETURN p2.project_name AS similar_project_name, rel.score AS similarity_score"
        )
        results = graph.run(query)

        for result in results:
            similar_project_name = result['similar_project_name']
            similarity_score = result['similarity_score']

            if similar_project_name not in visited:
                # 根据用户行为调整相似度分数
                if similar_project_name in favorite_projects:
                    similarity_score += 3  # 如果是收藏的项目，相似度分数增加 6
                if similar_project_name in view_counts:
                    similarity_score += view_counts[similar_project_name]  # 根据浏览次数增加相似度分数

                # 计算新节点的权重，权重乘以相似度分数（分数越高，权重越大）
                new_weight = current_weight * similarity_score

                # 将新节点和权重推入栈中
                stack.append((similar_project_name, new_weight))
                similar_projects.append((similar_project_name, new_weight))

    # 对相似项目按权重降序排序（权重越大，相关度越高）
    similar_projects.sort(key=lambda x: x[1], reverse=True)
    # 提取前10个项目名称
    top_10_projects = [project_name for project_name, weight in similar_projects[:6]]
    return top_10_projects


def like_project_3(data):
    project_names = data.get('project_names', [])  # 获取多个项目名称列表
    print(project_names)

    if not project_names:
        return {'error': '未提供项目名称列表'}

    similar_projects_all = []

    for project_name in project_names:
        # 使用 DFS 查找与用户感兴趣项目相关的其他项目
        similar_projects = find_similar_projects_3(project_name)
        similar_projects_all.append({
            'project_name': project_name,
            'similar_projects': similar_projects
        })

    return {'similar_projects_all': similar_projects_all, 'message': '推荐成功'}


def find_similar_projects_3(project_name):
    similar_projects = []
    stack = [(project_name, 1.0)]  # 初始节点和初始权重
    visited = set()

    username2 = session.get('username')

    # 根据用户名查询对应的用户
    user = User.query.filter_by(username=username2).first()
    if not user:
        return similar_projects  # 如果找不到对应的用户，返回空列表或其他处理方式

    # 获取用户的 user_id
    user_id = user.id
    # 查询用户收藏记录
    user_favorites = UserFavoriteWork.query.filter_by(user_id=user_id).all()
    favorite_projects = {fav.work_id for fav in user_favorites}

    # 查询用户浏览记录
    user_views = ViewWork.query.filter_by(user_id=user_id).all()
    view_counts = {view.work_id: view.view_count for view in user_views}

    while stack:
        current_project, current_weight = stack.pop()
        if current_project in visited:
            continue
        visited.add(current_project)

        # 查询当前项目的相邻项目以及相似度权重（根据 SIMILARITY6 关系）
        query = (
            f"MATCH (p1:Work {{project_name: '{current_project}'}})-[rel:SIMILARITY_W]->(p2:Work) "
            "RETURN p2.project_name AS similar_project_name, rel.score AS similarity_score"
        )
        results = graph.run(query)

        for result in results:
            similar_project_name = result['similar_project_name']
            similarity_score = result['similarity_score']

            if similar_project_name not in visited:
                # 根据用户行为调整相似度分数
                if similar_project_name in favorite_projects:
                    similarity_score += 0.8  # 如果是收藏的项目，相似度分数增加
                if similar_project_name in view_counts:
                    similarity_score += view_counts[similar_project_name]  # 根据浏览次数增加相似度分数

                # 计算新节点的权重，权重乘以相似度分数（分数越高，权重越大）
                new_weight = current_weight * similarity_score

                # 将新节点和权重推入栈中
                stack.append((similar_project_name, new_weight))
                similar_projects.append((similar_project_name, new_weight))

    # 对相似项目按权重降序排序（权重越大，相关度越高）
    similar_projects.sort(key=lambda x: x[1], reverse=True)
    # 提取前10个项目名称
    top_10_projects = [project_name for project_name, weight in similar_projects[:4]]
    return top_10_projects


def find_similar_projects(project_name):
    similar_projects = []
    stack = [(project_name, 1.0)]  # 初始节点和初始权重
    visited = set()

    while stack:
        current_project, current_weight = stack.pop()
        if current_project in visited:
            continue
        visited.add(current_project)

        # 查询当前项目的相邻项目以及相似度权重（根据 SIMILARITY6 关系）
        query = (
            f"MATCH (p1:IntangibleHeritage5 {{project_name: '{current_project}'}})-[rel:SIMILARITY6]->(p2:IntangibleHeritage5) "
            "RETURN p2.project_name AS similar_project_name, rel.score AS similarity_score"
        )
        print(query)
        results = graph.run(query)

        for result in results:
            similar_project_name = result['similar_project_name']
            similarity_score = result['similarity_score']

            if similar_project_name not in visited:
                # 计算新节点的权重，权重乘以相似度分数（分数越高，权重越大）
                new_weight = current_weight * similarity_score

                # 将新节点和权重推入栈中
                stack.append((similar_project_name, new_weight))
                similar_projects.append((similar_project_name, new_weight))

    # 对相似项目按权重降序排序（权重越大，相关度越高）
    similar_projects.sort(key=lambda x: x[1], reverse=True)
    return [project_name for project_name, weight in similar_projects]
