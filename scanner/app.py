import os
from services.file_service import ResumeScanner

def main():
    # Get file input
    file_path = input("Enter the resume file path (PDF or DOCX): ").strip()
    if not os.path.exists(file_path):
        print("File does not exist. Please try again.")
        return

    # Initialize scanner
    scanner = ResumeScanner(file_path)
    report = scanner.scan_resume()

    # Print results
    print("\nResume Analysis Report:")
    for key, value in report.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
