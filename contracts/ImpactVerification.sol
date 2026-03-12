// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title ImpactVerification
 * @dev Contract for logging and verifying cleaning drive impact
 */
contract ImpactVerification {
    // Admin address (corporate or platform authority)
    address public admin;
    
    // Impact record structure
    struct ImpactRecord {
        string eventId;
        uint256 cleanlinessScore;
        string ipfsHash;
        address ngo;
        uint256 timestamp;
        bool exists;
    }
    
    // Mapping of event ID to Impact Record
    mapping(string => ImpactRecord) public impactRecords;
    
    // Array to track all event IDs
    string[] public eventIds;
    
    // Events
    event ImpactLogged(
        string indexed eventId,
        uint256 cleanlinessScore,
        string ipfsHash,
        address indexed ngo,
        uint256 timestamp
    );
    
    // Modifier to check if caller is admin
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }
    
    constructor() {
        admin = msg.sender;
    }
    
    /**
     * @dev Log impact proof from cleaning drive
     * @param eventId Unique identifier for the cleaning event
     * @param cleanlinessScore AI-generated cleanliness score (0-100)
     * @param ipfsHash IPFS hash of the proof images
     * @param ngo The NGO wallet address that performed the cleaning
     */
    function logImpact(
        string memory eventId,
        uint256 cleanlinessScore,
        string memory ipfsHash,
        address ngo
    ) external onlyAdmin {
        require(bytes(eventId).length > 0, "Event ID cannot be empty");
        require(cleanlinessScore <= 100, "Score must be between 0 and 100");
        require(bytes(ipfsHash).length > 0, "IPFS hash cannot be empty");
        require(ngo != address(0), "Invalid NGO address");
        require(!impactRecords[eventId].exists, "Event ID already exists");
        
        impactRecords[eventId] = ImpactRecord({
            eventId: eventId,
            cleanlinessScore: cleanlinessScore,
            ipfsHash: ipfsHash,
            ngo: ngo,
            timestamp: block.timestamp,
            exists: true
        });
        
        eventIds.push(eventId);
        
        emit ImpactLogged(eventId, cleanlinessScore, ipfsHash, ngo, block.timestamp);
    }
    
    /**
     * @dev Get impact record by event ID
     * @param eventId The unique identifier for the cleaning event
     * @return eventId, cleanlinessScore, ipfsHash, ngo, timestamp
     */
    function getImpactRecord(string memory eventId) external view returns (
        string memory,
        uint256,
        string memory,
        address,
        uint256
    ) {
        ImpactRecord memory record = impactRecords[eventId];
        require(record.exists, "Impact record does not exist");
        
        return (
            record.eventId,
            record.cleanlinessScore,
            record.ipfsHash,
            record.ngo,
            record.timestamp
        );
    }
    
    /**
     * @dev Check if an impact record exists
     * @param eventId The unique identifier for the cleaning event
     * @return bool True if the record exists
     */
    function impactRecordExists(string memory eventId) external view returns (bool) {
        return impactRecords[eventId].exists;
    }
    
    /**
     * @dev Get total number of recorded impacts
     * @return uint256 Total count of impact records
     */
    function getTotalImpacts() external view returns (uint256) {
        return eventIds.length;
    }
    
    /**
     * @dev Get all event IDs (for iterating)
     * @return string[] Array of all event IDs
     */
    function getAllEventIds() external view returns (string[] memory) {
        return eventIds;
    }
}
