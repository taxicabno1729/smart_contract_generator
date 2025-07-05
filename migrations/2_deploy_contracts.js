const MyContract = artifacts.require("MyToken");

module.exports = function (deployer, network, accounts) {
  console.log(`Deploying to network: ${network}`);
  console.log(`Available accounts: ${accounts.length}`);
  console.log(`Deploying from account: ${accounts[0]}`);
  
  // Deploy SimpleStorage contract (no constructor arguments needed)
  deployer.deploy(MyContract, { from: accounts[0] })
    .then(() => {
      console.log("SimpleStorage deployed successfully!");
      return MyContract.deployed();
    })
    .then((instance) => {
      console.log(`Contract address: ${instance.address}`);
    })
    .catch((error) => {
      console.error("Deployment failed:", error);
    });
};