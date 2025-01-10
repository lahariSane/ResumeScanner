from services.file_service import process_file

def main():
    # Example file path (you can replace this with the actual path you want to test)
    file_path = "resumes/Resume.pdf"  # Replace with the path to your DOCX or PDF file

    # Process the file and print results
    process_file(file_path)

if __name__ == "__main__":
    main()
