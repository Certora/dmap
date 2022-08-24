/// SPDX-License-Identifier: AGPL-3.0



pragma solidity 0.8.13;

import {_dmap_} from "../../core/dmap.sol";

contract dmapHarness is _dmap_ {
    constructor(address rootzone) _dmap_(rootzone) {}
    function getMetaData (bytes32 slot) external returns(bytes32 meta, bytes32 data)
    { assembly{
                // let x := mload(64)
                // mstore(0, sload(calldataload(4)))
                mstore(0, sload(calldataload(4)))
                // mstore(0, sload(slot))
                // mstore(add(x,32), sload(add(1, calldataload(4))))
                mstore(32, sload(add(1, calldataload(4))))
                // mstore(add(x,32), sload(add(1, slot)))
                // return(x, 64)
                return(0, 64) 
            }
    }

    function setStore(bytes32 slot, bytes32 meta, bytes32 data) external {
        assembly{
        sstore(slot, meta)
        sstore(add(1,slot), data)
    }}

    function slotCal (address zone, bytes32 name) external pure returns(bytes32 slot) {
    assembly{
        // let x := mload(64)
        // let Zone := calldataload(4)
        // let Name := calldataload(36)
        // mstore(0x40, Zone)
        // mstore(add(0x40,32), Name)

        // let x := mload(64)
        // mstore(x, zone)
        // mstore(add(x,32), name)
        mstore(0, zone)
        mstore(32, name)

        // slot := keccak256(0,64)
        mstore(64, keccak256(0,64)) //storing hash in memory for better readability
        return(64,32) // returning hash from memory
    }
    }

    
    function set (bytes32 nameArg, bytes32 metaArg, bytes32 dataArg) external {
        assembly{
        let name := calldataload(4)
        let meta := calldataload(36)
        let data := calldataload(68)
        mstore(0, caller())
        mstore(32, name)
        let slot := keccak256(0, 64)
        // mstore(64,keccak256(0, 64)) //hash stored in memory for readability
        log4(0, 0, caller(), name, meta, data)
        sstore(add(slot, 1), data)
        // sstore(add(mload(64), 1), data) //loading hash from memory
        if iszero(or(xor(100, calldatasize()), and(LOCK, sload(slot)))) {
        // if iszero(or(xor(100, calldatasize()), and(LOCK, sload(mload(64))))) { //loading hash from memory
            sstore(slot, meta)
            // sstore(mload(64), meta)
            return(0, 0)
        }
        if eq(100, calldatasize()) {
            mstore(0, shl(224, 0xa1422f69))
            revert(0, 4)
        }
        revert(0, 0)

    }  
    }
    // fallback() external payable { assembly {
    //     if eq(36, calldatasize()) {
    //         mstore(0, sload(calldataload(4)))
    //         mstore(32, sload(add(1, calldataload(4))))
    //         return(0, 64)
    //     }
    //     let name := calldataload(4)
    //     let meta := calldataload(36)
    //     let data := calldataload(68)
    //     mstore(0, caller())
    //     mstore(32, name)
    //     let slot := keccak256(0, 64)
    //     log4(0, 0, caller(), name, meta, data)
    //     sstore(add(slot, 1), data)
    //     if iszero(or(xor(100, calldatasize()), and(LOCK, sload(slot)))) {
    //         sstore(slot, meta)
    //         return(0, 0)
    //     }
    //     if eq(100, calldatasize()) {
    //         mstore(0, shl(224, 0xa1422f69))
    //         revert(0, 4)
    //     }
    //     revert(0, 0)
    // }}


    // function testHarnessFunction(uint120 x, uint120 y) external pure returns(uint120 z){
    //     z=x+y;
    // }

    // bytes32 nameGlobal;
    // bytes32 metaGlobal;
    // bytes32 dataGlobal;

    // function checkArgs(bytes32 name, bytes32 meta, bytes32 data) public {
    //     nameGlobal = name;
    //     metaGlobal = meta;
    //     dataGlobal = data;
    // }
    function unpackArgs(bytes32 name, bytes32 meta, bytes32 data) public pure returns(bytes32 Name, bytes32 Meta, bytes32 Data){
        Name = name;
        Meta = meta;
        Data = data;
    }
    // function getName() public view returns(bytes32) {
    //     return nameGlobal;
    // }

    // function getMeta() public view returns(bytes32) {
    //     return metaGlobal;
    // }

    // function getData() public view returns(bytes32) {
    //     return dataGlobal;
    // }

    // function calculateSlot(address zone, bytes32 name) external pure returns(bytes32 slot){
    //     slot = keccak256(zone, name);
    // }
    
    // function setCall(bytes32 name, bytes32 meta, bytes32 data) external {
    //     this.set(name, meta, data);
    // }

    
}
