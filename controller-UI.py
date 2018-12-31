from flask import Flask, jsonify, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
import time

app = Flask(__name__)
#-------------------------------------------------------------        login
#  會使用到session，故為必設。
app.secret_key = 'Your Key'
login_manager = LoginManager(app)
#  login\_manager.init\_app(app)也可以

UI_users = {'123': {'password': '123'}}         #目前唯一的帳號 (多組帳號意義不大)

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

    elif request.form['password'] == UI_users[account]['password']: #correct
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

@app.route('/', methods=['GET'])
def main():
    if not current_user.is_active:              #這兩行用來檢測使用者登入狀況
        return redirect( url_for( 'login'))
    return render_template('UI_main_page.html')


@app.route('/main/', methods=['GET'])
def main_page():
    if not current_user.is_active:
        return redirect( url_for( 'login'))
    return render_template('main_page.html')


@app.route('/AP/', methods=['GET'])
def ap_page():
    if not current_user.is_active:
        return redirect( url_for( 'login'))
    data={}
    data['ap_names'] = get_ap_name()
    data['ap_status']= get_ap_status()
    data['nodes'] = get_node()
    return render_template('AP_page.html', **data)      # 一次送三個table過去
'''
@app.route('/AP_detail/<int:AP_id>')
def ap_detail(AP_id):
    if isinstance(AP_id, int):
        return 'find id in table'
    return """ <script>alert("Error:""" + AP_id + """ is not a number");</script> """

@app.route('/APdetail/', methods=['GET'])       #detail from pa en
def ap_detailed():
    return render_template('AP_detail.html')
'''
@app.route('/User/', methods=['GET'])
def user_page():
    if not current_user.is_active:
        return redirect( url_for( 'login'))
    return render_template('User_page.html', users= get_users() )


@app.route('/about/', methods=['GET', 'POST'])
def about_page():
    if not current_user.is_active:
        return redirect( url_for( 'login'))
    return '''
	<div style="margin-left:15%; padding:1px 16px; height: 20%; background-color: #ffffff; padding-top: 6%;" id="main">
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
        i= 1
        return ['nod'+str(j) for j in range(i+1, i+11)]

def get_ap_status(ind = 0):
    apdb={}
    if ind == 0:
        for i in range(1, AP_num+1):
            apdb[str(i) ]=['sta'+str(j) for j in range(i+1, i+5)]
        return apdb
    else:
        i= 1
        return ['sta'+str(j) for j in range(i+1, i+5)]

def get_ap_name(ind = 0):
    apna={}
    if ind == 0:
        for i in range(1, AP_num+1):
            apna[str(i) ]=['name'+str(j) for j in range(i+1, i+3)]
            apna[str(i) ][1]=[21, 22, 23]
        return apna
    else:
        i= 1
        ret_list = ['name'+str(j) for j in range(i+1, i+3)]
        ret_list[1]=[21,22,23]
        return ret_list

def get_users(ind = 0):
    userdb={}
    if ind == 0:
        for i in range(1, user_num+1):
            userdb[str(i) ]=[j for j in range(i+1, i+5)]
        return userdb
    else:
        i = 1
        return [j for j in range(i+1, i+5)]
# -----------------------------------------------------

@app.route('/_imfor', methods=['POST'])
def imfor():
    content = request.get_json()
    id = int( content['ap_id'] )
    #data=[i for i in range(start, start +17)]
    #data[2]=[21, 22, 23, 24]
    name= get_ap_name(id)
    status= get_ap_status(id)
    node= get_node(id)
    data=[]
    data+= [id]         #0
    data+= name[:]      #1 2
    data+= [id]         #3 device id
    data+= status[:]    #4 5 6 7
    data+= node[1:]     #8 ~ 16
    return jsonify({'data':data})

@app.route('/_change_ssid', methods=['POST'])
def change():
    content = request.get_json()
    print(content)
    
    return jsonify("")

if __name__ == "__main__":
    app.run(threaded=True, debug=True, port=5000)
    #app.run(host= '10.140.0.3',debug=True, threaded=True, port=27015)
    #app.run(host= '10.140.0.4',debug=True, threaded=True, port=27015)