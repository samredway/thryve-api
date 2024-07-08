from app.exceptions import ThryveError


class AuthError(ThryveError):
    pass


class ExpiredTokenError(AuthError):
    pass
