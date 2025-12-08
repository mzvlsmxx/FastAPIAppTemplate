class ExceptionTemplate(Exception):
    """Raised when ..."""
    def __init__(self, message: str = ''):
        defaultMessage: str = 'Default Message'
        if message:
            super().__init__(message)
        else:
            super().__init__(defaultMessage)


class DatabaseConnectionError(Exception):
    """Raised when can't connect to database"""
    def __init__(self, message: str = ''):
        defaultMessage: str = 'Can not connect to database'
        if message:
            super().__init__(message)
        else:
            super().__init__(defaultMessage)


class InvalidDatabaseInput(Exception):
    """Raised when invalid user profile data is trying to add into database"""
    def __init__(self, message: str = ''):
        defaultMessage: str = 'Invalid database input'
        if message:
            super().__init__(message)
        else:
            super().__init__(defaultMessage)


class DuplicateDatabaseInput(Exception):
    """Raised when duplicate user passport or insurance data is trying to add into database"""
    def __init__(self, message: str = ''):
        defaultMessage: str = 'Duplicate input'
        if message:
            super().__init__(message)
        else:
            super().__init__(defaultMessage)
