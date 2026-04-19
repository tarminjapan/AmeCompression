from collections.abc import Callable
from tkinter import Variable
from typing import Any

from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

class CTkSlider(CTkBaseClass):
    def __init__(
        self,
        master: Any,
        width: int | None = None,
        height: int | None = None,
        corner_radius: int | None = None,
        button_corner_radius: int | None = None,
        border_width: int | None = None,
        button_length: int | None = None,
        bg_color: str | tuple[str, str] = "transparent",
        fg_color: str | tuple[str, str] | None = None,
        border_color: str | tuple[str, str] = "transparent",
        progress_color: str | tuple[str, str] | None = None,
        button_color: str | tuple[str, str] | None = None,
        button_hover_color: str | tuple[str, str] | None = None,
        from_: float = 0,
        to: float = 1,
        state: str = "normal",
        number_of_steps: int | None = None,
        hover: bool = True,
        command: Callable[[float], Any] | None = None,
        variable: Variable | None = None,
        orientation: str = "horizontal",
        **kwargs: Any,
    ) -> None: ...
    def set(self, output_value: float, from_variable_callback: bool = False) -> None: ...
    def get(self) -> float: ...
