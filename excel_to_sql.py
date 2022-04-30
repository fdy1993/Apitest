import pandas as pd
from util.db_handler import DbHandler

db = DbHandler()
filepath = r'D:\workspce\document\ErgoSportive\接口文档\接口测试用例.xlsx'
df = pd.read_excel(filepath)
for indexs in df.index:
    a = df.loc[indexs].values[0:-2]
    a = tuple(a.tolist())
    # sql = "INSERT INTO interface_test.`case` (id, app, module, title, method, url, " \
    #       "run, headers, pre_case_id, pre_fields, request_body, expect_result,assert_type) VALUES {};".format(a)
    sql = sql = "INSERT INTO interface_test.`case` VALUES {};".format(a)
    db.execute_sql(sql)
