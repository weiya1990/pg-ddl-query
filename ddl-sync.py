import os
import psycopg2
import configparser
import logging
import threading
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s') 
# config_dir = os.getenv('CONFIG_DIR')

def get_sql_list():
    file = os.path.join(os.path.dirname(__file__),'etc/ddl.sql')
    with open(file, encoding='utf-8') as f:
        sql_list = f.read().split(";") #获取执行sql列表
        return sql_list
#通过连接从库批量执行更新DDL sql
def query_sql(tend, database, user, password, host, port, cmd):
    # 数据库连接参数
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    if conn:
        logging.info('客户环境：%s, 数据库: %s连接成功, 执行的sql: %s' %(tend, database,cmd))
    cur = conn.cursor()
    cur.execute(cmd)
   # rows = cur.fetchall()        # all rows in table
   # print(rows)
    conn.commit()
    cur.close()
    conn.close()
config = configparser.ConfigParser()
file = os.path.join(os.path.dirname(__file__),'etc/db.conf')
config.read(file, encoding="utf-8")

group_list = config.sections()
for i in group_list:
    # logging.info("正在连接从库%s执行命令" %(i))
    # logging.info("-------------------------------------------------------")
    host = config.get(i, 'host')
    port = config.get(i, 'port')
    database = config.get(i, 'database')
    user = config.get(i, 'user')
    password = config.get(i, 'password')
    sql_list = get_sql_list()
    for cmd in sql_list:
        try:
            t = threading.Thread(target=query_sql, args=(i, database, user, password, host, port, cmd))
            t.start()  
        except psycopg2.Error as errorMsg:
            logging.error(errorMsg)
            #print(errorMsg)    
