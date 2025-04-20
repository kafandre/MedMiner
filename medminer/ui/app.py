import gradio as gr

from medminer.ui.api import TaskType, process_files, process_sql, process_text

try:
    from smolagents import TransformersModel

    impoted_hf_transformer = True
except ImportError:
    impoted_hf_transformer = False

try:
    from smolagents import AzureOpenAIServerModel

    imported_azure_openai = True
except ImportError:
    imported_azure_openai = False


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
            with gr.Tabs() as model_tabs:
                if impoted_hf_transformer:
                    with gr.Tab("HF Transformer", id="hf_transformer"):
                        gr.Markdown("Enter a Model name of a HuggingFace transformer.")
                        hf_model = gr.Textbox(label="Model name", placeholder="Qwen/Qwen2.5-Coder-32B-Instruct")

                if imported_azure_openai:
                    with gr.Tab("Azure OpenAI", id="azure_openai"):
                        gr.Markdown("Enter the model name, endpoint, and API key.")
                        hf_model = gr.Textbox(label="Model name", placeholder="")
                        hf_endpoint = gr.Textbox(label="Endpoint", placeholder="")
                        hf_version = gr.Textbox(label="API Version", placeholder="")
                        hf_key = gr.Textbox(label="API Key", placeholder="", type="password")

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
                    text_input = gr.Textbox(label="Text", placeholder="Enter text here", lines=25)
                    process_text_btn = gr.Button("Process Text")

        with gr.Column(scale=1):
            output_text = gr.Markdown("## Output")

            output_data = gr.Dataframe()

        process_txt_files_btn.click(process_files, inputs=[txt_files_input, tasks_input], outputs=[output_data])
        process_csv_file_btn.click(process_files, inputs=[csv_file_input, tasks_input], outputs=[output_data])
        process_sql_btn.click(process_sql, inputs=[sql_input, tasks_input], outputs=[output_data])
        process_text_btn.click(process_text, inputs=[text_input, tasks_input], outputs=[output_data])


demo.launch()
