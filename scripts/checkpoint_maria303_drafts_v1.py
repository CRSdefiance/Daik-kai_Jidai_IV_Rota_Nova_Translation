"""Save all303 clean-first drafts without assigning editorial approval orcompletion credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint
from scripts.meaning_maria_B58_clean_v1 import ROOT

def main():
    draft_path=ROOT/'all303_clean_meanings_andindependent_drafts_v3.json';doc=load(draft_path)
    source_path=ROOT/'clean_source_packet.json';source=load(source_path)
    assert (len(doc['records']),doc['physical_speech_objects'],doc['typed_choice_objects'],doc['source_FE_panels'])==(303,299,4,12)
    assert doc['source_macro_counts']==dict(FI=11,FA=1,FO=4,FU=0)
    assert doc['all_meanings_saved_before_independent_drafts'] and doc['all_drafts_saved_before_current_story_English_intake']
    assert doc['current_English_not_consulted_for_these303_objects'] and doc['all_individual_five_review_gates_pending']
    assert all(r['review']==dict(source=False,context=False,localization=False,naturalness=False,formatting=False) for r in doc['records'])
    assert all(not r['covered'] and not r['exact_credited_source_bindings'] for r in doc['records'])
    assert doc['source_packet_sha256']==digest(source_path) and source['records']==303
    release_path=Path('work/maria310_release_v1/registered_release_verification.json');release=load(release_path)
    assert digest('translations/release_stack.json')==release['registry_sha256']
    paths=[draft_path,source_path,ROOT/'B58_clean_meanings_v1.json',ROOT/'B59_B61_clean_meanings_v1.json',
        ROOT/'B62_B70_clean_meanings_v1.json',*[Path(p) for p in doc['source_draft_files']],Path(__file__)]
    evidence={str(p):digest(p) for p in paths}
    summary=('The next Maria batch has all 303 clean meanings and independent logical English drafts saved across ten complete exchanges: '
        '299 speeches, 12 FE panels and four choice captions. Eleven FI, one FA and four FO tokens and all clean controls are preserved. '
        'Current-English comparison, individual findings/retentions, names/terms and all five review gates remain pending; no new credit. '
        'Integrated 20,058, registered 465cb3c3, main and full editorial scope are unchanged.')
    text='''# Maria303 clean-draft checkpoint — November 9, 2026

**All 303 clean meanings and independent English drafts are saved in ten complete exchanges.** This is draft progress, not completed review: existing-English comparisons, individual findings/revisions/retentions, scoped names/terms and all five gates remain pending. No new ROM, gameplay coverage or review credit is claimed.

Continue under `work/Maria_B58_B70_clean_20261109`:

- `all303_clean_meanings_andindependent_drafts_v3.json`: current selected draft manuscript, with exact clean references, Japanese, source meanings, exchange contexts, independent paragraphs and individual localization notes. The source controls and eleven FI/one FA/four FO tokens are checked; all editable English is ASCII and has no authored wrapping/alignment/padding.
- `clean_source_packet.json` and `source_selection_v1.json`: 303 disjoint original objects, exact clean block bytes and existing native inventories. Blocks/counts: 58/85, 59/29, 60/31, 61/29, 62/30, 64/26, 65/15, 66/19, 68/11, 70/28. No native inventory was replayed.
- `B58_clean_meanings_v1.json`, `B59_B61_clean_meanings_v1.json`, `B62_B70_clean_meanings_v1.json`: source glosses saved before their independent English drafts. Selected drafts are B58 v2, B59–B61 v1 and B62–B70 v3. All prior drafts and failed producers remain preserved.

There are 299 ordinary speech objects, including 12 FE panels, and four native choice captions. The FE cases include three explicitly labeled unseen boy lines, knocking, the ship instruction, four separate branch-dependent stat messages and three animal cries. Do not assign actor254 or invent a portrait/name for these. The two menus contain payment/funds-refusal alternatives and belief/disbelief alternatives; keep their native order and distinct results.

Source notes protect the London rescue's familiar older-sister/brother addresses without inventing kinship, Mivor's matched fear-versus-Cristina comparison-sign joke, Janus's exact1000-gold condition and name/ship-name misunderstanding, Charles's self-reported Dr. title and the explicitly abridged praise of Maria. The later exchanges preserve Silla, distinguish Meihua/美華 from Maria Huamei/華梅, keep miracle claims as reported belief and separate +1 stat outcomes, avoid turning a tomato merchant into a grower, keep unknown seeds uncertain and Gerhard's sword personal rather than an invented heirloom. The ninja line makes the exposed ninja the subject of the death rule. Nukenin is explained in the exchange; Angelo's Mamma mia and Yukihisa's formal voice remain.

Two source rereads refined working drafts before any current-English intake: the boy's reassurance does not add an explicit promise, and Maria's repeated tomato acknowledgment is neutral “Mm-hmm,” preserving her distracted tone without implying tomatoes are apples. The selected version is v3; v2 of the later draft failed before output because a derivation key differed in source escaping. No native check was bypassed and no earlier draft was deleted.

**Next bind these exact records to the current registered Maria310 candidate and extract the existing effective English through the established native lookup.** All selected independent drafts now predate that intake. Include all299 speech bodies and four captions; there are no4100 style alternatives in this source scope. Use the complete source commands and choice-object references already in the packet. Review each complete exchange again with the old English, retaining wording that works with an individual reason and revising real problems. Resolve the provisional crown/Meihua/black-garb/Katzbalger/stat/Refit terms and all scoped proper-name/role consumers before approval. Source notes and draft speaker metadata are not native label approval.

Use the current release proof and its own startup at `work/maria310_release_v1`, captain3. Preserve the entire713-entry prefix,114 accepted layers, market correction, six-section ARM9, ASCII right-bound repair, v2 source25 guard and B54 R507 storage amendment. Reuse matching runtime/font/macro proofs. Changed text still needs fresh native formatting, every new page visually reviewed, stored/allocation/branch checks and representative gameplay before registered integration. Existing70-page Maria310 observations are not gameplay coverage for this batch. No guide photos or exhaustive natural route playthrough are required.

Integrated totals remain **20,058 = 12,064 revisions + 7,994 retentions**. Historical meaning/prose/draft count stays20,061; the current draft-only303 are tracked separately. Registered candidate remains `work/maria310_release_v1/all_routes_maria310_candidate.nds`, SHA-256 `465cb3c39c17c08844cbabe3f58e313a6388ea7ec7750877ee9b28eb4de8b05a`. Native story objects remaining stay **5,840 (Lil1,805 / Maria4,035)** until additional review/integration is completed. Main, all ROMs, prior translations, retentions, coverage and evidence are preserved. Full story/shared shop/town/random/name/UI/player-prose scope remains active. Deferred graphics artwork and the later older-record technical re-audit stay separate. No process is live at this checkpoint.
'''
    checkpoint(mutation=ROOT/'clean_drafts_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria303 clean meanings/independent drafts complete;current comparison next.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,
            proposed_revisions=0,justified_retentions=0,native_job_live=False,registered_build_live=False,guide_photos=False,
            next_action='Bind/extract current native299 speeches andfour captions;whole-exchange comparison,scoped names/terms,then fresh display checks.'),
        additional_updates={'Maria_SC3_B58_B70_clean_20261109':dict(new_credit=0,
            source_meanings_saved=303,independent_drafts_saved=303,proposed_revisions=0,justified_retentions=0,
            latest_clean_drafts=str(draft_path),latest_clean_drafts_sha256=digest(draft_path),
            meanings_drafts_contextual_comparisons_andall_five_gates_pending=False,
            current_English_not_consulted_for_this_scope=True,contextual_comparisons_names_terms_andall_five_gates_pending=True,
            source_controls_andruntime_macros_preserved=True,no_authored_wraps_alignment_orpadding=True,
            actual_gameplay_observations=0,registered_integration_pending=True,source_draft_evidence=evidence)},
        summary=summary,document='docs/editorial_Maria303_clean_drafts_20261109.md',document_text=text,completed=20058,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Saved303 clean meanings/independent drafts;all comparisons andgates pending;20,058 integrated unchanged.')
if __name__=='__main__':main()
