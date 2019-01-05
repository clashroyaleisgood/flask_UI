import pymysql
import datetime

def connect_to_mysql(host="localhost",user="root",passwd="authpuppyadm",database="authpuppy",charset="utf8"):
                    #可更改 host,user,passwd,database 
    try:    #預設先自動輸入，否則手動輸入
        mydb = pymysql.connect(
            host = host,
            user = user,
                #這兩行事預設值，好像可以改但是DB應該沒改，所以不用動
            passwd = passwd,
                #mysql密碼,沒有的話直接 # 起來就可以了
            database = database,
                #DB名稱,測試用資料庫
            charset = charset
                #字元編碼 不太確定需不需要改 應該預設都是utf8吧
            )
        return mydb.cursor()
    except:
        return False

#mycursor = connect_to_mysql()


table_name = ['ap_user','nodes','ap_device','ap_status','connections']
    #table 的參數陣列

def change_table(i = 1,vectors = '*',id = 0):
        # i 控制想要拿哪一個table的值 預設為 1
        # vector 想要尋找的欄位        預設為*代表全部的欄位
    sql = "SELECT "+vectors+" "+' FROM '+table_name[i]
        #print(sql) 檢查用
    if id:
        sql = sql + ' where id = '+str(id)
    mycursor.execute(sql)
    
#拿取索引值(第i個table的index)
def get_index(i = 1):
    change_table(i,'id')
    index=[x for x in mycursor]
        #型態為int
    return index

#拿取使用者資料
def get_users(index = 0):
        #拿取該索引值所對應的資訊 ,若不輸入預設為全拿
    userdb={}
    change_table(0,id = index)
    for x in mycursor:
        userdb[x[0]]= [x[1],x[2],x[3],x[4].strftime("%Y-%m-%d %H:%M:%S")]
            #x[0]是user_id, 1 是username , 2 是password ,3 是email,4是註冊時間,
            #      string  ,      string   ,    string      ,       str 
    return userdb

#拿取連線點資訊
def get_node(index = 0):
        #拿取該索引值所對應的資訊 ,若不輸入預設為全拿
    nodes={}
    change_table(1,id = index)
    for x in mycursor:
        nodes[x[0]]=[x[1],x[2],x[3].strftime("%Y-%m-%d %H:%M:%S"),x[4],x[5],x[6],str(x[7]),x[8],x[9].strftime("%Y-%m-%d %H:%M:%S"),x[10].strftime("%Y-%m-%d %H:%M:%S")]
            #0: id, 1: name, 2: gw_id, 3:last 登錄 time, 4:wan_ip, 5:sys_uptime
               #int    str      str    str               str         int 

            #6: sys_memfree, 7: sys_load, 8: wifidog_uptime, 9: created_time, 10: update_time
               #int             str        int               str              str          
    return nodes

#拿取AP所對應的wifi名稱及密碼
def get_ap_device(index = 0): 
    apna={}
    change_table(2,id = index)
    for x in mycursor:
        apna[x[0]]=[x[1],x[2].lower(),x[3]]
        #0: ap_id, 1: SSID, 2: encrytion ,3:key
            #  int    str      str          str
    return apna

def get_ap_status(index = 0):
        #拿取該索引值所對應的資訊 ,若不輸入預設為全拿
    apdb={}
    change_table(3, id = index)
    for x in mycursor:
        apdb[x[0]] = [x[1],str(x[2]),str(x[3]),x[4].strftime("%Y-%m-%d %H:%M:%S")]
            #x[0]是device_id , 1 是 cup_usage , 2 是received ,3 是 transmit ,4 是 timestamp
            #       integer  ,      int       , str,          str,           str
    return apdb

def node_connection(index = 1):
    nodes_id = {}
    change_table(4,'node_id')
    for x in mycursor:
        nodes_id[x[0]] =[]
    change_table(4)
    for x in mycursor:
        nodes_id[x[1]].append([str(x[8]),str(x[9]),x[10].strftime("%Y-%m-%d %H:%M:%S"),x[11].strftime("%Y-%m-%d %H:%M:%S"),x[4],x[5]])
            # 1:node_id, 8:incoming(), 9:outgoing, 10:create_at, 11:update_at, 4:mac, 5:ip
            # int      , str       ,   str     ,   str    ,      str    , string,string
    return nodes_id

def getnow():
    return datetime.datetime.now()
def getdt(link,now):
    return (now - link).total_seconds()
def get_online(time = 3600):
                #連線時間，可以設定連線多久內算上限中，預設1小時
    dict = {}
    change_table(4,vectors = 'ip,created_at')
    for e in mycursor:
        if getdt(e[1],getnow()) < time:
            dict[e[0]] = [e[1]]
    return dict
    #拿出來的為連線者ip與連線起始時間 || ip | created_at ||
    #用len(get_online())即為連線使用者數量

def get_servdev(time = 3600):
    dict = {}
    change_table(3,vectors = 'id,timestamp')
    for e in mycursor:
        if getdt(e[1],getnow()) < time:
            dict[e[0]] = [e[1]]
    return dict
    #拿出來的為AP_id與最新連線時間 || id | timestamp ||
    #用len(get_servdev())即為連線AP數量

def get_avetime(times = 24 , trace = 24 , end = 0):
                #time 要分成幾筆資料 , trace 追蹤到前幾個小時 ， end 直到前第幾個小時
    trace = trace *3600
    end = end *3600
    if (times <= 0):
        print("error times!!")
        return -1
    time = (trace - end) / times
    data = []
    for i in range(times):
        a = trace - (time *i)
        data.append(len(get_online(a)))
    cor = []
    for i in range(times-1):
        cor.append(data[i] - data[i+1])
    cor.append(data[times-1])
    return cor
def print_data(test_dict,type_id = 0):
        #r檢查用(拿出來的格式),一般dict用 id = 0, list_dict用 id = 1;
    if type_id:
        for e in test_dict:
            print(str(e),end = '')
            for i in test_dict[e]:
                print(': ',' '.join(str(x)for x in i))
            print()
        return 1
    else:
        print('\n'.join(str(e) + ': ' + ' '.join(str(n) for n in test_dict[e] ) for e in test_dict)  )
        return 0

def get_ap_log(gwid):   #仲軒來的函式
    #db=0
    try:
        #db = pymysql.connect("localhost",account,password,database)
        #mycursor = db.cursor()
        selectlog="SELECT AP_log FROM ap_log WHERE id = (%s)"
        mycursor.execute(selectlog,gwid)
        row = mycursor.fetchone()
        deletelog = "DELETE from ap_log WHERE id = (%s)"
        mycursor.execute(deletelog,gwid)
        #db.commit()
        #db.close()
        return row[0]
    except:
        print('get ap log had error')
    pass

if __name__ == "__main__":
    mycursor = connect_to_mysql()
    #test_dict= node_connection()
    #print_data(test_dict,1)
    #print_data(get_online())
    print(get_avetime(24,96,48))
    print(get_servdev(1000000))
