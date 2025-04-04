require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config(); // Load environment variables

module.exports = {
  solidity: {
    version: "0.8.28",  // ✅ Match your contract's version
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,  // Adjust based on use case
      },
      viaIR: true,  // ✅ Enable Intermediate Representation (IR) optimization
    },
  },
  networks: {
    hardhat: {
      chainId: 31337  // Hardhat's default chain ID
    },
    amoy: {
      url: `https://polygon-amoy.g.alchemy.com/v2/${process.env.ALCHEMY_API_KEY}`,
      accounts: [process.env.PRIVATE_KEY], // ✅ No quotes, use directly
    },
  },
  etherscan: {
    apiKey: {
      polygonAmoy: "R6QI73UGF6QHYZ6QDH8WYPTWD9SBC5HEMX"
    }
  }
};
