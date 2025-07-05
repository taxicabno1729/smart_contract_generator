# Ethereum Smart Contract Generator

## Overview

This is a Streamlit-based web application that **now uses Google's Gemini LLM (via the Gemini API with the Flash model)** to generate Ethereum smart contracts based on customizable parameters. The application provides an intuitive interface for creating various types of smart contracts including ERC20 tokens, ERC721 NFTs, simple storage contracts, multi-signature wallets, and voting contracts. It includes deployment guidance for using Remix IDE to deploy the generated contracts.

**Important Note:** AI-generated code, especially for smart contracts, requires thorough review and testing by qualified developers before any production use. This tool is intended as an assistant and a starting point, not a replacement for expert auditing.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - chosen for rapid prototyping and easy deployment of data/utility applications
- **UI Components**: 
  - Streamlit's native components for form inputs and layout
  - Streamlit-ace for code editor functionality
  - Two-column layout for configuration and code display
- **State Management**: Streamlit's session state for maintaining contract generator instance

### Backend Architecture
- **Core Logic**: Python-based contract generation system.
- **LLM Integration**: Uses Google's Gemini API (Flash model) for dynamic Solidity code generation.
- **Prompt Engineering**: Prompts are constructed based on user-selected parameters to guide the LLM.
- **Contract Types**: Modular approach supporting multiple contract types through a unified interface, now generated via LLM.

## Key Components

### 1. Main Application (`app.py`)
- **Purpose**: Primary Streamlit application interface.
- **Responsibilities**:
  - User interface rendering for parameter collection.
  - Secure handling of Gemini API Key (via sidebar input, environment variable, or Streamlit secrets).
  - Integration with the Gemini-based contract generation module.
  - Display of generated code and deployment guidance.
- **Key Features**:
  - Contract type selection.
  - Dynamic parameter forms.
  - Code display and copying functionality.

### 2. LLM-Based Contract Generator (`gemini_generator.py`)
- **Purpose**: Handles communication with the Google Gemini API to generate Solidity code.
- **Responsibilities**:
  - Constructs detailed prompts from user parameters.
  - Manages API calls to the specified Gemini model (e.g., `gemini-1.5-flash-latest`).
  - Parses the API response to extract the generated Solidity code.
  - Basic error handling for API interactions.
- **Supported Contracts**:
  - ERC20 Token (with mintable, burnable, pausable options)
  - ERC721 NFT
  - Simple Storage
  - Multi-Signature Wallet
  - Voting Contract
- **Features**:
  - Leverages LLM capabilities for code generation.
  - Aims for OpenZeppelin integration for standard implementations where specified in prompts.
  - Configurable Solidity versions and licenses via prompt parameters.
  - Optional code comments based on user preference.

### 3. (Legacy) Template-Based Generator (`contract_templates.py`)
- **Purpose**: Original template-based contract generation engine. (Currently not primary, but code remains).
- **Architecture Pattern**: Strategy pattern with template method.

### 4. Deployment Guide (`deployment_guide.py`)
- **Purpose**: Provides step-by-step deployment instructions.
- **Target Platform**: Remix IDE.
- **Coverage**: Complete deployment workflow from IDE setup to contract deployment.

## Data Flow (with LLM)

1. **User Input & API Key**: User selects contract type, configures parameters, and provides Gemini API Key through the Streamlit interface.
2. **Prompt Construction**: `gemini_generator.py` constructs a detailed prompt based on user inputs.
3. **API Call**: The application sends the prompt to the Google Gemini API.
4. **Code Generation**: The Gemini LLM processes the prompt and generates Solidity code.
5. **Response Handling**: The application receives the generated code.
6. **Display**: Generated code is displayed in the UI with copy functionality.
7. **Deployment Guidance**: Context-aware deployment steps are provided based on contract type.

## Setup & Running with LLM

1.  **Clone the repository.**
2.  **Install dependencies:**
    ```bash
    # Create and activate a virtual environment (recommended)
    python -m venv venv
    source venv/bin/activate # On Windows: venv\Scripts\activate

    # Install dependencies using uv (or pip)
    uv pip install -r requirements.txt
    # or uv pip install -e . if pyproject.toml is fully configured for editable install
    ```
3.  **Set up Gemini API Key:**
    *   Obtain an API key from [Google AI Studio](https://aistudio.google.com/).
    *   You can provide the API key in one of three ways:
        *   **Environment Variable (recommended for local development):**
            Set an environment variable named `GEMINI_API_KEY`.
            ```bash
            export GEMINI_API_KEY="YOUR_API_KEY_HERE"
            ```
            (On Windows, use `set GEMINI_API_KEY="YOUR_API_KEY_HERE"`)
        *   **Streamlit Secrets (recommended for deployment on Streamlit Cloud):**
            If deploying to Streamlit Cloud, add your API key as a secret named `GEMINI_API_KEY` in your application's settings.
        *   **Manual Input in App:**
            The application will prompt you to enter the API key in the sidebar if it's not found via the other methods.
4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

## External Dependencies

### Python Libraries
- **Streamlit**: Web application framework.
- **streamlit-ace**: Code editor component.
- **pyperclip**: Clipboard integration for code copying.
- **google-generativeai**: Python SDK for Google Gemini API.

### Smart Contract Dependencies
- **OpenZeppelin Contracts**: Standard, audited contract implementations
  - ERC20 standard implementation
  - ERC721 standard implementation
  - Access control (Ownable)
  - Security features (Pausable, extensions)

### Development Tools
- **Remix IDE**: Primary deployment target
- **Solidity Compiler**: Version-flexible compilation support

## Deployment Strategy

### Application Deployment
- **Platform**: Suitable for deployment on Streamlit Cloud, Heroku, or similar Python hosting platforms
- **Requirements**: Python 3.7+ with pip dependencies
- **Configuration**: Streamlit page configuration for wide layout and branding

### Smart Contract Deployment
- **Primary Tool**: Remix IDE (web-based, no local installation required)
- **Supported Networks**: Any Ethereum-compatible network supported by Remix
- **Deployment Flow**: 
  1. Code generation in app
  2. Manual copy to Remix IDE
  3. Compilation and deployment through Remix interface

## Changelog

- July 05, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.