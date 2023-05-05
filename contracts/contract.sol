// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract votertransparency {
    // Struct for storing voter data
        string voterId;
        string fingerprintHash;
        string photo;

    
    function collectVoterID(string memory voterId_) public {
        voterId = voterId_;
    }

    function collectFingerprintHash(string memory fingerprintHash_) public {
        fingerprintHash = fingerprintHash_;
    }

    function collectPhoto(string memory photo_) public {
        photo = photo_;
    }


    function getVoterID() public view returns (string memory) {
        return voterId;
    }

    function getFingerprintHash() public view returns (string memory) {
        return fingerprintHash;
    }

    function getPhoto() public view returns (string memory) {
        return photo;
    }
}

