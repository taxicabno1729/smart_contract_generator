// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor() ERC20("MyToken", "ANI") {
        uint256 initialSupply = 1000000 * 10**18; // Adjust for 18 decimals
        _mint(msg.sender, initialSupply);
    }
}