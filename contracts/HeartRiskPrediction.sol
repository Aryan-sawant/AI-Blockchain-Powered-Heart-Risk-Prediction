// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HeartRiskPrediction {
    struct Prediction {
        uint256 age;
        uint8 sex;
        uint8 cp;
        uint256 trestbps;
        uint256 chol;
        uint8 fbs;
        uint8 restecg;
        uint256 thalach;
        uint8 exang;
        uint256 oldpeak;
        uint8 slope;
        uint8 ca;
        uint8 thal;
        uint256 timestamp;
        uint8 prediction;
    }

    address public owner;
    mapping(address => Prediction[]) private userPredictions;

    event NewPrediction(address indexed user, uint8 prediction, uint256 timestamp);

    constructor() {
        owner = msg.sender;
    }

    function storePrediction(
        uint256 age,
        uint8 sex,
        uint8 cp,
        uint256 trestbps,
        uint256 chol,
        uint8 fbs,
        uint8 restecg,
        uint256 thalach,
        uint8 exang,
        uint256 oldpeak,
        uint8 slope,
        uint8 ca,
        uint8 thal,
        uint8 prediction
    ) public {
        require(prediction == 0 || prediction == 1, "Invalid prediction value");

        userPredictions[msg.sender].push(Prediction({
            age: age,
            sex: sex,
            cp: cp,
            trestbps: trestbps,
            chol: chol,
            fbs: fbs,
            restecg: restecg,
            thalach: thalach,
            exang: exang,
            oldpeak: oldpeak,
            slope: slope,
            ca: ca,
            thal: thal,
            timestamp: block.timestamp,
            prediction: prediction
        }));

        emit NewPrediction(msg.sender, prediction, block.timestamp);
    }

    function getPredictionCount(address user) public view returns (uint256) {
        return userPredictions[user].length;
    }

    function getPrediction(address user, uint256 index)
        public
        view
        returns (
            uint256 age, uint8 sex, uint8 cp, uint256 trestbps, uint256 chol, uint8 fbs,
            uint8 restecg, uint256 thalach, uint8 exang, uint256 oldpeak, uint8 slope,
            uint8 ca, uint8 thal, uint8 prediction, uint256 timestamp
        )
    {
        require(index < userPredictions[user].length, "Invalid index");
        Prediction memory p = userPredictions[user][index];
        return (p.age, p.sex, p.cp, p.trestbps, p.chol, p.fbs, p.restecg, p.thalach, p.exang, p.oldpeak, p.slope, p.ca, p.thal, p.prediction, p.timestamp);
    }

    function getAllPredictions(address user) public view returns (Prediction[] memory) {
        return userPredictions[user];
    }

    function getMyPredictions() public view returns (Prediction[] memory) {
        return userPredictions[msg.sender];
    }
}
