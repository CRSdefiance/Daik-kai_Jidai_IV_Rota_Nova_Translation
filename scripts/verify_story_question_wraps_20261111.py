"""Verify unchanged native boundaries and recheck the four-route wrap queue."""

from inspect import getsource
from types import SimpleNamespace

from scripts import replay_story_question_wraps_20261111 as replay
from scripts import scan_current_progressive_wrap_leads_20261111 as scan
from scripts import stage_story_question_wraps_20261111 as stage
from scripts import verify_historical_story_wraps_storage_20261111 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base=stage.base
PROOF=stage.ROOT/'command_and_catalog_proof.json'
TRIAGE=scan.OUTPUT.with_name('current_progressive_wrap_triage_v2.json')


def main():
    adapter=SimpleNamespace(**(vars(stage.prior)|vars(stage)))
    source=checked_text(getsource(prior.main),{
        'assert len(matches)==12':'assert len(matches)==10',
        '12 unchanged native boundaries and before/after catalog misses on all four routes verified.':
            '10 unchanged native boundaries and before/after catalog misses on all four routes verified.',
    })
    env=vars(prior)|dict(stage=adapter,replay=replay,PROOF=PROOF,__file__=__file__)
    exec(compile(source,__file__+'::existing-exact-boundary-and-catalogue-proof','exec'),env)
    env['main']()
    source=checked_text(getsource(scan.main), {
        "    base.save(OUTPUT,dict(candidate_sha256=setup['candidate_sha256']":
            "    assert not by_kind.get('possible_split_question_tag')\n"
            "    base.save(OUTPUT,dict(candidate_sha256=setup['candidate_sha256']",
    })
    env=vars(scan)|dict(stage=adapter,replay=replay,OUTPUT=TRIAGE,__file__=__file__)
    exec(compile(source,__file__+'::same-four-route-wrap-triage','exec'),env)
    env['main']()


if __name__=='__main__':
    main()
