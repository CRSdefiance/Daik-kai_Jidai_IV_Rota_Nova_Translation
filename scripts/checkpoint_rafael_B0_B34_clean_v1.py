"""Save the exact SC0 residual census, all clean drafts and three contextual reviews."""
import re
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.bind_rafael_B0_B34_terms_v1 import OUT as TERMS
from scripts.build_registered_rafael4903_v1 import RELEASE, REGISTRY
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.review_rafael_B20_B24_B25_contextual_v1 import CURRENT, OUT as REVIEW
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER, PACKAGE
from scripts.seal_rafael_B0_B34_clean_v1 import AUDIT, ROOT, PACKET, SEALED


BATCH = 'Rafael_SC0_B0_B34_clean_20261106'


def main():
    audit, drafts, review, terms, ledger, release, package = map(load,
        (AUDIT, SEALED/'sealed_drafts.json', REVIEW, TERMS, LEDGER, RELEASE, PACKAGE))
    assert ledger['records_editorially_completed'] == 16748 and not ledger['full_goal_complete']
    assert len(audit['records']) == 6887 and len(audit['missing']) == 283
    assert sum(r['covered'] for r in audit['records']) == 6604
    assert not audit['inventory_failures'] and not audit['legacy_source_bindings_not_exact']
    known = {(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']
             if r['file_path']=='/data/SC0.DK4'}
    matched = {('/data/SC0.DK4',b['id']) for r in audit['records'] for b in r['exact_credited_source_bindings']}
    assert matched == known and len(matched) == 6604
    assert all(not r['covered'] for r in audit['records'] if r['block'] < 35)
    assert all(r['covered'] for r in audit['records'] if r['block'] >= 35)
    assert drafts['records_count'] == 283 and drafts['complete_blocks'] == list(range(35))
    assert review['records_count'] == 49 and review['remaining_current_comparisons'] == 234
    assert review['counts'] == {'revision':28,'retention':21}
    for row in review['records']:
        assert row['review'] == dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        assert re.findall(r'\bF[AOIU]\b',row['english']) == row['native_literal_tokens']
    assert len(terms['remaining_name_field_leads']) == 3
    summary = ('SC0 coverage reconciles all 6,604 credited dialogue objects and identifies 283 unreviewed speeches '
        'in B0–B34. All 283 clean-first drafts are sealed. Three complete exchanges have 49 contextual decisions: '
        '28 revisions and 21 justified retentions. Another 234 comparisons, scoped name work and fresh display '
        'checks remain. Integrated coverage stays 16,748 in Rafael4903.')
    doc = f'''# Rafael B0–B34 clean-source and contextual checkpoint

{summary}

The clean SC0 command inventory contains 6,133 ordinary speeches, 626 physical style alternatives and 128 typed menu captions: 6,887 objects. Every one of the 6,604 credited SC0 keys binds to exact clean bytes and positions. All objects in B35–B342 have those bindings. B0–B34 contains the remaining 283 speeches; it contains no style table or two-/three-choice caption. All nested command inventories pass. Existing source packets supplied 335 blocks; only eight blocks needed fresh inventory. This is source-object coverage, not proof of original event activation, a full route or all player-facing resources. [Authoritative v2 audit](../{AUDIT.as_posix()}). The earlier v1 diagnostic omitted older families with no top-level record-key list; it adds no gap or completion claim and is superseded by v2.

All 35 residual exchanges now have source meanings, complete-exchange context and logical English drafts, sealed before extracting Rafael4903's English for these records. The set includes artifact reactions, conditional battle openings and outcomes, guild arrests, the early pirate battle-stations reminder, Gerhard's confrontation with Vels, Manuel's poem and Aziza's full recruitment. They are not a single chronological scene. Existing complete reviews and source keys are preserved. [Sealed drafts](../{(SEALED/'sealed_drafts.json').as_posix()}). [283 exact current bindings](../{CURRENT.as_posix()}).

The first three complete comparisons cover B20, B24 and B25. Twenty-eight proposed revisions repair meaning and natural dialogue; 21 individual retentions explain why the existing wording works. Gerhard's source intention to kill Vels is restored without the invented judgment that he deserved death. Vels again describes his own behavior instead of giving second-person advice. Rafael again offers to compose music for Manuel's poem. The poem retains its repeated refrain and reported foreign-language comparison without naming a language. The battle-stations instruction already reads naturally and is retained. Full-width question marks and ellipsis are queued for fresh progressive rendering. [49 contextual decisions](../{REVIEW.as_posix()}). All five gates remain explicit on every record; formatting is false until its new checks pass.

Draft terms Xien, Proof of Conquest, Muramasa and Bloodstained Shamshir are bound to registered fields or completed reviews. Thirty-nine speaker selectors have source/current field bindings; these do not approve their final labels or glyphs. Stored middle-name leads remain for actor 30's デ, actor 59's デ and actor 40's full-width initial in Ｆong. Review the original consumers and naming context before correcting them. Iron-armored ship terminology also remains to qualify. [Scoped terms and name leads](../{TERMS.as_posix()}).

Continue the other 234 contextual comparisons in complete exchanges, prioritizing any tutorial-bearing text and preserving the 49 saved decisions. Then finish scoped names, automatic wrapping, fresh native and visual checks, stored reconstruction and representative gameplay before registering the batch. The current candidate remains Rafael4903; no new ROM, promotion or completion credit is created here. Main, the weekend package, all earlier ROMs and evidence are preserved. Full route/shared/town/random/player-prose scope, separate artwork and the later older-record technical re-audit remain open. No guide photographs are requested.
'''
    evidence = {str(p):digest(p) for p in (AUDIT,PACKET,SEALED/'sealed_drafts.json',CURRENT,REVIEW,TERMS,Path(__file__))}
    checkpoint(mutation=ROOT/'clean_context_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Rafael residual B0–B34; 283 drafts and 49 contextual decisions.',
            next_action='Review the remaining 234 comparisons, then scoped names and fresh display checks.',
            current_batch_not_yet_integrated=True,native_job_live=False,registered_build_live=False,
            registered_cumulative_build_live=False,guide_photos=False),
        new_entries={BATCH:dict(new_credit=0,source_records=283,ordinary_speeches=283,
            physical_style_alternatives=0,typed_captions=0,independently_drafted_records=283,
            independent_draft_blocks=list(range(35)),remaining_clean_meanings_anddrafts=0,
            contextual_decisions=49,four_prose_gate_records=49,proposed_revisions=28,justified_retentions=21,
            remaining_current_comparisons=234,remaining_display_checks=283,scoped_name_field_leads=3,
            registered_integration_pending=True,no_duplicate_credit=True,evidence=evidence)},
        summary=summary,document='docs/editorial_Rafael_B0_B34_clean_context_20261106.md',
        document_text=doc,completed=16748,protected={str(REGISTRY):release['registry_sha256'],
            release['canonical_base']:release['canonical_sha256'],release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved exact SC0 coverage, 283 clean drafts and 49 contextual decisions; no new completion credit.')


if __name__ == '__main__':
    main()
