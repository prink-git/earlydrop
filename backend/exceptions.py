"""
Custom exception classes for the EarlyDrop backend.
"""

class EarlyDropException(Exception):
    """Base exception for EarlyDrop backend."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class DatabaseError(EarlyDropException):
    """Raised when a database operation fails."""
    def __init__(self, message: str):
        super().__init__(f"Database error: {message}", 500)

class StudentNotFoundError(EarlyDropException):
    """Raised when a student is not found."""
    def __init__(self, student_id: str):
        super().__init__(f"Student with ID {student_id} not found", 404)

class ValidationError(EarlyDropException):
    """Raised when data validation fails."""
    def __init__(self, message: str):
        super().__init__(f"Validation error: {message}", 400)

class RiskComputationError(EarlyDropException):
    """Raised when risk computation fails."""
    def __init__(self, message: str):
        super().__init__(f"Risk computation error: {message}", 500)

class InterventionError(EarlyDropException):
    """Raised when intervention recording fails."""
    def __init__(self, message: str):
        super().__init__(f"Intervention error: {message}", 500)
