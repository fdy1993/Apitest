import requests
from util import logs_util


def requests_util(url, method, headers=None, param=None, content_type=None):
    """
    通⽤接口请求⼯工具方法
    :param url:请求URL
    :param method:请求方法，如post、get
    :param headers:请求头信息
    :param param:请求参数
    :param content_type:请求类型，如json、文本、图片、音频、表单
    :return:请求返回的response的json数据
    """
    try:
        if method == 'get':
            result = requests.get(url, param=param, headers=headers).json()
            return result
        elif method == 'post':
            if content_type == 'application/json':
                result = requests.post(url, json=param, headers=headers).json()
                return result
            elif content_type == 'x-www-form-urlencoded':
                result = requests.post(url, data=param, headers=headers).json()
                return result
            else:
                print("http method not allowed")
    except Exception as e:
        print(f'http请求报错:{e}')
        logs_util.logs_util('', e, 'error')


if __name__ == '__main__':
    requests_util('https://www.baidu.com', 'get')
