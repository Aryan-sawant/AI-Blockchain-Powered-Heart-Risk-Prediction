require("dotenv").config();
const { ethers } = require("ethers");

async function main() {
    const CONTRACT_ADDRESS = "0x9829FBEA9637244823A89384108662C654E50E5c"; 

    const ABI = [
        "function getAllPredictions(address user) public view returns (tuple(uint256,uint8,uint8,uint256,uint256,uint8,uint8,uint256,uint8,uint256,uint8,uint8,uint8,uint256,uint8)[])"
    ];

    // ✅ Ensure the RPC URL is loaded
    if (!process.env.ALCHEMY_RPC_URL) {
        console.error("Missing ALCHEMY_RPC_URL in .env file");
        process.exit(1);
    }

    // ✅ Correct provider instantiation
    const provider = new ethers.JsonRpcProvider(process.env.ALCHEMY_RPC_URL);

    // ✅ Read-only contract instance
    const contract = new ethers.Contract(CONTRACT_ADDRESS, ABI, provider);

    // ✅ Replace with an actual user address
    const userAddress = "0xd4c730Dd3D991672c5817F0A2A50Ca9E9a7bb6AE"; 

    try {
        const predictions = await contract.getAllPredictions(userAddress);
        
        if (predictions.length === 0) {
            console.log("No stored predictions found for this user.");
        } else {
            console.log("Stored Predictions:", predictions.map((p, index) => ({
                index,
                age: Number(p[0]),
                sex: Number(p[1]) === 1 ? "Male" : "Female",
                cp: Number(p[2]),
                trestbps: Number(p[3]),
                chol: Number(p[4]),
                fbs: Number(p[5]) === 1 ? "High (>120mg/dl)" : "Normal",
                restecg: Number(p[6]),
                thalach: Number(p[7]),
                exang: Number(p[8]) === 1 ? "Yes" : "No",
                oldpeak: Number(p[9]),
                slope: Number(p[10]),
                ca: Number(p[11]),
                thal: Number(p[12]),
                timestamp: new Date(Number(p[13]) * 1000).toLocaleString(),
                prediction: Number(p[14]) === 1 ? "Heart Disease Detected" : "No Heart Disease"
            })));
        }
    } catch (error) {
        console.error("Error fetching predictions:", error);
    }
}

main();
