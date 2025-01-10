import os
import zipfile
import fitz  # PyMuPDF
import docx  # For handling DOCX files
import spacy  # For natural language processing

# Load SpaCy language model
nlp = spacy.load("en_core_web_sm")


# Function to process text with SpaCy and group by headings
def process_with_spacy_grouped_by_headings(text):
    doc = nlp(text)
    sections = {}
    current_heading = "General"

    for paragraph in text.split("\n\n"):
        paragraph = paragraph.strip()

        # Check if a paragraph is likely a heading
        if paragraph.isupper() or paragraph.endswith(":") or paragraph.isdigit():
            current_heading = paragraph
            sections[current_heading] = []
        else:
            # Add content to the current heading
            if current_heading not in sections:
                sections[current_heading] = []
            sections[current_heading].append(paragraph)

    # Extract entities and tokens for each section
    for heading, content in sections.items():
        section_text = " ".join(content)
        spacy_doc = nlp(section_text)
        entities = [(ent.text, ent.label_) for ent in spacy_doc.ents]
        tokens = [token.text for token in spacy_doc]
        sections[heading] = {
            "content": content,
            "entities": entities,
            "tokens": tokens,
        }

    return sections


# Function to extract text from PDF
def extract_text_with_structure_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""


# Function to extract text from DOCX
def extract_text_with_structure_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        text = "\n".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])
        return text
    except Exception as e:
        print(f"Error processing DOCX: {e}")
        return ""


# Function to detect images in PDF
def detect_images_in_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        pages_with_images = []
        for page_num, page in enumerate(doc):
            if page.get_images(full=True):
                pages_with_images.append(page_num + 1)
        return pages_with_images
    except Exception as e:
        print(f"Error processing PDF for images: {e}")
        return []


# Function to detect images in DOCX
def detect_images_in_docx(docx_path):
    try:
        with zipfile.ZipFile(docx_path, 'r') as docx_zip:
            images = [name for name in docx_zip.namelist() if name.startswith('word/media/')]
        return images
    except Exception as e:
        print(f"Error processing DOCX for images: {e}")
        return []


# Main file processing function
def process_file(file_path):
    if file_path.endswith(".pdf"):
        # Extract text and detect images for PDF
        text = extract_text_with_structure_pdf(file_path)
        images = detect_images_in_pdf(file_path)
    elif file_path.endswith(".docx"):
        # Extract text and detect images for DOCX
        text = extract_text_with_structure_docx(file_path)
        images = detect_images_in_docx(file_path)
    else:
        print("Unsupported file format. Please provide a .pdf or .docx file.")
        return

    # Process text with SpaCy and group by headings
    if text:
        grouped_data = process_with_spacy_grouped_by_headings(text)
        # print("\nGrouped Data by Headings:")
        for heading, data in grouped_data.items():
            # print(f"\n{heading}:\n{'-' * len(heading)}")
            # print("\n".join(data["content"]))
            # print("\nEntities:")
            # for entity, label in data["entities"]:
            #     print(f"{entity} ({label})")
            print("\nTokens:")
            print(data["tokens"])

    # Print image detection results
    # if images:
    #     print("\nImages detected:")
    #     print(images)
    # else:
    #     print("\nNo images detected.")
