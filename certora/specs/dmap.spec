 /******************************************************************
 * IMPORTS/SETUP                                                  *
 ******************************************************************/
// using rootHarness as root

methods {
	set(bytes32 name, bytes32 meta, bytes32 data)
    get(bytes32 slot) returns (uint256 meta, bytes32 data) envfree
	calculateSlot(address zone, bytes32 name) returns(bytes32 slot)envfree
}

definition LOCK() returns uint256 = 1;


 /******************************************************************
 * USEFUL CONSTRUCTS.                                             *
 ******************************************************************/


// uninterpreted functions, useful for describing contract state
ghost metaValue(address, bytes32) returns uint256{
    init_state axiom forall address z. forall bytes32 n. metaValue(z, n) == 0;
}

// hook Sstore meta [KEY address zone][KEY bytes32 name] uint256 meta(uint256 meta) STORAGE{

//     }

 /******************************************************************
 * RULES AND INVARIANTS:                                             *
 ******************************************************************/

// sanity
// rule sanity(method f)
rule sanity(method f)
{
	bytes32 name;
	bytes32 meta;
	bytes32 data;
	env e;
	calldataarg args;
    f(e, args);
	// checkArgs(e, args);
	// setCall(e, name, meta, data);
	assert false;
}


rule getTwice(bytes32 hash1, bytes32 hash2){

uint256 meta1;
bytes32 data1;
uint256 meta2;
bytes32 data2;
uint256 meta3;
bytes32 data3;

require hash1 != hash2;

meta1, data1 = get(hash1);
meta2, data2 = get(hash2);
meta3, data3 = get(hash2);


assert meta1 == meta2;
assert data1 == data2;
}


rule hashCalCheck(env e){
// address zone1;
// bytes32 name1;
// address zone2;
// bytes32 name2;
// require zone1 != zone2;
// bytes32 slot1 = slotCal(e, zone1, name1);
// bytes32 slot2 = slotCal(e, zone2, name2);
// // assert false;
// assert slot1 != slot2,"hash collision";
address zone1;
bytes32 name1;
address zone2;
bytes32 name2;
address zone3;
bytes32 name3;
// address zone2;
// bytes32 name2;
require zone1 != zone2 || name1 != name2;
bytes32 slot1 = slotCal(e, zone1, name1);
bytes32 slot2 = slotCal(e, zone2, name2);
bytes32 slot3 = slotCal(e, zone2, name2);
// bytes32 slot2 = slotCal(e, zone2, name2);
assert slot1 != slot2;
// assert false;
// assert slot1 != slot2,"hash collision";
}


// only the caller can write to their partition

rule zonesCanWriteToTheirPartionsOnly(env e, method f){
uint256 metaBefore;
bytes32 dataBefore;
uint256 metaAfter;
bytes32 dataAfter;

address zone;
bytes32 name;
bytes32 slot = slotCal(e, zone, name);
metaBefore, dataBefore = get(slot);
// require metaBefore == 0x0;
calldataarg args;

f(e, args);
metaAfter, dataAfter = get(slot);

// require metaAfter != metaBefore;

// assert (metaAfter != metaBefore) => e.msg.sender != zone,
assert e.msg.sender == zone,
"zones cannot write to meta of partitions of other zones";
// assert dataBefore != dataAfter <=> e.msg.sender == zone,
// "zones cannot write to data of partitions of other zones";
assert false;

}


rule slotChange(env e, method f){

    bytes32 slot;
    uint256 metaBefore;
    bytes32 dataBefore;
    uint256 metaAfter;
    bytes32 dataAfter;

    metaBefore, dataBefore = get(slot);
    // require metaBefore == 0x0;
    calldataarg args;

    f(e, args);
    metaAfter, dataAfter = get(slot);

    assert metaBefore == metaAfter;

}


// rule to check if it's possible to write to locked values

rule noOverWritingLockedSlot(env e, method f)
// filtered{ f -> f.selector != }
{
    bytes32 slot;
    uint256 metaBefore;
    bytes32 dataBefore;
    uint256 metaAfter;
    bytes32 dataAfter;

    metaBefore, dataBefore = get(slot);
    // assert false;
    require metaBefore == 1;
    // assert false;
    calldataarg args;
    f(e, args);
    metaAfter, dataAfter = get(slot);

    // assert false;
    assert dataAfter == dataBefore,"Locked data cannot be overwritten";

}


// // invariant 

// invariant metaLessThanOne(address zone, bytes32 name)
// metaValue(zone, name) < 2

// // invariant()


// // rule to check if there is a way for a name to stay unlocked after calling the set function with that name
 
// rule settest(env e, bytes32 name){

//     bytes32 metaBefore; 
//     bytes32 dataBefore;
//     metaBefore, dataBefore = get(calculateSlot(e.msg.sender, name));

//     set(e, name, metaBefore, dataBefore);

//     bytes32 metaAfter; 
//     bytes32 dataAfter;

//     metaAfter, dataAfter = get(calculateSlot(e.msg.sender, name));
//     assert metaAfter == LOCK(),"meta should be locked for the name after calling set function";
// }

// // parametric rule to check that only set function can lock a name


// // parametric rule
// rule whoLocked(env e, bytes32 name, method f){

//     bytes32 metaBefore; 
//     bytes32 dataBefore;
//     metaBefore, dataBefore = get(e,calculateSlot(e.msg.sender, name));
//     calldataarg args;
    
//     if f.selector == set(bytes32, bytes32, bytes32).selector{
//     f(e, name, metaBefore, dataBefore);
//     }
//     else{
//     f(e, args);    
//     }
    

//     bytes32 metaAfter; 
//     bytes32 dataAfter;

//     metaAfter, dataAfter = get(e,calculateSlot(e.msg.sender, name));
//     assert (metaBefore == 0 && metaAfter == LOCK()) => f.selector == set(bytes32, bytes32, bytes32).selector,
//     "only set function should be able to lock a name";
// }

//  rule to check the immutability of a lock
// rule immutableLock(env e, bytes32 hash1,method f){

//     bytes32 metaBefore; 
//     bytes32 dataBefore;
//     metaBefore, dataBefore = get(hash1);
//     calldataarg args;
    
//     f(e, args);    

//     bytes32 metaAfter; 
//     bytes32 dataAfter;

//     metaAfter, dataAfter = get(hash1);
//     assert metaBefore == LOCK() => metaAfter == LOCK(),"Lock is not immutable";
// }

// rule revertBehaviourCheck(env e, bytes32 name){

// 	bytes32 metaBefore; 
//     bytes32 dataBefore;
//     metaBefore, dataBefore = get(calculateSlot(e.msg.sender, name));
	
// 	calldataarg args;
// 	f@withrevert(e,args);

// 	assert lastreverted => metaBefore == LOCK() || size(args) != 36 || size(args) != 100,"unexpected revert behaviour";
// }