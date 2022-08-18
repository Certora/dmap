certoraRun certora/harness/dmapHarness.sol \
    --verify dmapHarness:certora/specs/dmap.spec \
    --solc solc8.13 \
    --staging \
    --optimistic_loop \
    --send_only \
    --solc_args "['--optimize', '200']" \
    --msg "parametric with checkArgs without initialStorage with slot > 5" \
    --rule "$1" \
    --rule_sanity basic \
    --settings -useBitVectorTheory


  # certora/harness/rootHarness.sol \
    # --link rootHarness:dmap=Dmap \
#  --send_only \