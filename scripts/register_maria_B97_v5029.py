"""Validate atomic B97 reconstruction and rejection cases before appending its cumulative profile."""
import ast,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import maria_B97_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_registration_v5029')
PROFILE='all-routes-unified-v5030'
PARENT=Path('out/all_routes_combined_v4987_candidate.nds')
DOC=Path('translations/maria_B97_editorial_manuscript_v6.json')
MAP=Path('translations/maria_B97_editorial_relocation_map_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    verified=read('work/analysis/editorial_handoff_verification_v5020/verified_handoff.json');assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256'] and sha(PARENT.read_bytes())==verified['candidate_sha256']
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    doc,mapping=read(DOC),read(MAP);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');parent=NdsImage.open(PARENT)
    deps={str(DOC),str(MAP),'dk4tool/patch/maria_B97_editorial_v1.py','dk4tool/dialogue/maria_B97_layout_v2.py','dk4tool/dialogue/maria_B97_profile.py','dk4tool/dialogue/layout.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','scripts/current_maria_native_context_v4999.py',str(Path(__file__).relative_to(Path.cwd())),'work/analysis/maria_B97_reference_approval_v5026/approval_receipt.json','work/analysis/editorial_handoff_verification_v5020/verified_handoff.json'}
    for k,v in doc.items():
        if k.endswith('_sha256') and k[:-7] in doc and isinstance(doc[k[:-7]],str) and Path(doc[k[:-7]]).is_file():assert sha(Path(doc[k[:-7]]).read_bytes())==v;deps.add(doc[k[:-7]])
    deps.update([mapping['source_plan'],mapping['source_census']]);native=read(doc['native_font_proof']);actualapproval='work/analysis/maria_B97_actual_approval_v5018/all32_native_actual_approval_and_remaining_release_gates.json';deps.add(actualapproval)
    excluded={p.resolve() for p in [rp,builder,Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),*[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]]}
    pending=list(deps);seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p)
        if Path(p).suffix!='.json':continue
        value=read(p)
        if not isinstance(value,dict):continue
        for key in ['evidence','dependencies']:
            if not isinstance(value.get(key),dict):continue
            for item in value[key]:
                if Path(item).is_file() and Path(item).resolve() not in excluded and item not in deps:deps.add(item);pending.append(item)
    for c in native['cases']:deps.add(c['whole_font_plane']);deps.update(p['path'] for p in c['previews'])
    deps.update(p['path'] for p in native['review_sheets']);a=read(actualapproval);deps.update(p['path'] for p in a['all_six_actual_sheets_viewed']+a['four_full_resource_and_final_screens_viewed'])
    conf=dict(format='dk4-maria-B97-editorial-release-v1',manuscript=str(DOC),reference_map=str(MAP),source_SC3_sha256=mapping['source_SC3_sha256'],target_SC3_sha256=mapping['target_SC3_sha256'],clean_SC3_sha256=mapping['clean_SC3_sha256'],canonical_SC3_sha256=mapping['canonical_SC3_sha256'],clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),required_runtime_common_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),actual_approval=actualapproval,dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf);test=NdsImage.open(PARENT);proof=owned.apply_release(test,baseline,positive)
    assert test.read_file(owned.PATH)==Path(read(doc['final_padding_proof'])['target_SC3']).read_bytes() and len(proof['changed_records'])==32;save(ROOT/'positive_reconstruction.json',proof)
    negatives=[];original_load=owned.load
    def reject(label,path,edit):
        image=NdsImage.open(PARENT);paths=[owned.PATH,'/__arm9__.bin','/COMMON/MESFILE.DK4'];initial=[image.read_file(p) for p in paths];value=deepcopy(read(path));old=deepcopy(value);edit(value);assert value!=old,label
        def changed_load(p):return deepcopy(value) if Path(p)==Path(path) else original_load(p)
        owned.load=changed_load
        try:
            try:owned.apply_release(image,baseline,positive)
            except (ValueError,AssertionError,KeyError,IndexError) as error:negatives.append(dict(case=label,rejected=True,error=str(error)))
            else:raise AssertionError('Accepted negative:'+label)
        finally:owned.load=original_load
        assert initial==[image.read_file(p) for p in paths],label
    mutations=[
        ('wrong-format',str(positive),lambda v:v.update(format='unknown')),
        ('wrong-runtime',str(positive),lambda v:v.update(required_runtime_arm9_sha256='0'*64)),
        ('wrong-COMMON',str(positive),lambda v:v.update(required_runtime_common_sha256='0'*64)),
        ('wrong-canonical',str(positive),lambda v:v.update(canonical_SC3_sha256='0'*64)),
        ('wrong-clean',str(positive),lambda v:v.update(clean_SC3_sha256='0'*64)),
        ('missing-record',str(DOC),lambda v:v['records'].pop()),
        ('changed-selector',str(DOC),lambda v:v['records'][0].update(source_selector=3)),
        ('lost-gate',str(DOC),lambda v:v['records'][0]['review'].update(context=False)),
        ('changed-source',str(DOC),lambda v:v['records'][0].update(source_hex='fe48656c6c6f')),
        ('changed-reference',str(DOC),lambda v:v['records'][0]['current_reference'].update(offset=1)),
        ('changed-English',str(DOC),lambda v:v['records'][0].update(english='{SPEAKER:FE}Hello.')),
        ('authored-break',str(DOC),lambda v:v['records'][0].update(english=v['records'][0]['english']+'{LB}')),
        ('authored-padding',str(DOC),lambda v:v['records'][0].update(english=v['records'][0]['english']+'{PAD}')),
        ('changed-compiled',str(DOC),lambda v:v['records'][0].update(compiled_hex='fe48656c6c6f')),
        ('lost-retention-reason',str(DOC),lambda v:next(r for r in v['records'] if r['editorial_decision']=='retain-wording').update(fresh_retained_wording_justification='')),
        ('hardcoded-FO',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==22).update(english="{SPEAKER:03}I'm with Li Clan.")),
        ('false-actual-record',str(DOC),lambda v:v['records'][0].update(actual_B33_content_fixture_observed=False)),
        ('wrong-map-block',str(MAP),lambda v:v.update(block=109)),
        ('missing-map-gate',str(MAP),lambda v:v.update(external_references_complete=False)),
        ('invented-relative',str(MAP),lambda v:v['relative_skip_fixups'].append({})),
        ('lost-command',str(MAP),lambda v:v['mapped_native_commands'].pop()),
        ('wrong-command-offset',str(MAP),lambda v:v['mapped_native_commands'][3].update(new_offset=18)),
        ('wrong-end-command',str(MAP),lambda v:v['mapped_native_commands'][-1].update(word=1)),
        ('wrong-stored-offset',str(MAP),lambda v:v['text_records'][0].update(new_text_offset=1,new_offset=1)),
        ('wrong-parity',str(MAP),lambda v:v['text_records'][0].update(parity_space_added=not v['text_records'][0]['parity_space_added'])),
        ('wrong-target',str(MAP),lambda v:v.update(target_block_sha256='0'*64)),
        ('lost-first-glyph',doc['native_font_proof'],lambda v:v['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),
        ('wrong-native-bounds',doc['native_font_proof'],lambda v:v['cases'][0].update(all_visible_origins_zero_and_current_width_bounds_exact=False)),
        ('lost-second-page',doc['native_font_proof'],lambda v:next(r for r in v['cases'] if r['id']=='DK4_MES_B97_R0072').update(pages_projected=1)),
        ('missing-native-alignment',doc['native_font_proof'],lambda v:v['cases'][0]['current_native_macro_pipelines'][0]['cases'].pop()),
        ('false-native-negative',doc['native_font_proof'],lambda v:v['negative_controls'][0].update(rejected=False)),
        ('unviewed-native-sheet',doc['native_review_proof'],lambda v:v['viewed_sheets'][0].update(viewed_in_full_current_turn=False)),
        ('false-formatter-negative',doc['native_review_proof'],lambda v:v['formatter_negatives'][0].update(rejected=False)),
        ('missing-final-stored',doc['final_padding_proof'],lambda v:v['final_stored_cases'].pop()),
        ('missing-final-alignment',doc['final_padding_proof'],lambda v:v['final_stored_cases'][0]['macro_alignment_cases']['cases'].pop()),
        ('wrong-final-output',doc['final_padding_proof'],lambda v:v['final_stored_cases'][0]['macro_alignment_cases']['cases'][0].update(output_hex='48656c6c6f')),
        ('false-loader',doc['loader_proof'],lambda v:v.update(all303_whole_blocks_and606_modes_each_pass=False)),
        ('false-census',doc['reference_census_proof'],lambda v:v.update(only_original24070_interpreter_call_and_no_literal_alias=False)),
        ('false-end',doc['termination_decode_proof'],lambda v:v.update(all2_declared_end_decodes_return_type0_extent4_without_post_payload_read=False)),
        ('wrong-end-offset',doc['termination_decode_proof'],lambda v:v['cases'][1].update(end_offset=2040)),
        ('wrong-actor-name',doc['source_nameplate_consumer_proof'],lambda v:v['progressive_nameplate_values'].update({'3':'Admiral'})),
        ('wrong-catalogue-name',doc['source_nameplate_consumer_proof'],lambda v:v['full_catalogue_values'].update({'3':'Maria Lee'})),
        ('wrong-voice',doc['actor_voice_contract'],lambda v:next(r for r in v['catalog']['rows'] if r['actor_ID']==10).update(original_voice_class=0)),
        ('wrong-city',doc['item_terminology_reconciliation'],lambda v:v.update(approved_city='Hangzhou')),
        ('wrong-tablet-descriptor',doc['relocated_control_proof'],lambda v:v['target_item_hide_pairs'][0]['target_case']['original_picture_boundary_calls'][0].update(descriptor=[0,175,1,5])),
        ('wrong-hide-cursor',doc['relocated_control_proof'],lambda v:v['target_item_hide_pairs'][1]['target_case']['original_picture_boundary_calls'][0]['args'].__setitem__(3,0x02660000+1896)),
        ('wrong-dispatch-actor',doc['relocated_control_proof'],lambda v:v['relocated_dispatch_cases'][0].update(resolved_actor_ID=3)),
        ('wrong-event',doc['source_entry_proof'],lambda v:v['selected_B97_source_event'].update(event_ID=109)),
        ('missing-actual-version',doc['representative_proof'],lambda v:v['versions'].pop()),
        ('false-actual-page',doc['representative_proof'],lambda v:v.update(complete_actual_panel_pages=32)),
        ('wrong-A-advance',doc['representative_proof'],lambda v:v['source72_page_boundary']['original_A_event'].update(start=14801)),
        ('concealed-page-indent',doc['representative_proof'],lambda v:v['source72_page_boundary'].update(original_continuation_first_row_indent_px=0)),
        ('concealed-final-RGB-difference',doc['representative_proof'],lambda v:v.update(final31000_whole_RGB_equal=True)),
        ('concealed-PRNG-difference',doc['representative_proof'],lambda v:v['final_state_observations']['reviewed_English'].update(original_PRNG_word02168EB8=347786248)),
        ('wrong-timing-disclosure',actualapproval,lambda v:v['measured_timing_differences'].pop()),
        ('unviewed-actual-sheet',actualapproval,lambda v:v['all_six_actual_sheets_viewed'][0].update(viewed_in_full_current_turn=False)),
    ]
    for label,path,edit in mutations:reject(label,path,edit)
    save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_any_image_mutation=True,producer_sha256=sha(Path(__file__).read_bytes())))
    stage=b'''    maria_b97 = profile_config.get('maria_B97_editorial')
    if maria_b97:
        from dk4tool.patch.maria_B97_editorial_v1 import apply_release as apply_maria_b97

        maria_b97_report = apply_maria_b97(candidate, baseline, maria_b97)
        grouped.setdefault('/data/SC3.DK4', [])
        changed_records.setdefault('/data/SC3.DK4', []).extend(row['id'] for row in maria_b97_report['changed_records'])
        relocation_checks.setdefault('/data/SC3.DK4', {})['maria_B97_editorial'] = {
            'release_config': maria_b97,
            'release_config_sha256': sha256(Path(maria_b97).read_bytes()),
            'proof': maria_b97_report}
        more_batch = Path(maria_b97_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('Maria B97 must run once after the complete V4987 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('maria_B97_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[owned.__name__]
    save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);(ROOT/'builder_added_stage.bin').write_bytes(stage);save(owned.CONFIG,conf)
    profile=deepcopy(registry['profiles']['all-routes-unified-v4987']);profile.update(status='experimental',maria_B97_editorial=owned.CONFIG,description='Full V4987 stack plus32 source-context Maria B97 reviews:23 revisions/9 justified retentions. Original40 commands/eight leaves,FO,FE and item/hide/end remain. Source72 uses original A continuation with its measured6px first-row guard. Paired31000-frame B33 content cold boots show all33 complete pages and normal exit;34 timing differences and unequal final RGB/actor/PRNG remain disclosed.',note='All source/native/reference/focused-actual gates approved;registered build,patch and startup pending.');registry['profiles'][PROFILE]=profile
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    with builder.open('r+b') as f:f.write(after);f.truncate();f.flush();os.fsync(f.fileno())
    encoded=(json.dumps(registry,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    with rp.open('r+b') as f:f.write(encoded);f.truncate();f.flush();os.fsync(f.fileno())
    inverse=deepcopy(read(rp));inverse['profiles'].pop(PROFILE);assert inverse==read(ROOT/'release_stack.before.json') and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v4987',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts={str(DOC):sha(DOC.read_bytes())},reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=str(ROOT/'positive_reconstruction.json'),negative_cases=str(ROOT/'negative_cases.json'),negative_count=len(negatives),all_negatives_reject_before_mutation=True,expected_manifest_batches=567,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(registered=PROFILE,positive_records=32,negative_cases=len(negatives),expected_batches=567,accepted=114,promotion_unchanged=True))
