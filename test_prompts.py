from gemini_generator import _build_prompt

def print_prompt_for_contract(contract_type, params, description):
    print(f"\n--- Prompt for: {description} ({contract_type}) ---")
    prompt = _build_prompt(contract_type, params)
    print(prompt)
    print("--- End of Prompt ---")

if __name__ == "__main__":
    # Test ERC20
    erc20_params_basic = {
        'name': 'BasicCoin', 'symbol': 'BSC', 'decimals': 18, 'initial_supply': 1000,
        'mintable': False, 'burnable': False, 'pausable': False,
        'solidity_version': '0.8.20', 'license': 'MIT', 'include_comments': True
    }
    print_prompt_for_contract("ERC20 Token", erc20_params_basic, "Basic ERC20")

    erc20_params_full = {
        'name': 'FullFeatureCoin', 'symbol': 'FFC', 'decimals': 8, 'initial_supply': 500000,
        'mintable': True, 'burnable': True, 'pausable': True,
        'solidity_version': '0.8.19', 'license': 'GPL-3.0', 'include_comments': False
    }
    print_prompt_for_contract("ERC20 Token", erc20_params_full, "Full Feature ERC20")

    # Test ERC721
    erc721_params_simple = {
        'name': 'SimpleNFT', 'symbol': 'SNF', 'base_uri': 'ipfs://cid/', 'max_supply': 100,
        'mintable': True, 'enumerable': False,
        'solidity_version': '0.8.20', 'license': 'MIT', 'include_comments': True
    }
    print_prompt_for_contract("ERC721 NFT", erc721_params_simple, "Simple ERC721")

    erc721_params_enumerable = {
        'name': 'EnumNFT', 'symbol': 'ENF', 'base_uri': 'https://server.com/api/nft/', 'max_supply': 10000,
        'mintable': True, 'enumerable': True,
        'solidity_version': '0.8.20', 'license': 'Unlicense', 'include_comments': True
    }
    print_prompt_for_contract("ERC721 NFT", erc721_params_enumerable, "Enumerable ERC721")

    # Test Simple Storage
    storage_params_public = {
        'initial_value': 123, 'access_control': 'Public',
        'solidity_version': '0.8.18', 'license': 'MIT', 'include_comments': True
    }
    print_prompt_for_contract("Simple Storage", storage_params_public, "Public Simple Storage")

    storage_params_owner = {
        'initial_value': 0, 'access_control': 'Owner Only',
        'solidity_version': '0.8.18', 'license': 'MIT', 'include_comments': True
    }
    print_prompt_for_contract("Simple Storage", storage_params_owner, "Owner-Only Simple Storage")

    # Test Multi-Signature Wallet
    multisig_params_default_owners = {
        'required_confirmations': 2, 'owners': '', # Test default owners
        'solidity_version': '0.8.20', 'license': 'MIT', 'include_comments': True
    }
    print_prompt_for_contract("Multi-Signature Wallet", multisig_params_default_owners, "Multi-Sig Default Owners")

    multisig_params_custom_owners = {
        'required_confirmations': 3,
        'owners': '0xAlpha00000000000000000000000000000000000\n0xBeta000000000000000000000000000000000001\n0xGamma00000000000000000000000000000000002',
        'solidity_version': '0.8.20', 'license': 'MIT', 'include_comments': True
    }
    print_prompt_for_contract("Multi-Signature Wallet", multisig_params_custom_owners, "Multi-Sig Custom Owners")

    # Test Voting Contract
    voting_params_simple = {
        'voting_duration': 2880, 'require_registration': False, 'proposal_threshold': 1,
        'solidity_version': '0.8.20', 'license': 'MIT', 'include_comments': True
    }
    print_prompt_for_contract("Voting Contract", voting_params_simple, "Simple Voting Contract")

    voting_params_registration = {
        'voting_duration': 720, 'require_registration': True, 'proposal_threshold': 10,
        'solidity_version': '0.8.20', 'license': 'MIT', 'include_comments': False
    }
    print_prompt_for_contract("Voting Contract", voting_params_registration, "Voting Contract with Registration")

    print("\nPrompt generation tests complete. Review output for correctness.")
    print("Actual API calls and code validation would require running the Streamlit app and providing an API key.")
    print("Considerations for manual testing with the app:")
    print("- Does the UI correctly pass parameters to the generator?")
    print("- How does Gemini handle various combinations of features (e.g., ERC20 mintable but not pausable)?")
    print("- Is the generated code compilable in Remix/Hardhat?")
    print("- Does the generated code pass basic security checks or linters (e.g., Slither if possible)?")
    print("- Are OpenZeppelin imports correct and used appropriately by the LLM?")
    print("- Is the license, Solidity version, and comment inclusion respected?")
    print("- How robust is the error handling if the API key is invalid or the API call fails?")
