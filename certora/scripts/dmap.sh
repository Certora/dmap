certoraRun certora/harness/dmapHarness.sol certora/harness/rootHarness.sol \
    --verify dmapHarness:certora/specs/setup.spec \
    --solc solc8.13 \
    --staging \
    --optimistic_loop \
    --send_only \
    --solc_args "['--optimize', '200']" \
    --msg "sanity parametric to check if fallback is skipped or not" \
    --rule "sanity"


    # --link rootHarness:dmap=Dmap \
#  --send_only \