from flask import request, render_template
from sqlalchemy import or_

from MLLM_L.database import HeritageProject, Work


def search_projects():
    search_term = request.form.get('search', '')

    # 使用 SQLAlchemy 构建模糊搜索查询
    results = HeritageProject.query.filter(
        or_(
            HeritageProject.project_name.ilike(f'%{search_term}%'),
            HeritageProject.category_big.ilike(f'%{search_term}%'),
            HeritageProject.category_small.ilike(f'%{search_term}%')
        )
    ).all()

    print(f"Found {len(results)} results for search term: {search_term}")  # 调试输出搜索结果数量

    # 渲染搜索结果模板，并传递搜索结果到 base.html 中的 search_results 区域
    return render_template('base.html', content=None, search_results=results)


def search_works():
    search_term = request.form.get('search', '')

    # 使用 SQLAlchemy 构建模糊搜索查询
    results = Work.query.filter(
        or_(
            Work.price.ilike(f'%{search_term}%'),
            Work.work_name.ilike(f'%{search_term}%'),
            Work.category_big.ilike(f'%{search_term}%'),
            Work.category_small.ilike(f'%{search_term}%')
        )
    ).all()

    print(f"Found {len(results)} results for search term: {search_term}")  # 调试输出搜索结果数量

    # 渲染搜索结果模板，并传递搜索结果到 base.html 中的 search_results 区域
    return render_template('search_work.html', content=None, search_results=results)