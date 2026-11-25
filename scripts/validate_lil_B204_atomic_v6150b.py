"""Reconstruct all B204 bytes and reject semantic defects before the sole mutation."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B204_editorial_v2 as owned
from dk4tool.patch import lil_B204_editorial_guards_v1 as guards
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.seal_lil_B204_references_v6148 import FLAGS,OUTPUT as DOC,MAP,PROOFS
from scripts.prepare_lil_B204_references_v6135 import PARENT,ROM
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B204_atomic_v6150b');SEAL=Path('work/analysis/lil_B204_reference_approval_v6148/approval_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();doc,mapping=read(DOC),read(MAP);parent=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    verified=read('work/analysis/editorial_handoff_verification_v6134/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256'] and sha(PARENT.read_bytes())==verified['candidate_sha256']
    deps={str(p) for p in [DOC,MAP,SEAL,Path(owned.__file__).relative_to(Path.cwd()),Path(guards.__file__).relative_to(Path.cwd()),Path(__file__).relative_to(Path.cwd()),*PROOFS.values()]}
    deps.update(doc[k[:-7]] for k in doc if k.endswith('_sha256') and isinstance(doc.get(k[:-7]),str) and Path(doc[k[:-7]]).is_file());deps.update(mapping['evidence']);deps.update(['dk4tool/dialogue/layout.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','docs/editorial_testing_scope_v1870.md'])
    excluded={Path(p).resolve() for p in ['translations/release_stack.json','scripts/build_integrated_release.py','translations/editorial_review_current_v1.json','translations/rom_retention_pins.json',*[str(Path('docs')/n) for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]]};pending=list(deps);seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p)
        if Path(p).suffix!='.json':continue
        value=read(p)
        if not isinstance(value,dict):continue
        for key in ['evidence','dependencies']:
            for item in value.get(key,{}) if isinstance(value.get(key),dict) else []:
                if Path(item).is_file() and Path(item).resolve() not in excluded and item not in deps:deps.add(item);pending.append(item)
    deps={p for p in deps if Path(p).resolve() not in excluded}
    conf=dict(format='dk4-lil-B204-editorial-release-v1',manuscript=str(DOC),reference_map=str(MAP),reference_approval=str(SEAL),native_approval=PROOFS['native_approval'],reference_ROM=str(ROM),reference_ROM_sha256=sha(ROM.read_bytes()),required_map_flags=FLAGS,required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),required_runtime_common_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);config=ROOT/'positive_config.json';save(config,conf);test=NdsImage.open(PARENT);proof=owned.apply_release(test,baseline,config)
    assert test.read_file(owned.PATH)==NdsImage.open(ROM).read_file(owned.PATH) and len(proof['changed_records'])==20 and all(test.read_file(p)==v for _,p,v in parent.iter_files() if p!=owned.PATH) and all(test.read_file(p)==v for p,v in parent.iter_components())
    save(ROOT/'positive_reconstruction.json',proof);print('Positive20-object reconstruction and every other file/component exact.',flush=True)
    original_load,original_guard_load=owned.load,guards.load;negatives=[]
    def reject(label,path,edit):
        image=NdsImage.open(PARENT);value=deepcopy(read(path));before=deepcopy(value);edit(value);assert value!=before,label;initial=[image.read_file(p) for p in [owned.PATH,'/__arm9__.bin','/COMMON/MESFILE.DK4']];calls=[];replace=image.replace_file;image.replace_file=lambda *a,**k:(calls.append((a,k)),replace(*a,**k))[1]
        def injected(p):
            v=deepcopy(value) if Path(p)==Path(path) else original_load(p)
            if Path(p)==config:v['dependencies']={}
            return v
        owned.load=guards.load=injected
        try:
            try:owned.apply_release(image,baseline,config)
            except (ValueError,AssertionError) as exc:reason=str(exc) or type(exc).__name__
            else:raise RuntimeError('Negative accepted:'+label)
        finally:owned.load,guards.load=original_load,original_guard_load
        assert not calls and initial==[image.read_file(p) for p in [owned.PATH,'/__arm9__.bin','/COMMON/MESFILE.DK4']],label;negatives.append(dict(label=label,rejected=True,reason=reason,sole_mutation_not_reached=True))
    mutations=[]
    for key in ['source_SC2_sha256','canonical_SC2_sha256','clean_SC2_sha256','clean_ROM_sha256','required_runtime_arm9_sha256','required_runtime_common_sha256','target_SC2_sha256','reference_ROM_sha256']:mutations.append(('wrong-'+key,config,lambda v,k=key:v.update({k:'0'*64})))
    for flag in FLAGS:mutations.append(('lost-'+flag,MAP,lambda v,k=flag:v.update({k:False})))
    mutations += [
      ('missing-speech',DOC,lambda v:v['records'].pop()),('wrong-policy',DOC,lambda v:v.update(translation_policy='literal')),('wrong-locale',DOC,lambda v:v.update(target_locale='en-GB')),('unchecked-format',DOC,lambda v:v.update(formatting_review_pending=True)),
      ('lost-retention-reason',DOC,lambda v:next(r for r in v['records'] if r['editorial_decision']=='retain-wording').update(fresh_retained_wording_justification='')),
      ('wrong-selector',DOC,lambda v:v['records'][0].update(source_selector=18)),('wrong-preamble',DOC,lambda v:v['records'][0].update(source_complete_preamble_hex='0040ffff0012')),
      ('wrong-source-index',DOC,lambda v:v['records'][0].update(source_record_index=4)),('wrong-current-index',DOC,lambda v:v['records'][0].update(current_record_index=4)),('wrong-source-reference',DOC,lambda v:v['records'][0]['source_reference'].update(offset=14)),('wrong-current-reference',DOC,lambda v:v['records'][0]['current_reference'].update(offset=14)),
      ('invented-FI',DOC,lambda v:v['records'][0].update(english='{SPEAKER:0B}{MACRO:FI}')),('authored-break',DOC,lambda v:v['records'][0].update(english=v['records'][0]['english']+'{LB}')),('weak-waiver',DOC,lambda v:v['records'][0].update(qa_waivers=['weak-line-ending'],qa_waiver_reason='copy')),('wrong-compiled-target',DOC,lambda v:v['records'][0].update(compiled_hex='00')),('actual-claimed-offline',DOC,lambda v:v['records'][0].update(actual_B22_display_fixture_observed=False)),
      ('missing-command',MAP,lambda v:v['blocks'][0]['command_map'].pop()),('missing-independent-command',MAP,lambda v:v['blocks'][0]['mapped_native_commands'].pop()),('invented-ancestor',MAP,lambda v:v['blocks'][0]['mapped_native_commands'][0]['target_0100_ancestors'].append(8)),('wrong-logical-target',MAP,lambda v:v['blocks'][0].update(research_logical_end=1342)),('wrong-source-extent',MAP,lambda v:v['blocks'][0].update(source_bytes=1310)),('wrong-target-record-index',MAP,lambda v:v['blocks'][0]['text_records'][0].update(new_record_index=6)),('invented-relative-site',MAP,lambda v:v['blocks'][0]['relative_skip_fixups'].append({'offset':8})),('invented-choice',MAP,lambda v:v['blocks'][0]['choice_commands'].append({'offset':8})),('invented-pause',MAP,lambda v:v['blocks'][0]['original2000_pause_and_resume_maps'].append({'old_offset':8})),
      ('actual-coverage-lost',PROOFS['actual_proof'],lambda v:v.update(actual_unique_speech_panels=19)),('clipped-actual-panel',PROOFS['actual_proof'],lambda v:v['actual_panels'][0]['holds'][0].update(complete_ink_and_gray_masks_equal_native_plane=False)),('lost-timing-difference',PROOFS['actual_proof'],lambda v:next(iter(v['source_English_command_timing_differences'].values())).pop()),('lost-RNG-witness',PROOFS['actual_proof'],lambda v:next(iter(v['source_English_command_RNG_differences'].values())).pop()),('lost-current-source-region',PROOFS['actual_proof'],lambda v:v['same_frame_comparisons']['current-Japanese-V6110-prefix-before-menu'][0].update(upper_portrait_name_item_region_equal=False)),
      ('unviewed-sheets',PROOFS['representative_proof'],lambda v:v.update(visual_review_pending=True)),('claimed-world-equivalence',doc['postscene_native_state_proof'],lambda v:v.update(no_whole_state_equivalence_claim_from_cross_build_getter_comparison=False)),('lost-later-prompt-difference',doc['postscene_native_state_proof'],lambda v:v['later_source_English_RGB_differences'].pop()),('claimed-equal-PRNG',doc['postscene_native_state_proof'],lambda v:v.update(final_PRNG_equal=True)),('lost-cross-build-limit',doc['postscene_native_state_proof'],lambda v:v.update(actual_old_source_and_English_ARM9_hashes_differ=False)),
      ('lost-native-consumer',doc['native_font_proof'],lambda v:v['cases'].pop()),('missing-first-final-glyph',doc['native_font_proof'],lambda v:v['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),('lost-parity-proof',doc['final_padding_proof'],lambda v:v['final_target_parity_cases'].pop()),('lost-control-leaf',doc['relocated_control_proof'],lambda v:v['all6_source_current_target_control_leaves'].pop()),
      ('invented-speaker-rank',doc['source_nameplate_consumer_proof'],lambda v:v['progressive_nameplate_values'].update({'124':'Captain'})),('invented-royal-title',doc['source_nameplate_consumer_proof'],lambda v:v['progressive_nameplate_values'].update({'130':'King'})),('invented-family-label',doc['source_nameplate_consumer_proof'],lambda v:v['progressive_nameplate_values'].update({'145':'Aunt'})),('middle-name-forced-on-nameplate',doc['source_nameplate_consumer_proof'],lambda v:v['progressive_nameplate_values'].update({'11':'Jam Jack Ludwyan'})),
      ('changed-source-voice',doc['actor_voice_contract'],lambda v:v['fresh5_actor_names']['rows'][0].update(original_voice_class=7)),('unapproved-format',PROOFS['native_approval'],lambda v:v.update(all20_five_gates_approved=False)),('claimed-complete-goal',MAP,lambda v:v.update(full_goal_complete=True)),('invented-current-runtime-override',DOC,lambda v:v['records'][0].update(registered_runtime_catalog_entry={'table_index':1})),
      ('invented-FI-in-letter',DOC,lambda v:next(r for r in v['records'] if r['kind']=='system-FE').update(english=next(r for r in v['records'] if r['kind']=='system-FE')['english']+'{MACRO:FI}')),('FE-as-progressive',DOC,lambda v:next(r for r in v['records'] if r['kind']=='system-FE').update(kind='progressive')),('wrong-FE-native-consumer',DOC,lambda v:next(r for r in v['records'] if r['kind']=='system-FE').update(native_display_consumer='original_progressive_54020')),('invented-source-tail',MAP,lambda v:v['blocks'][0].update(source_alignment_tail_bytes=2)),('invented-target-tail',MAP,lambda v:v['blocks'][0].update(target_alignment_tail_bytes=2)),('lost-current-notice',PROOFS['representative_proof'],lambda v:v.update(current_Shachihoko_notice5530_whole_frame_equal_to_current_source=False)),('lost-336-block-loader',PROOFS['loader_proof'],lambda v:v['versions'][0].update(whole_SC2_loads_and_cache_hits=335)),('lost-672-parent-modes',PROOFS['loader_proof'],lambda v:v['versions'][1].update(original_parent_modes=671)),
    ]
    for gate in doc['records'][0]['review']:mutations.append(('unchecked-'+gate,DOC,lambda v,k=gate:v['records'][0]['review'].update({k:False})))
    for label,p,fn in mutations:reject(label,p,fn)
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    save(ROOT/'atomic_validation_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),parent_ROM_sha256=sha(PARENT.read_bytes()),positive_records=20,positive_proof=str(ROOT/'positive_reconstruction.json'),positive_proof_sha256=sha((ROOT/'positive_reconstruction.json').read_bytes()),negative_cases=negatives,negative_count=len(negatives),all_negatives_reject_before_mutation=True,dependency_files_verified_before_and_after_semantic_injection=True,semantic_injection_not_written_to_disk=True,registered_config_not_yet_written=True,full_goal_complete=False));print('Atomic20-object reconstruction and '+str(len(negatives))+' pre-mutation semantic negatives passed.')
