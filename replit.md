# Ethereum Smart Contract Generator

## Overview

This is a Streamlit-based web application that generates Ethereum smart contracts with customizable parameters. The application provides an intuitive interface for creating various types of smart contracts including ERC20 tokens, ERC721 NFTs, simple storage contracts, multi-signature wallets, and voting contracts. It includes deployment guidance for using Remix IDE to deploy the generated contracts.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - chosen for rapid prototyping and easy deployment of data/utility applications
- **UI Components**: 
  - Streamlit's native components for form inputs and layout
  - Streamlit-ace for code editor functionality
  - Two-column layout for configuration and code display
- **State Management**: Streamlit's session state for maintaining contract generator instance

### Backend Architecture
- **Core Logic**: Python-based contract generation system
- **Template Engine**: Class-based template system with method dispatch pattern
- **Contract Types**: Modular approach supporting multiple contract types through a unified interface

## Key Components

### 1. Main Application (`app.py`)
- **Purpose**: Primary Streamlit application interface
- **Responsibilities**:
  - User interface rendering
  - Parameter collection for different contract types
  - Integration with contract generation and deployment guidance
- **Key Features**:
  - Contract type selection
  - Dynamic parameter forms based on contract type
  - Code display and copying functionality

### 2. Contract Generator (`contract_templates.py`)
- **Purpose**: Core contract generation engine
- **Architecture Pattern**: Strategy pattern with template method
- **Supported Contracts**:
  - ERC20 Token (with mintable, burnable, pausable options)
  - ERC721 NFT
  - Simple Storage
  - Multi-Signature Wallet
  - Voting Contract
- **Features**:
  - OpenZeppelin integration for standard implementations
  - Configurable Solidity versions and licenses
  - Optional code comments

### 3. Deployment Guide (`deployment_guide.py`)
- **Purpose**: Provides step-by-step deployment instructions
- **Target Platform**: Remix IDE
- **Coverage**: Complete deployment workflow from IDE setup to contract deployment

## Data Flow

1. **User Input**: User selects contract type and configures parameters through Streamlit interface
2. **Contract Generation**: Parameters are passed to ContractGenerator which uses appropriate template method
3. **Code Generation**: Template method generates Solidity code with proper imports and inheritance
4. **Display**: Generated code is displayed in the UI with copy functionality
5. **Deployment Guidance**: Context-aware deployment steps are provided based on contract type

## External Dependencies

### Python Libraries
- **Streamlit**: Web application framework
- **streamlit-ace**: Code editor component
- **pyperclip**: Clipboard integration for code copying

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