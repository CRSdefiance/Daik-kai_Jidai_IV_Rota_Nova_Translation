"""Run atomic positive/negative checks,then add one cumulative profile and optional typed stage."""
import ast,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B167_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B167_registration_v4159b')
PROFILE='all-routes-unified-v4160'
PARENT=Path('out/all_routes_combined_v4110_candidate.nds')
DOC=Path('translations/lil_B167_editorial_manuscript_v13.json')
MENU=Path('translations/lil_B167_choice_manuscript_v3.json')
MAP=Path('translations/lil_B167_editorial_relocation_map_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp);assert sha(raw)=='88a09b1e14d4937b7e4678e157aebc35d630406910787ecb81493e42bdc36a46' and sha(before)=='eb1e4b87a67d1e2c4df177ffbca61b65ee00b2c56cbd5a72da41f64b8706fa11' and PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4046';doc,menu,mapping=map(read,[DOC,MENU,MAP]);parent,base=NdsImage.open(PARENT),NdsImage.open('out/raphael_natural_v2_accepted_base.nds');assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==menu['current_ROM_sha256'];deps={str(DOC),str(MENU),str(MAP),str(Path(owned.__file__).relative_to(Path.cwd())),str(Path(__file__).relative_to(Path.cwd())),'scripts/prepare_lil_B167_compiler_v4157.py','scripts/prepare_lil_B167_registration_v4158.py','dk4tool/dialogue/lil_B167_layout_v6.py','dk4tool/dialogue/lil_B167_profile.py','dk4tool/dialogue/layout.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','docs/editorial_testing_scope_v1870.md','work/analysis/lil_B167_reference_approval_v4154/approval_receipt.json','work/analysis/lil_B167_loader_v4143/whole_SC2_and_B167_initial_entry_proof.json'}
    deps.update(doc[k] for k in ['source_context','native_font_proof','native_progressive_proof','native_choice_proof','source_nameplate_consumer_proof','final_padding_proof','relocated_control_proof','representative_proof','termination_decode_proof','actor_voice_contract','effective_current_comparison','whole_exchange_context_notes','branch_proof','source_entry_proof','control_contract','actor_terminology_reconciliation','source_effect_and_predicate_contract']);deps.update(mapping[k] for k in ['source_plan','source_census']);pending=list(deps);seen=set();excluded={rp,builder,Path('translations/editorial_review_current_v1.json'),*[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]}
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p)
        if Path(p).suffix!='.json':continue
        value=read(p)
        for key in ['evidence','dependencies']:
            if isinstance(value.get(key),dict):
                for item in value[key]:
                    if Path(item).is_file() and Path(item) not in excluded and item not in deps:deps.add(item);pending.append(item)
    visual=read('work/analysis/lil_B167_transition_review_v4152/both_choices_all5_sheets_static_names_and_distinct_returns_review.json');deps.update(s['path'] for s in visual['English_full_screen_views']+visual['Japanese_full_screen_views']);native=read(doc['native_font_proof']);sample=read(doc['representative_proof']);deps.update(s['path'] for s in native['review_sheets']+sample['viewed_actual_sheets']);deps.update(c['preview'] for c in native['cases']);deps.add(native['choice_review_sheet']['path']);conf=dict(format='dk4-lil-B167-editorial-release-v1',manuscript=str(DOC),choices=str(MENU),reference_map=str(MAP),required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),required_runtime_common_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)});ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf);test=NdsImage.open(PARENT);proof=owned.apply_release(test,base,positive);expected=Path(read(mapping['source_plan'])['target_SC2']).read_bytes();assert test.read_file(owned.PATH)==expected and len(proof['changed_records'])==29;save(ROOT/'positive_reconstruction.json',proof);negatives=[]
    def reject(label,image,baseline,config):
        initial=[image.read_file(p) for p in [owned.PATH,'/__arm9__.bin','/COMMON/MESFILE.DK4']]
        try:owned.apply_release(image,baseline,config)
        except (ValueError,AssertionError,KeyError) as e:negatives.append(dict(case=label,rejected=True,error=str(e)))
        else:raise AssertionError('Accepted negative:'+label)
        assert initial==[image.read_file(p) for p in [owned.PATH,'/__arm9__.bin','/COMMON/MESFILE.DK4']],label
    for label,key,value in [('unknown_format','format','bad'),('wrong_runtime','required_runtime_arm9_sha256','0'*64),('wrong_COMMON','required_runtime_common_sha256','0'*64),('wrong_source','source_SC2_sha256','0'*64),('wrong_canonical','canonical_SC2_sha256','0'*64),('wrong_clean_input','clean_ROM_sha256','0'*64),('wrong_clean_script','clean_SC2_sha256','0'*64),('wrong_target','target_SC2_sha256','0'*64)]:c=deepcopy(conf);c[key]=value;cp=ROOT/(label+'_config.json');save(cp,c);reject(label,NdsImage.open(PARENT),base,cp)
    c=deepcopy(conf);c['dependencies'][str(DOC)]='0'*64;cp=ROOT/'bad_dependency_config.json';save(cp,c);reject('bad_dependency',NdsImage.open(PARENT),base,cp)
    mutations=[
        ('missing_review_gate','manuscript',lambda d:d['records'][0]['review'].update(source=False)),
        ('lost_source0D','manuscript',lambda d:next(r for r in d['records'] if r['source_selector']==13).update(english='We know ships.')),
        ('wrong_legal_source0D','manuscript',lambda d:next(r for r in d['records'] if r['source_selector']==13).update(english='{SPEAKER:02}We know ships.')),
        ('source0D_stripped_as_CR','manuscript',lambda d:next(r for r in d['records'] if r['source_selector']==13).update(source_hex=next(r for r in d['records'] if r['source_selector']==13)['source_hex'][2:])),
        ('printable6D_treated_as_m','manuscript',lambda d:d['records'][0].update(english='mAdmiral!')),
        ('printable6D_stripped','manuscript',lambda d:d['records'][0].update(source_hex=d['records'][0]['source_hex'][2:])),
        ('manual_break','manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+'{LB}')),
        ('manual_padding','manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+'{PAD}')),
        ('invented_FI','manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+' {MACRO:FI}')),
        ('missing_speech','manuscript',lambda d:d['records'].pop()),
        ('wrong_source_reference','manuscript',lambda d:d['records'][0]['source_reference'].update(offset=1)),
        ('wrong_current_reference','manuscript',lambda d:d['records'][0]['current_reference'].update(offset=1)),
        ('missing_choice','choices',lambda d:d['records'].pop()),
        ('swapped_choice_index','choices',lambda d:d['records'][0].update(option_index=1)),
        ('wrong_choice_label','choices',lambda d:d['records'][0].update(english='No')),
        ('wrong_choice_source_pointer','choices',lambda d:d['records'][0]['source_reference'].update(offset=1)),
        ('wrong_whole_choice','choices',lambda d:d['records'][0].update(typed_target_object_hex='002100000000')),
        ('wrong_entry','reference_map',lambda d:d.update(entry_point_offset=10)),
        ('missing_relative_edge','reference_map',lambda d:d['blocks'][0]['relative_skip_fixups'].pop()),
        ('bad_relative_target','reference_map',lambda d:d['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=999)),
        ('lost_separated_end','reference_map',lambda d:d['blocks'][0]['original_declared_end_word_maps'].pop()),
        ('wrong_native_command','reference_map',lambda d:d['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
        ('invented_pause','reference_map',lambda d:d['blocks'][0]['original2000_pause_and_resume_maps'].append({})),
        ('native_missing_plane','native_font_proof',lambda d:d['cases'].pop()),
        ('native_wrong_alignment_count','native_font_proof',lambda d:d.update(current_original_macro_alignment_calls=1)),
        ('native_missing_first_glyph','native_font_proof',lambda d:d['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),
        ('native_wrong_bounds','native_font_proof',lambda d:d['cases'][0].update(all_visible_origins_zero_and16px_rows_within4rows=False)),
        ('stored_missing_target','final_padding_proof',lambda d:d['final_target_parity_cases'].pop()),
        ('stored_wrong_alignment_count','final_padding_proof',lambda d:d.update(current_final_stored_macro_alignment_cases=1)),
        ('lost_relocated_actor','relocated_control_proof',lambda d:d['relocated_dispatch_cases'].pop()),
        ('wrong_relocated_actor0D','relocated_control_proof',lambda d:next(r for r in d['relocated_dispatch_cases'] if r['source_selector']==13).update(resolved_actor_ID=2)),
        ('lost_control_leaf','relocated_control_proof',lambda d:d['all6_source_current_target_nonrelative_nonspeech_nonchoice_leaves'].pop()),
        ('lost_menu_getter_phase','relocated_control_proof',lambda d:d['relocated_choice_getter_phases'].pop()),
        ('missing_actual_boot','representative_proof',lambda d:d.update(new_emulator_runs=0)),
        ('missing_actual_Shipwright_name','representative_proof',lambda d:d.update(actual_Shipwright109_Lil2_Janus4_Manuel23_original_names_and_portraits_observed=False)),
        ('missing_actual_speech','representative_proof',lambda d:d['actual_sampled_display_IDs'].pop()),
        ('missing_actual_choice','representative_proof',lambda d:d['actual_sampled_choice_IDs'].pop()),
        ('invented_natural_source_event','representative_proof',lambda d:d.update(actual_selected_B167_source_events=[167])),
        ('flattened_choice','representative_proof',lambda d:d.update(source_two_Cesare_queries12_relative_containers_choice_and_both_ends_retained_not_flattened=False)),
        ('lost_B22_initialization','representative_proof',lambda d:d.update(original_B22_four_A000_initialization_commands_retained=False)),
        ('lost_actual_four_boots','representative_proof',lambda d:d.update(actual_four_disclosed_cold_boots_pass=False)),
        ('invented_effect_omission','representative_proof',lambda d:d.update(no_B167_effect_or_source_command_omitted=False)),
        ('wrong_Cesare_progressive_name','source_nameplate_consumer_proof',lambda d:d['native_ten_consumer_cases']['rows'][4].update(text='Cesare Tohni')),
        ('wrong_Cesare_full_name','source_nameplate_consumer_proof',lambda d:d['native_ten_consumer_cases']['rows'][5].update(text='Professor Cesare Tony')),
        ('wrong_name_scratch','source_nameplate_consumer_proof',lambda d:d['native_ten_consumer_cases']['rows'][0].update(source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB=False)),
        ('Shipwright_invented_ring','source_nameplate_consumer_proof',lambda d:d['native_ten_consumer_cases']['rows'][8]['original_scratch_rings'].append({})),
        ('Shipwright_illegal_write','source_nameplate_consumer_proof',lambda d:d['native_ten_consumer_cases']['rows'][9]['original_getter_writes'].append({})),
        ('closed_older0D_audit','source_nameplate_consumer_proof',lambda d:d.update(later_older_record0D_reaudit_stays_open=False)),
        ('missing_end_decode','termination_decode_proof',lambda d:d['cases'].pop()),
        ('post_payload_end_read','termination_decode_proof',lambda d:d.update(all4_declared_end_decodes_return_type0_extent4_without_post_payload_read=False)),
        ('wrong_two_end_contract','termination_decode_proof',lambda d:d.update(B167_first_end_precedes_second_end_and_declared_logical_end=False)),
        ('lost_menu_selection_proof','native_choice_proof',lambda d:d.update(six_original_VM_selection_and_cancel_cases_pass=False)),
        ('lost_menu_glyph_proof','native_choice_proof',lambda d:d.update(eight_complete_native_style_label_planes_pass=False)),
        ('lost_Cesare_pair','relocated_control_proof',lambda d:d['relocated_predicate_pairs'].pop()),
        ('wrong_Cesare_result','relocated_control_proof',lambda d:d['relocated_predicate_pairs'][1]['relocated_case'].update(native_result=[2,9,0,0,0,0])),
        ('lost_offline_Cesare','representative_proof',lambda d:d['offline_only_display_IDs'].clear()),
        ('false_actual_Cesare','representative_proof',lambda d:d['offline_only_display_cases'][0].update(actual_display_or_byte_identical_reuse_claim=True)),
        ('wrong_offline_Cesare_actor','representative_proof',lambda d:d['offline_only_display_cases'][1].update(source_selector=2)),
    ]
    def changed_actual(sample,kind):
        old=next(p for p in sample['evidence'] if p.endswith('actual_both_choices_conditional_panels_and_distinct_returns.json'));value=read(old)
        if kind=='wrong_final_menu_word':next(v for v in value['versions'] if v['option_index']==1)['selected_B22_command_pairs'][-1]['result_words']=[0,1]
        elif kind=='wrong_refusal_end':next(v for v in value['versions'] if v['option_index']==1)['source_end_offset']=2172
        elif kind=='wrong_actual_choice':next(v for v in value['versions'] if v['option_index']==1)['actual_choice_command_pair']['result_words']=[2,0]
        else:value['versions'].pop()
        path=ROOT/kind/'actual_both_choices_conditional_panels_and_distinct_returns.json';path.parent.mkdir(parents=True);save(path,value);sample['evidence'].pop(old);sample['evidence'][str(path)]=sha(path.read_bytes())
    mutations.extend((kind,'representative_proof',lambda d,kind=kind:changed_actual(d,kind)) for kind in ['wrong_final_menu_word','wrong_refusal_end','wrong_actual_choice','missing_actual_version'])
    for flag in owned.FLAGS:mutations.append(('map_'+flag,'reference_map',lambda d,flag=flag:d.update({flag:False})))
    for label,key,edit in mutations:
        d,m,u,c=deepcopy(doc),deepcopy(mapping),deepcopy(menu),deepcopy(conf)
        if key in ['manuscript','choices','reference_map']:edit({'manuscript':d,'choices':u,'reference_map':m}[key])
        else:
            v=read(doc[key]);edit(v);vp=ROOT/(label+'_proof.json');save(vp,v);d[key]=str(vp);d[key+'_sha256']=sha(vp.read_bytes());c['dependencies'][str(vp)]=sha(vp.read_bytes())
        mp=ROOT/(label+'_map.json');save(mp,m)
        for obj in [d,u]:obj['reference_map']=str(mp);obj['reference_map_sha256']=sha(mp.read_bytes())
        dp,up=ROOT/(label+'_manuscript.json'),ROOT/(label+'_choices.json');save(dp,d);save(up,u);c.update(manuscript=str(dp),choices=str(up),reference_map=str(mp));c['dependencies'].update({str(p):sha(p.read_bytes()) for p in [mp,dp,up]});cp=ROOT/(label+'_config.json');save(cp,c);reject(label,NdsImage.open(PARENT),base,cp)
    assert len(negatives)==9+len(mutations);save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_mutation=True));stage=b'''    lil_sail_lesson = profile_config.get('lil_B167_editorial')
    if lil_sail_lesson:
        from dk4tool.patch.lil_B167_editorial_v2 import apply_release as apply_lil_sail_lesson

        lil_sail_lesson_report = apply_lil_sail_lesson(candidate, baseline, lil_sail_lesson)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_sail_lesson_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B167_editorial'] = {
            'release_config': lil_sail_lesson,
            'release_config_sha256': sha256(Path(lil_sail_lesson).read_bytes()),
            'proof': lil_sail_lesson_report}
        for more_batch in [Path(lil_sail_lesson_report['manuscript']), Path(lil_sail_lesson_report['choices'])]:
            if more_batch in release_batches:
                raise ValueError('B167 must run once after the complete V4110 stack')
            release_batches.append(more_batch)

''';anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B167_editorial')" not in before;after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[owned.__name__];save(ROOT/'builder_hook_AST_review.json',dict(import_module=owned.__name__,explicit_profile_field='lil_B167_editorial',after_full_V4110_before_literal_percent_safety=True,stage_sha256=sha(stage),all_unowned_builder_bytes_exact=True));save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before);save(owned.CONFIG,conf);profile=deepcopy(registry['profiles']['all-routes-unified-v4110']);profile.update(status='experimental',lil_B167_editorial=owned.CONFIG,description='Full V4110 cumulative stack plus29 complete Lil B167 sail-lesson reviews:16 revisions/13 retentions;27 speeches/two labels,46 commands/twelve spans,two Cesare queries,two resources and two separate ends. Four retained-condition B22 cold boots:25 unique/28 observed speeches,both menu outcomes and distinct normal returns;two conditional Cesare remarks offline-only. Native first/final glyphs,full source controls and exact clean-input patch required. No natural event eligibility or hardware claim.');registry['profiles'][PROFILE]=profile;assert registry['accepted_layers']==read(rp)['accepted_layers'] and registry['latest_promoted_build']==read(rp)['latest_promoted_build'] and rp.read_bytes()==raw and builder.read_bytes()==before;tmp=builder.with_name('build_integrated_release_v4159.tmp');assert not tmp.exists();tmp.write_bytes(after);os.replace(tmp,builder);save(rp,registry);check=deepcopy(read(rp));check['profiles'].pop(PROFILE);assert check==read(ROOT/'release_stack.before.json') and builder.read_bytes().replace(stage,b'',1)==before;save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v4110',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts={str(p):sha(p.read_bytes()) for p in [DOC,MENU]},reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=str(ROOT/'positive_reconstruction.json'),negative_cases=str(ROOT/'negative_cases.json'),negative_count=len(negatives),all_negatives_reject_before_mutation=True,expected_manifest_batches=543,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4046',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(registered=PROFILE,positive_records=29,negative_cases=len(negatives),expected_batches=543,accepted=114,promotion_unchanged=True))
