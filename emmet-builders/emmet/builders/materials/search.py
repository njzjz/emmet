from typing import Dict
from collections import defaultdict
from math import ceil

from maggma.builders import Builder
from maggma.utils import grouper

from emmet.core.mpid import MPID
from emmet.core.search import SearchDoc, key
from emmet.core.utils import jsanitize


class SearchBuilder(Builder):
    def __init__(
        self,
        materials,
        thermo,
        xas,
        grain_boundaries,
        electronic_structure,
        magnetism,
        elasticity,
        dielectric,
        phonon,
        insertion_electrodes,
        substrates,
        surfaces,
        eos,
        search,
        chunk_size=100,
        query=None,
        **kwargs,
    ):

        self.materials = materials
        self.thermo = thermo
        self.xas = xas
        self.grain_boundaries = grain_boundaries
        self.electronic_structure = electronic_structure
        self.magnetism = magnetism
        self.elasticity = elasticity
        self.dielectric = dielectric
        self.phonon = phonon
        self.insertion_electrodes = insertion_electrodes
        self.substrates = substrates
        self.surfaces = surfaces
        self.eos = eos
        self.search = search
        self.chunk_size = chunk_size
        self.query = query if query else {}

        super().__init__(
            sources=[
                materials,
                thermo,
                xas,
                grain_boundaries,
                electronic_structure,
                magnetism,
                elasticity,
                dielectric,
                phonon,
                insertion_electrodes,
                surfaces,
                substrates,
                eos,
            ],
            targets=[search],
            chunk_size=chunk_size,
            **kwargs,
        )

    def get_items(self):
        """
        Gets all items to process

        Returns:
            list of relevant materials and data
        """

        self.logger.info("Search Builder Started")

        q = dict(self.query)

        mat_ids = self.materials.distinct(field=self.materials.key, criteria=q)
        search_ids = self.search.distinct(field=self.search.key, criteria=q)

        search_set = set(mat_ids) - set(search_ids)

        self.total = len(search_set)

        self.logger.debug("Processing {} materials.".format(self.total))

        for entry in search_set:

            data = {
                "materials": list(self.materials.query({self.materials.key: entry})),
                "thermo": list(self.thermo.query({self.thermo.key: entry})),
                "xas": list(self.xas.query({self.xas.key: entry})),
                "grain_boundaries": list(
                    self.grain_boundaries.query({self.grain_boundaries.key: entry})
                ),
                "electronic_structure": list(
                    self.electronic_structure.query(
                        {self.electronic_structure.key: entry}
                    )
                ),
                "magnetism": list(self.magnetism.query({self.magnetism.key: entry})),
                "elasticity": list(self.elasticity.query({self.elasticity.key: entry})),
                "dielectric": list(self.dielectric.query({self.dielectric.key: entry})),
                "phonon": list(
                    self.phonon.query({self.phonon.key: entry}, [self.phonon.key])
                ),
                "insertion_electrodes": list(
                    self.insertion_electrodes.query(
                        {self.insertion_electrodes.key: entry},
                        [self.insertion_electrodes.key],
                    )
                ),
                "surface_properties": list(
                    self.surfaces.query({self.surfaces.key: entry})
                ),
                "substrates": list(self.surfaces.query({self.substrates.key: entry})),
                "eos": list(self.eos.query({self.eos.key: entry}, [self.eos.key])),
            }

            yield data

    def prechunk(self, number_splits: int):
        """
        Prechunk method to perform chunking by the key field
        """
        q = dict(self.query)

        keys = self.search.newer_in(self.materials, criteria=q, exhaustive=True)

        N = ceil(len(keys) / number_splits)
        for split in grouper(keys, N):
            yield {"query": {self.materials.key: {"$in": list(split)}}}

    def process_item(self, item):

        material_id = MPID(item["materials"]["material_id"])
        doc = SearchDoc.from_docs(material_id=material_id, **item)
        return jsanitize(doc.dict(exclude_none=True), allow_bson=True)

    def update_targets(self, items):
        """
        Copy each search doc to the store

        Args:
            items ([dict]): A list of dictionaries of mpid document pairs to update
        """
        items = list(filter(None, items))

        if len(items) > 0:
            self.logger.info("Inserting {} search docs".format(len(items)))
            self.search.update(docs=items)
        else:
            self.logger.info("No search entries to update")
