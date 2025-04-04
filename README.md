# AI-Powered Heart Risk Prediction with Blockchain and Generative AI

## Overview

This project demonstrates an end-to-end system for predicting heart disease risk using Machine Learning, storing prediction records immutably on the Polygon blockchain, visualizing historical trends, and generating personalized health action plans using Google's Gemini 2.0 Flash generative AI model.

The system integrates a highly accurate AI model (~99%), leverages blockchain for data integrity and transparency, provides an interactive dashboard for user insights, and delivers actionable health advice tailored to the prediction outcome.

**Repository Link:** [https://github.com/Aryan-sawant/AI-Blockchain-Powered-Heart-Risk-Prediction.git](https://github.com/Aryan-sawant/AI-Blockchain-Powered-Heart-Risk-Prediction.git)

## Key Features

*   **High-Accuracy Prediction:** Utilizes an optimized Random Forest Classifier (~99% accuracy) trained on standard heart disease datasets.
*   **AI Model API:** Flask-based API serves real-time predictions.
*   **Immutable Record Keeping:** Stores the *full prediction record* (input features, prediction outcome, timestamp) on the Polygon (Amoy Testnet) blockchain using a Solidity smart contract.
*   **Data Transparency & History:** Allows users to retrieve and view their complete, timestamped prediction history from the blockchain.
*   **Interactive Dashboard:** Streamlit application provides a user-friendly interface for inputting data, viewing predictions, and analyzing trends.
*   **Advanced Visualizations:** Uses Plotly for interactive charts including:
    *   Risk Trend Over Time (Line Chart)
    *   Prediction Distribution (Pie Chart)
    *   Feature Distributions (Histograms, Box Plot)
    *   Feature Correlation (Heatmap)
*   **Personalized Health Plans:** Integrates Google Gemini 2.0 Flash to generate tailored, actionable health advice based on the user's specific prediction result (Heart Disease Detected / No Heart Disease).
*   **Enhanced UI/UX:** Custom CSS styling for a professional and engaging user experience.

## Technology Stack

*   **Backend & AI:**
    *   Python 3.9+
    *   Flask (API Framework)
    *   Scikit-learn (Machine Learning Model - RandomForestClassifier, StandardScaler)
    *   Pandas, Numpy (Data Handling)
    *   Pickle (Model Serialization)
    *   Google Generative AI SDK (`google-generativeai`)
    *   Optuna (Hyperparameter Optimization - during development)
*   **Blockchain:**
    *   Solidity (Smart Contract Language)
    *   Hardhat (Development & Deployment Framework)
    *   Ethers.js (Blockchain Interaction in Scripts)
    *   Polygon (Amoy Testnet)
    *   Alchemy (Blockchain Node Provider)
    *   web3.py (Python Blockchain Interaction)
*   **Frontend & Visualization:**
    *   Streamlit (Web Application Framework)
    *   Plotly (Interactive Charting)
*   **Environment Management:**
    *   `virtualenv` / `conda`
    *   `npm` (for Hardhat)
    *   `dotenv` (Environment Variable Management)

## System Architecture / Workflow

1.  **User Input:** User enters 13 medical parameters via the Streamlit interface.
2.  **API Prediction:** Streamlit sends data to the Flask API (`/predict`).
3.  **AI Model Inference:** Flask API preprocesses the input (scaling) and uses the loaded Random Forest model to generate a prediction (text + probability).
4.  **Display Prediction:** Streamlit displays the prediction result and probability.
5.  **Generate Health Plan:** Based on the prediction outcome (0 or 1), Streamlit prompts the Gemini 2.0 Flash API to generate personalized health advice.
6.  **Display Health Plan:** Streamlit shows the AI-generated advice.
7.  **(Optional) Store on Blockchain:** User clicks "Store". Streamlit uses `web3.py` to call the `storePrediction` function on the deployed Polygon smart contract, sending the full input data and prediction result.
8.  **(Optional) View History:** User clicks "View Trends". Streamlit uses `web3.py` to fetch all historical prediction records for the user from the smart contract and displays them in a table and interactive Plotly charts.

## Prerequisites

*   Python 3.9 or higher
*   Node.js and npm (for Hardhat)
*   MetaMask browser extension (or other wallet management for private key handling)
*   An Alchemy account and API Key for Polygon Amoy Testnet
*   A Google Cloud account with the Gemini API enabled and an API Key
*   Test MATIC tokens for the Polygon Amoy Testnet (obtainable from an Amoy Faucet)

## Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Aryan-sawant/AI-Blockchain-Powered-Heart-Risk-Prediction.git
    cd AI-Blockchain-Powered-Heart-Risk-Prediction
    ```

2.  **Backend API Setup:**
    ```bash
    cd api # Or wherever your Flask app resides
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    # Install necessary Python packages (check imports in api.py):
    pip install Flask scikit-learn pandas numpy python-dotenv pickle5 # Add any other required API dependencies
    # Ensure 'best_heart_disease_model.pkl' and the scaler .pkl are in this directory
    cd ..
    ```

3.  **Blockchain Smart Contract Setup:**
    ```bash
    cd blockchain # Or wherever your Hardhat project resides
    npm install
    # Compile the contract
    npx hardhat compile
    # Configure Hardhat network in hardhat.config.js (see below)
    # Deploy the contract to Amoy Testnet
    npx hardhat run scripts/deploy.js --network amoy
    # *** IMPORTANT: Note the deployed contract address printed in the console ***
    cd ..
    ```

4.  **Frontend Streamlit App Setup:**
    ```bash
    # Assuming streamlit_app.py is in the root or a specific frontend directory
    # cd frontend # If applicable
    python -m venv venv_streamlit # Use a different venv name if needed
    source venv_streamlit/bin/activate # On Windows use `venv_streamlit\Scripts\activate`
    # Install necessary Python packages (check imports in streamlit_app.py):
    pip install streamlit requests web3 pandas plotly python-dotenv google-generativeai # Add any other required Streamlit dependencies
    ```

## Configuration

1.  **Hardhat Configuration (`hardhat.config.js`):**
    Make sure your `hardhat.config.js` (likely within the `blockchain` directory) includes the Amoy network configuration using your Alchemy API Key and the private key of the account you want to deploy from. **Handle your private key securely (e.g., using environment variables)!**

    ```javascript
    require("@nomicfoundation/hardhat-toolbox");
    require("dotenv").config(); // If using dotenv for keys

    /** @type import('hardhat/config').HardhatUserConfig */
    module.exports = {
      solidity: "0.8.24", // Match your contract's pragma
      networks: {
        amoy: {
          url: `https://polygon-amoy.g.alchemy.com/v2/${process.env.ALCHEMY_API_KEY}`,
          accounts: [`0x${process.env.PRIVATE_KEY}`] // Ensure PRIVATE_KEY is loaded from .env
        }
      }
    };
    ```

2.  **Environment Variables (`.env` file):**
    Create a `.env` file in the root directory (or where your Streamlit app `streamlit_app.py` is located). Add the following variables:

    ```env
    # Blockchain Configuration
    ALCHEMY_API_KEY="YOUR_ALCHEMY_API_KEY"
    PRIVATE_KEY="YOUR_METAMASK_ACCOUNT_PRIVATE_KEY" # The private key used for signing transactions in Streamlit
    CONTRACT_ADDRESS="YOUR_DEPLOYED_CONTRACT_ADDRESS" # Address from Hardhat deployment step

    # Google Gemini Configuration
    GEMINI_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY"
    ```
    **WARNING:** Never commit your `.env` file or private keys directly to Git. Add `.env` to your `.gitignore` file.

## Running the Application

1.  **Start the Backend API:**
    ```bash
    cd api # Or backend directory
    source venv/bin/activate
    flask run # Or python api.py, depending on your setup
    # The API should now be running, typically on http://127.0.0.1:5000
    ```
    Keep this terminal open.

2.  **Start the Streamlit Frontend:**
    Open a *new* terminal. Navigate back to the main project directory if needed.
    ```bash
    # cd .. # If you were in the api directory
    source venv_streamlit/bin/activate # Activate the Streamlit environment
    streamlit run streamlit_app.py
    ```
    Streamlit will open the application in your default web browser.

## Usage

1.  Open the Streamlit application URL in your browser.
2.  Enter your medical details into the input form.
3.  Click the "**Predict Heart Disease Risk**" button.
    *   The application will call the Flask API.
    *   The prediction result ("Heart disease detected" or "No heart disease") and probability will be displayed.
    *   Personalized health advice generated by Gemini will appear below the prediction.
4.  **(Optional)** Click the "**Store on Blockchain**" button to save the current prediction record immutably to the Polygon Amoy Testnet. You'll need sufficient test MATIC in the account associated with your `PRIVATE_KEY` for gas fees. A transaction hash will be shown upon success.
5.  **(Optional)** Click the "**View Past Predictions & Trends**" button to fetch your historical data from the blockchain and view the visualizations.

## Smart Contract Details

*   **Contract Name:** `HeartRiskPrediction`
*   **File:** `blockchain/contracts/HeartRiskPrediction.sol` (adjust path if needed)
*   **Network:** Polygon Amoy Testnet
*   **Deployed Address:** `YOUR_DEPLOYED_CONTRACT_ADDRESS` (Replace with the actual address from deployment)
*   **ABI:** Located in `blockchain/artifacts/contracts/HeartRiskPrediction.sol/HeartRiskPrediction.json` (adjust path if needed). The Streamlit app uses `HeartRiskPredictionABI.json` (ensure this file exists, is correctly named, and matches the compiled ABI).

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests via the repository link provided above.
<!-- Add more specific contribution guidelines if desired -->

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
<!-- Create a LICENSE file with the MIT license text -->

## Acknowledgements

*   The dataset creators (if known).
*   Libraries/Frameworks used (Flask, Streamlit, Plotly, Scikit-learn, Hardhat, etc.).
*   Alchemy & Google Cloud for their services.
