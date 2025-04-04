require("dotenv").config();
const { ethers } = require("hardhat");

async function main() {
    // ✅ Ensure environment variables are loaded
    if (!process.env.ALCHEMY_API_KEY || !process.env.PRIVATE_KEY) {
        console.error("Missing ALCHEMY_API_KEY or PRIVATE_KEY in .env file.");
        process.exit(1);
    }

    // ✅ Define provider & wallet
    const provider = new ethers.JsonRpcProvider(`https://polygon-amoy.g.alchemy.com/v2/${process.env.ALCHEMY_API_KEY}`);
    const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

    // ✅ Define contract ABI & address
    const contractABI = require("../artifacts/contracts/HeartRiskPrediction.sol/HeartRiskPrediction.json");
    const contractAddress = "0x9829FBEA9637244823A89384108662C654E50E5c"; // Replace with actual deployed contract address

    // ✅ Initialize contract instance
    const contract = new ethers.Contract(contractAddress, contractABI.abi, wallet);

    console.log("📢 Storing a new heart risk prediction...");

    try {
        // ✅ Call storePrediction with 14 parameters
        const tx = await contract.storePrediction(
            45,  // age
            1,   // sex (0 = Female, 1 = Male)
            2,   // cp (Chest Pain type)
            120, // trestbps (Resting Blood Pressure)
            200, // chol (Serum Cholesterol)
            1,   // fbs (Fasting Blood Sugar)
            1,   // restecg (Resting ECG results)
            150, // thalach (Maximum Heart Rate)
            0,   // exang (Exercise-induced angina)
            2,   // oldpeak (ST depression)
            2,   // slope (Slope of peak exercise ST segment)
            1,   // ca (Number of major vessels)
            3,   // thal (Thalassemia type)
            1    // prediction (0 = No Disease, 1 = Heart Disease)
        );

        console.log(`✅ Transaction sent: ${tx.hash}`);

        // ✅ Wait for transaction confirmation
        const receipt = await tx.wait();
        console.log(`✅ Prediction stored successfully in block: ${receipt.blockNumber}`);
    } catch (error) {
        console.error("❌ Error storing prediction:", error);
    }
}

// Run the script
main().catch((error) => {
    console.error("❌ Script execution error:", error);
    process.exit(1);
});
