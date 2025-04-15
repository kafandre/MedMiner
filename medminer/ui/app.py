import gradio as gr

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
            input_text = gr.Markdown("## Input")

            with gr.Tab("Files"):
                files_tab_text = gr.Markdown("Upload a file to extract information from it.")
                files_input = gr.File(
                    label="Upload a files", file_types=[".txt", ".csv", ".json"], file_count="multiple"
                )
                process_files_btn = gr.Button("Process Files")

            with gr.Tab("SQL"):
                sql_tab_text = gr.Markdown("Enter a SQL query to extract information from a database.")
                sql_input = gr.Textbox(label="SQL Query", placeholder="SELECT patient_id, text FROM patient_notes")
                process_sql_btn = gr.Button("Process SQL")

            with gr.Tab("Text"):
                text_tab_text = gr.Markdown("Enter a text to extract information from it.")
                text_input = gr.Textbox(label="Text", placeholder="Enter text here", lines=5)
                process_text_btn = gr.Button("Process Text")

        with gr.Column(scale=1):
            output_text = gr.Markdown("## Output")


demo.launch()
