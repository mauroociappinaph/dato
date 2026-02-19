from enum import Enum
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime


class RollbackStrategy(Enum):
    IMMEDIATE = "immediate"
    STAGED = "staged"
    GRACEFUL = "graceful"
    MANUAL = "manual"


class RollbackStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class RollbackOperation:
    operation_id: str
    stage_name: str
    skill_name: str
    rollback_strategy: RollbackStrategy
    rollback_function: Optional[Callable]
    rollback_data: Dict[str, Any]
    status: RollbackStatus
    start_time: datetime
    end_time: Optional[datetime]
    error_message: Optional[str]


@dataclass
class RollbackPlan:
    plan_id: str
    playbook_name: str
    execution_id: str
    strategy: RollbackStrategy
    operations: List[RollbackOperation]
    status: RollbackStatus
    created_at: datetime
    completed_at: Optional[datetime]
