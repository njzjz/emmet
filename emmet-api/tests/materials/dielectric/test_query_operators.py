from __future__ import annotations

from emmet.api.routes.materials.dielectric.query_operators import DielectricQuery
from monty.serialization import dumpfn, loadfn
from monty.tempfile import ScratchDir


def test_dielectric_query_operator():
    op = DielectricQuery()

    q = op.query(
        e_total_min=0,
        e_total_max=5,
        e_electronic_min=0,
        e_electronic_max=5,
        e_ionic_min=0,
        e_ionic_max=5,
        n_min=0,
        n_max=5,
    )

    fields = [
        "e_total",
        "e_ionic",
        "e_electronic",
        "n",
    ]

    assert q == {"criteria": {field: {"$gte": 0, "$lte": 5} for field in fields}}

    with ScratchDir("."):
        dumpfn(op, "temp.json")
        new_op = loadfn("temp.json")
        q = new_op.query(
            e_total_min=0,
            e_total_max=5,
            e_electronic_min=0,
            e_electronic_max=5,
            e_ionic_min=0,
            e_ionic_max=5,
            n_min=0,
            n_max=5,
        )
        assert dict(q) == {
            "criteria": {field: {"$gte": 0, "$lte": 5} for field in fields}
        }
