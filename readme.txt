# Creating an executable from the source files.
# ---------------------------------------------------------------------------------------------------------------------
# Install PyInstaller
# pip install pyinstaller

# Go into the ".py" file directory.
# cd <path to .py file>

# Run the PyInstaller command.

    # If project is in a virtual environment (to get required packages):
    # pyinstaller --onefile --paths <path prefix>\venv\Lib\site-packages <file name>.py

    # If not in virtual ennvironment:
    # pyinstaller --onefile <file name>.py

# The <file name>.exe file will be located in <path to .py file>\dist