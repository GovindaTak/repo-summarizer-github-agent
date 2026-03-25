from typing import Optional, Dict


class AppException(Exception):
    """
    Custom application exception for controlled error handling.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 400,
    ):
        self.message = message
        self.status_code = status_code

        super().__init__(message)