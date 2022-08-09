certoraRun certora/harness/rootHarness.sol certora/harness/dmapHarness.sol \
    --verify rootHarness:certora/specs/root.spec \
    --solc solc8.13 \
    --staging \
    --optimistic_loop \
    --send_only \
    --solc_args "['--optimize', '200']" \
    --msg "calling set with a harness wrapper function" \
    --rule "sanity"


    # --link rootHarness:dmap=Dmap \
#  --send_only \