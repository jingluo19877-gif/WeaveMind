from flask import request,render_template,flash
from MLLM_L.database import add_user_to_db
from MLLM_L.database import get_user_by_username,check_username_exist

#用户提交
def submit_1():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']
        gender = request.form['gender']

        # 检查用户名是否已经存在
        if check_username_exist(username):
            flash('用户名已被注册，请选择一个不同的用户名！', 'error')
            return render_template('project.html')
        else:
            add_user_to_db(name, email, username, password, address, gender)
            flash("注册成功，请登录")
            return render_template('login.html')

    return render_template('project.html')

#用户登录
def login(username, password):
    user = get_user_by_username(username)

    if user is None:
        return False

    if user.password == password:
        return True
    else:
        return False