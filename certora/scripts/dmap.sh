certoraRun certora/harness/dmapHarness.sol certora/harness/rootHarness.sol \
    --verify dmapHarness:certora/specs/dmap.spec \
    --solc solc8.13 \
    --staging shelly/memfixBankdev\
    --optimistic_loop \
    --send_only \
    --solc_args "['--optimize', '200']" \
    --msg "sanity" \
    --rule "sanity" \
    --rule_sanity basic


    # --link rootHarness:dmap=Dmap \
#  --send_only \