# Lenovo-"Xie Yan"
import re
import json
from django.core.handlers.asgi import ASGIRequest


# 邮箱正则表达式
def check_email_format(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)


# 解析request中的数据
def get_data_from_request(request: ASGIRequest)->dict:
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        return data
