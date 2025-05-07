import os
import sys
import shutil
import webbrowser
import threading
import time
from flask import Flask
from app import app as flask_app

def get_resource_path(relative_path):
    """获取资源的绝对路径，适用于开发环境和打包后的环境"""
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        # 非打包环境，使用当前目录
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def ensure_db_dir():
    """确保数据库目录存在"""
    db_dir = os.path.join(os.path.expanduser("~"), ".optimal_samples_app")
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    return db_dir

def open_browser():
    """延迟打开浏览器"""
    time.sleep(1.5)  # 等待Flask启动
    webbrowser.open('http://127.0.0.1:5001')
    print("已自动打开浏览器，如未打开请访问: http://127.0.0.1:5001")

def init_app():
    """初始化应用程序环境"""
    # 确保模板和静态文件路径正确
    flask_app.template_folder = get_resource_path('templates')
    flask_app.static_folder = get_resource_path('static')
    
    # 设置数据库路径
    db_dir = ensure_db_dir()
    
    # 如果是打包后的环境，复制必要的文件到数据库目录
    if hasattr(sys, '_MEIPASS'):
        # 复制默认数据库（如果存在）
        for db_file in ['algo_history.db', 'ai_project.db']:
            src_path = get_resource_path(db_file)
            dst_path = os.path.join(db_dir, db_file)
            if os.path.exists(src_path) and not os.path.exists(dst_path):
                shutil.copy2(src_path, dst_path)
    
    return flask_app

if __name__ == '__main__':
    app = init_app()
    
    # 启动浏览器线程
    threading.Thread(target=open_browser).start()
    
    # 启动Flask应用
    print("正在启动优化样本选择系统...")
    print("请稍候，浏览器将自动打开...")
    app.run(debug=False, host='127.0.0.1', port=5001) 