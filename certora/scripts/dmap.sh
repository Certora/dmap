certoraRun certora/harness/dmapHarness.sol certora/harness/rootHarness.sol \
    --verify dmapHarness:certora/specs/dmap.spec \
    --solc solc8.13 \
    --staging \
    --optimistic_loop \
    --send_only \
    --solc_args "['--optimize', '200']" \
    --msg "$1" \
    --rule "$1" \
    --rule_sanity basic


    # --link rootHarness:dmap=Dmap \
#  --send_only \