import streamlit as st
import pyperclip
from streamlit_ace import st_ace
# from contract_templates import ContractGenerator # Keep for now, might remove later or use as fallback
from gemini_generator import generate_contract_with_gemini, DEFAULT_MODEL as GEMINI_DEFAULT_MODEL
from deployment_guide import get_deployment_steps
import hashlib
import json
import os # For API Key

# Configure page
st.set_page_config(
    page_title="Ethereum Smart Contract Generator (LLM Powered)",
    page_icon="✨",
    layout="wide"
)

# # Initialize contract generator (old template based)
# if 'contract_generator' not in st.session_state:
#     st.session_state.contract_generator = ContractGenerator()

def main():
    st.title("✨ Ethereum Smart Contract Generator (LLM Powered)")
    st.markdown("Generate Ethereum smart contracts using AI and deploy them using Remix IDE")
    st.markdown("<style>.stButton button {background-color: #4CAF50; color: white;}</style>", unsafe_allow_html=True)


    # --- Gemini API Key Input ---
    st.sidebar.header("🔑 Gemini API Key")
    gemini_api_key_env = os.environ.get("GEMINI_API_KEY")

    # Try to get from st.secrets if available (for deployed apps)
    try:
        gemini_api_key_secrets = st.secrets.get("GEMINI_API_KEY")
    except (AttributeError, FileNotFoundError): # AttributeError if st.secrets doesn't exist, FileNotFoundError for local
        gemini_api_key_secrets = None

    # Prioritize secrets, then environment variable, then user input
    if gemini_api_key_secrets:
        gemini_api_key = gemini_api_key_secrets
        st.sidebar.success("Gemini API Key loaded from secrets.")
    elif gemini_api_key_env:
        gemini_api_key = gemini_api_key_env
        st.sidebar.success("Gemini API Key loaded from environment variable.")
    else:
        gemini_api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password", help="Get your API key from Google AI Studio.")
        if gemini_api_key:
            st.sidebar.success("Gemini API Key entered.")
        else:
            st.sidebar.warning("Gemini API Key is required for contract generation.")

    # Option to choose Gemini Model
    st.sidebar.header("🤖 LLM Configuration")
    # For now, let's stick to the default, but this is where model selection could go
    gemini_model_name = st.sidebar.selectbox(
        "Select Gemini Model",
        [GEMINI_DEFAULT_MODEL, "gemini-2.5-pro", "gemini-2.5-flash"], # Add other compatible models if needed
        help="Choose the Gemini model for generation."
    )
    # gemini_model_name = GEMINI_DEFAULT_MODEL # Keep it fixed for now based on gemini_generator
    st.sidebar.caption(f"Using model: `{gemini_model_name}`")

    st.info("""
        **Welcome to the LLM-Powered Smart Contract Generator!**
        - Configure your desired contract type and parameters below.
        - Ensure your Gemini API Key is provided in the sidebar.
        - The AI will generate the Solidity code for you.
        - **Always thoroughly review and test any AI-generated smart contract code before use.**
    """)
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📋 Contract Configuration")
        
        # Contract type selection
        contract_type = st.selectbox(
            "Select Contract Type",
            ["ERC20 Token", "ERC721 NFT", "Simple Storage", "Multi-Signature Wallet", "Voting Contract"],
            help="Choose the type of smart contract you want to generate"
        )
        
        # Contract parameters based on type
        contract_params = {}
        
        if contract_type == "ERC20 Token":
            st.subheader("🪙 ERC20 Token Parameters")
            contract_params['name'] = st.text_input("Token Name", value="MyToken", help="The name of your token")
            contract_params['symbol'] = st.text_input("Token Symbol", value="MTK", help="The symbol for your token (3-5 characters)")
            contract_params['decimals'] = st.number_input("Decimals", min_value=0, max_value=18, value=18, help="Number of decimal places")
            contract_params['initial_supply'] = st.number_input("Initial Supply", min_value=1, value=1000000, help="Initial token supply")
            contract_params['mintable'] = st.checkbox("Mintable", help="Allow minting new tokens")
            contract_params['burnable'] = st.checkbox("Burnable", help="Allow burning tokens")
            contract_params['pausable'] = st.checkbox("Pausable", help="Allow pausing token transfers")
            
        elif contract_type == "ERC721 NFT":
            st.subheader("🎨 ERC721 NFT Parameters")
            contract_params['name'] = st.text_input("NFT Collection Name", value="MyNFT", help="The name of your NFT collection")
            contract_params['symbol'] = st.text_input("NFT Symbol", value="MNFT", help="The symbol for your NFT collection")
            contract_params['base_uri'] = st.text_input("Base URI", value="https://api.example.com/metadata/", help="Base URI for metadata")
            contract_params['max_supply'] = st.number_input("Max Supply", min_value=1, value=10000, help="Maximum number of NFTs")
            contract_params['mintable'] = st.checkbox("Owner Mintable", value=True, help="Allow owner to mint NFTs")
            contract_params['enumerable'] = st.checkbox("Enumerable", help="Make NFTs enumerable")
            
        elif contract_type == "Simple Storage":
            st.subheader("💾 Simple Storage Parameters")
            contract_params['initial_value'] = st.number_input("Initial Value", value=0, help="Initial stored value")
            contract_params['access_control'] = st.selectbox("Access Control", ["Public", "Owner Only"], help="Who can modify the stored value")
            
        elif contract_type == "Multi-Signature Wallet":
            st.subheader("🔐 Multi-Signature Wallet Parameters")
            contract_params['required_confirmations'] = st.number_input("Required Confirmations", min_value=1, max_value=10, value=2, help="Number of confirmations required")
            contract_params['owners'] = st.text_area("Owner Addresses (one per line)", help="Enter Ethereum addresses of wallet owners")
            
        elif contract_type == "Voting Contract":
            st.subheader("🗳️ Voting Contract Parameters")
            contract_params['voting_duration'] = st.number_input("Voting Duration (minutes)", min_value=1, value=1440, help="Duration of voting period in minutes")
            contract_params['require_registration'] = st.checkbox("Require Voter Registration", help="Require voters to be registered")
            contract_params['proposal_threshold'] = st.number_input("Proposal Threshold", min_value=0, value=1, help="Minimum tokens required to create proposal")
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            contract_params['solidity_version'] = st.selectbox(
                "Solidity Version",
                ["0.8.20", "0.8.19", "0.8.18", "0.8.17"],
                help="Choose Solidity compiler version"
            )
            contract_params['license'] = st.selectbox(
                "License",
                ["MIT", "GPL-3.0", "Apache-2.0", "BSD-3-Clause", "Unlicense"],
                help="Choose license for your contract"
            )
            contract_params['include_comments'] = st.checkbox("Include Comments", value=True, help="Include explanatory comments in code")

        # --- Create Contract Button ---
        if 'contract_created' not in st.session_state:
            st.session_state.contract_created = False
        # Reset contract_created if contract_type or params change
        if 'last_contract_type' not in st.session_state or st.session_state.last_contract_type != contract_type:
            st.session_state.contract_created = False
        st.session_state.last_contract_type = contract_type
        # Hash params to detect changes
        params_hash = hashlib.md5(json.dumps(contract_params, sort_keys=True, default=str).encode()).hexdigest()
        if 'last_params_hash' not in st.session_state or st.session_state.last_params_hash != params_hash:
            st.session_state.contract_created = False
        st.session_state.last_params_hash = params_hash
        # Button
        if st.button("🚀 Create Contract", key="create_contract_btn"):
            st.session_state.contract_created = True
    
    with col2:
        st.header("📜 Generated Contract")
        if st.session_state.get('contract_created', False):
            if not gemini_api_key:
                st.error("🚨 Gemini API Key is missing. Please provide it in the sidebar to generate the contract.")
            else:
                # Generate contract code using Gemini
                try:
                    with st.spinner(f"🤖 Calling Gemini to generate {contract_type}... This may take a moment."):
                        contract_code = generate_contract_with_gemini(contract_type, contract_params, gemini_api_key, gemini_model_name)
                    
                    st.success(f"🎉 Successfully generated {contract_type} code with Gemini!")
                    # Display code with syntax highlighting
                    st_ace(
                        value=contract_code,
                        language='solidity',
                        theme='monokai',
                        height=400,
                        auto_update=True,
                        readonly=True,
                        key="contract_code"
                    )
                    # Copy to clipboard button
                    if st.button("📋 Copy to Clipboard", help="Copy the generated contract code"):
                        try:
                            pyperclip.copy(contract_code)
                            st.success("Contract code copied to clipboard!")
                        except Exception as e: # Changed from broad except to Exception as e
                            st.error(f"Unable to copy to clipboard. Please select and copy the code manually. Error: {e}")
                    # Download button
                    st.download_button(
                        label="💾 Download Contract",
                        data=contract_code,
                        file_name=f"{contract_params.get('name', 'contract').replace(' ', '_')}.sol",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error generating contract: {str(e)}")
                    st.info("Please check your input parameters, API key, and try again.")
        else:
            st.info("Fill in the contract parameters and click 'Create Contract' to generate your smart contract code.")
    
    # Deployment instructions
    st.markdown("---")
    st.header("🚀 Deployment Instructions")
    
    deployment_steps = get_deployment_steps(contract_type)
    
    for i, step in enumerate(deployment_steps, 1):
        with st.expander(f"Step {i}: {step['title']}"):
            st.markdown(step['description'])
            if 'code' in step:
                st.code(step['code'], language=step.get('language', 'javascript'))
            if 'warning' in step:
                st.warning(step['warning'])
            if 'info' in step:
                st.info(step['info'])
    
    # Additional resources
    st.markdown("---")
    st.header("📚 Additional Resources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🛠️ Development Tools**
        - [Remix IDE](https://remix.ethereum.org)
        - [Hardhat](https://hardhat.org)
        - [Truffle](https://trufflesuite.com)
        """)
    
    with col2:
        st.markdown("""
        **📖 Documentation**
        - [Solidity Docs](https://docs.soliditylang.org)
        - [OpenZeppelin](https://docs.openzeppelin.com)
        - [Ethereum.org](https://ethereum.org/developers)
        """)
    
    with col3:
        st.markdown("""
        **🔍 Testing Networks**
        - [Sepolia Testnet](https://sepolia.etherscan.io)
        - [Goerli Testnet](https://goerli.etherscan.io)
        - [Ganache](https://trufflesuite.com/ganache)
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit | ⚠️ **Always audit your contracts before mainnet deployment**")

if __name__ == "__main__":
    main()
