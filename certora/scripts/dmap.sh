certoraRun certora/harness/dmapHarness.sol \
    --verify dmapHarness:certora/specs/dmap.spec \
    --solc solc8.13 \
    --staging \
    --optimistic_loop \
    --send_only \
    --solc_args "['--optimize', '200']" \
    --msg "metaBefore = 0 and with initialStorage" \
    --rule "$1" \
    --rule_sanity basic


  # certora/harness/rootHarness.sol \
    # --link rootHarness:dmap=Dmap \
#  --send_only \