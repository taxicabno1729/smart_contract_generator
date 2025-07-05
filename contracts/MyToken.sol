// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/**
 * @title MyToken
 * @dev A standard ERC20 token with a fixed initial supply.
 * This token is not mintable, burnable, or pausable after deployment.
 */
contract MyToken is ERC20 {
    /**
     * @dev Constructor that deploys the token with a fixed initial supply.
     * @param initialOwner The address that will receive the initial supply of tokens.
     *                     This is typically the deployer of the contract.
     */
    constructor(address initialOwner) ERC20("MyToken", "MTK") {
        // Define the human-readable initial supply
        uint256 initialSupplyHumanReadable = 1_000_000; // 1,000,000 tokens

        // Calculate the initial supply in smallest units (wei for tokens, 18 decimals)
        // 1 token = 10^18 smallest units
        uint256 initialSupply = initialSupplyHumanReadable * (10 ** decimals());

        // Mint the total initial supply to the deployer (initialOwner).
        // The _mint function is an internal OpenZeppelin function used for initial token creation.
        // Since there's no external mint function, the token is not "mintable" by anyone after deployment.
        _mint(initialOwner, initialSupply);
    }
}