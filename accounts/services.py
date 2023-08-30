from accounts.repositories import user_repo, token_repo
from accounts.auth_dealer.auth_provider import auth_provider
from utils.exceptions import Status

class UserService:
    def sign_up(self, email: str, password: str,email_code:str):
        sign_up_res = auth_provider.register(email, password, email_code)
        return sign_up_res

    def login(self, email: str, password: str,img_code:str):
        login_res = auth_provider.login(email, password,img_code)
        return login_res

    def logout(self, user_id: str):
        token_repo.delete_by_user_id(user_id)
        return True


user_service = UserService()
