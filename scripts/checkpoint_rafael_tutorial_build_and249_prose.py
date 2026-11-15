"""Checkpoint the live registered data build and249 uncredited contextual reviews."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.save_editorial_progress_checkpoint_v3 import checkpoint
from scripts.gloss_rafael_B51_B59_clean import ROOT

PREP=Path('work/analysis/Shared_tutorial_name_data_release_v4_20261104/registered_preparation.json')
PROSE=ROOT/'B51_B60_249_contextual_prose_review_v1.json'
CAPTURE=Path('work/analysis/Shared_tutorial_name_data_identity_coldboot_20261104/capture_report.json')

if __name__=='__main__':
    prepared,prose,capture=map(load,[PREP,PROSE,CAPTURE])
    assert prose['compared']==249 and (prose['proposed_revisions'],prose['justified_retentions'])==(102,147)
    assert all(not r['review']['formatting'] for r in prose['records'])
    assert capture['ROM_sha256']==prepared['target_ROM_sha256'] and capture['frames']==4001
    assert capture['cold_boot'] and not capture['savestate_loaded'] and not capture['callback_errors']
    assert sha(Path('translations/release_stack.json').read_bytes())==prepared['registry_sha256']
    pins_path=Path('translations/rom_retention_pins.json');pins=load(pins_path);before=pins_path.read_bytes()
    pin_backup=Path(PREP).parent/'pins_before_progress_checkpoint.json';assert not pin_backup.exists();pin_backup.write_bytes(before)
    for root in Path('work/analysis').glob('Shared_tutorial_name_data_release*'):
        for rom in root.glob('*.nds'):
            if not any(Path(r['path']).resolve()==rom.resolve() for r in pins):
                pins.append(dict(path=str(rom.resolve()),reason='Preserve rejected preparation/reference;not a handoff candidate. SHA256 '+sha(rom.read_bytes())))
    save(pins_path,pins)
    summary=('Rafael/tutorial priority:four shared panels andtwo catalogue fields arequalified in a seven-stage registered successor;'
        'build54457/PID26012 islive,final manifest/patch/own RAM binding pending. Exact4b10fd67 reference coldboot completed4001frames. '
        'Next Rafael B51–B60 has249 contextual prose reviews (102 revisions/147 retentions),includingfour paired-choice captions;'
        'three full-width I fixes/two scoped name findings,all display gates pending. 10521 integrated completions;verified ee04bf6f/main unchanged. '
        'Full scope,all earlier work/ROMs andevidence preserved;no guide photos.')
    document=Path('docs/editorial_rafael_tutorial_build_and249_prose_20261104.md')
    text=f'''# Rafael tutorial integration and249 contextual reviews - 2026-11-04

Rafael early story andall tutorials remain the execution priority. The full editorial objective remains active. Integrated completions remain10521 (6253 revisions/4268 retentions);all historical credit,translations andjustified retentions remain intact. Main remains immutable3cb827e4. No promotion,commit/push,pruning orguide-photo collection.

## Live registered successor

The four reviewed shared Deck tutorial panels andtwo separately reviewed complete-name components now share one registered data-only successor,after allsix earlier final stages unchanged. Four panels:one First Mate wording revision,three retentions,four phrase/wrap preferences. Two names:Pedro de Valdes andBarbarossa Fazul Hayreddin;progressive names remain unchanged. These two full-name corrections add no dialogue-completion credit.

Profile: `{prepared['profile']}`. Configuration: `{prepared['config']}`. Preparation/positive pure plan/eight rejected defects: `{PREP}`. Whole target SHA256: `{prepared['target_ROM_sha256']}`. Target ARM9: `{prepared['target_ARM9_sha256']}`. Exact source-owned composition:four bounded tutorial allocations andtwo exclusive middle fields,with complete parent/target inverse. All unowned code,fonts,pointers,allocations,files andcomponents remain exact. Accepted layers remain114;expected final manifest entries667/seven final stages. Registry SHA256: `{prepared['registry_sha256']}`.

Build session54457/PID26012 waspolled live withno final output atthis checkpoint. Command:

```text
python scripts/build_integrated_release_with_reviewed_text_data_v3.py --profile {prepared['profile']} --out out/all_routes_combined_rafael_tutorial_name_data_20261104_candidate.nds --work work/rtn7
```

Do not start a second build while it islive. Poll its terminal status. The complete six-stage predecessor must equal verifiedee04bf6f. Earlier preparations arepreserved:the initial evidence traversal reached a list,the first wrapper used the wrong COMMON path,andthe next compared hex strings with different case. The finalv3 wrapper compares source bytes directly anduses `/COMMON/MESFILE.DK4`;eight semantic/fingerprint rejection cases pass. No failed preparation wasregistered orhanded off.

Own exact planned-identity coldboot isterminal exit0:4001frames,ordinary title/NewGame/Rafael inputs,no battery donor,savestate orRAM override. Capture: `{CAPTURE}`,SHA256 `{sha(CAPTURE.read_bytes())}`. The ROM is `{prepared['reference_ROM']}`. This isnew observed startup evidence,butits full own-RAM/getter/RGB chain andregistered whole-ROM identity still require binding;do not call it a verified release yet. No additional tutorial-target/catalogue UI activation isclaimed.

After buildsuccess:

```text
python scripts/verify_registered_reviewed_text_data_release.py --candidate out/all_routes_combined_rafael_tutorial_name_data_20261104_candidate.nds --preparation {PREP} --out work/analysis/Shared_tutorial_name_data_release_verified_20261104
python scripts/verify_registered_rafael_text_data_startup_v1.py --release work/analysis/Shared_tutorial_name_data_release_verified_20261104/registered_release_verification.json --capture {CAPTURE} --parent-startup work/analysis/Rafael_B36_B41_release_verified_20261104/own_registered_startup_verification.json --out work/analysis/Shared_tutorial_name_data_release_verified_20261104/own_registered_startup_verification.json
```

Then grant the four panel reviews completion credit exactly once:10525 total,6254 revisions/4271 retentions. Do not double-credit the superseded single First Mate draft orthe two name fields. Preserve all intermediate/research/reference ROMs;the failed preparations werepinned too. Full catalogue UI andthe four special tutorial bodies remain live-unvisited;their existing complete native/visual/connected proofs andseven ordinary live same-consumer bodies remain the honest qualification scope.

## Next249 prose reviews

All245 clean speeches inB51–B60 andallfour answers intwo B60 choice objects now have contextual comparisons:102 revisions/147 retentions,with exact source/current/draft references andindividual findings. Allfour prose gates pass;all249 formatting gates remainfalse. This isuncredited research,not deployed English.

Authoritative packet: `{PROSE}`,SHA256 `{sha(PROSE.read_bytes())}`. Source meanings werewritten before current English,drafts sealed before current extraction,andpaired menu captions independently drafted before their current captions wereconsulted. Source EV0 membership/prerequisites arebound in `B51_B60_source_identity_checkpoint_v1.json`;numeric block order isnot chronology. Branches remainalternatives. Seven actors/14 clean+14 current name getters werefresh;11 actors reused exact proofs. The five Hodram-context intrinsic-name reuses compare complete current ARM9/COMMON/font,each scoped32-byte actor object andall name fields. The entire actor array isnot assumed equal across protagonists. None isnew actualscene coverage.

Meaning/English findings include:regular military affiliation inAlbuquerque’s summons;invented Lord;Silveira’s deducted-gift reward joke;one untranslatedえ？;future conquest wrongly stated asAfrica already theirs;Emilio confined indoors rather thanstuck intown;Uddin’s first-person introductions;Evergreen Lotus Leaf/Rigveda/Kuhn terminology;Spain-king hypotheticals andpermanent royal succession rights;andthe Mediterranean Proof wrongly localized asthis sea. Good current wording wasretained withindividual reasons,including Uddin’s correct May it prove worthy ofyou farewell.

Two retained speeches have three scoped full-width I corrections:B55R78(one) andB55R168(two). Text changed onlyforthose glyphs retains wording credit. Two separate name-field findings remainpending:actor35Ｆernan Silveira;actor40middleＦong,whose full-width F andFong/von adaptation require a source-aware review,not automatic renaming. Spoken Antony Kuhn isbound toexact clean/current typed fields. No global207-name approval. Two final contextual refinements usecrewmates for仲間 andCome on without inventing a destination;earlier draft/comparison artifacts remainpreserved.

Next:prepare249 formatting input,qualify full preambles andtwo choice objects with existing consumer proofs,compile fresh pages,visually review every new page/boundary,reuse unchanged technical dependencies,scope names/glyph correction ownership,andperform stored/representative focused tests before registered integration. No new gameplay coverage yetforthese249 records. Preserve later Hodram drafts,all remaining story/shared/town/random/player prose,the separate graphics work andlater older-record technical re-audit.
'''
    checkpoint(mutation=Path(PREP).parent/'tutorial_build_and249_prose_mutation_v1',
        batch_key='shared_Deck_four_panel_contextual_20261104',
        batch_updates=dict(new_credit=0,registered_profile=prepared['profile'],registered_preparation=str(PREP),
            registered_build_session=54457,registered_build_PID=26012,registered_build_live_at_checkpoint=True,
            registered_integration_pending=True,exact_planned_identity_coldboot_frames=4001,
            remaining=['Terminal registered build','667-entry/seven-stage manifest andclean-input patch','Own RAM/getter/RGB binding','Once-only four-panel credit']),
        new_entries={'Rafael_SC0_B51_B60_contextual_20261104':dict(new_credit=0,source_speeches=245,typed_choice_captions=4,
            records_prose_reviewed=249,proposed_revisions=102,justified_retentions=147,source_current_review=str(PROSE),
            source_current_review_sha256=sha(PROSE.read_bytes()),individual_review_gates=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            glyph_fix_records=2,full_width_I_glyphs=3,separate_name_findings=2,actual_gameplay_records=0,
            fresh_formatting_stored_visual_representative_gameplay_andintegration_pending=True),
            'Pedro_Hayreddin_full_catalogue_fields_20261104':dict(new_credit=0,reviewed_names=2,
                final_review='translations/pedro_hayreddin_catalogue_fields_final_v1.json',all_five_scoped_gates_pass=True,
                twelve_viewed_native_planes_reused=True,full_catalogue_UI_unvisited=True,registered_deployment_pending=True)},
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='shared_Deck_four_panel_contextual_20261104',next_batch='Rafael_SC0_B51_B60_contextual_20261104',
            Rafael_early_story_andall_tutorials_first=True,full_editorial_scope_preserved=True)},
        summary=summary,document=document,document_text=text,completed=10521,
        protected={'translations/release_stack.json':prepared['registry_sha256'],
            str(Path(prepared['reference_ROM'])):prepared['target_ROM_sha256'],
            'out/all_routes_combined_rafael_b36_b41_static_text_20261104_candidate.nds':prepared['parent_ROM_sha256'],
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'})
    print('Checkpointed live seven-stage build and249 contextual prose reviews;10521 integrated completions,full goal active.')
