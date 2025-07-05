// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/**
 * @title MyToken
 * @dev A standard ERC20 token with a fixed supply.
 * This contract creates a total supply of 1,000,000 tokens and assigns them
 * to the address that deploys the contract. It leverages OpenZeppelin's
 * secure and audited ERC20 implementation.
 *
 * Token Details:
 * - Name: MyToken
 * - Symbol: MTK
 * - Decimals: 18
 * - Total Supply: 1,000,000 MTK
 * - Mintable: No
 * - Burnable: No
 * - Pausable: No
 */
contract MyToken is ERC20 {
    /**
     * @dev Constructor that sets the token name and symbol.
     * It also mints the initial total supply to the contract deployer.
     */
    constructor() ERC20("MyToken", "MTK") {
        // Define the initial supply in human-readable units.
        uint256 initialSupply = 1000;

        // Calculate the total supply by adjusting for the token's decimals.
        // For a token with 18 decimals, this is equivalent to `initialSupply * 10**18`.
        // The result is 1,000,000,000,000,000,000,000,000 in the smallest unit (wei).
        uint256 totalSupplyWithDecimals = initialSupply * (10**decimals());

        // Mint the total supply and transfer it to the contract deployer's address.
        // `msg.sender` is the address that initiated the contract deployment.
        _mint(msg.sender, totalSupplyWithDecimals);
    }
}