/// SPDX-License-Identifier: AGPL-3.0



pragma solidity 0.8.13;

import {_dmapSol_} from "certora/contracts/dmapSol.sol";

contract dmapSolHarness is _dmapSol_ {
    constructor(address rootzone) _dmapSol_(rootzone) {}
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

        slot := keccak256(0,64)
        // mstore(64, keccak256(0,64)) //storing hash in memory for better readability
        return(64,32) // returning hash from memory
    }
    }

    
    
    function unpackArgs(bytes32 name, bytes32 meta, bytes32 data) public pure returns(bytes32 Name, bytes32 Meta, bytes32 Data){
        Name = name;
        Meta = meta;
        Data = data;
    }
    
}
