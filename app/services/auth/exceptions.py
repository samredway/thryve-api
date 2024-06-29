from app.exceptions import EnWorthError


class AuthError(EnWorthError):
    pass


class ExpiredTokenError(AuthError):
    pass
