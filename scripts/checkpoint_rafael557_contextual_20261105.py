"""Atomically save the substantial contextual pass without premature integration credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    prose=Path('translations/rafael_B141_B160_contextual_review_v1.json')
    qual=Path('work/analysis/Rafael557_contextual_comparison_v1_20261105/comparison_qualification.json')
    names=Path('translations/rafael_B141_B160_scoped_names_review_v1.json')
    identities=Path('work/analysis/Rafael557_names_terms_v1_20261105/names_terms_andconsumer_dependency_qualification.json')
    current=Path('work/analysis/Rafael_B141_B160_current867_20261105/current_effective.json')
    captions=current.with_name('current_captions_andglyph_findings_v1.json')
    doc,q,review,identity=map(load,[prose,qual,names,identities])
    assert q['manuscript_sha256']==sha(prose.read_bytes())
    assert len(doc['records'])==557 and (doc['proposed_revisions'],doc['justified_retentions'])==(235,322)
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness']) and r['review']['formatting'] is False for r in doc['records'])
    assert len(review['records'])==20 and all(not r['review']['formatting'] for r in review['records'])
    release_path=Path('work/analysis/Rafael867_extended_release_verified_v3_20261105/registered_release_verification.json')
    release=load(release_path)
    summary=('Rafael and all tutorials remain first. All557 B141–B160 complete-exchange comparisons are saved: '
        '235 proposed revisions/322 justified retentions, all four prose gates passed, all fifth formatting gates pending. '
        '20 public names/roles individually retained; ten fresh/ten exact current native proof reuses. '
        'Bound12 item titles, First Mate and Sao Jorge; established Antony Kuhn spelling source/current fields matched. '
        'Corrected draft tutorial instructions, map geography, unsupported noble titles, voice/subject/qualification losses; '
        '13 actual glyph-defect records proposed for correction, nine preserving all wording. All61 substitutions preserved, '
        'including FU2. New work is offline editorial/binding evidence, not new gameplay/display approval or integration. '
        'Next fresh paragraph formatting, all-page visual review and focused distinct-behavior tests, then registered integration. '
        'Integrated12712/cumulative3bf3/main3cb8 unchanged. Full scope, ROMs and evidence preserved; no guide photos or promotion.')
    text=f'''# Rafael557 contextual editorial checkpoint — November 5, 2026

Rafael's storyline and all tutorials remain first. All other routes, earlier unfinished contextual reviews, shared shop/town dialogue, random scenes, speaker labels and remaining player-facing prose stay in scope. Preserve every ROM, earlier translation, retention and evidence item. No guide photos or main promotion.

## Editorial decisions

[{prose.name}](../{prose.as_posix()}) contains **557 exact source/current comparisons across all20 complete B141–B160 exchanges:235 proposed revisions and322 justified retentions**. There are549 speeches and eight captions. Each has an individual finding and all four source/context/localization/naturalness gates; every formatting gate remainsfalse. The original source-first meanings/drafts and the two209/348 comparison slices are preserved. The manuscript links exact source/current references, bytes, preambles and current catalogue-selected text. Qualification: `{qual}`.

The combat/investment lesson now directs the player to have their assigned **First Mate write the declaration at the Guild**, correcting the misleading guild employee. It preserves declaration alternatives, nearby-battle market effects, immediate contracts and the home-base exception. The Indian Ocean Proof map is no longer called the southern sea map. The two-key explanation retains its qualification and the seven-Proofs/fourteen-keys total. Map experiments keep the actual sequence and unknown-fluid context; good prose is not shortened for wrapping.

Other corrections preserve the Algiers pirates rather than annexing Algiers itself; Fernan's boast of no small contribution rather than modest gifts; Pereira's demands rather than established ownership; and the interrupted secret and uncertainty about his opponents. Remove noble Lord where source様 supplies courtesy alone; Nagalpur's source侯 remains separately supported. Restore natural first-person speech, familiar Clau/Yifa names, and the Estado institution with its source gloss. Use established **Antony Kuhn**, not provisional Coen or old Koon; its exact current/source fields match the earlier approved spoken spelling.

Arcadius's private Eirene revelation retains the explicit identity disclosure, stated safety rationale and continuing request for secrecy. It does not globally rename the public speaker. Charlotte's message retains her lack of opportunity to learn writing, distinguished family concern without invented nobility, and a conditional invitation after Portugal's restoration. It adds no marriage, permanent waiting or guaranteed reunion. Natural existing lines, pauses, teasing, roughness and formal voices have specific retention reasons. B143's Why not? choice is retained because it follows the statement that investment is insufficient; the other option becomes I already know to make skipping the lesson clear.

## Names, glyphs and evidence scope

`{names}` retains20 public names/roles individually. `{identities}` qualifies ten freshly bound clean/current getter sets and ten exact reuses; actor35 uses the already verified current Fernan correction. Cristina, Janus and Yifa follow actual source/current identity data rather than stale profile notes. Ibn Niyadi keeps his proper name. Barkeep/Guard/Innkeeper/Sailor remain source-supported roles. Twelve approved items, First Mate and Sao Jorge are bound; no new name data is written. Global207/full-catalogue UI review remainsopen.

The complete current comparison finds **13 actual glyph-defect records**:full-width English I/F letters and a stray Japanese character at B152R131. All have proposed corrections; **nine retain every word and change only the letter form**. The F at B147R12 is in Forgive, not a broken FI substitution. Legitimate source punctuation and ellipses are separately retained with reasons, not counted as untranslated Japanese prose. These manuscript changes are not yet shipped or visually verified.

All61 literal substitutions remain:FI41,FA8,FO10,FU2. FU is still dynamic at B143R67 and B146R6. Existing codec/profile/rebuild support is already available; qualify its actual full-name expansion, ASCII parity and width in the current runtime instead of repeating earlier engine research. `{current}` binds all549 current speeches; `{captions}` binds eight complete native menu captions. The source command walker proves structural inventory only. Current extraction/getters/spelling checks are offline native/data evidence, **no new gameplay or page/font-plane approval**.

## Continue

Prepare logical paragraphs for validated consumer-specific formatting, including typed captions separately and system-FE separately from progressive speech. Mark substitutions without changing words. All557 records need fresh wrapping/complete-leading-and-trailing-glyph/bounds/pagination checks; all generated pages need readable visual review. Reuse exact matching technical dependencies. Test representative actual transitions, multibatch pagination and FU behavior; unvisited conditional content must remain identified. Then check stored/catalogue/loader allocation and integrate through a registered cumulative release with an exactly reconstructable clean-input patch. Do not award credit until the complete required workflow passes.

Integrated totals remain **12,712 =7,283 revisions+5,429 retentions**; historical source/prose12,715. Current registered experimental ROM remains `{release['candidate']}`, SHA`{release['candidate_sha256']}`. Main remains3cb827e4. Registry, original core, all ROMs and114 accepted layers are protected. Two Dinis/Garcia catalogue de pointer corrections require their own proper ownership; they are not part of the Fernan stage. Deferred artwork and the later older-record technical re-audit remain separate. Full goal active.
'''
    evidence={str(p):sha(p.read_bytes()) for p in [prose,qual,names,identities,current,captions,Path(__file__)]}
    checkpoint(mutation='work/analysis/Rafael557_contextual_checkpoint_20261105',
        batch_key='Rafael_SC0_B141_B160_clean_20261105',
        batch_updates=dict(new_credit=0,current_comparisons=557,remaining_current_comparisons=0,
            contextual_comparisons=557,proposed_revisions=235,justified_retentions=322,four_prose_gate_passes=557,
            manuscript=str(prose),manuscript_sha256=sha(prose.read_bytes()),scoped_names=str(names),
            scoped_names_sha256=sha(names.read_bytes()),scoped_public_names_reviewed=20,scoped_name_changes=0,
            scoped_identity=str(identities),scoped_identity_sha256=sha(identities.read_bytes()),
            fresh_actor_getter_sets=10,exact_actor_getter_sets_reused=10,bound_item_titles=12,
            actual_glyph_defect_records=13,glyph_only_wording_retentions=9,all_five_review_gates_pending=False,
            all_fifth_formatting_gates_pending=True,native_display_stored_andrepresentative_gameplay_pending=True,
            registered_integration_pending=True,evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael557 contextual prose complete;235 proposed revisions/322 retentions;fresh formatting next',
            current_batch_not_yet_integrated=True,new_current_comparisons=557,
            all_current_batch_five_gates_pending=False,all_current_batch_fifth_gates_pending=True,
            next_action='Fresh557 consumer-specific paragraph formatting including FU2,all-page review andfocused distinct-behavior tests;then registered integration.',guide_photos=False)},
        summary=summary,document='docs/editorial_Rafael557_contextual_checkpoint_20261105.md',document_text=text,
        completed=12712,protected={'translations/release_stack.json':release['registry_sha256'],
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
            release['candidate']:release['candidate_sha256']})
    print('Saved557 contextual comparisons andscope/next-step handoff. Newcredit0;integrated12712/ROMs/main/registry/core unchanged. Full goal active.')
