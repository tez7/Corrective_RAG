from pathlib import Path


def load_pdf_files(data_folder):

    pdf_files = []

    for file_path in Path(data_folder).glob("*.pdf"):

        pdf_files.append({
            "file_path": str(file_path),
            "file_name": file_path.name
        })

    return pdf_files