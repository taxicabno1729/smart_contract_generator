const MyContract = artifacts.require("MyToken");

module.exports = function (deployer, network, accounts) {
  console.log(`Deploying MyContract to network: ${network}`);
  console.log(`Deploying from account: ${accounts[0]}`);
  
  deployer.deploy(MyContract)
    .then(() => {
      console.log("MyContract deployed successfully!");
      return MyContract.deployed();
    })
    .then((instance) => {
      console.log(`MyContract contract address: ${instance.address}`);
    })
    .catch((error) => {
      console.error("Deployment failed:", error);
    });
};