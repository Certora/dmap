certoraRun certora/harness/dmapHarness.sol \
    --verify dmapHarness:certora/specs/dmap.spec \
    --solc solc8.13 \
    --staging shelly/bankdevHack \
    --optimistic_loop \
    --send_only \
    --solc_args "['--optimize', '200']" \
    --msg "shelly's fix - basic data check, no name requirement" \
    --rule "$1" \
    --rule_sanity basic \
    --settings -enableCalldataSplitting=false


  # certora/harness/rootHarness.sol \
    # --link rootHarness:dmap=Dmap \
#  --send_only \