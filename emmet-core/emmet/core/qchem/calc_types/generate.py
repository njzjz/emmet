"""Module to define various calculation types as Enums for Q-Chem."""
from __future__ import annotations

from itertools import product
from pathlib import Path

from emmet.core.qchem.calc_types.calc_types import (
    BASIS_SETS,
    FUNCTIONALS,
    SOLVENT_MODELS,
    TASK_TYPES,
)
from emmet.core.utils import get_enum_source

__author__ = "Evan Spotte-Smith <ewcspottesmith@lbl.gov>"


_LOTS = list()

for funct in FUNCTIONALS:
    for basis in BASIS_SETS:
        for solv_model in SOLVENT_MODELS:
            _LOTS.append(f"{funct}/{basis}/{solv_model}")

lot_enum = get_enum_source(
    "LevelOfTheory",
    "Levels of theory for calculations in Q-Chem",
    {
        "_".join(lot.split())
        .replace("+", "_")
        .replace("-", "_")
        .replace("(", "_")
        .replace(")", "_")
        .replace("/", "_")
        .replace("*", "_d"): lot
        for lot in _LOTS
    },
)

task_type_enum = get_enum_source(
    "TaskType",
    "Calculation task types for Q-Chem",
    {"_".join(tt.split()).replace("-", "_"): tt for tt in TASK_TYPES},
)

calc_type_enum = get_enum_source(
    "CalcType",
    "Calculation types (LOT + task type) for Q-Chem",
    {
        f"{'_'.join(lot.split()).replace('+','_').replace('-','_').replace('(', '_').replace(')', '_').replace('/', '_').replace('*', '_d')}_{'_'.join(tt.split()).replace('-', '_')}": f"{lot} {tt}"
        for lot, tt in product(_LOTS, TASK_TYPES)
    },
)

with open(Path(__file__).parent / "enums.py", "w") as f:
    f.write(
        """\"\"\"
Autogenerated Enums for Q-Chem LevelOfTheory, TaskType, and CalcType
Do not edit this by hand. Edit generate.py or types.py instead
\"\"\"
from emmet.core.utils import ValueEnum

"""
    )
    f.write(lot_enum)
    f.write("\n\n")
    f.write(task_type_enum)
    f.write("\n\n")
    f.write(calc_type_enum)
    f.write("\n")
