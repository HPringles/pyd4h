"""Custom Exception for D4H Errors"""


class D4HException(Exception):
    """Custom Exception for D4H Errors"""

    status_code: int = None
    message: str = None

    def __init__(self, message, status_code=None):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)
