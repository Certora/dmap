 /******************************************************************
 * IMPORTS/SETUP                                                  *
 ******************************************************************/
// using rootHarness as root

methods {
	set(bytes32 name, bytes32 meta, bytes32 data)
    get(bytes32 slot) returns (bytes32 meta, bytes32 data) envfree
	calculateSlot(address zone, bytes32 name) returns(bytes32 slot)envfree
}

definition LOCK() returns uint256 = 1;
definition MAX_bytes32() returns bytes32 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff;


 /******************************************************************
 * USEFUL CONSTRUCTS.                                             *
 ******************************************************************/


// uninterpreted functions, useful for describing contract state
ghost metaValue(address, bytes32) returns uint256{
    init_state axiom forall address z. forall bytes32 n. metaValue(z, n) == 0;
}

 /******************************************************************
 * RULES AND INVARIANTS:                                             *
 ******************************************************************/

// sanity
rule sanity(method f){
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


// rule to check that getMetaData is working as expected
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

// rule to ensure there isn't any hash collision
rule hashCalCheck(env e){

    address zone1;
    bytes32 name1;
    address zone2;
    bytes32 name2;
    address zone3;
    bytes32 name3;

    require zone1 != zone2 || name1 != name2;
    bytes32 slot1 = slotCal(e, zone1, name1);
    bytes32 slot2 = slotCal(e, zone2, name2);
    bytes32 slot3 = slotCal(e, zone2, name2);

    assert slot1 != slot2;
    assert slot2 == slot3;
}


// basic parametric rule checking immutability of locked slot. Checking if the data in a locked slot can be changed by
// calling any function with any arguments.
// FAILED. All non-view/pure functions fail this including checkArgs().
// https://vaas-stg.certora.com/output/11775/56275102f2f888aeadc8/?anonymousKey=b4aa8b53bb98a2eb6125284112820592de84a32e


rule basicImmutabilityCheck(env e, method f){
    bytes32 slot;
    bytes32 metaBefore;
    bytes32 dataBefore;
    bytes32 argsName;
    bytes32 argsMeta;
    bytes32 argsData;
    
    metaBefore, dataBefore = getMetaData(e, slot);
    require metaBefore == 0x1;

    calldataarg args;

    argsName, argsMeta, argsData = unpackArgs(e, args);
    
    f(e, args);

    bytes32 metaAfter;
    bytes32 dataAfter;

    metaAfter, dataAfter = getMetaData(e, slot);

    assert dataAfter == dataBefore,"locked slot must be immutable";
}


rule zonesCanWriteToTheirPartionsOnly(env e, method f){
    bytes32 metaBefore;
    bytes32 dataBefore;
    bytes32 metaAfter;
    bytes32 dataAfter;

    bytes32 name1;
    bytes32 name2;
    bytes32 meta;
    bytes32 data;
    bytes32 argsName;
    bytes32 argsMeta;
    bytes32 argsData;

    address zone;
    bytes32 slot;

    require slot == slotCal(e, zone, name1);  

    metaBefore, dataBefore = getMetaData(e, slot);

    calldataarg args;
    argsName, argsMeta, argsData = unpackArgs(e, args);
    
    f(e, args);

    // set(e, name2, meta, data);

    metaAfter, dataAfter = getMetaData(e, slot);

    // assert true;
    // assert dataBefore == dataAfter,"data should not have changed";
    // assert (dataBefore != dataAfter && metaAfter == metaBefore) => (e.msg.sender == zone && name1 == argsName),"zones cannot write to partitions of other zones";
    assert (dataBefore != dataAfter && metaAfter == metaBefore)  => e.msg.sender == zone,"zones cannot write to partitions of other zones";
}

// same as above but with tied slot
// https://vaas-stg.certora.com/output/11775/0a06f0b16ade6eede9a9/?anonymousKey=dbf6f3cc7f356357591c472b41aaf062b3d10c74

rule immutabilityParametricWithCheckArgsAndTiedSlot(env e, method f)
{
    bytes32 slot;
    bytes32 metaBefore;
    bytes32 dataBefore;
    bytes32 name;
    bytes32 meta;
    bytes32 data;
    bytes32 argsName;
    bytes32 argsMeta;
    bytes32 argsData;
    require slot == slotCal(e, e.msg.sender, name);
    
    metaBefore, dataBefore = getMetaData(e, slot);
    
    calldataarg args;

    argsName, argsMeta, argsData = unpackArgs(e, args);

    require argsName == name;
    
    f(e, args);

    bytes32 metaAfter;
    bytes32 dataAfter;

    metaAfter, dataAfter = getMetaData(e, slot);

    assert metaBefore == 0x1 => dataAfter == dataBefore,"locked slot must be immutable"; // wrong assertion to generate a violation
}

// parametric rule with unpackArgs to see if storage variables could be messing with storage. 
rule immutabilityParametricWithUnpackArgs(env e, method f){
    bytes32 slot;
    bytes32 metaBefore;
    bytes32 dataBefore;
    bytes32 argsName;
    bytes32 argsMeta;
    bytes32 argsData;
    bytes32 name;
    bytes32 meta;
    bytes32 data;

    require slot == slotCal(e, e.msg.sender, name);
    metaBefore, dataBefore = getMetaData(e, slot);
    require metaBefore == 0x1;

    // storage initialStorage = lastStorage;
    
    calldataarg args;
    argsName, argsMeta, argsData = unpackArgs(e, args);

    f(e, args);

    bytes32 metaAfter;
    bytes32 dataAfter;

    metaAfter, dataAfter = getMetaData(e, slot);

    assert dataAfter == dataBefore && metaBefore == metaAfter,"locked slot must be immutable";
}