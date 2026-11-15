"""Save286 uncredited contextual reviews while protecting the registered cumulative."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v8 import checkpoint

ROOT=Path('work/Maria_B37_B50_clean_20261109')
PROSE=Path('translations/maria_B37_B50_contextual_review_v1.json')

def main():
    proof=ROOT/'prose_gate_qualification_v1.json';q=load(proof);doc=load(PROSE)
    assert q['records']==len(doc['records'])==286 and q['all_four_prose_gates_pass'] and q['all_fifth_gates_false']
    assert q['final_manuscript_sha256']==digest(PROSE)
    release=load('work/maria301_release_v1/registered_release_verification.json')
    assert doc['current_ROM_sha256']==release['candidate_sha256']
    evidence={str(p):digest(p) for p in [PROSE,proof,ROOT/'all286_contextual_proposals_v1.json',
        ROOT/'scoped28_name_editorial_review_v1.json',ROOT/'scoped_terms_v1.json',
        ROOT/'current_v1/current_effective.json',ROOT/'current_objects_v1/current_objects.json',Path(__file__)]}
    summary=('Maria B37–B50 has 286 contextual prose reviews: 170 proposed revisions/116 justified retentions in '
        '14 complete exchanges, plus 28 scoped name retentions and 56 native getter checks. Four prose gates pass; '
        'all formatting gates remain false. Fresh wrapping, all new page review, FE/menu behavior, stored checks '
        'and representative gameplay precede registered integration. Integrated 19,462/remaining native-story '
        '6,436 and the registered c9b583a6 candidate/main are unchanged; zero new credit.')
    text='''# Maria B37–B50 contextual checkpoint — November 9, 2026

All 286 source objects in 14 complete exchanges have individual contextual decisions: **170 proposed dialogue revisions and 116 justified retentions**. The four prose gates pass; formatting stays false on every row, and the release validator correctly rejects this unformatted manuscript. This is substantial editorial progress, not an integrated or gameplay-tested batch.

The final logical prose and exact source/current references are in [the contextual manuscript](../translations/maria_B37_B50_contextual_review_v1.json). Source meanings and independent drafts were sealed before current conversation English intake. Original drafts, ten source-only reread refinements, native bindings and all six individual decision files remain under `work/Maria_B37_B50_clean_20261109` and `scripts/`. This batch is disjoint from all 19,462 credited records. Native census/inventory proofs are reused, not replayed.

The scenes cover Lil’s rescue aftermath, Uddin’s bargain, Nagarpur’s defeat, the complete Tamsui construction/wine chain including its unfinished branch, African exploitation/confrontations, Espinosa’s capture and crowd gratitude, Rafael’s trade ideals and conditional Mediterranean reports, Maldonado’s conditional bargain, and Richard’s defection/unnamed monologue. Conditional intelligence and betrayal alternatives are preserved as alternatives, not combined into one chronology. No new noble rank, family connection, completed appointment, execution or historical claim is invented.

Concrete corrections include the malformed choice “、greed.”, Crow→Clau, Kuen→Kuhn, source-bound Nagarpur spelling, Portugal’s loss of sovereignty being weakened to Spain taking the lead, advice-to-you replacing Maldonado’s explanation about himself, a future life threat turned into a past death implication, invented Lord titles, and cheering replacing explicit waving. Existing natural wording is retained individually, including the fearsome-reputation idiom that already avoids a literal crying-child translation. Proposed wording still requires fresh display checks.

`scoped28_name_editorial_review_v1.json` records 28 contextual name/role retentions with exact source component fields and 56 original native nameplate/catalogue getters. Shopkeeper, Port Worker and Innkeeper are natural role labels; workplace/familiar address and Africa metadata do not establish kinship, age or nationality. The proper-name forms remain registered, including Rafael, Hodram/Joakim, Maria and Camille. Nagalpur→Nagarpur is a dialogue spelling reconciliation, not a new name-table patch. The full 207-name and separate older consumer audits remain open.

`scoped_terms_v1.json` binds six native aliases for Sofala/Cape Town/Mogadishu/Hangzhou, the registered Tamsui span, Wine’s exact pointer/metadata and the default captain3 macros FI=Maria, FA=Li, FO=Li Clan, FU=Maria Huamei Li. It documents the five-hold quantity, mainland Ming trade rights, England, wokou pirates and the gift/Proof distinction. These bindings do not approve every city/commodity widget or arbitrary custom-name width.

The formatting scope is **269 progressive bodies, 13 FE bodies and four captions in two menus**. There are 21 runtime-token occurrences and 17 current non-ASCII target records; these target counts are not 17 newly verified rendering failures. FE includes the unseen-voice entrance, location transition, hidden monologue and trade-share notice. Do not assign a static speaker/portrait from context alone. Maria301 had no FE bodies, so its no-FE proof cannot approve this batch’s FE ABI; reuse the separately validated FE consumer only after matching relevant current dependencies and run fresh formatted tests.

Next format all 286 logical paragraphs with validated full available widths, preserving native headers/controls/substitutions and avoiding old authored early breaks. Review every new body/menu/name page directly with readable sheets; check phrase continuity, tags and page boundaries. Run stored-script/allocation/load checks and representative initialized gameplay for FE/progressive pagination, both menus and transitions. The verified current Maria3 startup is reusable and is not B37–B50 gameplay coverage. No new pages, natural event activations or hardware observations are claimed here.

The current registered cumulative remains [Maria301](editorial_Maria301_registered_20261109.md), candidate SHA-256 `c9b583a629a327e7e4893e3d10d57c5e7a4c591f724354ac9561937cba6cfa01`, with 709 entries/114 accepted layers/44 passing checks and an exact clean-input patch. Main and canonical baseline are unchanged; do not promote without user acceptance. Integrated totals remain **19,462 = 11,710 revisions + 7,752 retentions**. The native story census still has **6,436 remaining**, including this not-yet-integrated batch; shared/UI prose remains separate. All ROMs, earlier translations and evidence are preserved.

Keep every remaining storyline and unfinished earlier contextual pass, town/shop/random dialogue, names, wrap/glyph fixes and other player-facing text in scope. No guide photos. Deferred graphics artwork and the later older-record technical re-audit remain separate. No process is live at this checkpoint.
'''
    checkpoint(mutation=ROOT/'contextual_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria286:170 revisions/116 retentions;four prose gates pass;fresh formatting next.',
            new_source_meanings=286,new_independent_drafts=286,new_current_comparisons=286,proposed_revisions=170,
            justified_retentions=116,all_current_batch_five_gates_pending=False,all_current_batch_fifth_gates_pending=True,
            current_batch_not_yet_integrated=True,native_job_live=False,registered_build_live=False,guide_photos=False,
            next_action='Fresh-format269 progressive/13 FE/four captions;review every new page andscoped names;stored/representative checks,thenregistered integration.'),
        new_entries={'Maria_SC3_B37_B50_clean_20261109':dict(new_credit=0,source_objects=286,complete_exchanges=14,
            source_meanings=286,independent_drafts=286,current_comparisons=286,remaining_current_comparisons=0,
            proposed_revisions=170,justified_retentions=116,all_four_prose_gates_pass=True,
            all_fifth_formatting_gates_pending=True,scoped_name_retentions=28,native_name_getters=56,
            contextual_manuscript=str(PROSE),contextual_manuscript_sha256=digest(PROSE),
            glyph_targets=17,actual_current_batch_gameplay_observations=0,registered_integration_pending=True,evidence=evidence)},
        summary=summary,document='docs/editorial_Maria286_contextual_20261109.md',document_text=text,
        completed=19462,protected={'translations/release_stack.json':release['registry_sha256'],
            release['canonical_base']:release['canonical_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256']})
    print('Saved Maria286 contextual checkpoint;19462 integrated unchanged,zero credit.')

if __name__=='__main__':main()
