## Environment Variables

This project uses `.env` files for setting environment variables during development. Follow these steps to configure your `.env` file:

1. Copy `.env.example` to `.env` in the project root.
2. Update the `.env` file with your settings for `USERNAME` and `PASSWORD`.

Never commit the `.env` file to the repository.



# Aquarius DMS Interaction Scripts

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A collection of Python scripts to interact with Aquarius DMS via the Aquarius Web API and local database configurations.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- Retrieve data from Aquarius DMS via Web API
- Manipulate and analyze data locally
- Insert modified data back into Aquarius DMS
- Utilize local database configurations for advanced queries

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

1. **Clone the Repository**: 

    ```bash
    git clone https://github.com/YOUR_USERNAME/aquarius-dms-scripts.git
    ```

2. **Navigate to the project directory and create a virtual environment**:

    ```bash
    cd aquarius-dms-scripts
    python -m venv venv
    ```

    Activate the virtual environment:

    ```bash
    source venv/bin/activate  # For Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

    Each processor under `service/` also provides its own minimal requirements
    file if you only need a subset of the features.  For example:

    ```bash
    pip install -r service/requirements_pdf.txt      # PDF importer only
    pip install -r service/requirements_csv.txt      # CSV importer only
    pip install -r service/requirements_ocr.txt      # OCR processing only
    pip install -r service/requirements_docid.txt    # Barcode DocID importer
    pip install -r service/requirements_fulltext.txt # Full text indexing
    ```

    On Windows machines install the [Tesseract OCR engine](https://github.com/UB-Mannheim/tesseract/wiki)
    if you plan to use OCR. Some packages such as `opencv-python` may require the
    Microsoft Visual C++ Redistributable. After installing the Python packages
    you may need to run `pywin32_postinstall.py -install` from the `Scripts`
    folder of your virtual environment.

4. **Environment Variables**:

    Copy `.env.example` to `.env` and fill in the required variables:

    ```bash
    cp .env.example .env
    ```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For bugs, features, and questions, feel free to open an issue or contact the maintainer at sid@aquariusimaging.net