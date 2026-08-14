from enum import Enum


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class AssessmentStatus(str, Enum):
    DRAFT = "DRAFT"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"