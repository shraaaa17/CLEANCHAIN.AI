// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title NGORegistry
 * @dev Contract for verifying NGOs before they can receive CSR funds
 */
contract NGORegistry {
    // Admin address (corporate or platform authority)
    address public admin;
    
    // Mapping to track verified NGOs
    mapping(address => bool) public verifiedNGOs;
    
    // Mapping to track registered NGOs
    mapping(address => bool) public registeredNGOs;
    
    // Events
    event NGORegistered(address indexed ngo, uint256 timestamp);
    event NGOApproved(address indexed ngo, uint256 timestamp);
    event NGORejected(address indexed ngo, uint256 timestamp);
    
    // Modifier to check if caller is admin
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }
    
    constructor() {
        admin = msg.sender;
    }
    
    /**
     * @dev Register an NGO (submitted by NGO or admin)
     * @param ngo The wallet address of the NGO
     */
    function registerNGO(address ngo) external {
        require(ngo != address(0), "Invalid NGO address");
        require(!registeredNGOs[ngo], "NGO already registered");
        
        registeredNGOs[ngo] = true;
        emit NGORegistered(ngo, block.timestamp);
    }
    
    /**
     * @dev Approve a registered NGO (only by admin)
     * @param ngo The wallet address of the NGO to approve
     */
    function approveNGO(address ngo) external onlyAdmin {
        require(registeredNGOs[ngo], "NGO not registered");
        require(!verifiedNGOs[ngo], "NGO already verified");
        
        verifiedNGOs[ngo] = true;
        emit NGOApproved(ngo, block.timestamp);
    }
    
    /**
     * @dev Reject a registered NGO (only by admin)
     * @param ngo The wallet address of the NGO to reject
     */
    function rejectNGO(address ngo) external onlyAdmin {
        require(registeredNGOs[ngo], "NGO not registered");
        
        registeredNGOs[ngo] = false;
        verifiedNGOs[ngo] = false;
        emit NGORejected(ngo, block.timestamp);
    }
    
    /**
     * @dev Check if an NGO is verified
     * @param ngo The wallet address of the NGO
     * @return bool True if the NGO is verified
     */
    function isVerified(address ngo) external view returns (bool) {
        return verifiedNGOs[ngo];
    }
    
    /**
     * @dev Check if an NGO is registered
     * @param ngo The wallet address of the NGO
     * @return bool True if the NGO is registered
     */
    function isRegistered(address ngo) external view returns (bool) {
        return registeredNGOs[ngo];
    }
}
