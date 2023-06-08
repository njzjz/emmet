from __future__ import annotations

from emmet.api.routes.materials.piezo.query_operators import PiezoelectricQuery
from monty.serialization import dumpfn, loadfn
from monty.tempfile import ScratchDir


def test_piezo_query():
    op = PiezoelectricQuery()

    assert op.query(piezo_modulus_min=0, piezo_modulus_max=5) == {
        "criteria": {"e_ij_max": {"$gte": 0, "$lte": 5}}
    }

    with ScratchDir("."):
        dumpfn(op, "temp.json")
        new_op = loadfn("temp.json")
        assert new_op.query(piezo_modulus_min=0, piezo_modulus_max=5) == {
            "criteria": {"e_ij_max": {"$gte": 0, "$lte": 5}}
        }
