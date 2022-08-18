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


rule lockedSlotOverwriteSetCheck(env e)
{
bytes32 slot;
bytes32 Slot;
bytes32 name;
bytes32 meta;
bytes32 data;
bytes32 metaBefore;
bytes32 dataBefore;
bytes32 metaAfter;
bytes32 dataAfter;

metaBefore, dataBefore = getMetaData(e, slot);
require metaBefore == 0x1;
 require slot == slotCal(e, e.msg.sender, name);
// calldataarg args;
// certorafallback_0(e, name, meta, data);
// require Slot == slot;

set@withrevert(e, name, meta, data);


metaAfter, dataAfter = getMetaData(e, slot);

bool isReverted = lastReverted;
assert isReverted;

// assert dataAfter == dataBefore,"locked data should be immutable";
}

rule getTwice(env e, bytes32 hash1, bytes32 hash2){

bytes32 meta1;
bytes32 data1;
bytes32 meta2;
bytes32 data2;
bytes32 meta3;
bytes32 data3;

require hash1 != hash2;

meta1, data1 = getMetaData(e, hash1);
meta2, data2 = getMetaData(e, hash2);
meta3, data3 = getMetaData(e, hash2);


assert meta2 == meta3;
assert data2 == data3;
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
bytes32 metaBefore;
bytes32 dataBefore;
bytes32 metaAfter;
bytes32 dataAfter;

address zone;
bytes32 name;
bytes32 slot = slotCal(e, zone, name);
metaBefore, dataBefore = getMetaData(e, slot);
// require metaBefore == 0x0;
calldataarg args;

f(e, args);
metaAfter, dataAfter = getMetaData(e, slot);

// require metaAfter != metaBefore;

// assert (metaAfter != metaBefore) => e.msg.sender != zone,
assert e.msg.sender == zone,
"zones cannot write to meta of partitions of other zones";
// assert dataBefore != dataAfter <=> e.msg.sender == zone,
// "zones cannot write to data of partitions of other zones";
assert false;

}

rule slotGetCheck(env e, method f){

    bytes32 Slot;
    bytes32 metaBefore;
    bytes32 dataBefore;
    bytes32 metaAfter;
    bytes32 dataAfter;
    bytes32 meta;
    bytes32 data;
    
    metaBefore, dataBefore = getMetaData(e, Slot);

    setStore(e, Slot, meta, data);

    metaAfter, dataAfter = getMetaData(e, Slot);
    assert false;
    assert metaAfter == meta && dataAfter == data,"meta data not set properly in storage";
}

// rule to check if it's possible to write to a locked slot
// STATUS - in progress
rule slotChange(env e, method f){

    bytes32 Slot;
    bytes32 metaBefore;
    bytes32 dataBefore;
    bytes32 metaAfter;
    bytes32 dataAfter;
    bytes32 name;
    bytes32 meta;
    bytes32 data;
    bytes32 argsName;
    bytes32 argsMeta;
    bytes32 argsData;

    // require Slot != 0 && Slot != 1 && Slot != 2;
    require Slot == slotCal(e, e.msg.sender, name);
    metaBefore, dataBefore = getMetaData(e, Slot);
    require metaBefore == 0x1;
    calldataarg args;

    storage initialStorage = lastStorage;
    
    // checkArgs(e, args) at initialStorage;
    argsName, argsMeta, argsData = checkArgs(e, args);
    
    require argsName == name;

    f@withrevert(e, args);
    
    // set@withrevert(e, name, meta, data);

    bool isReverted = lastReverted;
    
    // bytes32 argsName = getName(e);
    // uint256 argsMeta = getMeta(e);
    // bytes32 argsData = getData(e);

    // f(e, args) at initialStorage;

    metaAfter, dataAfter = getMetaData(e, Slot);
    assert isReverted;
    // assert  dataBefore == dataAfter;

}

rule slotChangeSetFunction(env e, method f){

    bytes32 Slot;
    bytes32 metaBefore;
    bytes32 dataBefore;
    bytes32 metaAfter;
    bytes32 dataAfter;
    bytes32 name;
    bytes32 meta;
    bytes32 data;

    metaBefore, dataBefore = getMetaData(e, Slot);
    require metaBefore == 0x0;
    calldataarg args;

    storage initialStorage = lastStorage;

    // checkArgs(e, args) at initialStorage;
    checkArgs(e, args);

    // bytes32 argsName = getName(e);
    // uint256 argsMeta = getMeta(e);
    // bytes32 argsData = getData(e);

    // f(e, args) at initialStorage;
    // set(name, meta, data);
    
    metaAfter, dataAfter = getMetaData(e, Slot);

    assert dataBefore == dataAfter;

}


// rule to check if it's possible to write to locked values
// STATUS - in progress
rule noOverWritingLockedSlot(env e, method f)
filtered{ f -> f.isFallback }
{
    bytes32 slot;
    bytes32 metaBefore;
    bytes32 dataBefore;
    bytes32 metaAfter;
    bytes32 dataAfter;
    bytes32 lockCheckBefore;
    bytes32 lockCheckAfter;
    bytes32 name;
    bytes32 meta;
    bytes32 data;
    


    slot = slotCal(e, e.msg.sender, name);
    // slot = slotCal(e.msg.sender, name);
    metaBefore, dataBefore = getMetaData(e, slot);
    // assert false;
    // require metaBefore == LOCK();
    require metaBefore == 0x1;
    // assert false;

    calldataarg args;

    // storage initialStorage = lastStorage;

    // checkArgs(e, args) at initialStorage;
    checkArgs(e, args);

    bytes32 argsName;
    uint256 argsMeta;
    bytes32 argsData;

    require argsName == name;
    require argsData != dataBefore;
    require argsMeta == 0x0;

    // f(e, args) at initialStorage;
    f(e, args);
    // set@withrevert(name, meta, data);
    
    // set(e, name, meta, data);
    // certorafallback_0(e, name, meta, data);
    metaAfter, dataAfter = getMetaData(e, slot);

    assert false;
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

// STATUS - in progress / verified / error / timeout / etc.
// TODO: rule description

rule basicFRule(env e, method f) {
    bytes32 meta1;
    bytes32 data1;
    bytes32 name1;

    bytes32 slot1 = slotCal(e, e.msg.sender, name1);

    calldataarg args;

    storage initialStorage = lastStorage;

    certorafallback_0(e, args);

    meta1, data1 = getMetaData(e, slot1);

    checkArgs(e, args) at initialStorage;

    // bytes32 name = getName(e);
    // uint256 meta = getMeta(e);
    // bytes32 data = getData(e);

    assert false, "Remember, with great power comes great responsibility.";
}
