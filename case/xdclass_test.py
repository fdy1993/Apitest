import json
import os
import sys
import datetime
import time

from util.db_handler import DbHandler
from util import logs_util
from util import requests_util
from util.send_mail import SendMail

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
db = DbHandler()


class ApiTestCase(object):
    def load_all_case_by_app(self, app):
        """
        根据app加载全部的测试用例
        :param app: app
        :return:
        """
        sql = 'select * from `case` where app="{}"'.format(app)
        result = db.query_by_sql(sql)
        return result

    def load_one_case_by_id(self, case_id):
        """
        根据app加载全部的测试用例
        :param case_id: app
        :return:
        """
        sql = 'select * from `case` where id="{}"'.format(case_id)
        result = db.query_by_sql(sql, state="one")
        return result

    def load_config(self, app, dict_key):
        """
        根据app、dict_key加载配置信息
        :param app: app
        :param dict_key: dict_key
        :return: dict_value
        """
        sql = 'select * from `config` where app="{}" and dict_key="{}"'.format(app, dict_key)
        result = db.query_by_sql(sql)
        return result

    def update_result(self, response, is_pass, msg, case_id):
        """
        更新测试测试结果
        :param response: response
        :param is_pass: is_pass
        :param msg: msg
        :param case_id: case_id
        :return:
        """
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if is_pass:
            sql = "update `case` set response=\"{0}\", pass=\"{1}\", msg=\"{2}\",update_time=\"{3}\" where id={4}".format(
                "", is_pass, msg, current_time, case_id)
        else:
            sql = "update `case` set response=\"{0}\", pass=\"{1}\", msg=\"{2}\",update_time=\"{3}\" where id={4}".format(
                str(response), is_pass, msg, current_time, case_id)
        rows = db.execute_sql(sql)
        return rows

    def run_all_case(self, app):
        """
        执行全部测试用例
        :param app: app
        :return:
        """
        api_host = self.load_config(app, 'host')
        results = self.load_all_case_by_app(app)
        for case in results:
            if case['run'] == 'yes':
                try:
                    response = self.run_case(case, api_host)  # 执⾏用例
                    assert_msg = self.assert_response(case, response)  # 断言判断
                    rows = self.update_result(response, assert_msg['is_pass'], assert_msg['msg'],
                                              case['id'])  # 更新结果存储数据库
                    message = "更新测试用例执行结果,受影响行数row={0},测试用例id={1},通过情况pass={2}.".format(str(rows), case['id'],
                                                                                        assert_msg['is_pass'])
                    # print("更新结果 rows={0}".format(str(rows)))
                    print(message)
                    # logs_util.logs_util(task_id='', message=str(rows))
                    logs_util.logs_util(task_id='', message=message)
                except Exception as e:
                    msg = "测试用例id={0},标题:{1},执行报错信息:{2}".format(case['id'], case['title'], e)
                    print(msg)
                    logs_util.logs_util('', msg, 'error')
        self.send_test_report(app)

    def run_case(self, case, api_host):
        """
        执行单个测试用例
        :param case: case
        :param api_host: host
        :return:
        """
        headers = json.loads(case['headers'])
        body = json.loads(case['request_body'])
        method = case['method']
        req_url = api_host[0]['dict_value'] + case['url']
        # 判断是否存在前置条件
        if case['pre_case_id'] == 1:
            pre_case_id = case['pre_case_id']
            pre_case = self.load_one_case_by_id(pre_case_id)
            # 递归调用
            pre_response = self.run_case(pre_case, api_host)
            #    前置条件断言
            pre_assert_msg = self.assert_response(pre_case, pre_response)
            if not pre_assert_msg['is_pass']:
                # 前置条件不通过直接返回
                pre_response['msg'] = '前置条件不通过,' + pre_response['msg']
                return pre_response
            # 判断需要case的前置条件是那个字段
            pre_fields = json.loads(case['pre_fields'])
            for pre_field in pre_fields:
                print(pre_field)
                if pre_field['scope'] == 'header':
                    # 遍历headers ,替换对应的字段值，即寻找同名的字段
                    for header in headers:
                        field_name = pre_field['field']
                        if header == field_name:
                            field_value = pre_response['data'][field_name]
                            headers[field_name] = field_value
                elif pre_field['scope'] == 'body':
                    print("替换body")
                    for replace_body in body:
                        field_name = pre_field['field']
                        if replace_body == field_name:
                            field_value = pre_response['data']["userId"]
                            body[field_name] = field_value
        print(headers)
        print(body)
        if headers is not None:
            content_type = headers["Content-Type"]
        else:
            content_type = None
        response = requests_util.requests_util(url=req_url, method=method, headers=headers, param=body,
                                               content_type=content_type)
        return response

    def assert_response(self, case, response):
        """
        断⾔言响应内容，更更新⽤用例例执⾏行行情况
        {"is_pass":true, "msg":"code is wrong"}
        :param case:
        :param response:
        :return:
        """
        assert_type = case['assert_type']
        expect_result = case['expect_result']
        is_pass = False
        if assert_type == 'code':
            response_code = response['code']
            if int(expect_result) == response_code:
                is_pass = True
                print("测试⽤用例例通过")
            else:
                print("测试⽤用例例不不通过")
                is_pass = False
        elif assert_type == 'data_json_array':
            data_array = response['data']
            if data_array is not None and isinstance(data_array, list) and len(data_array) > int(expect_result):
                is_pass = True
                print("测试⽤用例例通过")
            else:
                is_pass = False
                print("测试⽤用例例不不通过")
        elif assert_type == 'data_json':
            data = response['data']
            if data is not None and isinstance(data, dict) and len(data) > int(expect_result):
                is_pass = True
                print("测试⽤用例例通过")
            else:
                is_pass = False
                print("测试⽤用例例不不通过")
        msg = "模块:{0}, 标题:{1},断⾔言类型:{2},响应:{3}".format(case['module'], case['title'], assert_type, response['message'])
        assert_msg = {"is_pass": is_pass, "msg": msg}
        return assert_msg

    def query_test_results(self, app):
        """
        加载所有运行过的测试用例
        :param app: App名称
        :return:
        """
        sql = 'select * from `case` where app="{}" and run="yes" order by pass'.format(app)
        result = db.query_by_sql(sql)
        return result

    def query_count(self, app, is_pass="all"):
        """
        加载所有运行过的测试用例执行情况数据量
        :param app: App名称
        :param is_pass:是否通过
        :return:
        """
        if is_pass == "P":
            sql = 'select count(1) as count from `case` where app="{}" and run="yes" and pass="True"'.format(app)
        elif is_pass == "F":
            sql = 'select count(1) as count from `case` where app="{}" and run="yes" and pass="False"'.format(app)
        else:
            sql = 'select count(1) as count from `case` where app="{}" and run="yes"'.format(app)
        result = db.query_by_sql(sql, state=0)
        return result

    def send_test_report(self, app):
        """
        发送测试报告
        :param app: app
        :return:
        """
        results = self.query_test_results(app)
        count = self.query_count(app)["count"]
        count_pass = self.query_count(app, is_pass="P")["count"]
        count_failure = self.query_count(app, is_pass="F")["count"]
        success_rate = count_pass / count
        title = f'{app}接口自动化测试报告'
        content = """
        <html><body>
        <h4>{0} 接口测试报告：</h4>
        <h4>共计执行用例数: {1}, 测试用例通过数: {2}, 成功率: {3}</h4>
        <table border="1">
        <tr>
        <th>编号</th>
        <th>模块</th>
        <th>标题</th>
        <th>是否通过</th>
        <th>响应</th>
        <th>备注</th>
        </tr>
        {4}
        </table></body></html> 
         """
        template = ""
        for case in results:
            template += "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>".format(
                case['id'], case['module'], case['title'], case['pass'], case['response'], case['msg'])
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content = content.format(current_time, count, count_pass, success_rate, template)
        mail_host = self.load_config(app, "mail_host")[0]['dict_value']
        mail_sender = self.load_config(app, "mail_sender")[0]['dict_value']
        mail_auth_code = self.load_config(app, "mail_auth_code")[0]['dict_value']
        mail_receivers = self.load_config(app, "mail_receivers")[0]['dict_value'].split(",")
        mail = SendMail(mail_host)
        mail.send(title, content, mail_sender, mail_auth_code, mail_receivers)


if __name__ == '__main__':
    app = ApiTestCase()
    # res = app.load_all_case_by_app("ErgoSportive")
    # res = app.load_one_case_by_id("2")
    # res = app.load_config("ErgoSportive", "host")
    # res = app.query_test_results("ErgoSportive")
    # res = app.query_count("ErgoSportive", is_pass="F")
    # print(res)
    # api_host = app.load_config("ErgoSportive", 'host')
    # app.run_case(res, api_host)
    app.send_test_report("ErgoSportive")
    # app.run_all_case("ErgoSportive")
