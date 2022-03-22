'''Application Exceptions'''
import logging
from fastapi import HTTPException, status


class ApplicationExceptions:
    """Application Exceptons"""
    @staticmethod
    def too_many_rquests():
        """Too Many Requests"""
        logging.info('🛑 Request is limited')
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit Exceeded")

    @staticmethod
    def invalid_username_password():
        """Incorrect Username or Password"""
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    @staticmethod
    def invalid_client_id_and_client_secret():
        """Incorrect Client_id or Client Secret"""
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect client_id or client_secret",
            headers={"WWW-Authenticate": "Bearer"},
        )

    @staticmethod
    def could_not_validate_credentials():
        """Could not validate Credentials"""
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    @staticmethod
    def internal_server_error():
        """internal server error"""
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
            headers={"WWW-Authenticate": "Bearer"},
        )


exception = ApplicationExceptions
