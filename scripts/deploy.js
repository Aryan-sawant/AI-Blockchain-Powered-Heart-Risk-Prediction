const hre = require("hardhat");

async function main() {
    // Compile contract (optional, ensures latest build)
    await hre.run("compile");

    // Deploy the contract
    const HeartRiskPrediction = await hre.ethers.deployContract("HeartRiskPrediction");

    console.log("Deploying contract...");
    
    // Wait for contract to be mined
    const contract = await HeartRiskPrediction.waitForDeployment();

    console.log("Contract deployed to:", contract.target); // Or contract.address

    return contract; // Ensure contract instance is returned
}

// Execute deployment
main().catch((error) => {
    console.error("Deployment failed:", error);
    process.exit(1);
});
