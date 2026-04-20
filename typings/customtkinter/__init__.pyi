from tkinter import BooleanVar as BooleanVar
from tkinter import DoubleVar as DoubleVar
from tkinter import IntVar as IntVar
from tkinter import StringVar as StringVar
from tkinter import Variable as Variable

from customtkinter.windows import CTk as CTk
from customtkinter.windows import CTkInputDialog as CTkInputDialog
from customtkinter.windows import CTkToplevel as CTkToplevel
from customtkinter.windows.widgets import (
    CTkButton as CTkButton,
)
from customtkinter.windows.widgets import (
    CTkCheckBox as CTkCheckBox,
)
from customtkinter.windows.widgets import (
    CTkComboBox as CTkComboBox,
)
from customtkinter.windows.widgets import (
    CTkEntry as CTkEntry,
)
from customtkinter.windows.widgets import (
    CTkFrame as CTkFrame,
)
from customtkinter.windows.widgets import (
    CTkLabel as CTkLabel,
)
from customtkinter.windows.widgets import (
    CTkOptionMenu as CTkOptionMenu,
)
from customtkinter.windows.widgets import (
    CTkProgressBar as CTkProgressBar,
)
from customtkinter.windows.widgets import (
    CTkRadioButton as CTkRadioButton,
)
from customtkinter.windows.widgets import (
    CTkScrollableFrame as CTkScrollableFrame,
)
from customtkinter.windows.widgets import (
    CTkScrollbar as CTkScrollbar,
)
from customtkinter.windows.widgets import (
    CTkSegmentedButton as CTkSegmentedButton,
)
from customtkinter.windows.widgets import (
    CTkSwitch as CTkSwitch,
)
from customtkinter.windows.widgets import (
    CTkTabview as CTkTabview,
)
from customtkinter.windows.widgets import (
    CTkTextbox as CTkTextbox,
)
from customtkinter.windows.widgets.core_rendering import CTkCanvas as CTkCanvas
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass as CTkBaseClass
from customtkinter.windows.widgets.ctk_slider import CTkSlider as CTkSlider
from customtkinter.windows.widgets.font import CTkFont as CTkFont
from customtkinter.windows.widgets.image import CTkImage as CTkImage

def set_appearance_mode(mode_string: str) -> None: ...
def get_appearance_mode() -> str: ...
def set_default_color_theme(color_string: str) -> None: ...
def set_widget_scaling(scaling_value: float) -> None: ...
def set_window_scaling(scaling_value: float) -> None: ...
def deactivate_automatic_dpi_awareness() -> None: ...
def set_ctk_parent_class(ctk_parent_class: type[object]) -> None: ...
