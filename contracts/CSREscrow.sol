// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./NGORegistry.sol";

/**
 * @title CSREscrow
 * @dev Contract for managing CSR fund escrow and releases
 */
contract CSREscrow {
    // Reference to NGO Registry contract
    NGORegistry public ngoRegistry;
    
    // Admin address (corporate or platform authority)
    address public admin;
    
    // Campaign structure
    struct Campaign {
        address ngoAddress;
        uint256 fundAmount;
        uint256 requiredScore;
        bool isReleased;
        bool isCreated;
    }
    
    // Mapping of campaign ID to Campaign
    mapping(uint256 => Campaign) public campaigns;
    
    // Counter for campaign IDs
    uint256 public campaignCount;
    
    // Events
    event CampaignCreated(uint256 indexed campaignId, address indexed ngo, uint256 requiredScore);
    event FundsDeposited(uint256 indexed campaignId, address indexed depositor, uint256 amount);
    event FundsReleased(uint256 indexed campaignId, address indexed ngo, uint256 amount);
    
    // Modifier to check if caller is admin
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }
    
    /**
     * @dev Constructor
     * @param _ngoRegistryAddress Address of the NGORegistry contract
     */
    constructor(address _ngoRegistryAddress) {
        require(_ngoRegistryAddress != address(0), "Invalid registry address");
        admin = msg.sender;
        ngoRegistry = NGORegistry(_ngoRegistryAddress);
    }
    
    /**
     * @dev Create a new CSR campaign
     * @param ngo The NGO wallet address
     * @param requiredScore Minimum score required for fund release
     * @return campaignId The ID of the created campaign
     */
    function createCampaign(address ngo, uint256 requiredScore) external onlyAdmin returns (uint256) {
        require(ngo != address(0), "Invalid NGO address");
        require(ngoRegistry.isVerified(ngo), "NGO not verified");
        
        campaignCount++;
        uint256 newCampaignId = campaignCount;
        
        campaigns[newCampaignId] = Campaign({
            ngoAddress: ngo,
            fundAmount: 0,
            requiredScore: requiredScore,
            isReleased: false,
            isCreated: true
        });
        
        emit CampaignCreated(newCampaignId, ngo, requiredScore);
        return newCampaignId;
    }
    
    /**
     * @dev Deposit CSR funds into a campaign
     * @param campaignId The ID of the campaign
     */
    function depositFunds(uint256 campaignId) external payable {
        require(campaigns[campaignId].isCreated, "Campaign does not exist");
        require(!campaigns[campaignId].isReleased, "Funds already released");
        require(msg.value > 0, "Must deposit some funds");
        
        campaigns[campaignId].fundAmount += msg.value;
        
        emit FundsDeposited(campaignId, msg.sender, msg.value);
    }
    
    /**
     * @dev Release funds to NGO after verification
     * @param campaignId The ID of the campaign
     */
    function releaseFunds(uint256 campaignId) external onlyAdmin {
        require(campaigns[campaignId].isCreated, "Campaign does not exist");
        require(!campaigns[campaignId].isReleased, "Funds already released");
        require(campaigns[campaignId].fundAmount > 0, "No funds to release");
        
        address ngo = campaigns[campaignId].ngoAddress;
        uint256 amount = campaigns[campaignId].fundAmount;
        
        campaigns[campaignId].isReleased = true;
        
        // Transfer funds to NGO
        payable(ngo).transfer(amount);
        
        emit FundsReleased(campaignId, ngo, amount);
    }
    
    
    function getCampaign(uint256 campaignId) external view returns (
        address ngoAddress,
        uint256 fundAmount,
        uint256 requiredScore,
        bool isReleased
    ) {
        Campaign memory c = campaigns[campaignId];
        return (c.ngoAddress, c.fundAmount, c.requiredScore, c.isReleased);
    }
    
    /**
     * @dev Get contract balance
     * @return The contract's MATIC balance
     */
    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
