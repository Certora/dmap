const { ethers } = require("hardhat");
const { want } = require('minihat')
const {hexZeroPad} = require("@ethersproject/bytes");
const lib = require('../../dmap')

function padRight(addrStr) {
    const numBits = 256 - 160
    const hexstr = ethers.BigNumber.from(addrStr).shl(numBits).toHexString()
    return hexZeroPad(hexstr, 32);
}

async function check_gas (gas, minGas, maxGas) {
  await want(gas.toNumber()).to.be.at.most(maxGas);
  if( gas.toNumber() < minGas ) {
    console.log("gas reduction: previous min=", minGas, " gas used=", gas.toNumber());
  }
}


let testlib = {}
testlib.get = async (dmap, slot) => {
    // like lib.get, but calls dmap instead of direct storage access
    const pairabi = ["function pair(bytes32) returns (bytes32 meta, bytes32 data)"]
    const iface = new ethers.utils.Interface(pairabi)
    const calldata = iface.encodeFunctionData("pair", [slot])
    const resdata = await dmap.signer.call({to: dmap.address, data: calldata})
    const res = iface.decodeFunctionResult("pair", resdata)
    want(res).to.eql(await lib.get(dmap, slot))
    return res
}
// check that get, pair, and slot all return [meta, data]
const check_entry = async (dmap, usr, key, _meta, _data) => {
    const meta = typeof(_meta) == 'string' ? _meta : '0x'+_meta.toString('hex')
    const data = typeof(_data) == 'string' ? _data : '0x'+_data.toString('hex')
    const resZoneName = await lib.getByZoneAndName(dmap, usr, key)
    want(resZoneName[0]).to.eql(meta)
    want(resZoneName[1]).to.eql(data)
    want(resZoneName).to.eql([meta, data])

    const coder = ethers.utils.defaultAbiCoder
    const keccak256 = ethers.utils.keccak256
    const slot = keccak256(coder.encode(["address", "bytes32"], [usr, key]))
    const resGet = await testlib.get(dmap, slot)
    want(resGet[0]).to.eql(meta)
    want(resGet[1]).to.eql(data)
    want(resGet).to.eql([meta, data])

    const nextslot = ethers.utils.hexZeroPad(
        ethers.BigNumber.from(slot).add(1).toHexString(), 32
    )
    want(await lib.slot(dmap, slot)).to.eql(meta)
    want(await lib.slot(dmap, nextslot)).to.eql(data)
}


module.exports = { padRight, check_gas, check_entry, testlib }
