const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {

  console.log("\n🚀 Deploying CleanChain Contracts...\n");

  const [deployer] = await hre.ethers.getSigners();

  console.log("Deploying with account:", deployer.address);

  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", hre.ethers.formatEther(balance), "ETH");


  /*
  ===============================
  1️⃣ Deploy NGORegistry
  ===============================
  */

  console.log("\nDeploying NGORegistry...");

  const NGORegistry = await hre.ethers.getContractFactory("NGORegistry");
  const ngoRegistry = await NGORegistry.deploy();

  await ngoRegistry.waitForDeployment();

  const ngoRegistryAddress = await ngoRegistry.getAddress();

  console.log("✅ NGORegistry deployed to:", ngoRegistryAddress);



  /*
  ===============================
  2️⃣ Deploy ImpactVerification
  ===============================
  */

  console.log("\nDeploying ImpactVerification...");

  const ImpactVerification = await hre.ethers.getContractFactory("ImpactVerification");
  const impactVerification = await ImpactVerification.deploy();

  await impactVerification.waitForDeployment();

  const impactAddress = await impactVerification.getAddress();

  console.log("✅ ImpactVerification deployed to:", impactAddress);



  /*
  ===============================
  3️⃣ Deploy CSREscrow
  ===============================
  */

  console.log("\nDeploying CSREscrow...");

  const CSREscrow = await hre.ethers.getContractFactory("CSREscrow");

  // Pass NGORegistry address to constructor
  const csrEscrow = await CSREscrow.deploy(ngoRegistryAddress);

  await csrEscrow.waitForDeployment();

  const escrowAddress = await csrEscrow.getAddress();

  console.log("✅ CSREscrow deployed to:", escrowAddress);



  /*
  ===============================
  Save Contract Addresses
  ===============================
  */

  const addresses = {
    NGORegistry: ngoRegistryAddress,
    ImpactVerification: impactAddress,
    CSREscrow: escrowAddress,
    deployer: deployer.address,
    network: hre.network.name
  };

  const addressesPath = path.join(__dirname, "../contract-addresses.json");

  fs.writeFileSync(
    addressesPath,
    JSON.stringify(addresses, null, 2)
  );

  console.log("\n📄 Contract addresses saved to contract-addresses.json");



  /*
  ===============================
  Export ABIs
  ===============================
  */

  console.log("\n📦 Exporting ABIs...");

  const abiDir = path.join(__dirname, "../abi");

  if (!fs.existsSync(abiDir)) {
    fs.mkdirSync(abiDir);
  }

  const contractNames = ["NGORegistry", "CSREscrow", "ImpactVerification"];

  for (const name of contractNames) {

    const artifact = await hre.artifacts.readArtifact(name);

    const abiPath = path.join(abiDir, `${name}.json`);

    fs.writeFileSync(
      abiPath,
      JSON.stringify(artifact.abi, null, 2)
    );

    console.log(`✅ ABI exported: ${name}.json`);
  }


  console.log("\n🎉 Deployment Completed Successfully!\n");

  console.log("Contract Addresses:");
  console.log("---------------------------");
  console.log("NGORegistry:", ngoRegistryAddress);
  console.log("ImpactVerification:", impactAddress);
  console.log("CSREscrow:", escrowAddress);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});