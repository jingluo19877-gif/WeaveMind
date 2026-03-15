from flask import Flask, render_template, request,flash,session
from py2neo import Node

from MLLM_L.neo4j_utils import graph
from MLLM_L.utils import login
from flask import redirect, url_for



# 用户登录
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if login(username, password):
            session['username'] = username  # 将用户名存储在会话中
            flash("登录成功")
            return redirect(url_for('index'))
        else:
            flash('登录失败，请检查用户名和密码！')
            return redirect(url_for('login',))
    return render_template('login.html')




