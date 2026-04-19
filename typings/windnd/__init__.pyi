from collections.abc import Callable, Sequence
from typing import Any

DropFile = bytes | str
DropCallback = Callable[[Sequence[DropFile]], Any]

def hook_dropfiles(widget: Any, func: DropCallback) -> Any: ...
