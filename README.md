# Automated Tests for ClickUp Tasks Module

## 📝 Project Description

This repository contains a comprehensive suite of automated tests for the **Tasks module** of the **ClickUp service** ([https://clickup.com/](https://clickup.com/)). The test suite includes both **UI (User Interface)** tests, driven by Playwright, and **API (Application Programming Interface)** tests, utilizing the `requests` library and `Pydantic` for data validation.

The tests are developed in **Python** using the **Pytest** testing framework, with **Allure Reports** providing detailed and interactive test reporting.

The primary goal of this project is to ensure the robust functionality and stability of task management within ClickUp, covering various user workflows and API interactions.

## 🚀 Requirements

To successfully run these automated tests on your local machine, please ensure you have the following tools installed:

  * **Python 3.9+** (latest stable version is recommended)
  * **Git** (for cloning the repository)
  * **Node.js** and **npm** (required for Playwright Browser Drivers installation; Playwright CLI usually handles this, but Node.js is necessary)
  * **Allure Commandline** (for generating and viewing Allure Reports)

-----

## 🛠️ Installation and Setup (using `uv`)

Follow these step-by-step instructions to prepare your environment and install the necessary dependencies using `uv`.

### 1\. Clone the Repository

Open your terminal or command prompt and execute the following command:

```bash
git clone https://github.com/kyryl01011/clickup_tests.git
cd clickup_tests
```

### 2\. Install `uv` (if not already installed)

`uv` is a fast Python package installer and resolver, which replaces `pip` and `venv`.
To install `uv` globally, use the standalone installer:

  * **For macOS / Linux:**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
  * **For Windows:** Refer to the official `uv` documentation for installation instructions (e.g., using `pipx install uv` or downloading a standalone executable).

### 3\. Create Virtual Environment and Install Python Dependencies with `uv`

`uv` will automatically create a virtual environment (if one doesn't exist) and install all dependencies defined in your `pyproject.toml` (and locked in `uv.lock`) into it.

```bash
uv sync
```

This command will:

  * Create a virtual environment (by default in `.venv`).
  * Read the `uv.lock` file to ensure exact dependency versions are installed.
  * Install all required Python libraries into the environment.

### 4\. Activate the Virtual Environment (Optional, for direct usage in terminal)

While `uv` allows running commands directly (e.g., `uv run pytest`), you might want to activate the environment for general terminal use.

  * **For macOS / Linux:**
    ```bash
    source .venv/bin/activate
    ```
  * \*\*For Windows (PowerShell):
    ```powershell
    .venv\Scripts\Activate.ps1
    ```
  * \*\*For Windows (Command Prompt / CMD):
    ```cmd
    .venv\Scripts\activate.bat
    ```

### 5\. Install Playwright Browser Drivers

Playwright needs to download and install browser drivers for Chromium, Firefox, and WebKit to execute UI tests.

```bash
uv run playwright install
```

*(Note: We use `uv run` here to ensure Playwright uses the Python environment managed by `uv`.)*

### 6\. Install Allure Commandline

To generate and view Allure Reports, you will need the Allure Commandline tool.

  * **macOS (using Homebrew):**
    ```bash
    brew install allure
    ```
  * **Windows (using Chocolatey):**
    ```bash
    choco install allure
    ```
  * **Linux:** Detailed instructions for various distributions can be found in the official Allure documentation.

### 7\. Configure Environment Variables

This project uses environment variables to store sensitive information (like API tokens) and configurable parameters.

1.  **Create a `.env` file:** Copy the provided `env-copy` file and rename it to `.env` in the root directory of the project.
    ```bash
    cp env-copy .env
    ```
    *(For Windows CMD, use `copy env-copy .env`)*
2.  **Edit the `.env` file:** Open the newly created `.env` file and fill in your specific credentials or configuration details according to the template provided inside.
      * **Crucially, you will need to obtain a ClickUp API Token.** Refer to the ClickUp API documentation for instructions on how to generate one.

## 🚀 Running Tests

Once the installation and setup are complete, you are ready to run the tests.
Use `uv run` to execute Pytest commands within the virtual environment without needing to activate it manually.

### Run All Tests (UI and API) and Generate Allure Report

This command will execute all tests (both UI and API) discovered by Pytest and save the Allure results to the `allure-results/` directory.

```bash
uv run pytest --alluredir=allure-results
```

### Running Specific Test Types (Optional)

You can use Pytest markers to run specific subsets of tests, if they are defined in your `pytest.ini` (e.g., `@pytest.mark.api`, `@pytest.mark.ui`).

  * **Run only API tests:**
    ```bash
    uv run pytest -m api --alluredir=allure-results
    ```
  * **Run only UI tests:**
    ```bash
    uv run pytest -m ui --alluredir=allure-results
    ```
  * **Run tests in headless UI mode (without opening browser UI):**
    ```bash
    uv run pytest --headed=false
    ```
    *(Note: Playwright tests run in headless mode by default unless configured otherwise. You might need to adjust your `playwright.config.js` or command-line options for headed runs.)*

## 📊 Viewing Allure Reports

After successfully running the tests with `--alluredir` and saving the results, you can generate and view the interactive Allure report.

### 1\. Generate the Report

This command takes the collected test results from `allure-results/`, generates the HTML report, and saves it to the `allure-report/` directory.

```bash
allure generate allure-results --clean -o allure-report
```

  * `--clean`: Deletes previous report data before generating a new one.
  * `-o allure-report`: Specifies the output directory for the generated report.

### 2\. Open the Report in Your Browser

Once the report is generated, you can open it in your default web browser:

```bash
allure open allure-report
```

## 📚 ClickUp API Documentation

For a detailed understanding of the API functionality tested by this project, you can refer to the official ClickUp API documentation:
[https://developer.clickup.com/reference/](https://developer.clickup.com/reference/)