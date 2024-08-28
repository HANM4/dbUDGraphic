from tkinter import *
from tkinter import ttk, filedialog
import pandas
import docxtpl
from support_function import check_extensions_path
from graphic_interface import BlockOpenFile, BlockConsole, CustomButton
from threading import Thread
from typing import Optional, Any


class AsyncRender(Thread):
    path_db_csv: str
    path_template_doc: str
    path_save_doc: Optional[str]
    console_block: Optional[BlockConsole]

    def __init__(self, path_db_csv: str,
                 path_template_doc: str,
                 path_save_doc: Optional[str],
                 console_block: Optional[BlockConsole] = None) -> None:
        super().__init__()
        self.path_db_csv = path_db_csv
        self.path_template_doc = path_template_doc
        if path_save_doc:
            self.path_save_doc = path_save_doc
        if console_block:
            self.console_block = console_block

    def run(self) -> None:
        """
        convert the database to a template and save it to the selected folder
        """
        if self.path_db_csv and self.path_template_doc and self.path_save_doc:
            db = pandas.read_csv(self.path_db_csv)
            header_db = db.columns.values.tolist()

            indicator_extension = check_extensions_path(
                self.path_save_doc,
                ('.doc', '.docx')
            )

            for i, row in db.iterrows():
                template = docxtpl.DocxTemplate(self.path_template_doc)

                context = {}
                for header in header_db:
                    context[header] = row[header]
                if self.console_block:
                    self.console_block.write_to_console(str(context))
                template.render(context)

                if not indicator_extension:
                    path_save_doc_final = f"{self.path_save_doc}{i}.docx"
                else:
                    i_extension = self.path_save_doc.rfind(".")
                    path_save_doc_final = (
                        f"{self.path_save_doc[:i_extension]}"
                        f"{i}{self.path_save_doc[i_extension:]}")
                template.save(path_save_doc_final)


class Converter:
    def __init__(self) -> None:
        self.window = Tk()
        # window.geometry('536x320')
        self.window.title('dbUDG')
        '''
        main frame
        '''
        self.main_frame = ttk.Frame(padding=5, borderwidth=1, relief=GROOVE)
        self.main_frame.pack()
        '''
        block console
        '''
        # frame
        self.console_frame = ttk.Frame(master=self.main_frame,
                                       padding=5, borderwidth=1, relief=GROOVE)
        self.console_frame.grid(row=2, column=0, columnspan=2)
        # console
        self.console_scrolled_text = BlockConsole(self.console_frame)
        '''
        block doc template
        '''
        # frame
        self.doc_temp_frame = ttk.Frame(master=self.main_frame,
                                        padding=5, borderwidth=1, relief=GROOVE)
        self.doc_temp_frame.grid(row=0, column=0)
        # model open file
        self.doc_temp_model_open_file = BlockOpenFile(
            self.doc_temp_frame,
            extensions=(".doc", ".docx"),
            console_block=self.console_scrolled_text
        )
        self.doc_temp_model_open_file.var_string.trace_add(
            "write",
            self.check_fullness_and_switch_blocs_open_file
        )
        self.doc_temp_model_open_file.label['text'] = "Doc template"
        '''
        block db
        '''
        # frame
        self.db_frame = ttk.Frame(master=self.main_frame,
                                  padding=5, borderwidth=1, relief=GROOVE)
        self.db_frame.grid(row=0, column=1)
        # model open file
        self.db_model_open_file = BlockOpenFile(
            father_frame=self.db_frame,
            extensions=(".csv",),
            console_block=self.console_scrolled_text
        )
        self.db_model_open_file.var_string.trace_add(
            "write",
            self.check_fullness_and_switch_blocs_open_file
        )
        self.db_model_open_file.label['text'] = "DB"

        # '''one_file
        # '''
        # # checkbox
        # self.var_one_file_checkbox = BooleanVar()
        # self.one_file_checkbox = ttk.Checkbutton(
        #     master=self.main_frame,
        #     text="One file",
        #     variable=self.var_one_file_checkbox
        # )
        # self.var_one_file_checkbox.set(True)
        # self.one_file_checkbox.grid(row=1, column=0, sticky='W')

        '''
        block finish button
        '''
        # frame
        self.finish_frame = ttk.Frame(master=self.main_frame,
                                      padding=5, borderwidth=1, relief=GROOVE)
        self.finish_frame.grid(row=3, column=0, columnspan=2, sticky='E')
        # render and save button
        self.render_button = CustomButton(
            master=self.finish_frame,
            state=DISABLED,
            text="Render and Save",
            command=self.handle_render
        )
        self.render_button.grid(row=0, column=0)

    # know path to save dir
    @staticmethod
    def know_path_save() -> Optional[str]:
        filepath = filedialog.asksaveasfilename()
        if not filepath == "":
            return filepath
        return None

    # Под вопросом, мне не нравится как выглядит функция
    def check_fullness_and_switch_blocs_open_file(self, *args: Any) -> None:
        if self.render_button.check_fullness_data(
                (self.doc_temp_model_open_file, self.db_model_open_file)
        ):
            self.render_button['state'] = NORMAL
        else:
            self.render_button['state'] = DISABLED

    def handle_render(self) -> None:
        self.render_button['state'] = DISABLED

        render_thread = AsyncRender(
            path_db_csv=self.db_model_open_file.entry.get(),
            path_template_doc=self.doc_temp_model_open_file.entry.get(),
            path_save_doc=self.know_path_save(),
            console_block=self.console_scrolled_text
        )
        render_thread.start()
        self.monitor(render_thread)

    def monitor(self, thread: AsyncRender) -> None:
        if thread.is_alive():
            # check the thread every 100ms
            self.window.after(100, lambda: self.monitor(thread))
        else:
            self.render_button['state'] = NORMAL


if __name__ == "__main__":
    converter = Converter()
    converter.window.mainloop()
