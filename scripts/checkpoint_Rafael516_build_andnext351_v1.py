"""Save the qualified cumulative build handle andclean-only continuation without new credit."""
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

PREP = Path('work/analysis/Rafael516_registered_preparation_v1_20261105/registered_preparation.json')
QUAL = Path('work/analysis/Rafael516_release_qualification_v1_20261105/qualification.json')
STARTUP = Path('work/analysis/Rafael516_identity_coldboot_20261105/identity_RGB_qualification.json')
BUILD = Path('work/analysis/Rafael516_registered_build_v1_20261105')
NEXT = Path('work/analysis/Rafael_B121_B140_clean_20261105')
DRAFTS = NEXT/'B121_B126_meanings_andindependent_drafts_v1.json'

if __name__ == '__main__':
    prep, qual, startup, live, request = map(load,[PREP,QUAL,STARTUP,BUILD/'OS_live_snapshot.json',BUILD/'request.json'])
    assert prep['expected_manifest_entries'] == 680 and prep['new_source_editorial_objects'] == 516
    assert len(prep['configs']) == len(prep['new_extension_specs']) == 2
    assert qual['preparation_sha256'] == sha(PREP.read_bytes()) and len(qual['changed_scope_andordering_rejections']) == 10
    assert qual['direct_prepublication_andshared_targets_equal'] and qual['unchanged_eight_final_stage_contracts_compared_exactly']
    assert startup['actual_coldboot_frames'] == 4001 and len(startup['exact_RGB_pairs']) == 10
    assert all(r['byte_identical_to_prior_reviewed_RGB'] for r in startup['exact_RGB_pairs'])
    assert startup['planned_ROM_sha256'] == prep['target_ROM_sha256']
    assert live['confirmed_live_by_OS'] and live['PID'] == 56664 and live['session'] == 20868
    assert request['profile'] == prep['profile'] and request['registry_sha256'] == prep['registry_sha256']
    assert not (BUILD/'completion.json').exists()
    for path,digest in request['driver_andcanonical_bytes'].items():
        assert sha(Path(path).read_bytes()) == digest
    packet, styles, choices, drafts = map(load,[NEXT/'clean_source_packet.json',NEXT/'clean_style_objects.json',NEXT/'clean_choice_objects.json',DRAFTS])
    rows = [r for g in packet['groups'] for r in g['records']]+styles['records']+choices['records']
    keys = {(r['file_path'],r['id']) for r in rows}
    assert (packet['records'],len(styles['records']),len(choices['records']),len(keys),len(drafts['records'])) == (307,34,10,351,115)
    assert all(not any(r['review'].values()) for r in drafts['records'])
    ledger_path = Path('translations/editorial_review_current_v1.json'); ledger = load(ledger_path)
    assert ledger['records_editorially_completed'] == 11845
    families = {k:v['record_keys'] for k,v in ledger.items() if isinstance(v,dict) and isinstance(v.get('record_keys'),list)}
    completed = {(r['file_path'],r['id']) for values in families.values() for r in values}
    assert not keys & completed
    census = NEXT/'completed_overlap_andfull_object_census_v1.json'; assert not census.exists()
    save(census,dict(source_packet=str(NEXT/'clean_source_packet.json'),source_packet_sha256=sha((NEXT/'clean_source_packet.json').read_bytes()),
        ordinary_speeches=307,physical_style_variants=34,style_objects=6,style_slots=48,choice_labels=10,choice_objects=5,
        unique_source_objects=351,ledger_record_key_families=list(families),completed_source_key_overlap=[],
        ledger_before_sha256=sha(ledger_path.read_bytes()),integrated_completed=11845,
        first_six_complete_blocks_drafts=115,remaining_meanings_anddrafts=236,
        numeric_block_order_is_not_narrative_chronology=True,new_credit=0))
    pin_path = Path('translations/rom_retention_pins.json'); pin_before = pin_path.read_bytes(); pins = load(pin_path)
    rom = Path(prep['final_ROM']); assert sha(rom.read_bytes()) == prep['target_ROM_sha256']
    pin_audit = Path('work/analysis/Rafael516_combined_retention_pin_20261105'); assert not pin_audit.exists(); pin_audit.mkdir()
    (pin_audit/'pins.before.json').write_bytes(pin_before)
    if not any(Path(r['path']).resolve() == rom.resolve() for r in pins):
        pins.append(dict(path=str(rom.resolve()),reason='Preserve exact qualified516 final reference,not a registered candidate. SHA256 '+prep['target_ROM_sha256']))
    pending = pin_path.with_name('rom_retention_pins.rafael516.pending.json'); assert not pending.exists()
    save(pending,pins); assert pin_path.read_bytes() == pin_before; os.replace(pending,pin_path)
    save(pin_audit/'receipt.json',dict(all_previous_pins_preserved=True,new_pin=str(rom),ROM_sha256=prep['target_ROM_sha256'],new_credit=0))
    summary = ('Rafael early story andall tutorials remain first. Ready261+255 are nowregistered asone680-entry cumulative profile '
        'all-routes-rafael516-20261105:516 five-gate reviews,246 revisions/270 retentions,504 body pages/18 captions. '
        'Both ordered shared plans andten semantic/order rejections pass;114 accepted layers/eight final stages/original27ce core retained. '
        'Fresh own4001-frame planned startup matchesall10 reviewed RGB pairs;final identity/RAM/patch binding remains. '
        'Original-source build20868/PID56664 isOS-confirmed live,targeta51c79e4,registry9bc4dd5e;no concurrent native/emulator jobs. '
        'Original679 failure remains preserved. Next351 clean objects havezero credited overlaps;115 meanings/independent drafts '
        'acrosssix whole blocks aresaved beforecurrent-English extraction,includingall34 personality variants;236 drafts/allcomparisons remain. '
        '11845 integrated;verifiedcc71/main unchanged. No promotion,pruning orguidephotos;full scope/ROMs/evidence preserved.')
    document = f'''# Rafael516 cumulative build and next351 — November 5, 2026

Rafael’s early storyline and all tutorials remain first. Full editorial scope remains active: every route, unfinished contextual pass, shared town/shop dialogue, random scene, name, glyph/wrap defect and remaining player-facing prose. Preserve all ROMs, translations and evidence. No guide photos, pruning, main promotion or commit/push.

## Registered integration now running

`{PREP}` registers `all-routes-rafael516-20261105`, expecting680 manifest entries andtarget SHA-256`{prep['target_ROM_sha256']}`. The actual registered predecessor is verified678/cc71ec06. The profile preserves its full prefix and appends the original qualified261 adapter followed by the new mixed255 adapter. Failed679 remains an unchanged historical profile/failure, not a verified predecessor. No accepted layer or prior profile was changed; all114 accepted layers andall eight final runtime/name/data stages remain mandatory. Registry SHA-256`{prep['registry_sha256']}`; locked core27ce0796 unchanged.

`work/analysis/Rafael516_combined_research_v1_20261105/dependency_reuse.json` proves disjoint ownership and exact local source/target bytes for all20 B101–B120 blocks, including two unchanged controls. Only the18 owned255 blocks are copied over the qualified261 research image. ARM9,COMMON,font,names andall other files/components are exact; complete serialized inverses restore both261 research andverified678. Both reviewed batches’ existing native/storage/catalogue/load/display proofs remain valid for their exact local inputs. No new rendering or gameplay coverage is claimed by that comparison.

`{QUAL}` passes both ordered shared plans andten semantic/order rejections. These include failed text/name gates, changed source controls, changed caption index, false observed/offline scope, changed prose, broken personality aliases, a stored virtual prefix, a wrongly owned control-only block andthe wrong predecessor. All eight final-stage contracts are compared exactly. All existing proofs andthe prior679 MemoryError remain preserved.

`{STARTUP}` binds a fresh4001-frame ordinary New Game capture ofthe combined planned identity. All10 RGB pairs equal the reviewed678 startup. Only29 registered owned SC0 blocks differ; B44,EV0,Help,COMMON,font,all code andname bytes remain exact. Its own final read-only RAM is available. This does not yet approve a registered release: require exact final output equality andthe existing own-RAM/current captain0/route0/Fernan getter checks afterterminal0. Do not repeat the same capture merely because the final output has another filename.

Build **session20868/PID56664** was freshly OS-confirmed live by `{BUILD/'OS_live_snapshot.json'}`. It uses unchanged `run_registered_build_with_gc_v3.py`, original nine pipeline drivers, the system allocator andtight collection. No other native/emulator jobs were live at launch. Collector errors were empty at this checkpoint. Workdirectory`work/r516`; candidate target`out/all_routes_combined_rafael516_20261105_candidate.nds`. Poll the same handle/PID or its authoritative`completion.json`; quiet output, stale telemetry or an observation timeout is not terminal anddoes not authorize a duplicate restart.

Onterminal0, use the prepared`verify_rafael516_registered_release_v1.py` withthis preparation/qualification, actual verified678 parentproof, buildterminal andworkdirectory. It must prove680 entries/all114 layers/26 checks/eight stages, exactly516 source/current/final bindings across29 owned blocks, complete parent inverse andan exactly reconstructable clean-input patch. It is syntax-checked buthas **not** run onan emitted candidate. Then bind ownstartup via`verify_registered_rafael_startup_v2.py` andboth ownFernan getters. Grant246 revision/270 retention credits exactlyonce onlyafterthose checks. Onfailure preserveit, inspectthe concrete cause andcontinue independent prose work. Do not credit the planned image.

## Clean-source editorial continuation

`{NEXT/'clean_source_packet.json'}`, `clean_style_objects.json` and`clean_choice_objects.json` inventory**351 source objects:307 ordinary speeches,34 physical personality variants acrosssix eight-slot objects,and10 captions acrossfive two-choice menus**. The two control-only blocks130/131 remain in scope. `{census}` finds zero overlap against every ledger family exposing explicit`record_keys`. Numeric block order is not narrative chronology; source dispatch includes alternative protagonists/companions. Do not force every line to Rafael because it resides inSC0.

`{DRAFTS}` saves**115 individual clean-source meanings andindependent drafts across B121–B126:81 ordinary speeches andall34 personality variants**. Current English was not extracted for this intake before those drafts; no blanket claim about historical unexposure is made. These are not final reviews: identity/name/term bindings, current-English comparisons andall five gates remain pending. The source notes preserve real grandfather/grandson kinship butnotan invented sibling relation withthe rescuer; the bandit’s lost-livelihood idiom; value versus usefulness ofa gift; the imported-tablet inference; colonial/slave-trade context; map-conditional travel; anddifferent degrees of certainty/proposed use across figurehead personality variants. Source town spelling andunnamed roles/objects remain pendingapproved bindings. Do notinvent a landmark,deity,rank orrelationship.

Next save the remaining236 clean meanings/independent drafts (226 speeches+10 captions), thencompare complete exchanges against current English andresolve clean native name/term/role contracts. Reuse these115 drafts. During the full registered build, avoid overlapping heavy native/emulator jobs; clean-text reading/drafting cancontinue. No premature fifth gates ornew source credit.

Integrated totals remain11845=6836 revisions+5009 retentions; historical source/prose11848 unchanged. Main3cb827e4 andverified experimentalcc71ec06 areunchanged. Graphics artwork andthe later older-record technical re-audit remain separate. Full goal active.
'''
    evidence = {str(p):sha(p.read_bytes()) for p in [PREP,QUAL,STARTUP,BUILD/'OS_live_snapshot.json',DRAFTS,census]}
    checkpoint(mutation='work/analysis/Rafael516_build_next351_checkpoint_20261105',
        batch_key='Rafael_SC0_B101_B120_clean_20261105',
        batch_updates=dict(registered_profile=prep['profile'],registered_preparation=str(PREP),registered_preparation_sha256=sha(PREP.read_bytes()),
            registered_build_session=20868,registered_build_PID=56664,registered_integration_pending=True,new_credit=0),
        additional_updates={
            'Rafael_SC0_B85_B100_contextual_20261105':dict(new_credit=0,registered_profile=prep['profile'],
                registered_preparation=str(PREP),registered_build_session=20868,registered_build_PID=56664,registered_integration_pending=True),
            'editorial_execution_priority_20261104':dict(new_credit=0,current_batch='Registered516 building;next351 cleanfirst editorial intake',
                registered_build_live=True,registered_build_session=20868,registered_build_PID=56664,
                next_action='Poll20868/PID56664;continue remaining236 clean meanings/drafts beforecurrent English. No concurrent heavy native jobs.')},
        new_entries={
            'Rafael516_registered_cumulative_20261105':dict(profile=prep['profile'],previous_verified_profile=prep['previous_profile'],
                preparation=str(PREP),preparation_sha256=sha(PREP.read_bytes()),qualification=str(QUAL),qualification_sha256=sha(QUAL.read_bytes()),
                expected_target_sha256=prep['target_ROM_sha256'],registry_sha256=prep['registry_sha256'],build_session=20868,build_PID=56664,
                build_live_at_OS_checkpoint=True,build_live_receipt=str(BUILD/'OS_live_snapshot.json'),terminal_proof=str(BUILD/'completion.json'),
                pending_source_credit=516,pending_revisions=246,pending_retentions=270,final_candidate_patch_startup_andcredit_pending=True,
                planned_startup=str(STARTUP),planned_startup_sha256=sha(STARTUP.read_bytes()),evidence=evidence,new_credit=0),
            'Rafael_SC0_B121_B140_clean_20261105':dict(source_packet=str(NEXT/'clean_source_packet.json'),source_packet_sha256=sha((NEXT/'clean_source_packet.json').read_bytes()),
                source_objects=351,ordinary_speeches=307,physical_style_variants=34,choice_captions=10,
                clean_meanings_andindependent_drafts=115,remaining_clean_drafts=236,meanings_anddrafts=str(DRAFTS),meanings_anddrafts_sha256=sha(DRAFTS.read_bytes()),
                completed_overlap_census=str(census),completed_overlap_census_sha256=sha(census.read_bytes()),
                all_current_comparisons_name_term_controls_andfive_gates_pending=True,new_credit=0)},
        summary=summary,document='docs/editorial_Rafael516_build_next351_20261105.md',document_text=document,completed=11845,
        protected={'translations/release_stack.json':prep['registry_sha256'],
            'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
            'out/all_routes_combined_help97_rafael330_20261105_candidate.nds':'cc71ec06ce5345dcc71f8b631232f4d8d501152f6989374741616260fa0ca448'})
    print('Checkpoint saved:qualified680-entry build20868/PID56664 active;next351 cleanobjects/115 independent drafts.11845 integrated;no newcredit ormain promotion.')
