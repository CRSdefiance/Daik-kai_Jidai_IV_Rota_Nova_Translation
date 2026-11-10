"""Reconstruct B208 and challenge independent semantic guards before any mutation."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B208_editorial_v3 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.seal_lil_B208_references_v6434 import FLAGS,OUTPUT as DOC,MAP,PROOFS,PARENT,ROM
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B208_atomic_v6437');SEAL=Path('work/analysis/lil_B208_reference_approval_v6434/approval_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();doc,mapping=read(DOC),read(MAP);parent=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    deps={str(p) for p in [DOC,MAP,SEAL,Path(owned.__file__).relative_to(Path.cwd()),Path(__file__).relative_to(Path.cwd()),*PROOFS.values(),'scripts/seal_lil_B208_references_v6434.py','dk4tool/dialogue/layout.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','docs/editorial_testing_scope_v1870.md']}
    deps.update(doc[k[:-7]] for k in doc if k.endswith('_sha256') and isinstance(doc.get(k[:-7]),str) and Path(doc[k[:-7]]).is_file());deps.update(mapping['evidence']);deps.add('dk4tool/patch/lil_B208_editorial_guards_v2.py')
    excluded={Path(p).resolve() for p in ['translations/release_stack.json','scripts/build_integrated_release.py','translations/editorial_review_current_v1.json','translations/rom_retention_pins.json',*[str(Path('docs')/n) for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]]}
    pending=list(deps);seen=set()
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
    conf=dict(format='dk4-lil-B208-editorial-release-v3',manuscript=str(DOC),reference_map=str(MAP),reference_approval=str(SEAL),required_map_flags=FLAGS,
        required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),required_runtime_common_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),
        source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),reference_ROM=str(ROM),reference_ROM_sha256=sha(ROM.read_bytes()),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);config=ROOT/'positive_config.json';save(config,conf);test=NdsImage.open(PARENT);proof=owned.apply_release(test,baseline,config)
    assert test.read_file(owned.PATH)==NdsImage.open(ROM).read_file(owned.PATH) and len(proof['changed_records'])==24
    assert all(test.read_file(p)==v for _,p,v in parent.iter_files() if p!=owned.PATH) and all(test.read_file(p)==v for p,v in parent.iter_components());save(ROOT/'positive_reconstruction.json',proof);print('Positive24-record reconstruction and all other assets exact.',flush=True)
    original_load=owned.load;negatives=[]
    def reject(label,path,edit):
        image=NdsImage.open(PARENT);value=deepcopy(read(path));before=deepcopy(value);edit(value);assert value!=before,label
        initial=[image.read_file(p) for p in [owned.PATH,'/__arm9__.bin','/COMMON/MESFILE.DK4']];calls=[];replace=image.replace_file;image.replace_file=lambda *a,**k:(calls.append((a,k)),replace(*a,**k))[1]
        def injected(p):
            v=deepcopy(value) if Path(p)==Path(path) else original_load(p)
            if Path(p)==config:v['dependencies']={}
            return v
        owned.load=injected
        try:
            try:owned.apply_release(image,baseline,config)
            except (ValueError,AssertionError) as exc:reason=str(exc) or type(exc).__name__
            else:raise RuntimeError('Negative accepted:'+label)
        finally:owned.load=original_load
        assert not calls and initial==[image.read_file(p) for p in [owned.PATH,'/__arm9__.bin','/COMMON/MESFILE.DK4']],label
        negatives.append(dict(label=label,rejected=True,reason=reason,sole_mutation_not_reached=True))
    mutations=[]
    for key in ['source_SC2_sha256','canonical_SC2_sha256','clean_SC2_sha256','clean_ROM_sha256','required_runtime_arm9_sha256','required_runtime_common_sha256','target_SC2_sha256','reference_ROM_sha256']:mutations.append(('wrong-'+key,config,lambda v,k=key:v.update({k:'0'*64})))
    for flag in FLAGS:mutations.append(('lost-'+flag,MAP,lambda v,k=flag:v.update({k:False})))
    mutations.extend([
      ('missing-record',DOC,lambda v:v['records'].pop()),('wrong-policy',DOC,lambda v:v.update(translation_policy='literal')),('wrong-locale',DOC,lambda v:v.update(target_locale='en-GB')),
      ('unchecked-format',DOC,lambda v:v.update(formatting_review_pending=True)),('wrong-encoder',DOC,lambda v:v.update(encoder='typed-menu-relocatable-v1')),
      ('missing-retention-reason',DOC,lambda v:next(r for r in v['records'] if r['editorial_decision']=='retain-wording').update(fresh_retained_wording_justification='')),
      ('wrong-selector',DOC,lambda v:v['records'][0].update(source_selector=19)),('wrong-preamble',DOC,lambda v:v['records'][0].update(source_complete_preamble_hex='0040ffff0013')),
      ('wrong-source-reference',DOC,lambda v:v['records'][0]['source_reference'].update(offset=14)),('wrong-current-index',DOC,lambda v:v['records'][0].update(current_record_index=4)),
      ('invented-macro',DOC,lambda v:v['records'][0].update(english='{SPEAKER:AA}{MACRO:FI}')),('authored-break',DOC,lambda v:v['records'][0].update(english=v['records'][0]['english']+'{LB}')),
      ('blanket-waiver',DOC,lambda v:v['records'][0].update(qa_waivers=['weak-line-ending'],qa_waiver_reason='copy')),
      ('missing-boundary',DOC,lambda v:next(r for r in v['records'] if r.get('reviewed_ordinary_boundaries')).update(reviewed_ordinary_boundaries=[])),
      ('wrong-boundary-source',DOC,lambda v:next(r for r in v['records'] if r.get('reviewed_ordinary_boundaries'))['reviewed_ordinary_boundaries'][0].update(exact_source_hex='00')),
      ('missing-rowcount-reason',DOC,lambda v:next(r for r in v['records'] if r.get('qa_waivers')).update(qa_waiver_reason='')),
      ('wrong-compiled',DOC,lambda v:v['records'][0].update(compiled_hex='00')),('actual-claimed-offline',DOC,lambda v:v['records'][0].update(actual_B22_display_fixture_observed=False)),
      ('missing-command',MAP,lambda v:v['blocks'][0]['command_map'].pop()),('missing-independent-command',MAP,lambda v:v['blocks'][0]['mapped_native_commands'].pop()),
      ('invented-ancestor',MAP,lambda v:v['blocks'][0]['mapped_native_commands'][0]['target_0100_ancestors'].append(8)),('wrong-source-tail',MAP,lambda v:v['blocks'][0].update(source_alignment_tail_bytes=0)),
      ('wrong-target-extent',MAP,lambda v:v['blocks'][0].update(research_logical_end=610)),('wrong-stored-target',MAP,lambda v:v['blocks'][0]['text_records'][0].update(target_hex='00')),
      ('invented-pause',MAP,lambda v:v['blocks'][0]['original2000_pause_and_resume_maps'].append({'old_offset':8})),
      ('missing-A000',MAP,lambda v:v['blocks'][0]['mapped_native_commands'].pop(-2)),('missing-end',MAP,lambda v:v['blocks'][0]['original_declared_end_word_maps'].pop()),
      ('actual-clipped-body',PROOFS['actual_proof'],lambda v:v['actual_panels'][0]['holds'][0].update(all_complete_216x64_or_FE228x64_ink_gray_pixels_equal_native_plane=False)),
      ('actual-clipped-name',PROOFS['actual_proof'],lambda v:v['actual_panels'][0]['holds'][0].update(complete_current_style11_nameplate_glyphs_and_blank_guards_equal=False)),
      ('lost-shared-source-hold',PROOFS['actual_proof'],lambda v:v['actual_panels'][0]['holds'][0].update(both_versions_in_same_semantic_speech_at_this_frame=False)),
      ('invented-speaker-relationship',PROOFS['actual_proof'],lambda v:v['actual_panels'][0].update(name='Father')),
      ('lost-timing',PROOFS['actual_proof'],lambda v:v['command_timing_differences'].pop()),('lost-RNG',PROOFS['actual_proof'],lambda v:v['command_RNG_differences'].pop()),('lost-RGB',PROOFS['actual_proof'],lambda v:v['later_whole_RGB_differences'].pop()),
      ('claimed-final-seed-equal',PROOFS['postscene_native_state_proof'],lambda v:v.update(final_PRNG_equal=True)),
      ('unviewed',PROOFS['representative_proof'],lambda v:v.update(visual_review_pending=True)),('claimed-world-equal',PROOFS['representative_proof'],lambda v:v.update(broad_postscene_full_RAM_future_world_equivalence_unproven=False)),
      ('claimed-natural-event',PROOFS['representative_proof'],lambda v:v.update(natural_event208_original_location_earned_progress_full_effect_semantics_routes_and_hardware_unclaimed=False)),
      ('lost-following-scene-end',PROOFS['representative_proof'],lambda v:v.update(following_B120_end_frame=0)),
      ('missing-native-case',doc['native_font_proof'],lambda v:v['cases'].pop()),('missing-parity-case',PROOFS['final_padding_proof'],lambda v:v['final_target_parity_cases'].pop()),
      ('missing-control-leaf',PROOFS['relocated_control_proof'],lambda v:v['all5_source_current_target_nontext_leaves'].pop()),
      ('unapproved-native',PROOFS['native_approval'],lambda v:v.update(all24_five_gates_approved=False)),('unsafe-loader',PROOFS['loader_proof'],lambda v:v.update(B208_fits_original_0x2400_cache=False)),
      ('unsafe-end',PROOFS['termination_decode_proof'],lambda v:v.update(no_end_decode_zero_tail_dependency=False)),
      ('unapproved-names',PROOFS['speaker_name_approval'],lambda v:v.update(two_native_name_planes_four_getters32_macro_alignments91_actual_header_holds_approved=False)),
      ('closed-name-queue',DOC,lambda v:v.update(broader207_name_and_full_editorial_scope_remain_open=False)),('claimed-complete-goal',MAP,lambda v:v.update(full_goal_complete=True))])
    mutations.extend([
      ('FE-attributed-to-actor',PROOFS['relocated_control_proof'],lambda v:v['relocated_dispatch_cases'][-1].update(resolved_actor_ID=254)),
      ('FE-attributed-voice',PROOFS['relocated_control_proof'],lambda v:v['relocated_dispatch_cases'][-1].update(source_voice_class=3)),
      ('FE-invented-nameplate',PROOFS['actual_proof'],lambda v:v['actual_panels'][-1]['holds'][0].update(nameplate_expected=True)),
      ('FE-clipped-literal-name',PROOFS['actual_proof'],lambda v:v['actual_panels'][-1]['holds'][0].update(all_complete_216x64_or_FE228x64_ink_gray_pixels_equal_native_plane=False)),
      ('thought-unparenthesized',DOC,lambda v:next(r for r in v['records'] if r['source_record_index']==86).update(english=next(r['english'] for r in v['records'] if r['source_record_index']==86).replace('(','',1))),
      ('FE-wrong-person',DOC,lambda v:v['records'][-1].update(english='{SPEAKER:FE}Lil: Charm +1!')),
      ('FE-wrong-attribute',DOC,lambda v:v['records'][-1].update(english='{SPEAKER:FE}Cristina: Charisma +1!')),
      ('FE-wrong-amount',DOC,lambda v:v['records'][-1].update(english='{SPEAKER:FE}Cristina: Charm +2!')),
      ('phase-36-cell-guard-lost',doc['phase_capacity_proof'],lambda v:v.update(first36_cell_preLF_auto_wrap_rejected=False)),
      ('phase-missing-native-plane',doc['phase_capacity_proof'],lambda v:v['cases'].pop()),
      ('phase-codec-hash-lost',doc['phase_capacity_proof'],lambda v:v.update(unchanged_codec_sha256='0'*64)),
      ('target-tail-lost',MAP,lambda v:v['blocks'][0].update(target_alignment_tail_bytes=0)),
      ('erased-duration-difference',PROOFS['postscene_native_state_proof'],lambda v:v['command_duration_changes'].pop()),
      ('claimed-all-final-groups-equal',PROOFS['postscene_native_state_proof'],lambda v:v['five_native_component_equality'].update(models=True)),
      ('erased-actual-hold',PROOFS['actual_proof'],lambda v:v['actual_panels'][0]['holds'].pop()),
      ('lost-FE-null-actor-native-proof',doc['native_font_proof'],lambda v:v['cases'][-1].update(original_null_actor_consumer_preserved=False)),
      ('wrong-FE-font-consumer',DOC,lambda v:v['records'][-1].update(native_display_consumer='original_progressive_54020')),
      ('lost-declared-end-extent',MAP,lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(extent=2)),
    ])
    for gate in doc['records'][0]['review']:mutations.append(('unchecked-'+gate,DOC,lambda v,k=gate:v['records'][0]['review'].update({k:False})))
    for label,p,fn in mutations:reject(label,p,fn)
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    save(ROOT/'atomic_validation_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),parent_ROM_sha256=sha(PARENT.read_bytes()),positive_records=24,positive_proof=str(ROOT/'positive_reconstruction.json'),positive_proof_sha256=sha((ROOT/'positive_reconstruction.json').read_bytes()),negative_cases=negatives,negative_count=len(negatives),all_negatives_reject_before_mutation=True,dependency_files_verified_before_and_after_semantic_injection=True,semantic_injection_not_written_to_disk=True,full_goal_complete=False));print('Atomic24-record reconstruction and '+str(len(negatives))+' semantic negatives passed.')
