## IMPORTANT ##

Before you begin, make sure to create a `.env` file in your project root. Copy the contents of `.env.example` into your `.env` file and configure the variables accordingly.
Important: Never commit the .env file. It is included in .gitignore to prevent accidental commits.


# Contributing to Aquarius DMS Interaction Scripts

Thank you for your interest in contributing to this project! This document outlines the guidelines and best practices for contributing.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Local Development Setup](#local-development-setup)
- [Branching Strategy](#branching-strategy)
- [Code Style](#code-style)
- [Testing](#testing)
- [Commit Guidelines](#commit-guidelines)
- [Pull Requests](#pull-requests)
- [Contact](#contact)

## Prerequisites

- Python 3.x
- `pip` for package management

## Getting Started

1. **Fork the Repository**: Create your own fork of this repository by clicking the "Fork" button at the top right corner of the repository page on GitHub.
2. **Clone the Fork**: After forking, clone your fork locally by running `git clone https://github.com/YOUR_USERNAME/aquarius-dms-scripts.git`.
3. **Add Upstream Remote**: To keep your fork in sync with the original repository, add it as a remote:

    ```bash
    git remote add upstream https://github.com/ORIGINAL_OWNER/aquarius-dms-scripts.git
    ```

## Local Development Setup

### Virtual Environment Setup

We recommend setting up a virtual environment for isolating dependencies:


python -m venv venv
source venv/bin/activate  # For Windows, use `venv\Scripts\activate`


### Installing Dependencies
Install project dependencies by running:

pip install -r requirements.txt


###  Environment Variables
This project uses a .env file to manage environment variables. Make sure to create one based on the .env.example provided:

Copy .env.example to .env in the project root:

cp .env.example .env

Open .env and fill in the variables for Aquarius DMS, such as AQUARIUS_USERNAME and AQUARIUS_PASSWORD.

Important: Never commit the .env file. It is included in .gitignore to prevent accidental commits.

### Branching Strategy
For adding new features or fixing bugs, create a new branch from main. Name the branch according to the feature or bug you are working on:

git checkout -b feature/your-feature-name

### Code Style
We follow the PEP 8 style guide for Python. You can use tools like flake8 for linting.

### Testing
Before submitting a pull request, make sure your changes pass any existing tests and add new tests for your feature if necessary:

python -m unittest discover tests


### Commit Guidelines
Write clear, concise commit messages that describe the changes you've made. If you're fixing a bug from an issue, refer to the issue number in your commit message.

Example:

git commit -m "Add data retrieval function for Aquarius DMS, resolves #42"

### Pull Requests
Create a Pull Request: After pushing your changes to your fork, navigate to the "Pull Requests" tab of the original repository and create a new pull request.
Describe Your Changes: In the pull request description, explain your changes and how they improve the project.
Code Review: Address any comments the maintainers or contributors may have.
Merge: Once approved, your pull request will be merged.

### Contact
For any questions or concerns, please open an issue or contact the project maintainer at sid@aquariusimaging.net