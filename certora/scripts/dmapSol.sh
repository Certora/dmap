certoraRun certora/harness/dmapSolHarness.sol \
    --verify dmapSolHarness:certora/specs/dmap.spec \
    --solc solc8.13 \
    --staging alex/skey-add-vs-normal-add-vs-to-skey\
    --optimistic_loop \
    --send_only \
    --solc_args "['--optimize', '200']" \
    --msg "testing with solidity code" \
    --rule "$1" \
    --rule_sanity basic \
    --settings -enableCalldataSplitting=false


  # certora/harness/rootHarness.sol \
    # --link rootHarness:dmap=Dmap \
#  --send_only \