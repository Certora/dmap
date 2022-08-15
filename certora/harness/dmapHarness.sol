/// SPDX-License-Identifier: AGPL-3.0

// One day, someone is going to try very hard to prevent you
// from accessing one of these storage slots.

pragma solidity 0.8.13;

// import "../../core/dmap.sol";
interface Dmap {
    error LOCKED();
    event Set(
        address indexed zone,
        bytes32 indexed name,
        bytes32 indexed meta,
        bytes32 indexed data
    ) anonymous;

    function set(bytes32 name, bytes32 meta, bytes32 data) external;
    function get(bytes32 slot) external view returns (bytes32 meta, bytes32 data);
}

contract dmapHarness{
    error LOCKED();
    uint256 constant LOCK = 0x1;
    constructor(address rootzone) { assembly {
        sstore(0, LOCK)
        sstore(1, shl(96, rootzone))
    }}
    function get (bytes32 slot) external returns(uint256 meta, bytes32 data)
    { assembly{
                // let x := mload(64)
                mstore(0, sload(calldataload(4)))
                // mstore(0, sload(slot))
                mstore(32, sload(add(1, calldataload(4))))
                // mstore(add(x,32), sload(add(1, slot)))
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
    }
    }

    fallback() external payable { assembly {
        if eq(36, calldatasize()) {
            mstore(0, sload(calldataload(4)))
            mstore(32, sload(add(1, calldataload(4))))
            return(0, 64)
        }
        let name := calldataload(4)
        let meta := calldataload(36)
        let data := calldataload(68)
        mstore(0, caller())
        mstore(32, name)
        let slot := keccak256(0, 64)
        log4(0, 0, caller(), name, meta, data)
        sstore(add(slot, 1), data)
        if iszero(or(xor(100, calldatasize()), and(LOCK, sload(slot)))) {
            sstore(slot, meta)
            return(0, 0)
        }
        if eq(100, calldatasize()) {
            mstore(0, shl(224, 0xa1422f69))
            revert(0, 4)
        }
        revert(0, 0)
    }}


    // function testHarnessFunction(uint120 x, uint120 y) external pure returns(uint120 z){
    //     z=x+y;
    // }

    bytes32 nameGlobal;
    uint256 metaGlobal;
    bytes32 dataGlobal;

    function checkArgs(bytes32 name, uint256 meta, bytes32 data) public {
        nameGlobal = name;
        metaGlobal = meta;
        dataGlobal = data;
    }

    function getName() public returns(bytes32) {
        return nameGlobal;
    }

    function getMeta() public returns(uint256) {
        return metaGlobal;
    }

    function getData() public returns(bytes32) {
        return dataGlobal;
    }

    // function calculateSlot(address zone, bytes32 name) external pure returns(bytes32 slot){
    //     slot = keccak256(zone, name);
    // }
    
    // function setCall(bytes32 name, bytes32 meta, bytes32 data) external {
    //     this.set(name, meta, data);
    // }

    
}
