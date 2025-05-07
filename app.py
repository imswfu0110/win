from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
from algo import get_anstr, set_combination
from db_connect import save_data, get_history, delete_record as db_delete_record, get_record_by_id
from db_connect import get_datam, get_datan, save_algo_data, get_algo_history

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于flash消息

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            # 获取表单数据
            n = int(request.form['n'])
            j = int(request.form['j'])
            k = int(request.form['k'])
            s = int(request.form['s'])
            m = int(request.form['m'])
            at_least = int(request.form['at_least'])
            # 生成数据
            data_n = get_datan(n, m)
            data_k = set_combination(n, k)
            # 调用算法
            num, duration, anstr = get_anstr(data_k, data_n, n, j, k, s, at_least)
            result = {
                'num': num, 
                'duration': duration, 
                'anstr': anstr, 
                'data_n': data_n,
                'n': n
            }
            # 将数据存储在会话中，供后续使用
            session['last_result'] = {
                'n': n, 'j': j, 'k': k, 's': s, 'm': m, 'at_least': at_least,
                'data_n': data_n, 'anstr': anstr, 'num': num, 'duration': duration
            }
        except Exception as e:
            flash(f'处理请求时出错: {str(e)}', 'error')
    return render_template('index.html', result=result)

# 历史记录页面
@app.route('/history')
def history():
    try:
        print("\n" + "="*50)
        print("开始获取历史记录")
        records = get_algo_history()
        print(f"获取到 {len(records)} 条历史记录")
        if records:
            print("第一条记录:")
            print(f"ID: {records[0][0]}")
            print(f"输入: {records[0][1]}")
            print(f"输出: {records[0][2]}")
            print(f"时间: {records[0][3]}")
        else:
            print("没有找到任何记录！")
        print("="*50 + "\n")
        return render_template('history.html', records=records)
    except Exception as e:
        print("\n" + "="*50)
        print(f"获取历史记录时出错: {str(e)}")
        print("="*50 + "\n")
        flash('获取历史记录时出错', 'error')
        return render_template('history.html', records=[])

# 保存数据到数据库
@app.route('/store')
def store():
    if 'last_result' in session:
        try:
            result = session['last_result']
            input_data = str({
                'n': result['n'], 
                'j': result['j'], 
                'k': result['k'], 
                's': result['s'], 
                'm': result['m'], 
                'at_least': result['at_least'], 
                'data_n': result['data_n']
            })
            save_algo_data(input_data, result['anstr'])
            flash('数据已成功保存到数据库', 'success')
        except Exception as e:
            flash(f'保存数据时出错: {str(e)}', 'error')
    else:
        flash('没有可保存的数据', 'warning')
    return redirect(url_for('index'))

# 删除指定记录
@app.route('/delete_record/<int:record_id>')
def delete_record(record_id):
    try:
        success = db_delete_record(record_id)
        if success:
            flash('记录已成功删除', 'success')
        else:
            flash('删除记录失败', 'error')
    except Exception as e:
        flash(f'删除记录时出错: {str(e)}', 'error')
    return redirect(url_for('history'))

# 显示单条记录详情
@app.route('/display_record/<int:record_id>')
def display_record(record_id):
    try:
        record = get_record_by_id(record_id)
        if record:
            return render_template('record_detail.html', record=record)
        else:
            flash('未找到记录', 'error')
            return redirect(url_for('history'))
    except Exception as e:
        flash(f'获取记录详情时出错: {str(e)}', 'error')
        return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True, port=5001) 