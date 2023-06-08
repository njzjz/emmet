# TODO:
# TrajectoryQuery,
# EntryQuery,
from __future__ import annotations

from emmet.api.core.global_header import GlobalHeaderProcessor
from emmet.api.core.settings import MAPISettings
from emmet.api.routes.molecules.molecules.query_operators import (
    ChemsysQuery,
    ElementsQuery,
    FormulaQuery,
)
from emmet.api.routes.molecules.tasks.hint_scheme import TasksHintScheme
from emmet.api.routes.molecules.tasks.query_operators import (
    DeprecationQuery,
    MultipleTaskIDsQuery,
)
from emmet.core.qchem.task import TaskDocument
from emmet.core.tasks import DeprecationDoc
from maggma.api.query_operator import PaginationQuery, SortQuery, SparseFieldsQuery
from maggma.api.resource import ReadOnlyResource

timeout = MAPISettings().TIMEOUT


def task_resource(task_store):
    resource = ReadOnlyResource(
        task_store,
        TaskDocument,
        query_operators=[
            FormulaQuery(),
            ChemsysQuery(),
            ElementsQuery(),
            MultipleTaskIDsQuery(),
            SortQuery(),
            PaginationQuery(),
            SparseFieldsQuery(
                TaskDocument,
                default_fields=["task_id", "formula_alphabetical", "last_updated"],
            ),
        ],
        header_processor=GlobalHeaderProcessor(),
        hint_scheme=TasksHintScheme(),
        tags=["Molecules Tasks"],
        sub_path="/tasks/",
        timeout=timeout,
        disable_validation=True,
    )

    return resource


def task_deprecation_resource(task_store):
    resource = ReadOnlyResource(
        task_store,
        DeprecationDoc,
        query_operators=[DeprecationQuery(), PaginationQuery()],
        tags=["Molecules Tasks"],
        enable_get_by_key=False,
        enable_default_search=True,
        sub_path="/tasks/deprecation/",
        header_processor=GlobalHeaderProcessor(),
        timeout=timeout,
    )

    return resource


# TODO: def trajectory_resource(task_store):
# TODO: def entries_resource(task_store):
