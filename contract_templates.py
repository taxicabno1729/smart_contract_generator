class ContractGenerator:
    def __init__(self):
        self.templates = {
            "ERC20 Token": self._generate_erc20,
            "ERC721 NFT": self._generate_erc721,
            "Simple Storage": self._generate_simple_storage,
            "Multi-Signature Wallet": self._generate_multisig,
            "Voting Contract": self._generate_voting
        }
    
    def generate_contract(self, contract_type, params):
        if contract_type not in self.templates:
            raise ValueError(f"Unsupported contract type: {contract_type}")
        
        return self.templates[contract_type](params)
    
    def _generate_erc20(self, params):
        name = params.get('name', 'MyToken')
        symbol = params.get('symbol', 'MTK')
        decimals = params.get('decimals', 18)
        initial_supply = params.get('initial_supply', 1000000)
        mintable = params.get('mintable', False)
        burnable = params.get('burnable', False)
        pausable = params.get('pausable', False)
        version = params.get('solidity_version', '0.8.20')
        license = params.get('license', 'MIT')
        include_comments = params.get('include_comments', True)
        
        imports = ["import \"@openzeppelin/contracts/token/ERC20/ERC20.sol\";"]
        inheritance = ["ERC20"]

        # Ownable logic:
        # ERC20Pausable already inherits Ownable.
        # If pausable is selected, Ownable is covered.
        # If only mintable is selected (not pausable), then Ownable needs to be added.
        if pausable:
            imports.append("import \"@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol\";")
            inheritance.append("ERC20Pausable") # ERC20Pausable includes Ownable
        elif mintable: # Only mintable, not pausable
            imports.append("import \"@openzeppelin/contracts/access/Ownable.sol\";")
            inheritance.append("Ownable")
        
        if burnable:
            imports.append("import \"@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol\";")
            inheritance.append("ERC20Burnable")
        
        # Remove duplicates while preserving order
        imports = list(dict.fromkeys(imports))
        inheritance = list(dict.fromkeys(inheritance))
        
        # Generate contract code without complex f-string nesting
        contract_code = f"// SPDX-License-Identifier: {license}\n"
        contract_code += f"pragma solidity ^{version};\n\n"
        contract_code += "\n".join(imports) + "\n\n"
        
        if include_comments:
            contract_code += f"/**\n * @title {name}\n * @dev ERC20 Token with customizable features\n */\n"
        
        contract_code += f"contract {name.replace(' ', '')} is {', '.join(inheritance)} {{\n"
        
        # Constructor
        constructor_params = ["uint256 initialSupply"]
        # Initializer list for ERC20 and potentially Ownable (if not pausable)
        initializers = [f"ERC20(\"{name}\", \"{symbol}\")"]
        if not pausable and mintable: # If only mintable (hence Ownable is explicit)
             # OpenZeppelin's Ownable constructor takes an initialOwner.
             # We'll use msg.sender as the initial owner.
            initializers.append("Ownable(msg.sender)")


        constructor_body = f"        _mint(msg.sender, initialSupply * 10**uint256({decimals}));\n"
        
        if include_comments:
            contract_code += "    /**\n     * @dev Constructor that sets up the token\n     * @param initialSupply The initial supply of tokens\n     */\n"
        
        contract_code += f"    constructor({', '.join(constructor_params)}) { ' '.join(initializers) } {{\n"
        contract_code += constructor_body
        contract_code += "    }\n"
        
        # Override decimals() only if it's not the default 18
        if decimals != 18:
            if include_comments:
                contract_code += "\n    /**\n     * @dev Returns the number of decimals used for token amounts.\n     */\n"
            contract_code += "    function decimals() public view virtual override returns (uint8) {\n"
            contract_code += f"        return {decimals};\n"
            contract_code += "    }\n"
        elif include_comments: # Add comment if not overriding but comments are on
            contract_code += "\n    // Note: decimals() is inherited from ERC20.sol and defaults to 18.\n"


        if mintable:
            # If pausable is true, onlyOwner comes from ERC20Pausable's Ownable.
            # If pausable is false (and mintable is true), onlyOwner comes from the explicitly added Ownable.
            contract_code += "\n    \n"
            if include_comments:
                contract_code += "    /**\n     * @dev Mints new tokens (only owner)\n     * @param to The address to mint tokens to\n     * @param amount The amount of tokens to mint\n     */\n"
            contract_code += "    function mint(address to, uint256 amount) public onlyOwner {\n"
            contract_code += "        _mint(to, amount);\n"
            contract_code += "    }"

        if pausable:
            contract_code += "\n    \n"
            if include_comments:
                contract_code += "    /**\n     * @dev Pauses all token transfers\n     */\n"
            contract_code += "    function pause() public onlyOwner {\n"
            contract_code += "        _pause();\n"
            contract_code += "    }\n    \n"
            if include_comments:
                contract_code += "    /**\n     * @dev Unpauses all token transfers\n     */\n"
            contract_code += "    function unpause() public onlyOwner {\n"
            contract_code += "        _unpause();\n"
            contract_code += "    }"

        contract_code += "\n}"
        
        return contract_code
    
    def _generate_erc721(self, params):
        name = params.get('name', 'MyNFT')
        symbol = params.get('symbol', 'MNFT')
        base_uri = params.get('base_uri', 'https://api.example.com/metadata/')
        max_supply = params.get('max_supply', 10000)
        mintable = params.get('mintable', True)
        enumerable = params.get('enumerable', False)
        version = params.get('solidity_version', '0.8.20')
        license = params.get('license', 'MIT')
        include_comments = params.get('include_comments', True)
        
        imports = [
            "import \"@openzeppelin/contracts/token/ERC721/ERC721.sol\";",
            "import \"@openzeppelin/contracts/access/Ownable.sol\";",
            "import \"@openzeppelin/contracts/utils/Counters.sol\";"
        ]
        
        inheritance = ["ERC721", "Ownable"]
        
        if enumerable:
            imports.append("import \"@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol\";")
            inheritance.append("ERC721Enumerable")
        
        contract_code = f"// SPDX-License-Identifier: {license}\n"
        contract_code += f"pragma solidity ^{version};\n\n"
        contract_code += "\n".join(imports) + "\n\n"
        
        if include_comments:
            contract_code += f"/**\n * @title {name}\n * @dev ERC721 NFT Contract with customizable features\n */\n"
        
        contract_code += f"contract {name.replace(' ', '')} is {', '.join(inheritance)} {{\n"
        contract_code += "    using Counters for Counters.Counter;\n    \n"
        
        if include_comments:
            contract_code += "    // Token ID counter\n    "
        contract_code += "Counters.Counter private _tokenIds;\n    \n"
        
        if include_comments:
            contract_code += "    // Maximum supply of NFTs\n    "
        contract_code += f"uint256 public constant MAX_SUPPLY = {max_supply};\n    \n"
        
        if include_comments:
            contract_code += "    // Base URI for metadata\n    "
        contract_code += "string private _baseTokenURI;\n    \n"
        
        if include_comments:
            contract_code += "    /**\n     * @dev Constructor that sets up the NFT collection\n     */\n"
        
        contract_code += f"    constructor() ERC721(\"{name}\", \"{symbol}\") {{\n"
        contract_code += f"        _baseTokenURI = \"{base_uri}\";\n"
        contract_code += "    }\n    \n"
        
        if include_comments:
            contract_code += "    /**\n     * @dev Returns the base URI for tokens\n     */\n"
        
        contract_code += "    function _baseURI() internal view virtual override returns (string memory) {\n"
        contract_code += "        return _baseTokenURI;\n"
        contract_code += "    }\n    \n"
        
        if include_comments:
            contract_code += "    /**\n     * @dev Sets the base URI for tokens (only owner)\n     * @param newBaseURI The new base URI\n     */\n"
        
        contract_code += "    function setBaseURI(string memory newBaseURI) public onlyOwner {\n"
        contract_code += "        _baseTokenURI = newBaseURI;\n"
        contract_code += "    }"

        if mintable:
            contract_code += "\n    \n"
            if include_comments:
                contract_code += "    /**\n     * @dev Mints a new NFT (only owner)\n     * @param to The address to mint the NFT to\n     * @return tokenId The ID of the newly minted token\n     */\n"
            
            contract_code += "    function mint(address to) public onlyOwner returns (uint256) {\n"
            contract_code += "        require(_tokenIds.current() < MAX_SUPPLY, \"Max supply reached\");\n        \n"
            contract_code += "        _tokenIds.increment();\n"
            contract_code += "        uint256 tokenId = _tokenIds.current();\n        \n"
            contract_code += "        _mint(to, tokenId);\n        \n"
            contract_code += "        return tokenId;\n"
            contract_code += "    }\n    \n"
            
            if include_comments:
                contract_code += "    /**\n     * @dev Returns the total number of tokens minted\n     */\n"
            
            contract_code += "    function totalSupply() public view returns (uint256) {\n"
            contract_code += "        return _tokenIds.current();\n"
            contract_code += "    }"

        if enumerable:
            contract_code += "\n    \n"
            if include_comments:
                contract_code += "    /**\n     * @dev See {IERC165-supportsInterface}.\n     */\n"
            # Corrected override order for OZ v5.x
            contract_code += "    function supportsInterface(bytes4 interfaceId) public view virtual override(ERC721Enumerable, ERC721) returns (bool) {\n"
            contract_code += "        return super.supportsInterface(interfaceId);\n"
            contract_code += "    }\n    \n"
            
            if include_comments:
                contract_code += "    /**\n     * @dev See {ERC721-_beforeTokenTransfer}.\n     *\n     * Requirements:\n     *\n     * - `from` cannot be the zero address.\n     * - `to` cannot be the zero address.\n     * - `tokenId` token must exist and be owned by `from`.\n     */\n"
            # Corrected signature and override order for OZ v5.x ERC721Enumerable
            # The parameter name is `firstTokenId` in ERC721Enumerable's specific override.
            # ERC721's _beforeTokenTransfer is (address from, address to, uint256 tokenId, uint256 batchSize)
            # ERC721Enumerable's _beforeTokenTransfer is (address from, address to, uint256 firstTokenId, uint256 batchSize)
            contract_code += "    function _beforeTokenTransfer(address from, address to, uint256 firstTokenId, uint256 batchSize) internal virtual override(ERC721Enumerable, ERC721) {\n"
            contract_code += "        super._beforeTokenTransfer(from, to, firstTokenId, batchSize);\n"
            contract_code += "    }"

        contract_code += "\n}"
        
        return contract_code
    
    def _generate_simple_storage(self, params):
        initial_value = params.get('initial_value', 0)
        access_control = params.get('access_control', 'Public')
        version = params.get('solidity_version', '0.8.20')
        license = params.get('license', 'MIT')
        include_comments = params.get('include_comments', True)
        
        imports = []
        inheritance = []
        
        if access_control == "Owner Only":
            imports.append("import \"@openzeppelin/contracts/access/Ownable.sol\";")
            inheritance.append("Ownable")
        
        contract_code = f"// SPDX-License-Identifier: {license}\n"
        contract_code += f"pragma solidity ^{version};\n\n"
        
        if imports:
            contract_code += "\n".join(imports) + "\n\n"
        
        if include_comments:
            contract_code += "/**\n * @title SimpleStorage\n * @dev A simple storage contract that stores and retrieves a value\n */\n"
        
        contract_code += "contract SimpleStorage"
        if inheritance:
            contract_code += f" is {', '.join(inheritance)}"
        contract_code += " {\n    \n"
        
        if include_comments:
            contract_code += "    // Stored value\n    "
        contract_code += "uint256 private storedValue;\n    \n"
        
        if include_comments:
            contract_code += "    // Event emitted when value is updated\n    "
        contract_code += "event ValueUpdated(uint256 oldValue, uint256 newValue, address updatedBy);\n    \n"
        
        if include_comments:
            contract_code += "    /**\n     * @dev Constructor that sets initial value\n     */\n"
        
        contract_code += "    constructor() {\n"
        contract_code += f"        storedValue = {initial_value};\n"
        contract_code += "    }\n    \n"
        
        if include_comments:
            contract_code += "    /**\n     * @dev Stores a value\n     * @param value The value to store\n     */\n"
        
        contract_code += "    function setValue(uint256 value) public"
        if access_control == "Owner Only":
            contract_code += " onlyOwner"
        contract_code += " {\n"
        contract_code += "        uint256 oldValue = storedValue;\n"
        contract_code += "        storedValue = value;\n"
        contract_code += "        emit ValueUpdated(oldValue, value, msg.sender);\n"
        contract_code += "    }\n    \n"
        
        if include_comments:
            contract_code += "    /**\n     * @dev Retrieves the stored value\n     * @return The stored value\n     */\n"
        
        contract_code += "    function getValue() public view returns (uint256) {\n"
        contract_code += "        return storedValue;\n"
        contract_code += "    }\n    \n"
        
        if include_comments:
            contract_code += "    /**\n     * @dev Increments the stored value by 1\n     */\n"
        
        contract_code += "    function increment() public"
        if access_control == "Owner Only":
            contract_code += " onlyOwner"
        contract_code += " {\n"
        contract_code += "        uint256 oldValue = storedValue;\n"
        contract_code += "        storedValue++;\n"
        contract_code += "        emit ValueUpdated(oldValue, storedValue, msg.sender);\n"
        contract_code += "    }\n    \n"
        
        if include_comments:
            contract_code += "    /**\n     * @dev Decrements the stored value by 1\n     */\n"
        
        contract_code += "    function decrement() public"
        if access_control == "Owner Only":
            contract_code += " onlyOwner"
        contract_code += " {\n"
        contract_code += "        require(storedValue > 0, \"Cannot decrement below zero\");\n"
        contract_code += "        uint256 oldValue = storedValue;\n"
        contract_code += "        storedValue--;\n"
        contract_code += "        emit ValueUpdated(oldValue, storedValue, msg.sender);\n"
        contract_code += "    }\n"
        contract_code += "}"
        
        return contract_code
    
    def _generate_multisig(self, params):
        required_confirmations = params.get('required_confirmations', 2)
        owners_text = params.get('owners', '')
        owners = [addr.strip() for addr in owners_text.split('\n') if addr.strip()]
        version = params.get('solidity_version', '0.8.20')
        license = params.get('license', 'MIT')
        include_comments = params.get('include_comments', True)
        
        # Default owners if none provided
        if not owners:
            owners = [
                "0x1234567890123456789012345678901234567890",
                "0x2345678901234567890123456789012345678901",
                "0x3456789012345678901234567890123456789012"
            ]
        
        contract_code = f"// SPDX-License-Identifier: {license}\n"
        contract_code += f"pragma solidity ^{version};\n\n"
        
        if include_comments:
            contract_code += "/**\n * @title MultiSigWallet\n * @dev A multi-signature wallet contract\n */\n"
        
        contract_code += "contract MultiSigWallet {\n    \n"
        
        if include_comments:
            contract_code += "    // Events\n    "
        contract_code += "event Deposit(address indexed sender, uint256 amount, uint256 balance);\n"
        contract_code += "    event SubmitTransaction(address indexed owner, uint256 indexed txIndex, address indexed to, uint256 value, bytes data);\n"
        contract_code += "    event ConfirmTransaction(address indexed owner, uint256 indexed txIndex);\n"
        contract_code += "    event RevokeConfirmation(address indexed owner, uint256 indexed txIndex);\n"
        contract_code += "    event ExecuteTransaction(address indexed owner, uint256 indexed txIndex);\n    \n"
        
        if include_comments:
            contract_code += "    // State variables\n    "
        contract_code += "address[] public owners;\n"
        contract_code += "    mapping(address => bool) public isOwner;\n"
        contract_code += "    uint256 public numConfirmationsRequired;\n    \n"
        
        contract_code += "    struct Transaction {\n"
        contract_code += "        address to;\n"
        contract_code += "        uint256 value;\n"
        contract_code += "        bytes data;\n"
        contract_code += "        bool executed;\n"
        contract_code += "        uint256 numConfirmations;\n"
        contract_code += "    }\n    \n"
        
        if include_comments:
            contract_code += "    // mapping from tx index => owner => bool\n    "
        contract_code += "mapping(uint256 => mapping(address => bool)) public isConfirmed;\n    \n"
        
        contract_code += "    Transaction[] public transactions;\n    \n"
        
        if include_comments:
            contract_code += "    // Modifiers\n    "
        contract_code += "modifier onlyOwner() {\n"
        contract_code += "        require(isOwner[msg.sender], \"Not owner\");\n"
        contract_code += "        _;\n"
        contract_code += "    }\n    \n"
        
        contract_code += "    modifier txExists(uint256 _txIndex) {\n"
        contract_code += "        require(_txIndex < transactions.length, \"Transaction does not exist\");\n"
        contract_code += "        _;\n"
        contract_code += "    }\n    \n"
        
        contract_code += "    modifier notExecuted(uint256 _txIndex) {\n"
        contract_code += "        require(!transactions[_txIndex].executed, \"Transaction already executed\");\n"
        contract_code += "        _;\n"
        contract_code += "    }\n    \n"
        
        contract_code += "    modifier notConfirmed(uint256 _txIndex) {\n"
        contract_code += "        require(!isConfirmed[_txIndex][msg.sender], \"Transaction already confirmed\");\n"
        contract_code += "        _;\n"
        contract_code += "    }\n    \n"
        
        if include_comments:
            contract_code += "    /**\n     * @dev Constructor that sets up the multi-sig wallet\n     */\n"
        
        contract_code += f"    constructor() {{\n"
        contract_code += f"        address[] memory _owners = new address[]({len(owners)});\n"
        
        for i, owner in enumerate(owners):
            contract_code += f"        _owners[{i}] = {owner};\n"
        
        contract_code += f"        \n        require(_owners.length > 0, \"Owners required\");\n"
        contract_code += f"        require({required_confirmations} > 0 && {required_confirmations} <= _owners.length, \"Invalid number of required confirmations\");\n        \n"
        
        contract_code += "        for (uint256 i = 0; i < _owners.length; i++) {\n"
        contract_code += "            address owner = _owners[i];\n"
        contract_code += "            require(owner != address(0), \"Invalid owner\");\n"
        contract_code += "            require(!isOwner[owner], \"Owner not unique\");\n            \n"
        contract_code += "            isOwner[owner] = true;\n"
        contract_code += "            owners.push(owner);\n"
        contract_code += "        }\n        \n"
        
        contract_code += f"        numConfirmationsRequired = {required_confirmations};\n"
        contract_code += "    }\n    \n"
        
        if include_comments:
            contract_code += "    /**\n     * @dev Receive function to accept ETH deposits\n     */\n"
        
        contract_code += "    receive() external payable {\n"
        contract_code += "        emit Deposit(msg.sender, msg.value, address(this).balance);\n"
        contract_code += "    }\n    \n"
        
        if include_comments:
            contract_code += "    /**\n     * @dev Submit a transaction for confirmation\n     */\n"
        
        contract_code += "    function submitTransaction(address _to, uint256 _value, bytes memory _data) public onlyOwner {\n"
        contract_code += "        uint256 txIndex = transactions.length;\n        \n"
        contract_code += "        transactions.push(Transaction({\n"
        contract_code += "            to: _to,\n"
        contract_code += "            value: _value,\n"
        contract_code += "            data: _data,\n"
        contract_code += "            executed: false,\n"
        contract_code += "            numConfirmations: 0\n"
        contract_code += "        }));\n        \n"
        contract_code += "        emit SubmitTransaction(msg.sender, txIndex, _to, _value, _data);\n"
        contract_code += "    }\n    \n"
        
        contract_code += "    function getTransactionCount() public view returns (uint256) {\n"
        contract_code += "        return transactions.length;\n"
        contract_code += "    }\n"
        contract_code += "}"
        
        return contract_code
    
    def _generate_voting(self, params):
        voting_duration = params.get('voting_duration', 1440)  # in minutes
        require_registration = params.get('require_registration', False)
        proposal_threshold = params.get('proposal_threshold', 1)
        version = params.get('solidity_version', '0.8.20')
        license = params.get('license', 'MIT')
        include_comments = params.get('include_comments', True)
        
        imports = ["import \"@openzeppelin/contracts/access/Ownable.sol\";"]
        
        contract_code = f"// SPDX-License-Identifier: {license}\n"
        contract_code += f"pragma solidity ^{version};\n\n"
        contract_code += "\n".join(imports) + "\n\n"
        
        if include_comments:
            contract_code += "/**\n * @title VotingContract\n * @dev A decentralized voting contract\n */\n"
        
        contract_code += "contract VotingContract is Ownable {\n    \n"
        
        if include_comments:
            contract_code += "    // Voting duration in seconds\n    "
        contract_code += f"uint256 public constant VOTING_DURATION = {voting_duration * 60};\n    \n"
        
        if include_comments:
            contract_code += "    // Proposal threshold\n    "
        contract_code += f"uint256 public constant PROPOSAL_THRESHOLD = {proposal_threshold};\n    \n"
        
        contract_code += "    struct Proposal {\n"
        contract_code += "        string description;\n"
        contract_code += "        uint256 voteCount;\n"
        contract_code += "        uint256 startTime;\n"
        contract_code += "        uint256 endTime;\n"
        contract_code += "        bool executed;\n"
        contract_code += "    }\n    \n"
        
        if include_comments:
            contract_code += "    // State variables\n    "
        contract_code += "Proposal[] public proposals;\n"
        contract_code += "    uint256 public proposalCount;\n    \n"
        
        if include_comments:
            contract_code += "    // Mappings\n    "
        contract_code += "mapping(uint256 => mapping(address => bool)) public hasVoted;\n"
        contract_code += "    mapping(address => bool) public registeredVoters;\n"
        contract_code += "    mapping(address => uint256) public voterTokens;\n    \n"
        
        if include_comments:
            contract_code += "    // Events\n    "
        contract_code += "event ProposalCreated(uint256 indexed proposalId, string description, uint256 startTime, uint256 endTime);\n"
        contract_code += "    event VoteCasted(uint256 indexed proposalId, address indexed voter, uint256 weight);\n"
        contract_code += "    event ProposalExecuted(uint256 indexed proposalId);\n"
        contract_code += "    event VoterRegistered(address indexed voter, uint256 tokens);\n    \n"
        
        if include_comments:
            contract_code += "    // Modifiers\n    "
        contract_code += "modifier onlyRegistered() {\n"
        contract_code += f"        require(registeredVoters[msg.sender] || !{str(require_registration).lower()}, \"Not registered to vote\");\n"
        contract_code += "        _;\n"
        contract_code += "    }\n    \n"
        
        contract_code += "    modifier validProposal(uint256 _proposalId) {\n"
        contract_code += "        require(_proposalId < proposalCount, \"Invalid proposal ID\");\n"
        contract_code += "        _;\n"
        contract_code += "    }\n    \n"
        
        contract_code += "    modifier votingActive(uint256 _proposalId) {\n"
        contract_code += "        require(block.timestamp >= proposals[_proposalId].startTime, \"Voting not started\");\n"
        contract_code += "        require(block.timestamp <= proposals[_proposalId].endTime, \"Voting period ended\");\n"
        contract_code += "        _;\n"
        contract_code += "    }\n    \n"
        
        if include_comments:
            contract_code += "    /**\n     * @dev Constructor\n     */\n"
        contract_code += "    constructor() {\n"
        if include_comments:
            contract_code += "        // Initial setup\n        "
        contract_code += "proposalCount = 0;\n"
        contract_code += "    }\n    \n"
        
        if include_comments:
            contract_code += "    /**\n     * @dev Create a new proposal\n     */\n"
        contract_code += "    function createProposal(string memory _description) public {\n"
        contract_code += "        require(bytes(_description).length > 0, \"Description cannot be empty\");\n        \n"
        contract_code += "        uint256 startTime = block.timestamp;\n"
        contract_code += "        uint256 endTime = startTime + VOTING_DURATION;\n        \n"
        contract_code += "        proposals.push(Proposal({\n"
        contract_code += "            description: _description,\n"
        contract_code += "            voteCount: 0,\n"
        contract_code += "            startTime: startTime,\n"
        contract_code += "            endTime: endTime,\n"
        contract_code += "            executed: false\n"
        contract_code += "        }));\n        \n"
        contract_code += "        emit ProposalCreated(proposalCount, _description, startTime, endTime);\n"
        contract_code += "        proposalCount++;\n"
        contract_code += "    }\n    \n"
        
        if include_comments:
            contract_code += "    /**\n     * @dev Vote on a proposal\n     */\n"
        contract_code += "    function vote(uint256 _proposalId) public onlyRegistered validProposal(_proposalId) votingActive(_proposalId) {\n"
        contract_code += "        require(!hasVoted[_proposalId][msg.sender], \"Already voted\");\n        \n"
        contract_code += "        hasVoted[_proposalId][msg.sender] = true;\n"
        contract_code += "        proposals[_proposalId].voteCount++;\n        \n"
        contract_code += "        emit VoteCasted(_proposalId, msg.sender, 1);\n"
        contract_code += "    }\n    \n"
        
        if include_comments:
            contract_code += "    /**\n     * @dev Get proposal details\n     */\n"
        contract_code += "    function getProposal(uint256 _proposalId) public view validProposal(_proposalId) returns (string memory, uint256, uint256, uint256, bool) {\n"
        contract_code += "        Proposal memory proposal = proposals[_proposalId];\n"
        contract_code += "        return (proposal.description, proposal.voteCount, proposal.startTime, proposal.endTime, proposal.executed);\n"
        contract_code += "    }\n"
        contract_code += "}"
        
        return contract_code