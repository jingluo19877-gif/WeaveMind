from flask import render_template, session, redirect, url_for


def index_session():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
    else:
        return redirect(url_for('login'))
