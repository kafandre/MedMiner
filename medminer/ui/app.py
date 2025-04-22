from typing import Any

import gradio as gr

from medminer.ui.api import process_files, process_sql, process_text
from medminer.ui.settings import MODEL_TABS, TASK_SETTINGS

with gr.Blocks(
    title="MedMiner",
) as demo:
    model_settings = gr.State({})
    task_settings = gr.State({})
    tasks_state = gr.State([])

    def set_state(state: dict, name: str, param: Any) -> dict:
        if not name:
            return state

        if param:
            state[name] = param
        elif name in state and state[name]:
            del state[name]

        return state

    title = gr.Markdown(
        """
        # MedMiner
        A tool for extracting information from medical text in natural langauage.
        """
    )
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Accordion("Model settings"):

                @gr.render()
                def draw_model_tabs() -> None:
                    with gr.Tabs():
                        for tab in MODEL_TABS:
                            if not tab.get("available", False):
                                continue

                            with gr.Tab(tab.get("name", ""), id=tab.get("id", "")):
                                if desc := tab.get("description"):
                                    gr.Markdown(desc)
                                for field in tab.get("fields", []):
                                    _field = gr.Textbox(**field.get("params", {}))
                                    _field.input(
                                        set_state,
                                        inputs=[
                                            model_settings,
                                            gr.Textbox(value=field.get("id"), visible=False),
                                            _field,
                                        ],
                                        outputs=model_settings,
                                    )

            with gr.Accordion("Task settings"):
                _tasks = [task.get("name", "") for task in TASK_SETTINGS.get("tasks", [])]
                _task_ids = [task.get("id", "") for task in TASK_SETTINGS.get("tasks", [])]

                tasks_input = gr.CheckboxGroup(
                    label=TASK_SETTINGS.get("description", ""),
                    type="index",
                    choices=_tasks,
                )
                tasks_input.input(
                    lambda tasks: [_task_ids[i] for i in tasks], inputs=[tasks_input], outputs=tasks_state
                )

                @gr.render(inputs=tasks_state)
                def draw_task_settings(tasks: list[int]) -> None:
                    for setting in TASK_SETTINGS.get("settings", []):
                        if setting.get("dependent") and not any(
                            [task in setting.get("dependent", []) for task in tasks]
                        ):
                            continue

                        _field = gr.Textbox(**setting.get("params", {}))
                        _field.input(
                            set_state,
                            inputs=[
                                task_settings,
                                gr.Textbox(value=setting.get("id"), visible=False),
                                _field,
                            ],
                            outputs=task_settings,
                        )

            gr.Markdown("## Data")
            with gr.Tabs() as data_tabs:
                with gr.Tab(".txt Files"):
                    gr.Markdown("Upload a file to extract information from it.")
                    txt_files_input = gr.Files(label="Upload a files", file_types=[".txt"], file_count="multiple")
                    process_txt_files_btn = gr.Button("Process Files")

                with gr.Tab("CSV"):
                    gr.Markdown("Upload a file to extract information from it.")
                    csv_file_input = gr.Files(
                        label="Upload a files",
                        file_types=[".csv"],
                    )
                    process_csv_file_btn = gr.Button("Process Files")

                with gr.Tab("SQL"):
                    gr.Markdown("Enter a SQL query to extract information from a database.")
                    sql_input = gr.Textbox(label="SQL Query", placeholder="SELECT patient_id, text FROM patient_notes")
                    process_sql_btn = gr.Button("Process SQL")

                with gr.Tab("Text"):
                    gr.Markdown("Enter a text to extract information from it.")
                    text_input = gr.Textbox(label="Text", placeholder="Enter text here", lines=20)
                    process_text_btn = gr.Button("Process Text")

        with gr.Column(scale=1):
            output_text = gr.Markdown("## Output")

            output_data = gr.Dataframe()

        process_txt_files_btn.click(process_files, inputs=[txt_files_input, tasks_input], outputs=[output_data])
        process_csv_file_btn.click(process_files, inputs=[csv_file_input, tasks_input], outputs=[output_data])
        process_sql_btn.click(process_sql, inputs=[sql_input, tasks_input], outputs=[output_data])
        process_text_btn.click(process_text, inputs=[text_input, tasks_input], outputs=[output_data])


demo.launch()
