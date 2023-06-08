"""Core definition of a Task Document which represents a calculation from some program."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from emmet.core.base import EmmetBaseModel
from pydantic import Field

if TYPE_CHECKING:
    from emmet.core.mpid import MPID, MPculeID


class BaseTaskDocument(EmmetBaseModel):
    """Definition of base Task Document."""

    calc_code: str = Field(description="The calculation code used to compute this task")
    version: str = Field(None, description="The version of the calculation code")
    dir_name: str = Field(None, description="The directory for this task")
    task_id: MPID | MPculeID = Field(None, description="the Task ID For this document")

    completed: bool = Field(False, description="Whether this calcuation completed")
    completed_at: datetime = Field(
        None, description="Timestamp for when this task was completed"
    )
    last_updated: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp for this task document was last updated",
    )
