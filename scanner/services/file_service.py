import pdfplumber
from docx import Document
from PIL import Image
import pytesseract

class ResumeScanner:
    def __init__(self, file_path):
        self.file_path = file_path

    def scan_resume(self):
        """Scans the resume and extracts relevant information."""
        if self.file_path.endswith(".pdf"):
            return self._scan_pdf()
        elif self.file_path.endswith(".docx"):
            return self._scan_docx()
        else:
            return {"error": "Unsupported file format. Only PDF and DOCX are supported."}

    def _scan_pdf(self):
        """Extracts data from a PDF resume."""
        report = {"file_type": "PDF"}
        try:
            with pdfplumber.open(self.file_path) as pdf:
                text = ""
                tables = []
                for page in pdf.pages:
                    text += page.extract_text()
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)
                report["text"] = text
                report["resume_length"] = len(pdf.pages)
                report["contains_images"] = self._detect_images()
                report["tables"] = len(tables) if tables else 0
                report["tables_data"] = tables
        except Exception as e:
            report["error"] = str(e)
        return report

    def _scan_docx(self):
        """Extracts data from a DOCX resume."""
        report = {"file_type": "DOCX"}
        try:
            doc = Document(self.file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            tables = []
            for table in doc.tables:
                table_data = []
                for row in table.rows:
                    row_data = [cell.text.strip() for cell in row.cells]
                    table_data.append(row_data)
                tables.append(table_data)
            
            report["text"] = text
            report["resume_length"] = len(doc.paragraphs)
            report["contains_images"] = self._detect_images()
            report["tables"] = len(tables) if tables else 0
            report["tables_data"] = tables
        except Exception as e:
            report["error"] = str(e)
        return report

    def _detect_images(self):
        """Detects if the file contains images."""
        try:
            with open(self.file_path, "rb") as f:
                if "image" in f.read(1000).decode(errors="ignore").lower():
                    return True
        except:
            pass
        return False
