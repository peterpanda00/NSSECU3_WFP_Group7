# SQLiteParseXpert

SQLiteParseXpert is a Python tool designed to parse SQLite database files, focusing on recovering deleted records and extracting data from various page types within the SQLite database structure.

## Features

- **Parsing SQLite Files:** Parses SQLite database files (.db) to extract data from allocated and unallocated spaces.
- **Recovery of Deleted Records:** Identifies and recovers deleted records from unallocated space within the SQLite file.
- **Flexible Output Options:** Outputs parsed data either in CSV format or as raw text, depending on user preference.
- **Graphical User Interface (GUI):** Provides a user-friendly interface using Tkinter for easy file selection and output configuration.

## Requirements

- Python 3.x
- Tkinter (usually included with Python installations)

## Usage

1. **Run the Application:**
   - Launch the application using `python sqlite_parsexpert.py` in your terminal.
   - Alternatively, run the script in your IDE.

2. **Select Input File:**
   - Click on the "Browse" button next to "Input SQLite file:" to select the SQLite database file you want to parse.

3. **Select Output File:**
   - Click on the "Browse" button next to "Output file:" to choose where you want to save the parsed output (default format is CSV).

4. **Configure Options:**
   - Check "Raw output" if you want the output in raw text format.
   - Check "Print pages" to include page content in the output.

5. **Run Parser:**
   - Click "Run Parser" to start parsing the SQLite file based on your selected options.

6. **View Output:**
   - The parsing progress and results will be displayed in the text area below the GUI.

