from tkinter import *
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText
from support_function import check_extensions_path
from typing import Optional, Union


class BlockConsole:
    father_frame: Union[Frame, ttk.Frame]

    def __init__(self, father_frame: Union[Frame, ttk.Frame]) -> None:
        # label
        self.label = ttk.Label(master=father_frame,
                               text="Console")
        self.label.grid(row=0, column=0, sticky='W')
        # console scrolled text
        self.console = ScrolledText(master=father_frame,
                                    height=10, width=60,
                                    state=DISABLED)
        self.console.grid(row=1, column=0)

    # activate console, write to console ,disabled console
    def write_to_console(self, text: str) -> None:
        self.console['state'] = NORMAL
        self.console.insert(END, f"{text}\n")
        self.console['state'] = DISABLED


class BlockOpenFile:
    father_frame: Union[Frame, ttk.Frame]
    console_block: BlockConsole
    extensions: tuple

    def __init__(self, father_frame: Union[Frame, ttk.Frame],
                 console_block: Optional[BlockConsole] = None,
                 extensions: Optional[tuple] = None) -> None:
        if console_block:
            self.console_block = console_block
        if extensions:
            self.extensions = extensions
        self.var_string = StringVar()
        # label
        self.label = ttk.Label(master=father_frame, text="Text")
        self.label.grid(row=0, column=0, columnspan=2, sticky='W')
        # enry
        self.entry = ttk.Entry(master=father_frame, width=27, state=DISABLED,
                               textvariable=self.var_string)
        self.entry.grid(row=1, column=0, columnspan=2)
        self.entry.bind(sequence='<Button-1>', func=self.open_file)
        # button
        self.button = ttk.Button(master=father_frame, text="...",
                                 command=self.open_file)
        self.button.grid(row=1, column=3)

    def write_entry(self, text: str) -> None:
        self.entry['state'] = NORMAL
        self.entry.delete(0, END)
        self.entry.insert(0, text)
        self.entry['state'] = DISABLED

    def open_file(self, event: Optional[Event] = None):
        filepath: str = filedialog.askopenfilename()
        if self.extensions and filepath:
            if check_extensions_path(filepath, self.extensions):
                self.write_entry(filepath)
            else:
                if self.console_block:
                    self.console_block.write_to_console(
                        f"Error: Incorrect format, valid format "
                        f"{self.extensions}")
        elif filepath:
            self.write_entry(filepath)


# Под вопросом, думаю нужен ли этот класс
class CustomButton(ttk.Button):
    """
    Под вопросом, думаю нужна ли такая
    функция здесь или перенести её в Convert
    думаю это слишком персонализированная функция для Convert
    """
    @staticmethod
    def check_fullness_data(items: tuple[BlockOpenFile, ...]) -> bool:
        for item in items:
            if not item.entry.get() == "":
                break
            else:
                return False
        return True

    # def switch_state(self):
    #     if self['state'] == DISABLED:
    #         self['state'] = NORMAL
    #     else:
    #         self['state'] == DISABLED
