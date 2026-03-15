from flask import request, redirect, url_for, send_file, send_from_directory, Response, session
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from sqlalchemy import text, or_, func
from MLLM_L.collection import get_user_favorites, get_user_favorites_work
from MLLM_L.database import db, HeritageProject, User, UserFavoriteProject, SimilarProject, \
    ViewProject, Work, ViewWork, UserFavoriteWork, SelectProject, SelectWork
from MLLM_L.favorite_logic import delete_favorite_project, delete_favorite_work, add_favorite_select_project, \
    add_favorite_select_work
from MLLM_L.neo4j_utils import execute_neo4j_query, execute_node_detail_query, \
    like_project_2, browse_project
from MLLM_L.recommendation_logic import recommend2, recommend3, get_user_projects, get_user_fav, \
    log_project_interaction_project, display_heartpp_recommend, log_work_interaction_work
from MLLM_L.search_logic import search_projects, search_works
from MLLM_L.user_logic import get_user_favorites_2
from MLLM_L.utils import submit_1
from MLLM_L.user_management import user_login
from MLLM_L.view import index_session
import subprocess
from flask_socketio import SocketIO
from flask import jsonify
import logging

app = Flask(__name__)
bootstrap = Bootstrap(app)
# 设置会话保护级别
app.config['SESSION_PROTECTION'] = 'strong'
socketio = SocketIO(app, async_mode='threading')  # 不设置路径，使用默认路径
pp = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0000@localhost/fychat'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:309817@localhost:3307/feiyi'
app.config['SECRET_KEY'] = '0000'

streamlit_process = None

db.init_app(app)

logging.basicConfig(level=logging.INFO)  # 设置日志级别为INFO
logger = logging.getLogger(__name__)


@app.route("/")
def first():
    return render_template('first.html')


@app.route("/index.html")
def index():
    return render_template('index.html')


@app.route('/404.html')
def page_404():
    return render_template('404.html')


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/blog.html')
def blog():
    return render_template('blog.html')


@app.route('/blog-details.html')
def blog_details():
    return render_template('blog-details.html')


@app.route('/blog-grid.html')
def blog_grid():
    return render_template('blog-grid.html')


@app.route('/client.html')
def client():
    return render_template('client.html')


@app.route('/contact.html')
def contact():
    return render_template('contact.html')


@app.route('/embed.html')
def embed():
    return render_template('embed.html')


@app.route('/index2.html')
def index2():
    return render_template('index2.html')


@app.route('/index3.html')
def index3():
    return render_template('index3.html')


@app.route('/portfolio.html')
def portfolio():
    return render_template('portfolio.html')


@app.route('/portfolio-details.html')
def portfolio_details():
    return render_template('portfolio-details.html')


@app.route('/project.html')
def project():
    return render_template('project.html')


@app.route('/service.html')
def service():
    return render_template('service.html')


@app.route('/shop.html')
def shop():
    return render_template('shop.html')


@app.route('/shop-details.html')
def shop_details():
    return render_template('shop-details.html')


@app.route('/team-member.html')
def team_member():
    return render_template('team-member.html')


@app.route('/login.html')
def login_l():
    return render_template('login.html')


@app.route('/linyun_l.html')
def linyun_l():
    return render_template('linyun_l.html')


# 注册功能
@app.route("/register", methods=['POST'])
def submit_route():
    return submit_1()


# 登录功能
@app.route('/login', methods=['GET', 'POST'])
def login():
    return user_login()


@app.route('/index')
def index_route():
    return index_session()  # 使用导入的index函数


@app.route('/start_streamlit_3')
def start_streamlit_3():
    global streamlit_process

    # 检查 Streamlit 服务是否已经在运行
    # if streamlit_process is None or not psutil.pid_exists(streamlit_process.pid):
    # 使用 subprocess 模块启动 Streamlit 应用程序，并存储进程对象
    streamlit_process = subprocess.Popen(['streamlit', 'run', 'MLLM_L3/Home.py'])

    return '个性化非遗探索即刻开启'


@app.route('/start_streamlit_4')
def start_streamlit_4():
    global streamlit_process

    # 检查 Streamlit 服务是否已经在运行
    # if streamlit_process is None or not psutil.pid_exists(streamlit_process.pid):
    # 使用 subprocess 模块启动 Streamlit 应用程序，并存储进程对象
    streamlit_process = subprocess.Popen(['streamlit', 'run', 'MLLM_L4/Home.py'])

    return '文创助手即刻开启'


@app.route('/t_recommend.html')
def recommend():
    return render_template('t_recommend.html')


@app.route('/t_connect.html')
def connect():
    return render_template('t_connect.html')


@app.route('/t_line.html')
def line():
    return render_template('t_line.html')


@app.route('/search', methods=['GET'])
def search_heritage():
    query = '%' + request.args.get('q', '') + '%'

    engine = db.engine

    with engine.connect() as conn:
        stmt = text("SELECT * FROM heritage WHERE project_name LIKE :query")
        result = conn.execute(stmt, {"query": f'%{query}%'})
        heritage_items = [dict(zip(result.keys(), row)) for row in result] if result else []

    for row in result:
        print(row)

    return jsonify(heritage_items)


##非遗测试页面
@app.route('/z_test.html')
def z_test():
    return render_template('z_test.html')


##非遗地图页面
@app.route('/z_map.html')
def z_map():
    return render_template('z_map.html')


##非遗地图页面
@app.route('/start_z_map')
def start_z_map():
    return render_template('z_map.html')


@app.route('/w_communicate.html')
def w_communicate():
    return render_template('w_communicate.html')


@app.route('/w_MLanguageSupport.html')
def w_MLanguageSupport():
    page = request.args.get('page', 1, type=int)
    # 查询数据库，按照 id 降序排列，返回分页对象
    projects_pagination = HeritageProject.query.order_by(HeritageProject.id.desc()).paginate(page=page,
                                                                                             per_page=5)

    return render_template('w_MLanguageSupport.html', projects=projects_pagination)
    # return render_template('w_MLanguageSupport.html')


@app.route('/w_collection.html')
def w_collection():
    return render_template('w_collection.html')


@app.route('/number.html')
def test():
    return render_template('number.html')


@app.route('/dream.html')
def dream():
    return render_template('dream.html')


@app.route('/first.html')
def first_2():
    return render_template('first.html')


@app.route('/appointment.html')
def appointment():
    return render_template('appointment.html')


@app.route('/knowledge.html')
def knowledge():
    return render_template('knowledge.html')


# 这里保留路径跳转
@app.route('/search_2', methods=['POST'])
def search_projects_route():
    return search_projects()


@app.route('/transport.html')
def transport():
    return render_template('transport.html')


@app.route('/base.html')
def base():
    return render_template('base.html')


@app.route('/search_work.html')
def search_work():
    return render_template('search_work.html')


@app.route('/heartp.html')
def heartp():
    return render_template('heartp.html')


@app.route('/select_recommend.html')
def select_recommend():
    select_projects = SelectProject.query.all()
    return render_template('select_recommend.html', select_projects=select_projects)


@app.route('/select_recommend_work.html')
def select_recommend_work():
    select_works = SelectWork.query.all()
    for work in select_works:
        print(f"SelectWork id={work.id}, work_id={work.work_id}, picture_id={work.picture_id}")
    print("ok", select_works)
    return render_template('select_recommend_work.html', select_works=select_works)


# 定义 /data 路由
@app.route('/data')
def get_data():
    selected_province = request.args.get('province')
    print(selected_province)

    # 调用函数执行Neo4j查询
    links = execute_neo4j_query(selected_province)
    print(links)

    return jsonify(links)


@app.route('/node_detail')
def get_node_detail():
    node_name = request.args.get('node_name')

    # 调用函数执行Neo4j查询获取节点详细信息
    node_detail = execute_node_detail_query(node_name)

    return jsonify(node_detail)


@app.route('/visualize_node_detail', methods=['GET'])
def visualize_node_detail():
    search_keyword = request.args.get('search_keyword')

    # 调用函数执行Neo4j查询获取节点详细信息
    node_data = execute_node_detail_query(search_keyword)

    return jsonify(node_data)


@app.route('/browse_project', methods=['POST'])
def handle_browse_project():
    data = request.get_json()
    session_username = session.get('username')  # 假设已经存储在会话中

    result = browse_project(data, session_username)

    return jsonify(result)


@app.route('/favorite', methods=['POST'])
def show_user_favorites():
    # 调用 get_user_favorites 函数来获取当前用户的收藏列表
    return get_user_favorites(session)


@app.route('/favorite_work', methods=['POST'])
def show_user_favorites_work():
    # 调用 get_user_favorites 函数来获取当前用户的收藏列表
    return get_user_favorites_work(session)


@app.route('/user/favorites', methods=['GET'])
def get_user_favorites_route():
    return get_user_favorites_2()


# 这里保留路径跳转
@app.route('/mycollectp.html')
def mycollectp():
    return show_collection()


# 这里保留路径跳转
@app.route('/show_collection')
def show_collection():
    return get_user_fav()


@app.route('/heartpp.html')
def display_heartpp():
    return display_heartpp_recommend()


@app.route('/show_user_projects')
def show_user_projects():
    return get_user_projects()


# 这里保留路径跳转
@app.route('/delete_favorite_project/<int:project_id>', methods=['GET'])
def delete_favorite_project_route(project_id):
    return delete_favorite_project(project_id)


@app.route('/delete_favorite_work/<int:work_id>', methods=['GET'])
def delete_favorite_work_route(work_id):
    return delete_favorite_work(work_id)


# 这里保留路径跳转
@app.route('/recommend2', methods=['POST'])
def recommend2_route():
    return recommend2()


@app.route('/recommend3', methods=['POST'])
def recommend3_route():
    return recommend3()


@app.route('/log_project_interaction', methods=['POST'])
def log_project_interaction():
    return log_project_interaction_project()


@app.route('/log_work_interaction', methods=['POST'])
def log_work_interaction():
    return log_work_interaction_work()


@app.route('/work.html')
def work():
    page = request.args.get('page', 1, type=int)
    per_page = 8  # 每页显示的作品数量

    # 查询数据库，按照 id 从小到大排列，并返回分页对象
    projects_pagination = Work.query.order_by(Work.id).paginate(page=page, per_page=per_page, error_out=False)

    # 渲染 work.html 模板，传递分页对象给模板
    return render_template('work.html', projects_pagination=projects_pagination)


@app.route('/search_3', methods=['POST'])
def search_work_route():
    return search_works()


@app.route('/add_favorite_select_project', methods=['POST'])
def add_favorite_select_project_route():
    return add_favorite_select_project()


@app.route('/add_favorite_select_work', methods=['POST'])
def add_favorite_select_work_route():
    return add_favorite_select_work()


@app.route('/非遗游戏集-1.0-web/index.html')
def game():
    return render_template('非遗游戏集-1.0-web/index.html')


@app.route('/非遗游戏集-1.0-web/<path:filename>')
def custom_static(filename):
    # 处理静态文件的请求，从指定目录中发送文件
    return send_from_directory('templates/非遗游戏集-1.0-web', filename)


if __name__ == '__main__':
    # app.run(debug=True)
    # socketio.run(app, debug=True)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
