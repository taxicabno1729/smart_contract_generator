// Replace 'MyToken' with the actual name of your contract from the .sol file.
const MyContract = artifacts.require("MyToken");

// The function signature is updated to include 'network' and 'accounts'
module.exports = function (deployer, network, accounts) {
  // --- SELECT YOUR DEPLOYER ACCOUNT HERE ---
  // You can choose any account from the 'accounts' array.
  // accounts[0] is the first account, accounts[1] is the second, etc.
  const customDeployerAccount = accounts[0]; // Using the first account as it's typically default and funded.
  
  console.log(`Attempting to deploy from account: ${customDeployerAccount}`);

  // --- DEPLOYMENT LOGIC ---
  // You will need to uncomment and adjust the correct section below
  // based on the contract you are deploying.

  // --- 1. For contracts with NO constructor arguments ---
  // (e.g., Basic ERC721, Simple Storage, Voting Contract)
  //
  // deployer.deploy(MyContract);

  // --- 2. For ERC20 Token (with an initial supply) ---
  // The generated ERC20 contract takes the initial supply as an argument.
  // Note: The amount should be in the smallest unit (wei), so multiply by 10**decimals.
  //
  const initialSupply = '1000000000000000000000000'; // Example: 1,000,000 tokens with 18 decimals

  // Deploy the contract, explicitly setting the 'from' address
  // The MyToken constructor expects the initialOwner as the first argument.
  deployer.deploy(MyContract, customDeployerAccount, { from: customDeployerAccount });

  // --- 3. For Multi-Signature Wallet ---
  // This contract requires an array of owner addresses and the number of required confirmations.
  // Get these addresses from your Ganache accounts for testing.
  //
  // const owners = [
  //   accounts[2], // Different owners for the wallet itself
  //   accounts[3],
  //   accounts[4]
  // ];
  // const requiredConfirmations = 2;
  // deployer.deploy(MyContract, owners, requiredConfirmations, { from: customDeployerAccount });
  // Note: The 'from' option is always the *last* argument after all constructor arguments.
};