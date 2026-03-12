const hre = require("hardhat");

async function main() {

  const [deployer] = await hre.ethers.getSigners();

  console.log("Testing with account:", deployer.address);

  // Load deployed contract
  const addresses = require("../contract-addresses.json");

  const NGORegistry = await hre.ethers.getContractFactory("NGORegistry");

  const ngoRegistry = NGORegistry.attach(addresses.NGORegistry);


  // Call registerNGO function
  const tx = await ngoRegistry.registerNGO(
    "Clean India NGO",
    "Mumbai"
  );

  await tx.wait();

  console.log("NGO registered successfully");

}
const ngo = await ngoRegistry.ngos(deployer.address);

console.log("NGO Name:", ngo.name);
console.log("Location:", ngo.location);
console.log("Registered:", ngo.isRegistered);

const ImpactVerification = await hre.ethers.getContractFactory("ImpactVerification");

const verifier = ImpactVerification.attach(addresses.ImpactVerification);

const tx2 = await verifier.submitImpactScore(1, 85);

await tx2.wait();

console.log("Impact score submitted");

const CSREscrow = await hre.ethers.getContractFactory("CSREscrow");

const escrow = CSREscrow.attach(addresses.CSREscrow);

const tx3 = await escrow.depositFunds(1, {
  value: hre.ethers.parseEther("1")
});

await tx3.wait();

console.log("CSR funds deposited");

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
