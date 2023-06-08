from __future__ import annotations

from typing import TYPE_CHECKING

from monty.json import MontyDecoder
from pydantic import BaseModel, Field, validator

if TYPE_CHECKING:
    from datetime import datetime


class FermiDoc(BaseModel):
    """Fermi surfaces."""

    fermi_surfaces: list[dict] = Field(
        None,
        description="List of IFermi FermiSurface objects.",
    )

    surface_types: list[str] = Field(
        None,
        description="Type of each fermi surface in the fermi_surfaces list.\
            Is either CBM or VBM for semiconductors, or fermi_surface for metals.",
    )

    task_id: str = Field(
        None,
        description="The Materials Project ID of the material. This comes in the form: mp-******.",
    )

    last_updated: datetime = Field(
        None,
        description="Timestamp for the most recent calculation for this fermi surface document.",
    )

    # Make sure that the datetime field is properly formatted
    @validator("last_updated", pre=True)
    def last_updated_dict_ok(cls, v):
        return MontyDecoder().process_decoded(v)
