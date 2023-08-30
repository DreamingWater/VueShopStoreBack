# Lenovo-"Xie Yan"
from accounts.services import user_service
from utils.exceptions import Status


class AccountReturn:
    def __init__(self):
        self.return_pattern = {}

    def deal_event(self, login_result) -> dict:
        if not isinstance(login_result, Status):  # if success: login_result means token
            self.get_success_info(login_result)
            return self.return_pattern
        else:  # failed
            self.get_status_info(login_result.value)  # 获取status的value
        return self.return_pattern

    # 成功处理数据
    def get_success_info(self, data: dict):
        self.return_pattern['data'] = data
        self.return_pattern['code'] = 200
        self.return_pattern['message'] = 'success'
        self.return_pattern['ok'] = 'true'

    # deal status
    def get_status_info(self, status_enum):
        status_info = status_enum.values
        self.return_pattern['code'] = status_info['code']
        self.return_pattern['message'] = status_info['msg']
        self.return_pattern['ok'] = 'false'
        self.return_pattern['data'] = None

    def return_error_status(self, status_enum) -> dict:
        self.get_status_info(status_enum)
        return self.return_pattern

    # img
    def return_img_status(self, img_base64: str) -> dict:
        self.return_pattern['data'] = {'img': img_base64}
        self.return_pattern['code'] = 200
        self.return_pattern['message'] = 'success'
        self.return_pattern['ok'] = 'true'
        return


accounts_return = AccountReturn()
