/// SPDX-License-Identifier: AGPL-3.0

// One day, someone is going to try very hard to prevent you
// from accessing one of these storage slots.

pragma solidity 0.8.13;

// interface Dmap {
//     // error LOCKED();
//     event Set(
//         address indexed zone,
//         bytes32 indexed name,
//         bytes32 indexed meta,
//         bytes32 indexed data
//     ) anonymous;

//     function set(bytes32 name, bytes32 meta, bytes32 data) external;
//     function get(bytes32 slot) external view returns (bytes32 meta, bytes32 data);
// }

contract _dmapSol_ {
    error LOCKED();
    event Set(
        address indexed zone,
        bytes32 indexed name,
        bytes32 indexed meta,
        bytes32 indexed data
    ) anonymous;
    uint256 constant LOCK = 0x1;
    uint256 lock;
    uint256 rootZone;
    mapping(bytes32 => bytes32) dns;

    constructor(address root) { 
        lock = LOCK;
        rootZone = uint256(uint160(root)) * 2**96;
    }

    function set(bytes32 name, bytes32 meta, bytes32 data) external {
        
        uint256 zone = uint256(uint160(msg.sender));

        bytes32 slot = keccak256(abi.encodePacked(zone, name));
        
        // event for setting a new slot
        emit Set(msg.sender, name, meta, data);
        // storing data in slot+1
        dns[bytes32(uint256(slot)+1)] = data;

        // getting value of meta stored in the slot
        bytes32 metaBefore = dns[slot];
        // checking value of meta to see if the slot if already locked
        if(uint256(metaBefore) & LOCK == 0)
        {
        // storing meta in the slot
        dns[slot] = meta;
        } 
        // revert for an already locked slot
        else revert LOCKED();
    }

    function get(bytes32 slot) external view returns(bytes32 meta, bytes32 data){
        // retrieving the value of meta and data from the supplied slot
        meta = dns[slot];
        data = dns[bytes32(uint256(slot)+1)];
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
}
