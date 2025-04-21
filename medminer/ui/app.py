import gradio as gr

from medminer.ui.api import TaskType, process_files, process_sql, process_text
from medminer.ui.settings import MODEL_TABS

with gr.Blocks(
    title="MedMiner",
) as demo:
    title = gr.Markdown(
        """
        # MedMiner
        A tool for extracting information from medical text in natural langauage.
        """
    )
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## Model")
            model_settings = gr.State({})

            def set_setting(settings: dict, name: str, param: str) -> dict:
                if not name:
                    return settings

                if param:
                    settings[name] = param
                elif name in settings and settings[name]:
                    del settings[name]

                return settings

            @gr.render()
            def model_tabs() -> None:
                with gr.Tabs():
                    for tab in MODEL_TABS:
                        with gr.Tab(tab.get("name", ""), id=tab.get("id", "")):
                            if desc := tab.get("description"):
                                gr.Markdown(desc)
                            for field in tab.get("fields", []):
                                _field = gr.Textbox(**field.get("params", {}))  # type: ignore[attr-defined]
                                _field.input(
                                    set_setting,
                                    inputs=[model_settings, gr.Textbox(value=field.get("id"), visible=False), _field],  # type: ignore[attr-defined]
                                    outputs=model_settings,
                                )

            gr.Markdown("## Task")
            tasks_input = gr.CheckboxGroup(
                label="Select the task you want to perform.",
                choices=TaskType.list(),
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
