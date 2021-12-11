import xlwings as xw


def convert_slq():
    """
    将一个用例Excel固定格式的文件转化Sql语句
    """
    app = xw.App(visible=True, add_book=False)
    app.display_alerts = False
    app.screen_updating = False
    filepath = r'D:\workspce\document\ErgoSportive\接口文档\接口测试用例.xlsx'
    wb = app.books.open(filepath)
    sht = xw.sheets.active

    wb.save()
    wb.close()
    app.quit()
