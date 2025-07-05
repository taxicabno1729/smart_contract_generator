// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title SimpleStorage
 * @dev A basic smart contract to demonstrate storing and retrieving a single uint256 value.
 *      It includes functions to set, get, increment, and decrement the stored value,
 *      along with event emission and basic error handling.
 */
contract SimpleStorage {
    // State variable to store the main value.
    // Declared as private to encourage access via public getter functions,
    // which is a common pattern for explicit API definition.
    uint256 private storedValue;

    // Event emitted whenever the 'storedValue' is modified.
    // Provides transparency and allows off-chain applications to react to state changes.
    event ValueUpdated(
        uint256 oldValue,   // The value before the modification.
        uint256 newValue,   // The value after the modification.
        address updatedBy   // The address of the account that initiated the update.
    );

    /**
     * @dev Constructor function.
     * Executed only once when the contract is deployed.
     * Initializes the 'storedValue' to a predefined initial value.
     */
    constructor() {
        storedValue = 1000; // Set the initial stored value as per specification.
    }

    /**
     * @dev Sets a new value for 'storedValue'.
     * Emits a 'ValueUpdated' event upon successful modification.
     * @param _newValue The new uint256 value to be stored.
     */
    function setValue(uint256 _newValue) public {
        uint256 oldValue = storedValue; // Capture the current value before modification.

        // Prevent unnecessary state changes and event emissions if the new value is identical to the current one.
        require(_newValue != oldValue, "New value must be different from current value.");

        storedValue = _newValue; // Update the state variable.

        // Emit the event to log the change.
        emit ValueUpdated(oldValue, storedValue, msg.sender);
    }

    /**
     * @dev Retrieves the current 'storedValue'.
     * Declared as 'view' because it does not modify the contract's state.
     * @return The current uint256 value stored in the contract.
     */
    function getValue() public view returns (uint256) {
        return storedValue;
    }

    /**
     * @dev Increments the 'storedValue' by 1.
     * Emits a 'ValueUpdated' event upon successful modification.
     * Note: For uint256, overflow is highly unlikely with a single increment
     * unless the value is already near the maximum uint256. Solidity 0.8.0+
     * automatically checks for overflow/underflow for arithmetic operations.
     */
    function increment() public {
        uint256 oldValue = storedValue; // Capture the current value.

        storedValue++; // Increment the value.

        // Emit the event to log the change.
        emit ValueUpdated(oldValue, storedValue, msg.sender);
    }

    /**
     * @dev Decrements the 'storedValue' by 1.
     * Includes a check to prevent underflow (i.e., going below zero).
     * Emits a 'ValueUpdated' event upon successful modification.
     */
    function decrement() public {
        uint256 oldValue = storedValue; // Capture the current value.

        // Prevent underflow: ensure the value is greater than 0 before decrementing.
        require(storedValue > 0, "Cannot decrement below zero.");

        storedValue--; // Decrement the value.

        // Emit the event to log the change.
        emit ValueUpdated(oldValue, storedValue, msg.sender);
    }
}