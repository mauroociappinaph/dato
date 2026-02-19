"""
Core exceptions for Global Skills.

Provides a hierarchy of exceptions for different error scenarios
to enable precise error handling and debugging.
"""


class SkillError(Exception):
    """Base exception for all skill-related errors."""
    def __init__(self, message: str, skill_name: str = None, details: dict = None):
        super().__init__(message)
        self.skill_name = skill_name
        self.details = details or {}


class ValidationError(SkillError):
    """Raised when input validation fails."""
    def __init__(self, message: str, skill_name: str = None, validation_errors: list = None):
        super().__init__(message, skill_name)
        self.validation_errors = validation_errors or []


class ExecutionError(SkillError):
    """Raised when skill execution fails."""
    def __init__(self, message: str, skill_name: str = None, execution_id: str = None, cause: Exception = None):
        super().__init__(message, skill_name)
        self.execution_id = execution_id
        self.cause = cause


class CostExceededError(SkillError):
    """Raised when execution cost exceeds limit."""
    def __init__(self, message: str, skill_name: str = None, estimated_cost: float = None, limit: float = None):
        super().__init__(message, skill_name)
        self.estimated_cost = estimated_cost
        self.limit = limit


class SkillNotFoundError(SkillError):
    """Raised when a requested skill is not found."""
    def __init__(self, skill_name: str, available_skills: list = None):
        message = f"Skill '{skill_name}' not found"
        super().__init__(message, skill_name)
        self.available_skills = available_skills or []


class PlaybookError(Exception):
    """Base exception for playbook-related errors."""
    def __init__(self, message: str, playbook_name: str = None, details: dict = None):
        super().__init__(message)
        self.playbook_name = playbook_name
        self.details = details or {}


class StageError(PlaybookError):
    """Raised when a stage execution fails."""
    def __init__(self, message: str, playbook_name: str = None, stage_name: str = None):
        super().__init__(message, playbook_name)
        self.stage_name = stage_name


class DependencyError(PlaybookError):
    """Raised when stage dependencies cannot be resolved."""
    def __init__(self, message: str, playbook_name: str = None, dependency_chain: list = None):
        super().__init__(message, playbook_name)
        self.dependency_chain = dependency_chain or []


class ApprovalRequiredError(PlaybookError):
    """Raised when playbook execution requires approval."""
    def __init__(self, message: str, playbook_name: str = None, estimated_cost: float = None):
        super().__init__(message, playbook_name)
        self.estimated_cost = estimated_cost


class TimeoutError(SkillError):
    """Raised when execution exceeds time limit."""
    def __init__(self, message: str, skill_name: str = None, timeout_seconds: int = None):
        super().__init__(message, skill_name)
        self.timeout_seconds = timeout_seconds
