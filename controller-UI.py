from flask import Flask, jsonify, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
import time

app = Flask(__name__)
#-------------------------------------------------------------        login
#  會使用到session，故為必設。
app.secret_key = 'Your Key'
login_manager = LoginManager(app)
#  login\_manager.init\_app(app)也可以

UI_users = {'123': {'password': '123'}}
  
  
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
    if account not in UI_users:
        flash('wrong')
        flash('account!')
        return redirect( url_for('login'))

    elif request.form['password'] == UI_users[account]['password']:
        #  實作User類別
        user = User()
        #  設置id就是email
        user.id = account
        #  這邊，透過login_user來記錄user_id，如下了解程式碼的login_user說明。
        login_user(user)
        #  登入成功，轉址
        return redirect(url_for('main'))

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

@app.route('/logout')
def logout():
    logout_user()
    #return 'Logged out'
    return redirect( url_for( 'main'))
#-------------------------------------------------------------      end login
#--------------------------------------------------------------------------------------- HTMLs

@app.route('/', methods=['GET'])
def main():
    if not current_user.is_active:
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
    data['success']= imfor_ap_succ()
    data['fail']= imfor_ap_fail()
    return render_template('AP_page.html', **data)


@app.route('/User/', methods=['GET'])
def user_page():
    if not current_user.is_active:
        return redirect( url_for( 'login'))
    return render_template('User_page.html', users= users)


@app.route('/about/', methods=['GET', 'POST'])
def about_page():
    if not current_user.is_active:
        return redirect( url_for( 'login'))
    return render_template('about_to_test_submitting.html')

#------------------------------------------------------     data

def imfor_ap_succ():
    imfor= [[10*i+j for j in range(5)]for i in range(1, 20)]
    return imfor

def imfor_ap_fail():
    imfor= [[10*i+j for j in range(5)]for i in range(6, 1, -1)]
    return imfor

@app.route('/_test', methods=["POST"])
def _test():
    content = request.get_json()
    to_json= {}
    to_json['get data']= [content['test1'], content['test2']]
    return jsonify(to_json)

@app.route('/test_imfor_page/', methods=['GET', 'POST'])
def imfor_page():
    #content = request.get_data()
    contentj = request.get_json() #json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
    #print('#get raw data:\t', content)
    #print('#get json:\t', contentj)
    
    return render_template('small.html', content = contentj)

#init
users= {}
for i in range(1, 6):
    users['name' + str(i)]= i*11

@app.route('/_add_user', methods=['POST'])
def _add_user():
    content = request.get_json()
    global users
    users[content['name']]= content['value']
    #print('get')
    return jsonify({'success': True, 'user': content['name'] })


if __name__ == "__main__":
    app.run(threaded=True, debug=True, port=5000)
    #app.run(host= '10.140.0.3',debug=True, threaded=True, port=27015)
    #app.run(host= '10.140.0.4',debug=True, threaded=True, port=27015)