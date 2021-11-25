import os
import psycopg2
import configparser
import logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s') 
config_dir = os.getenv('CONFIG_DIR')
def get_sql_list():
    with open(config_dir+'/all.txt', encoding='utf-8') as f:
        sql_list = f.read().split(";") #获取执行sql列表
        return sql_list
#通过连接从库批量执行更新DDL sql
def query_sql(database, user, password, host, port, cmd):
    # 数据库连接参数
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cur = conn.cursor()
    cur.execute(cmd)
   # rows = cur.fetchall()        # all rows in table
   # print(rows)
    conn.commit()
    cur.close()
    conn.close()

config = configparser.ConfigParser()
config.read(config_dir+'/db.conf')
group_list = config.sections()
for i in group_list:
    logging.info("正在连接从库%s执行命令" %(i))
    logging.info("-------------------------------------------------------")
    host = config.get(i, 'host')
    port = config.get(i, 'port')
    database = config.get(i, 'database')
    user = config.get(i, 'user')
    password = config.get(i, 'password')

    sql_list = get_sql_list()
    for cmd in sql_list:
        try:
            query_sql(database, user, password, host, port, cmd)
        except psycopg2.Error as errorMsg:
            logging.info(errorMsg)
            #print(errorMsg)        

        
        









