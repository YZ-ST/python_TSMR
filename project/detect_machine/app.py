from flask import Flask, render_template, request

app = Flask(__name__)

# 定义一个路由来处理表单提交
@app.route('/submit', methods=['POST'])
def submit_form():
    # 获取表单中提交的数据
    name = request.form['name']
    phone = request.form['phone']
    gender = request.form['gender']
    blood_type = request.form['bloodType']
    line_id = request.form['lineId']

    # 在这里可以对表单数据进行处理，例如将其存储到数据库中

    # 返回一个响应，可以是一个感谢页面或重定向到其他页面
    return f"姓名: {name}, 电话: {phone}, 性别: {gender}, 血型: {blood_type}, Line ID: {line_id}"

# 定义一个路由来显示表单页面
@app.route('/')
def show_form():
    return render_template('form.html')

if __name__ == '__main__':
    app.run( debug=True, port=80)

#host="0.0.0.0",
