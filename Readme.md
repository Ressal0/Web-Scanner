# WebsiteScanner

WebsiteScanner is a Python application with a graphical user interface that allows users to perform Nmap and SQLMap scans on specified websites. It provides an easy-to-use interface for running these security scanning tools and viewing their results.

## Features

- Scan multiple websites simultaneously
- Choose between Nmap scan, SQLMap scan, or both
- User-friendly graphical interface built with Kivy
- Ability to cancel ongoing scans
- Real-time display of scan results
- Threaded scanning to keep the UI responsive

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher
- Kivy library
- Nmap
- SQLMap

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/WebsiteScanner.git
   ```

2. Navigate to the project directory:
   ```
   cd WebsiteScanner
   ```

3. Install the required Python packages:
   ```
   pip install kivy
   ```

4. Ensure Nmap and SQLMap are installed on your system and accessible from the command line.

## Usage

To run the WebsiteScanner:

1. Navigate to the project directory in your terminal.

2. Run the following command:
   ```
   python websitescanner.py
   ```

3. In the application window:
   - Enter the websites you want to scan in the input field, separated by spaces.
   - Select the type of scan you want to perform (Nmap, SQLMap, or Both).
   - Click the "Scan" button to start the scan.
   - The results will be displayed in the output field as they become available.
   - You can cancel the scan at any time by clicking the "Cancel" button.

## Warning

Please ensure you have permission to scan any websites you do not own. Unauthorized scanning may be illegal and unethical.

## Contributing

Contributions to the WebsiteScanner project are welcome. Please adhere to the following steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## Authors

- Abdellah Ressal
- Bouslam Elmehdi (https://github.com/Mido-Hyuga)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
