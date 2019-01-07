from flask import Flask, jsonify, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
import get_DB as db
import connect_socket as cs
import time
import hashlib

app = Flask(__name__)
#-------------------------------------------------------------        login
#  會使用到session，故為必設。
app.secret_key = 'Your Key'
login_manager = LoginManager(app)
#  login\_manager.init\_app(app)也可以

#目前唯一的帳號 (多組帳號意義不大)
UI_users = {'123': {'password': 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'}}

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(account):
    if account not in UI_users:
        return
    user = User()
    user.id = account
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_active:
            return redirect( url_for( 'main'))
        else:
            return render_template('login.html')

    #-------------------- POST
    account = request.form['account']
    if account not in UI_users:                                     #wrong account
        flash('wrong')          #傳資料到login.html 裡面
        flash('account!')
        return redirect( url_for('login'))

    else:
        abc = hashlib.new('sha256', request.form['password'].encode("utf-8")) #使用者輸入hash過後
        if abc.hexdigest() == UI_users[account]['password']:
            #  實作User類別
            user = User()
            #  設置id就是email
            user.id = account
            #  這邊，透過login_user來記錄user_id，如下了解程式碼的login_user說明。
            login_user(user)
            #  登入成功，轉址
            return redirect(url_for('main'))
                                                                    #wrong password
    flash('wrong')
    flash('password!')
    return redirect( url_for('login'))

@app.route('/protected')
#@login_required
def protected():
    # 在login_user(user)之後，我們就可以透過current_user.id來取得用戶的相關資訊了
    #  current_user確實的取得了登錄狀態
    if not current_user.is_active:
        return 'you are not logged in'
    return 'Logged in as: ' + current_user.id + 'Login is_active:True'

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    #return 'Logged out'
    return redirect( url_for( 'main'))
#-------------------------------------------------------------      end login
#--------------------------------------------------------------------------------------- HTMLs

def try_connect_db():
    global status
    db.mycursor = db.connect_to_mysql()
    if db.mycursor:
        status = 'work'

@app.route('/', methods=['GET'])
def main():
    if not current_user.is_active:              #這兩行用來檢測使用者登入狀況
        return redirect( url_for( 'login'))
    if status == 'fail':
        print('database connect fail')
        try_connect_db()
    try_connect_db()
    return render_template('UI_main_page.html')


status= 'fail'      #"work" or "fail"
@app.route('/main/', methods=['GET'])
def main_page():
    if not current_user.is_active:
        return redirect( url_for( 'login'))
    try_connect_db()
    if status == 'work':
        ap= str(len(db.get_servdev() )) +'/'+ str(len(db.get_ap_device() ))
        user= str(len(db.get_online() )) +'/'+ str(len(db.get_users() ))
        graph_data= db.get_avetime()
    else:
        ap, user, graph_data =['<br>Not Connected<br>']*3
    return render_template('main_page.html', graph_data= graph_data , status= status, ap= ap, user= user)


@app.route('/AP/', methods=['GET'])
def ap_page():
    if not current_user.is_active:
        return redirect( url_for( 'login'))
    try_connect_db()
    data={}
    data['ap_names'] = db.get_ap_device()
    data['ap_status']= db.get_ap_status()
    data['nodes'] = db.get_node()
    #data['online'] = [str(e) for e in range(5)]
    return render_template('AP_page.html', **data)      # 一次送三個table過去


@app.route('/User/', methods=['GET'])
def user_page():
    if not current_user.is_active:
        return redirect( url_for( 'login'))
    try_connect_db()
    if status != 'work':
        return "<h1>Not Connected</h1>"
    return render_template('User_page.html', users= db.get_users() )


@app.route('/about/', methods=['GET', 'POST'])
def about_page():
    if not current_user.is_active:
        return redirect( url_for( 'login'))
    return '''
	<div style="width: 100%;">
    none
    <div>
    '''

#------------------------------------------------------     data
# --------------------------- 以下四個函式模擬 db 回傳資料
AP_num= 10
user_num=10
def get_node(ind = 0):
    nodes={}
    if ind == 0:
        for i in range(1, AP_num+1):
            nodes[str(i) ]=['nod'+str(j) for j in range(i+1, i+11)]
        return nodes
    else:
        return { ind: ['name+', str(ind), '最後登陸時間+', 'wan_ip+', 'sys_uptime+', 'sys_memfree+', 'sys_load+', 'wifidog_uptime+', 'create_time+', 'update_time+']}

def get_ap_status(ind = 0):
    apdb={}
    if ind == 0:
        for i in range(1, AP_num+1):
            apdb[str(i) ]=['sta'+str(j) for j in range(i+1, i+5)]
        return apdb
    else:
        i= 1
        return {ind: ['cpu_usage+', 'received+', 'transmit+', 'timestamp+']}

def get_ap_device(ind = 0):
    apna={}
    if ind == 0:
        for i in range(1, AP_num+1):
            apna[str(i) ]=['id2121', 'none', '123+']
        return apna
    else:
        i= 1
        ret_list = ['id2121', 'psk2', '123+']
        return {ind: ret_list}

def get_users(ind = 0):
    userdb={}
    if ind == 0:
        for i in range(1, user_num+1):
            userdb[str(i) ]=[j for j in range(i+1, i+5)]
        return userdb
    else:
        i = 1
        return [j for j in range(i+1, i+5)]

def get_graph():
    return [i*10 for i in range(1, 25)]
# -----------------------------------------------------

@app.route('/_imfor/', methods=['POST'])
def imfor():
    if not current_user.is_active:
        return jsonify("")
    try_connect_db()
    content = request.get_json()
    id = int( content['ap_id'] )
    
    data={}
    data['name']= db.get_ap_device(id)[id]     #回傳的竟然是 dict ==+
    data['status']= db.get_ap_status(id)[id]
    data['node']= db.get_node(id)[id]
    data['id']= id
    return jsonify(data)
#                                           AP_page 用到的
@app.route('/_change_ssid/', methods=['POST'])
def change_ssid():
    if not current_user.is_active:
        return jsonify("")
    try_connect_db()
    content = request.get_json()
    print(content)
    #cs.act_21(content['ap_id'] , content['new_ssid'] )
    return jsonify("")

@app.route('/_change_encryption/', methods=['POST'])
def change_encry():
    if not current_user.is_active:
        return jsonify("")
    try_connect_db()
    content = request.get_json()
    print(content)
    #cs.act_23(content['ap_id'], content['encry'] )
    return jsonify("")

@app.route('/_change_key/', methods=['POST'])
def change_key():
    if not current_user.is_active:
        return jsonify("")
    try_connect_db()
    content = request.get_json()
    print(content)
    #cs.act_24(content['ap_id'], content['new_key'] )
    return jsonify("")

@app.route('/_get_log/<ap_id>', methods=['GET'])
def get_log(ap_id):
    if not current_user.is_active:
        return jsonify("")
    try_connect_db()
    #content= request.get_json()
    #print(content)
    print("get ap log:", ap_id)

    #cs.act_10(ap_id)
    time.sleep(3)   #sleep 3s
    #return 'ap_log: ' + str(ap_id)
    return db.get_ap_log(ap_id )

if __name__ == "__main__":
    try_connect_db()

    #app.run(threaded=True, debug=True, port=5000)
    app.run(host= '10.140.0.4',debug=True, threaded=True, port=3389)