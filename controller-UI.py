from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

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

#---------------------------------------------------------------------------------------

@app.route('/', methods=['GET'])
def main():
    return render_template('UI_main_page.html')


@app.route('/main/', methods=['GET'])
def main_page():
    return render_template('main_page.html')


@app.route('/AP/', methods=['GET'])
def ap_page():
    data={}
    data['success']= imfor_ap_succ()
    data['fail']= imfor_ap_fail()
    return render_template('AP_page.html', **data)


@app.route('/User/', methods=['GET'])
def user_page():
    return render_template('User_page.html', users= users)


@app.route('/about/', methods=['GET', 'POST'])
def about_page():
    return render_template('about_to_test_submitting.html')


if __name__ == "__main__":
    app.run(threaded=True, debug=True, port=5000)
    #app.run(host= '10.140.0.3',debug=True, threaded=True, port=27015)