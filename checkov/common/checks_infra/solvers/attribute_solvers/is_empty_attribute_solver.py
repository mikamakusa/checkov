from typing import List, Optional, Any, Dict
from collections.abc import Sized
from checkov.common.graph.checks_infra.enums import Operators
from checkov.common.checks_infra.solvers.attribute_solvers.base_attribute_solver import BaseAttributeSolver


class IsEmptyAttributeSolver(BaseAttributeSolver):
    operator = Operators.IS_EMPTY

    def __init__(self, resource_types: List[str], attribute: Optional[str], value: Any, is_jsonpath_check: bool = False) -> None:
        super().__init__(resource_types=resource_types, attribute=attribute, value=value,
                         is_jsonpath_check=is_jsonpath_check)

    def _get_operation(self, vertex: Dict[str, Any], attribute: Optional[str]) -> bool:
        attr = vertex.get(attribute)  # type:ignore[arg-type]  # due to attribute can be None

        # if this value contains an underendered variable, then we cannot evaluate the check,
        # so return True (since we cannot return UNKNOWN)
        if self._is_variable_dependant(attr, vertex["source_"]):
            return True

        if isinstance(attr, (list, Sized)):
            return len(attr) == 0

        return False
