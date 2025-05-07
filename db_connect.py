import sqlite3
import os
import time
import random

def get_app_data_dir():
    """获取应用数据目录"""
    app_dir = os.path.join(os.path.expanduser("~"), ".optimal_samples_app")
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
    return app_dir

def get_conn():
    db_path = os.path.join(get_app_data_dir(), 'ai_project.db')
    return sqlite3.connect(db_path)

def save_data(user_input, output):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO records (user_input, output) VALUES (?, ?)"
        cursor.execute(sql, (user_input, output))
        conn.commit()
    except Exception as e:
        print("保存数据失败:", str(e))
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_history():
    conn = get_conn()
    cursor = conn.cursor()
    try:
        sql = """
            SELECT id, user_input, output, 
                   datetime(create_time, 'localtime') as create_time 
            FROM records 
            ORDER BY id DESC
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print("查询历史记录失败:", str(e))
        return []
    finally:
        cursor.close()
        conn.close()

def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT NOT NULL,
                output TEXT NOT NULL,
                create_time TIMESTAMP DEFAULT (datetime('now', 'localtime'))
            )
        """)
        conn.commit()
        print("数据库表创建成功")
    except Exception as e:
        print("初始化数据库失败:", str(e))
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# 初始化数据库
init_db()

# 连接到本地 MySQL 数据库
conn = sqlite3.connect('ai_project.db')
cursor = conn.cursor()

# 示例：查询所有表
cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
tables = cursor.fetchall()
print(tables)

# 关闭连接
cursor.close()
conn.close()

def set_combination(base, up):
    if up > base or up < 0:
        return []
    # ...原有代码... 

def get_datan(n, m):
    if m < n:
        raise ValueError("m 必须大于等于 n")
    data_n = set_zero_list(n)
    data_m = get_datam(m)
    random.shuffle(data_m)
    index = random.randint(0, m-n) if m > n else 0
    for i in range(n):
        data_n[i] = data_m[index + i]
    return data_n 

def get_db_connection():
    db_path = os.path.join(get_app_data_dir(), 'algo_history.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def create_table_if_not_exists():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS algo_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input_data TEXT NOT NULL,
        output_data TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

def save_algo_data(input_data, output_data):
    try:
        create_table_if_not_exists()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO algo_history (input_data, output_data, created_at) VALUES (?, ?, ?)',
            (input_data, output_data, time.strftime('%Y-%m-%d %H:%M:%S'))
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"保存数据时出错: {e}")
        return False

def get_algo_history():
    try:
        create_table_if_not_exists()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, input_data, output_data, created_at FROM algo_history ORDER BY id DESC')
        records = cursor.fetchall()
        conn.close()
        return [(row['id'], row['input_data'], row['output_data'], row['created_at']) for row in records]
    except Exception as e:
        print(f"获取历史记录时出错: {e}")
        return []

def delete_record(record_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM algo_history WHERE id = ?', (record_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except Exception as e:
        print(f"删除记录时出错: {e}")
        return False

def get_record_by_id(record_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, input_data, output_data, created_at FROM algo_history WHERE id = ?', (record_id,))
        record = cursor.fetchone()
        conn.close()
        if record:
            return (record['id'], record['input_data'], record['output_data'], record['created_at'])
        return None
    except Exception as e:
        print(f"获取记录详情时出错: {e}")
        return None

# 以下函数用于算法历史记录，避免与上面函数冲突
def set_zero_list(n):
    return [0] * n

def get_datam(m):
    return list(range(1, m + 1)) 