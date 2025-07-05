import google.generativeai as genai
import logging
import os # Added for example usage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default model to use
DEFAULT_MODEL = "gemini-1.5-flash-latest"

def generate_contract_with_gemini(contract_type: str, params: dict, api_key: str, model_name: str = DEFAULT_MODEL) -> str:
    """
    Generates a Solidity smart contract using the Gemini API.

    Args:
        contract_type: The type of contract (e.g., "ERC20 Token", "ERC721 NFT").
        params: A dictionary of parameters for the contract.
        api_key: The Gemini API key.
        model_name: The specific Gemini model to use.

    Returns:
        A string containing the generated Solidity code.

    Raises:
        ValueError: If the API key is missing or if contract generation fails.
        Exception: For other API-related errors.
    """
    if not api_key:
        logger.error("Gemini API key is missing.")
        raise ValueError("Gemini API key is missing.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    prompt = _build_prompt(contract_type, params)
    logger.info(f"Generated prompt for Gemini (first 100 chars): {prompt[:100]}...")

    try:
        generation_config = genai.types.GenerationConfig(
            candidate_count=1,
            temperature=0.2,
        )
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        response = model.generate_content(
            prompt,
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        if not response.candidates:
            logger.error("Gemini API returned no candidates. Response: %s", response)
            block_reason_message = "Unknown reason"
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
                 block_reason_message = response.prompt_feedback.block_reason_message or str(response.prompt_feedback.block_reason)
            raise ValueError(f"Contract generation failed. Prompt may have been blocked. Reason: {block_reason_message}")

        generated_text = response.text

        # Clean up markdown
        if generated_text.strip().lower().startswith("```solidity"):
            generated_text = generated_text.splitlines()[1:] # Remove first line
            if generated_text and generated_text[-1].strip() == "```":
                generated_text = generated_text[:-1] # Remove last line
            generated_text = "\n".join(generated_text)
        elif generated_text.strip().startswith("```"):
            generated_text = generated_text.splitlines()[1:]
            if generated_text and generated_text[-1].strip() == "```":
                generated_text = generated_text[:-1]
            generated_text = "\n".join(generated_text)

        logger.info("Successfully generated contract code.")
        return generated_text.strip()

    except Exception as e:
        logger.error(f"Error generating contract with Gemini: {e}")
        # Attempt to get more detailed error if prompt was blocked
        if "prompt_feedback" in str(e).lower() and "block_reason" in str(e).lower():
             # This is a basic check; more specific parsing might be needed depending on SDK's error structure
            raise ValueError(f"Contract generation likely failed due to prompt blocking: {e}")
        raise

def _build_prompt(contract_type: str, params: dict) -> str:
    solidity_version = params.get('solidity_version', '0.8.20')
    license_type = params.get('license', 'MIT')
    include_comments = params.get('include_comments', True)

    prompt_lines = [
        "You are an expert Solidity smart contract developer.",
        "Generate a complete Solidity smart contract based on the following specifications.",
        "The contract should be secure, well-structured, and ready for compilation.",
        "Code shouldn;t have this error",
        """
        "MyToken" hit an invalid opcode while deploying. Try:
        * Verifying that your constructor params satisfy all assert conditions.
        * Verifying your constructor code doesn't access an array out of bounds.
        * Adding reason strings to your assert statements.
        """,
        f"Solidity version: ^{solidity_version}",
        f"SPDX License Identifier: {license_type}",
        f"Include comments: {'Yes' if include_comments else 'No'}",
        f"Contract Type: {contract_type}",
    ]

    if contract_type == "ERC20 Token":
        prompt_lines.extend([
            f"Token Name: {params.get('name', 'MyToken')}",
            f"Token Symbol: {params.get('symbol', 'MTK')}",
            f"Decimals: {params.get('decimals', 18)}",
            f"Initial Supply: {params.get('initial_supply', 1000000)} (this is the human-readable amount, adjust for decimals in the constructor, e.g. initialSupply * (10**decimals))",
            f"Mintable: {'Yes' if params.get('mintable', False) else 'No'}",
            f"Burnable: {'Yes' if params.get('burnable', False) else 'No'}",
            f"Pausable: {'Yes' if params.get('pausable', False) else 'No'}",
            "If mintable or pausable, ensure it uses OpenZeppelin's Ownable (or Ownable2Step) for access control, and the deployer is the initial owner.",
            "Use OpenZeppelin contracts for standard implementations (e.g., ERC20.sol, ERC20Burnable.sol, ERC20Pausable.sol, Ownable.sol). Specify correct import paths like '@openzeppelin/contracts/token/ERC20/ERC20.sol'."
        ])
    elif contract_type == "ERC721 NFT":
        prompt_lines.extend([
            f"NFT Collection Name: {params.get('name', 'MyNFT')}",
            f"NFT Symbol: {params.get('symbol', 'MNFT')}",
            f"Base URI for metadata: {params.get('base_uri', 'https://api.example.com/metadata/')}",
            f"Max Supply: {params.get('max_supply', 10000)}",
            f"Owner Mintable: {'Yes' if params.get('mintable', True) else 'No'}",
            f"Enumerable: {'Yes' if params.get('enumerable', False) else 'No'}",
            "If Owner Mintable, ensure it uses OpenZeppelin's Ownable (or Ownable2Step) for access control, and the deployer is the initial owner.",
            "The mint function should take 'address to' as a parameter and return the tokenId.",
            "Include a totalSupply function that returns the number of NFTs minted so far (e.g., using OpenZeppelin's Counters.Counter).",
            "Include a setBaseURI function, callable only by the owner, to update the base URI.",
            "Use OpenZeppelin contracts for standard implementations (e.g., ERC721.sol, ERC721Enumerable.sol, Ownable.sol, Counters.sol). Specify correct import paths."
        ])
    elif contract_type == "Simple Storage":
        prompt_lines.extend([
            f"Initial Stored Value: {params.get('initial_value', 0)}",
            f"Access Control for modification functions (setValue, increment, decrement): {params.get('access_control', 'Public')}",
            "If 'Owner Only' access control, use OpenZeppelin's Ownable (or Ownable2Step) and make the deployer the initial owner.",
            "Include functions: setValue(uint256 value), getValue() returns (uint256), increment(), decrement().",
            "The decrement function should prevent underflow (e.g., require storedValue > 0).",
            "Emit an event 'ValueUpdated(uint256 oldValue, uint256 newValue, address updatedBy)' when value changes via setValue, increment, or decrement."
        ])
    elif contract_type == "Multi-Signature Wallet":
        owners_text = params.get('owners', '')
        owners_list = [addr.strip() for addr in owners_text.split('\n') if addr.strip()]
        if not owners_list:
            owners_list = ["0x1234567890123456789012345678901234567890", "0x2345678901234567890123456789012345678901"]

        prompt_lines.extend([
            f"Required Confirmations: {params.get('required_confirmations', 2)}",
            f"Owner Addresses: {', '.join(owners_list)}",
            "Implement core multi-sig functionality: submitTransaction(address to, uint256 value, bytes calldata data), confirmTransaction(uint txId), executeTransaction(uint txId), revokeConfirmation(uint txId).",
            "Store transactions (to, value, data, executed status, confirmation count) and their confirmation status per owner.",
            "Owners should be set in the constructor. Validate owner addresses (not zero address, unique) and required confirmations ( > 0 and <= number of owners).",
            "Include a receive() external payable function to accept Ether deposits.",
            "This contract does not need to use OpenZeppelin Ownable, as owner management is its core logic."
        ])
    elif contract_type == "Voting Contract":
        prompt_lines.extend([
            f"Voting Duration (minutes): {params.get('voting_duration', 1440)} (convert this to seconds for internal use, e.g., block.timestamp + (duration_minutes * 60))",
            f"Require Voter Registration: {'Yes' if params.get('require_registration', False) else 'No'}",
            # f"Proposal Threshold: {params.get('proposal_threshold', 1)} (For now, assume any authorized user can propose).",
            "If voter registration is required, include functions for `registerVoter(address voter)` (owner-only) and `unregisterVoter(address voter)` (owner-only). Use OpenZeppelin Ownable for these admin functions.",
            "Allow creating proposals with a description: `createProposal(string memory description)`. If registration is required, only registered voters can create proposals. Otherwise, anyone can.",
            "Allow voting on proposals: `vote(uint256 proposalId)`. If registration is required, only registered voters can vote.",
            "Track proposal details (ID, description, vote count, voting start time, voting end time, executed status).",
            "Prevent double voting on the same proposal.",
            "A proposal is considered passed if it has more 'yes' votes (simple majority, for now, we are just counting total votes).",
            "Include a function `getProposal(uint256 proposalId)` to view proposal details.",
            "Include an event `ProposalCreated(uint256 proposalId, address proposer, string description, uint256 endTime)`.",
            "Include an event `Voted(uint256 proposalId, address voter)`."
        ])
    else:
        prompt_lines.append(f"Parameters for {contract_type}: {params}")

    prompt_lines.extend([
        "Ensure the contract uses appropriate error handling (require statements with clear messages).",
        "Follow Solidity best practices for security and gas efficiency where possible.",
        "Provide ONLY the Solidity code as a single block, without any surrounding text, conversation, or markdown formatting like ```solidity ... ``` or ``` ... ```."
    ])

    return "\n".join(prompt_lines)

if __name__ == '__main__':
    # Example usage (for testing this module directly)
    # You would need to set your GEMINI_API_KEY as an environment variable
    # For local testing, consider creating a .env file with:
    # GEMINI_API_KEY="YOUR_ACTUAL_API_KEY"

    # Attempt to load .env if python-dotenv is installed
    try:
        from dotenv import load_dotenv
        load_dotenv()
        logger.info(".env loaded if present.")
    except ImportError:
        logger.info("python-dotenv not installed, .env file will not be loaded automatically.")
        pass # python-dotenv not installed

    test_api_key = os.environ.get("GEMINI_API_KEY")

    if not test_api_key:
        print("Please set the GEMINI_API_KEY environment variable for testing this script's API call functionality.")
        print("Example: export GEMINI_API_KEY='your_key_here'")
        print("\nSkipping actual API calls. To test API calls, set the key and re-run.")
    else:
        print(f"Using API Key: {test_api_key[:5]}...{test_api_key[-5:]}")

        # Test ERC20
        erc20_params = {
            'name': 'Test Gemini Token', 'symbol': 'TGT', 'decimals': 18,
            'initial_supply': 1000000, 'mintable': True, 'burnable': True, 'pausable': True,
            'solidity_version': '0.8.20', 'license': 'MIT', 'include_comments': True
        }
        try:
            print("\n--- Testing ERC20 Generation (API Call) ---")
            erc20_code = generate_contract_with_gemini("ERC20 Token", erc20_params, test_api_key)
            print("Generated ERC20 Code (first 200 chars):")
            print(erc20_code[:200] + "...")
        except Exception as e:
            print(f"Error generating ERC20: {e}")

        # Test ERC721
        erc721_params = {
            'name': 'Test Gemini NFT', 'symbol': 'TGN', 'base_uri': 'https://myapi.com/nft/',
            'max_supply': 5000, 'mintable': True, 'enumerable': True,
            'solidity_version': '0.8.20', 'license': 'MIT', 'include_comments': True
        }
        try:
            print("\n--- Testing ERC721 Generation (API Call) ---")
            erc721_code = generate_contract_with_gemini("ERC721 NFT", erc721_params, test_api_key)
            print("Generated ERC721 Code (first 200 chars):")
            print(erc721_code[:200] + "...")
        except Exception as e:
            print(f"Error generating ERC721: {e}")

        # Test Simple Storage
        storage_params = {
            'initial_value': 42, 'access_control': 'Owner Only',
            'solidity_version': '0.8.19', 'license': 'GPL-3.0', 'include_comments': False
        }
        try:
            print("\n--- Testing Simple Storage Generation (API Call) ---")
            storage_code = generate_contract_with_gemini("Simple Storage", storage_params, test_api_key)
            print("Generated Simple Storage Code (first 200 chars):")
            print(storage_code[:200] + "...")
        except Exception as e:
            print(f"Error generating Simple Storage: {e}")

    print("\n--- End of gemini_generator.py direct execution ---")
# Ensure there's a newline at the end of the file if necessary by some linters/tools
