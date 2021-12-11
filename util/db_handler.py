import os
import pymysql
import configparser
from util import logs_util

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = BASE_DIR + '/' + 'config/APITest.ini'
config = configparser.ConfigParser()
config.read(file_path, encoding='utf-8')
host = config.get('mysql', 'host')
port = config.get('mysql', 'port')
user = config.get('mysql', 'user')
password = config.get('mysql', 'password')
database = config.get('mysql', 'database')


# noinspection PyBroadException
class DbHandler(object):
    """
    对于数据库内的用例加载、配置加载、用例执行结果更新等操作
    """

    def __init__(self):
        self.connect = pymysql.connect(user=user, password=password, host=host, port=int(port), database=database)
        self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        self.cursor.close()
        self.connect.close()

    def query_by_sql(self, sql, state="all"):
        """
        依据SQL查询测试用例或者配置信息
        :param sql: 执行的sql语句
        :param state: 查询单挑信息或者全部信息
        :return:
        """
        self.cursor.execute(sql)
        if state == "all":
            data = self.cursor.fetchall()
        else:
            data = self.cursor.fetchone()
        return data

    def execute_sql(self, sql):
        """
        执行sql语句进行增、上、改操作
        :param sql: 执行的sql语句
        :return: 受影响的数据行
        """
        try:
            rows = self.cursor.execute(sql)
            self.connect.commit()
            return rows
        except Exception as e:
            logs_util.logs_util('', e, 'error')
            self.connect.rollback()


if __name__ == '__main__':
    db = DbHandler()
    sql = "select * from `case`"
    result = db.query_by_sql(sql)
    # sql = "insert into `case` (app) values('xd')"
    # result = db.execute_sql(sql)
    print(result)
