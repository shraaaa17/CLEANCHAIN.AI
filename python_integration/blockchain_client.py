"""
CleanChain Blockchain Client
Python integration module for interacting with CleanChain smart contracts
using Web3.py
"""

import os
import json
from typing import Dict, List, Optional, Tuple
from web3 import Web3
from eth_typing import ChecksumAddress
from web3.contract import ContractFunction
from web3.exceptions import ContractNotFound

# Load environment variables
from dotenv import load_dotenv

load_dotenv()


class CleanChainClient:
    """
    Client for interacting with CleanChain smart contracts on Polygon Amoy
    """
    
    def __init__(
        self,
        rpc_url: Optional[str] = None,
        private_key: Optional[str] = None,
        contract_addresses: Optional[Dict[str, str]] = None
    ):
        """
        Initialize the CleanChain blockchain client
        
        Args:
            rpc_url: Polygon Amoy RPC URL (defaults to env var POLYGON_AMOY_RPC_URL)
            private_key: Wallet private key (defaults to env var PRIVATE_KEY)
            contract_addresses: Dict with contract addresses. 
                              If None, loads from contract-addresses.json
        """
        # Set up Web3 connection
        self.rpc_url = rpc_url or os.getenv("POLYGON_AMOY_RPC_URL")
        if not self.rpc_url:
            raise ValueError("RPC URL is required. Set POLYGON_AMOY_RPC_URL or pass as parameter")
        
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        if not self.w3.isConnected():
            raise ConnectionError(f"Failed to connect to {self.rpc_url}")
        
        print(f"✅ Connected to Polygon Amoy: {self.w3.eth.chain_id}")
        
        # Set up account
        self.private_key = private_key or os.getenv("PRIVATE_KEY")
        if self.private_key:
            self.account = self.w3.eth.account.from_key(self.private_key)
            print(f"✅ Wallet loaded: {self.account.address}")
        else:
            self.account = None
            print("⚠️ No private key provided. Read-only mode.")
        
        # Load contract addresses
        if contract_addresses:
            self.contract_addresses = contract_addresses
        else:
            self.contract_addresses = self._load_contract_addresses()
        
        # Load ABIs
        self.contracts = self._load_contracts()
    
    def _load_contract_addresses(self) -> Dict[str, str]:
        """Load contract addresses from JSON file"""
        path = os.path.join(os.path.dirname(__file__), "..", "contract-addresses.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        raise FileNotFoundError("Contract addresses file not found. Run deployment first.")
    
    def _load_contracts(self) -> Dict:
        """Load contract ABIs and create contract instances"""
        contracts = {}
        abi_dir = os.path.join(os.path.dirname(__file__), "..", "abi")
        
        contract_names = ["NGORegistry", "CSREscrow", "ImpactVerification"]
        
        for name in contract_names:
            abi_path = os.path.join(abi_dir, f"{name}.json")
            if os.path.exists(abi_path):
                with open(abi_path, "r") as f:
                    abi = json.load(f)
                
                address = self.contract_addresses.get(name)
                if address:
                    contracts[name] = self.w3.eth.contract(
                        address=Web3.toChecksumAddress(address),
                        abi=abi
                    )
            else:
                print(f"⚠️ ABI file not found: {abi_path}")
        
        return contracts
    
    def _get_explorer_url(self, tx_hash: str) -> str:
        """Get Polygonscan explorer URL for transaction"""
        return f"https://amoy.polygonscan.com/tx/{tx_hash}"
    
    def _send_transaction(self, func: ContractFunction, gas_limit: int = 500000) -> Dict:
        """Send a transaction and return receipt"""
        if not self.account:
            raise ValueError("Private key required for transactions")
        
        # Build transaction
        tx = func.buildTransaction({
            "from": self.account.address,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "gas": gas_limit,
            "gasPrice": self.w3.eth.gas_price,
            "chainId": self.w3.eth.chain_id
        })
        
        # Sign transaction
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        
        # Send transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Wait for receipt
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "transaction_hash": receipt.transactionHash.hex(),
            "block_number": receipt.blockNumber,
            "gas_used": receipt.gasUsed,
            "status": receipt.status,
            "explorer_url": self._get_explorer_url(receipt.transactionHash.hex())
        }
    
    # ==================== NGO Registry Functions ====================
    
    def register_ngo(self, ngo_address: str) -> Dict:
        """
        Register an NGO on the blockchain
        
        Args:
            ngo_address: Wallet address of the NGO
            
        Returns:
            Transaction receipt with hash, block number, and explorer URL
        """
        ngo_address = Web3.toChecksumAddress(ngo_address)
        func = self.contracts["NGORegistry"].functions.registerNGO(ngo_address)
        return self._send_transaction(func)
    
    def approve_ngo(self, ngo_address: str) -> Dict:
        """
        Approve a registered NGO (only callable by admin)
        
        Args:
            ngo_address: Wallet address of the NGO to approve
            
        Returns:
            Transaction receipt with hash, block number, and explorer URL
        """
        ngo_address = Web3.toChecksumAddress(ngo_address)
        func = self.contracts["NGORegistry"].functions.approveNGO(ngo_address)
        return self._send_transaction(func)
    
    def reject_ngo(self, ngo_address: str) -> Dict:
        """
        Reject a registered NGO (only callable by admin)
        
        Args:
            ngo_address: Wallet address of the NGO to reject
            
        Returns:
            Transaction receipt with hash, block number, and explorer URL
        """
        ngo_address = Web3.toChecksumAddress(ngo_address)
        func = self.contracts["NGORegistry"].functions.rejectNGO(ngo_address)
        return self._send_transaction(func)
    
    def is_verified(self, ngo_address: str) -> bool:
        """
        Check if an NGO is verified
        
        Args:
            ngo_address: Wallet address of the NGO
            
        Returns:
            True if the NGO is verified
        """
        ngo_address = Web3.toChecksumAddress(ngo_address)
        return self.contracts["NGORegistry"].functions.isVerified(ngo_address).call()
    
    def is_registered(self, ngo_address: str) -> bool:
        """
        Check if an NGO is registered
        
        Args:
            ngo_address: Wallet address of the NGO
            
        Returns:
            True if the NGO is registered
        """
        ngo_address = Web3.toChecksumAddress(ngo_address)
        return self.contracts["NGORegistry"].functions.isRegistered(ngo_address).call()
    
    # ==================== CSR Escrow Functions ====================
    
    def create_campaign(
        self,
        ngo_address: str,
        required_score: int
    ) -> Dict:
        """
        Create a new CSR campaign (only callable by admin)
        
        Args:
            ngo_address: Wallet address of the NGO
            required_score: Minimum score required for fund release
            
        Returns:
            Transaction receipt with hash, block number, and explorer URL
        """
        ngo_address = Web3.toChecksumAddress(ngo_address)
        func = self.contracts["CSREscrow"].functions.createCampaign(ngo_address, required_score)
        return self._send_transaction(func)
    
    def deposit_funds(self, campaign_id: int, amount_wei: int) -> Dict:
        """
        Deposit CSR funds into a campaign
        
        Args:
            campaign_id: ID of the campaign
            amount_wei: Amount in wei to deposit
            
        Returns:
            Transaction receipt with hash, block number, and explorer URL
        """
        func = self.contracts["CSREscrow"].functions.depositFunds(campaign_id)
        tx = func.buildTransaction({
            "from": self.account.address,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "gas": 500000,
            "gasPrice": self.w3.eth.gas_price,
            "chainId": self.w3.eth.chain_id,
            "value": amount_wei
        })
        
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "transaction_hash": receipt.transactionHash.hex(),
            "block_number": receipt.blockNumber,
            "gas_used": receipt.gasUsed,
            "status": receipt.status,
            "explorer_url": self._get_explorer_url(receipt.transactionHash.hex())
        }
    
    def release_funds(self, campaign_id: int) -> Dict:
        """
        Release funds to NGO after verification (only callable by admin)
        
        Args:
            campaign_id: ID of the campaign
            
        Returns:
            Transaction receipt with hash, block number, and explorer URL
        """
        func = self.contracts["CSREscrow"].functions.releaseFunds(campaign_id)
        return self._send_transaction(func)
    
    def get_campaign(self, campaign_id: int) -> Dict:
        """
        Get campaign details
        
        Args:
            campaign_id: ID of the campaign
            
        Returns:
            Dict with campaign details
        """
        result = self.contracts["CSREscrow"].functions.getCampaign(campaign_id).call()
        return {
            "ngo_address": result[0],
            "fund_amount": result[1],
            "required_score": result[2],
            "is_released": result[3]
        }
    
    def get_contract_balance(self) -> int:
        """
        Get the contract's MATIC balance
        
        Returns:
            Contract balance in wei
        """
        return self.w3.eth.get_balance(self.contract_addresses["CSREscrow"])
    
    # ==================== Impact Verification Functions ====================
    
    def log_impact(
        self,
        event_id: str,
        cleanliness_score: int,
        ipfs_hash: str,
        ngo_address: str
    ) -> Dict:
        """
        Log impact proof from cleaning drive (only callable by admin)
        
        Args:
            event_id: Unique identifier for the cleaning event
            cleanliness_score: AI-generated cleanliness score (0-100)
            ipfs_hash: IPFS hash of the proof images
            ngo_address: Wallet address of the NGO
            
        Returns:
            Transaction receipt with hash, block number, and explorer URL
        """
        ngo_address = Web3.toChecksumAddress(ngo_address)
        func = self.contracts["ImpactVerification"].functions.logImpact(
            event_id,
            cleanliness_score,
            ipfs_hash,
            ngo_address
        )
        return self._send_transaction(func)
    
    def get_impact_record(self, event_id: str) -> Dict:
        """
        Get impact record by event ID
        
        Args:
            event_id: Unique identifier for the cleaning event
            
        Returns:
            Dict with impact record details
        """
        result = self.contracts["ImpactVerification"].functions.getImpactRecord(event_id).call()
        return {
            "event_id": result[0],
            "cleanliness_score": result[1],
            "ipfs_hash": result[2],
            "ngo": result[3],
            "timestamp": result[4]
        }
    
    def impact_record_exists(self, event_id: str) -> bool:
        """
        Check if an impact record exists
        
        Args:
            event_id: Unique identifier for the cleaning event
            
        Returns:
            True if the record exists
        """
        return self.contracts["ImpactVerification"].functions.impactRecordExists(event_id).call()
    
    def get_total_impacts(self) -> int:
        """
        Get total number of recorded impacts
        
        Returns:
            Total count of impact records
        """
        return self.contracts["ImpactVerification"].functions.getTotalImpacts().call()
    
    # ==================== Utility Functions ====================
    
    def get_wallet_balance(self, address: str = None) -> int:
        """
        Get MATIC balance of a wallet
        
        Args:
            address: Wallet address (defaults to loaded account)
            
        Returns:
            Balance in wei
        """
        if address:
            address = Web3.toChecksumAddress(address)
        else:
            address = self.account.address
        return self.w3.eth.get_balance(address)
    
    def get_transaction_receipt(self, tx_hash: str) -> Dict:
        """
        Get transaction receipt
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            Transaction receipt
        """
        return self.w3.eth.get_transaction_receipt(tx_hash)


# ==================== Convenience Functions ====================

def create_client() -> CleanChainClient:
    """Create a CleanChain client with default settings"""
    return CleanChainClient()


# Example usage
if __name__ == "__main__":
    # Create client
    client = CleanChainClient()
    
    print("\n" + "="*50)
    print("CleanChain Blockchain Client")
    print("="*50)
    
    # Print contract addresses
    print("\n📋 Contract Addresses:")
    for name, address in client.contract_addresses.items():
        print(f"  - {name}: {address}")
    
    # Get wallet balance
    if client.account:
        balance = client.get_wallet_balance()
        print(f"\n💰 Wallet Balance: {client.w3.fromWei(balance, 'ether')} MATIC")
    
    # Get contract balance
    escro_balance = client.get_contract_balance()
    print(f"💰 Escrow Balance: {client.w3.fromWei(escro_balance, 'ether')} MATIC")
