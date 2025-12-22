# -*- coding: utf-8 -*-
from typing import Any


# Base errors -----------------------------------------------------------------------------------------------------------
class BaseApiError(Exception):
    """The base class for all API errors."""

    def __init__(
        self,
        msg: object,
        url: str | None = None,
        data: Any | None = None,
        err_code: int | None = None,
    ):
        if not isinstance(msg, str):
            msg = str(msg)
        if url is not None:
            msg += "\n请求路径: %s" % url
        if data is not None:
            if isinstance(data, dict):
                data = {k: v for k, v in data.items() if v is not None}
            msg += "\n数据信息: %r" % data
        if err_code is not None:
            msg += "\n错误代码: %r" % err_code
        super().__init__(msg)


# API Settings errors ---------------------------------------------------------------------------------------------------
class ApiSettingsError(BaseApiError):
    """Raised when there is an error with the API settings."""


# Request errors --------------------------------------------------------------------------------------------------------
class RequestError(BaseApiError):
    """Raised when a request to the API fails."""


# Internet Error
class InternetConnectionError(RequestError):
    """Raised when there is an internet connectivity issue."""


# Timeout
class ApiTimeoutError(RequestError, TimeoutError):
    """Raise when the API request times out."""


# Server
class ServerError(RequestError):
    """Raised when the API server deos not return proper response."""


class InternalServerError(ServerError):
    """Raised when the API server returns a 500 error."""


# Authrization
class AuthorizationError(RequestError):
    """Raised when the API server returns a 4xx error related to authorization."""


class UnauthorizedApiError(AuthorizationError):
    """Raised when the API is not authorized for the app ID or secret."""


class UnauthorizedRequestIpError(AuthorizationError):
    """Raised when the IP address is not whitelisted for API access."""


# Token
class TokenError(RequestError):
    """Raised when the access token has expired."""


class TokenExpiredError(TokenError):
    """Raised when the access token has expired."""


class AccessTokenExpiredError(TokenExpiredError):
    """Raised when the access token has expired."""


class RefreshTokenExpiredError(TokenExpiredError):
    """Raised when the refresh token has expired."""


class InvalidTokenError(TokenError):
    """Raised when the token is invalid or malformed."""


class InvalidAccessTokenError(InvalidTokenError):
    """Raised when the access token is invalid."""


class InvalidRefreshTokenError(InvalidTokenError):
    """Raised when the refresh token is invalid."""


# App ID or Secret
class AppIdOrSecretError(RequestError):
    """Raised when the app ID or secret is invalid or missing."""


# Signature errors
class SignatureError(RequestError):
    """Raised when the signature is invalid or missing."""


class SignatureExpiredError(SignatureError):
    """Raised when the signature has expired."""


class InvalidSignatureError(SignatureError):
    """Raised when the signature is invalid."""


# Parameter
class ParametersError(RequestError):
    """Raised when the request parameters are invalid or missing."""


class InvalidApiUrlError(ParametersError):
    """Raised when the API server returns an error response."""


class InvalidParametersError(ParametersError):
    """Raised when a required parameter is missing."""


# API Limit
class ApiLimitError(RequestError):
    """Raised when the API limit has been reached."""


class TooManyRequestsError(ApiLimitError):
    """Raised when too many requests have been made to the API."""


# Unknown
class UnknownRequestError(RequestError):
    """Raised when an unknown error occurs during the request."""


# Response errors -------------------------------------------------------------------------------------------------------
class ReponseError(BaseApiError):
    """Raised when the data returned by the API is invalid or malformed."""


# Response data
class ResponseDataError(ReponseError):
    """Raised when the response data is not in the expected format."""
