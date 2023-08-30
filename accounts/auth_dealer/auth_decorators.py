from functools import wraps
from accounts.auth_dealer.auth_provider import auth_provider
from utils.exceptions import Status
from rest_framework.views import APIView


def must_be_user():
    def decorator(api_func):
        @wraps(api_func)
        def _wrapped_view(request, *args, **kwargs):
            request = request.request if isinstance(request, APIView) else request
            auth_token = auth_provider.get_token_from_request(request)
            if auth_token is None:
                raise Exception('The token is None')
            res = auth_provider.check_auth(
                auth_token
            )  # check_auth will raise error on not valid user
            if not isinstance(res, Status):
                request.user = res
                return api_func(request, *args, **kwargs)
        return _wrapped_view

    return decorator
