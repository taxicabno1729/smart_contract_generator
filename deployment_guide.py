def get_deployment_steps(contract_type):
    """
    Returns deployment steps specific to the contract type
    """
    
    base_steps = [
        {
            "title": "Open Remix IDE",
            "description": """
            1. Go to [Remix IDE](https://remix.ethereum.org) in your web browser
            2. Wait for the IDE to load completely
            3. You'll see the file explorer on the left side
            """,
            "info": "Remix is a web-based IDE for developing Ethereum smart contracts"
        },
        {
            "title": "Create New File",
            "description": """
            1. In the file explorer, right-click on the `contracts` folder
            2. Select "New File"
            3. Name your file with a `.sol` extension (e.g., `MyContract.sol`)
            4. The file will open in the editor
            """,
            "info": "Solidity files must have the .sol extension"
        },
        {
            "title": "Paste Contract Code",
            "description": """
            1. Copy the generated contract code from above
            2. Paste it into the newly created file in Remix
            3. Save the file using `Ctrl+S` (or `Cmd+S` on Mac)
            4. You should see the file appear in the file explorer
            """,
            "info": "Make sure to save the file before compiling"
        },
        {
            "title": "Compile Contract",
            "description": """
            1. Click on the "Solidity Compiler" tab (compiler icon) in the left sidebar
            2. Select the appropriate compiler version (match the pragma version in your contract)
            3. Click "Compile [YourContractName].sol"
            4. Check for any compilation errors in the console
            """,
            "warning": "Make sure the compiler version matches your contract's pragma statement"
        },
        {
            "title": "Configure Deployment Environment",
            "description": """
            1. Click on the "Deploy & Run Transactions" tab (Ethereum logo) in the left sidebar
            2. Select your desired environment:
               - **Remix VM**: For testing (recommended for beginners)
               - **Injected Web3**: For MetaMask integration
               - **External HTTP Provider**: For custom networks
            3. If using MetaMask, make sure it's connected and on the correct network
            """,
            "info": "Start with Remix VM for testing, then move to testnets before mainnet"
        }
    ]
    
    # Contract-specific deployment steps
    contract_specific_steps = {
        "ERC20 Token": [
            {
                "title": "Deploy ERC20 Token",
                "description": """
                1. In the Deploy section, select your ERC20 contract from the dropdown
                2. Enter the constructor parameters:
                   - `initialSupply`: The initial token supply (e.g., 1000000)
                3. Click "Deploy"
                4. Confirm the transaction in MetaMask (if using injected Web3)
                5. Your contract address will appear in the "Deployed Contracts" section
                """,
                "info": "The initial supply will be minted to the deployer's address"
            },
            {
                "title": "Interact with Token",
                "description": """
                1. Expand your deployed contract in the "Deployed Contracts" section
                2. Try these functions:
                   - `name()`: Get token name
                   - `symbol()`: Get token symbol
                   - `totalSupply()`: Get total supply
                   - `balanceOf(address)`: Check balance of an address
                   - `transfer(address, amount)`: Transfer tokens
                """,
                "warning": "Be careful with transfer amounts - they need to include decimals"
            }
        ],
        "ERC721 NFT": [
            {
                "title": "Deploy ERC721 NFT",
                "description": """
                1. In the Deploy section, select your ERC721 contract from the dropdown
                2. No constructor parameters needed for basic deployment
                3. Click "Deploy"
                4. Confirm the transaction in MetaMask (if using injected Web3)
                5. Your contract address will appear in the "Deployed Contracts" section
                """,
                "info": "The contract owner will be the deployer's address"
            },
            {
                "title": "Mint NFTs",
                "description": """
                1. Expand your deployed contract in the "Deployed Contracts" section
                2. Use the `mint` function to create NFTs:
                   - `mint(address)`: Mint to a specific address
                   - `batchMint(address, quantity)`: Mint multiple NFTs
                3. Use `tokenURI(tokenId)` to get metadata URI
                4. Use `ownerOf(tokenId)` to check NFT owner
                """,
                "warning": "Only the contract owner can mint NFTs (if mintable is enabled)"
            }
        ],
        "Simple Storage": [
            {
                "title": "Deploy Simple Storage",
                "description": """
                1. In the Deploy section, select your SimpleStorage contract
                2. No constructor parameters needed
                3. Click "Deploy"
                4. The contract will be deployed with the initial value you specified
                """,
                "info": "The contract starts with your specified initial value"
            },
            {
                "title": "Test Storage Functions",
                "description": """
                1. Expand your deployed contract
                2. Try these functions:
                   - `getValue()`: Read the stored value
                   - `setValue(uint256)`: Set a new value
                   - `increment()`: Increase value by 1
                   - `decrement()`: Decrease value by 1
                3. Watch the console for ValueUpdated events
                """,
                "info": "Each state change will emit a ValueUpdated event"
            }
        ],
        "Multi-Signature Wallet": [
            {
                "title": "Deploy Multi-Sig Wallet",
                "description": """
                1. In the Deploy section, select your MultiSigWallet contract
                2. Enter constructor parameters:
                   - `_owners`: Array of owner addresses (comma-separated)
                   - `_numConfirmationsRequired`: Number of required confirmations
                3. Click "Deploy"
                4. The wallet will be created with the specified owners
                """,
                "code": """
                // Example constructor parameters:
                _owners: ["0x123...", "0x456...", "0x789..."]
                _numConfirmationsRequired: 2
                """,
                "language": "solidity"
            },
            {
                "title": "Test Multi-Sig Functions",
                "description": """
                1. Send some ETH to the contract address
                2. Use `submitTransaction` to propose a transaction
                3. Other owners use `confirmTransaction` to approve
                4. Once enough confirmations, use `executeTransaction`
                5. Monitor events for transaction lifecycle
                """,
                "warning": "Test thoroughly with small amounts before using with real funds"
            }
        ],
        "Voting Contract": [
            {
                "title": "Deploy Voting Contract",
                "description": """
                1. In the Deploy section, select your VotingContract
                2. No constructor parameters needed
                3. Click "Deploy"
                4. The contract owner will be the deployer
                """,
                "info": "The deployer becomes the contract owner and can register voters"
            },
            {
                "title": "Setup Voting",
                "description": """
                1. Register voters using `registerVoter(address, tokens)` (if registration required)
                2. Set voting tokens using `setVoterTokens` (if registration not required)
                3. Create proposals using `createProposal(description)`
                4. Voters can vote using `vote(proposalId)`
                5. Monitor proposal status with `getProposal(proposalId)`
                """,
                "info": "Voting duration is fixed at deployment time"
            }
        ]
    }
    
    final_steps = [
        {
            "title": "Verify Contract (Optional)",
            "description": """
            1. Go to the blockchain explorer (e.g., Etherscan)
            2. Search for your contract address
            3. Click on the "Contract" tab
            4. Click "Verify and Publish"
            5. Select the compiler version and optimization settings
            6. Paste your contract source code
            7. Submit for verification
            """,
            "info": "Contract verification makes your code publicly viewable and trustworthy"
        },
        {
            "title": "Security Considerations",
            "description": """
            **Before mainnet deployment:**
            1. **Audit your contract**: Have it reviewed by security experts
            2. **Test extensively**: Use testnets like Sepolia or Goerli
            3. **Start small**: Deploy with minimal funds first
            4. **Monitor closely**: Watch for unusual activity
            5. **Have an emergency plan**: Consider pause/upgrade mechanisms
            """,
            "warning": "Never deploy unaudited contracts to mainnet with significant funds"
        },
        {
            "title": "Gas Optimization Tips",
            "description": """
            1. **Use events**: Instead of storing data on-chain when possible
            2. **Pack structs**: Organize struct members to minimize storage slots
            3. **Batch operations**: Combine multiple operations in single transaction
            4. **Use view functions**: For read-only operations
            5. **Optimize loops**: Minimize gas-consuming iterations
            """,
            "info": "Gas optimization can significantly reduce deployment and usage costs"
        }
    ]
    
    # Combine all steps
    all_steps = base_steps + contract_specific_steps.get(contract_type, []) + final_steps
    
    return all_steps
