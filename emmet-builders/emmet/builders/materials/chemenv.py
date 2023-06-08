from __future__ import annotations

from typing import TYPE_CHECKING

from emmet.core.chemenv import ChemEnvDoc
from emmet.core.utils import jsanitize
from maggma.builders.map_builder import MapBuilder
from pymatgen.core.structure import Structure

if TYPE_CHECKING:
    from maggma.core import Store


class ChemEnvBuilder(MapBuilder):
    def __init__(
        self,
        oxidation_states: Store,
        chemenv: Store,
        query: dict | None = None,
        **kwargs
    ):
        self.oxidation_states = oxidation_states
        self.chemenv = chemenv
        self.kwargs = kwargs

        self.chemenv.key = "material_id"
        self.oxidation_states.key = "material_id"

        super().__init__(
            source=oxidation_states,
            target=chemenv,
            query=query,
            projection=["material_id", "structure", "deprecated"],
            **kwargs
        )

    def unary_function(self, item):
        structure = Structure.from_dict(item["structure"])
        mpid = item["material_id"]
        deprecated = item["deprecated"]

        doc = ChemEnvDoc.from_structure(
            structure=structure,
            material_id=mpid,
            deprecated=deprecated,
        )

        return jsanitize(doc.dict(), allow_bson=True)
