"""Register14 guarded funding reviews after the complete V3526 cumulative stack."""
import ast,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B141_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B141_registration_v3560')
PROFILE='all-routes-unified-v3561'
PARENT=Path('out/all_routes_combined_v3526_candidate.nds')
DOC=Path('translations/lil_B141_editorial_manuscript_v7.json')
MAP=Path('translations/lil_B141_editorial_relocation_map_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert sha(raw)=='b67df9838ccbba54184c17c9954265096f3dcee55ec16f33181609a8a9ee55ea' and PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    parent,base=NdsImage.open(PARENT),NdsImage.open('out/raphael_natural_v2_accepted_base.nds');doc,mapping=map(read,[DOC,MAP]);assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']
    deps={str(DOC),str(MAP),str(Path(owned.__file__).relative_to(Path.cwd())),str(Path(__file__).relative_to(Path.cwd())),'dk4tool/dialogue/lil_B141_layout_v2.py','dk4tool/dialogue/lil_B141_profile.py','dk4tool/dialogue/layout.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','docs/editorial_testing_scope_v1870.md','work/analysis/editorial_handoff_verification_v3552/verified_handoff.json','work/analysis/lil_B141_reference_approval_v3559/approval_receipt.json','work/analysis/lil_B141_loader_v3555/whole_SC2_and_B141_initial_entry_proof.json'}
    deps.update(doc[k] for k in ['source_context','native_font_proof','native_progressive_proof','final_padding_proof','relocated_control_proof','representative_proof','termination_proof','actor_voice_contract','effective_current_comparison','whole_exchange_context_notes','branch_proof','source_finance_contract','source_entry_proof','control_contract','item_terminology_reconciliation'])
    deps.update(mapping[k] for k in ['source_plan','source_census']);pending=list(deps);seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p)
        if Path(p).suffix!='.json':continue
        d=read(p)
        for key in ['evidence','dependencies']:
            if isinstance(d.get(key),dict):
                for item in d[key]:
                    if Path(item).is_file() and item not in deps:deps.add(item);pending.append(item)
    native=read(doc['native_font_proof']);deps.update(s['path'] for s in native['review_sheets']);deps.update(c['preview'] for c in native['cases'])
    for k in ['historical_representative_sheet_review','prior_current_sheet_review']:deps.add(doc[k]);deps.add(read(doc[k])['sheet'])
    conf=dict(format='dk4-lil-B141-editorial-release-v1',manuscript=str(DOC),reference_map=str(MAP),required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf);test=NdsImage.open(PARENT);proof=owned.apply_release(test,base,positive);expected=Path(read(mapping['source_plan'])['target_SC2']).read_bytes();assert test.read_file(owned.PATH)==expected and len(proof['changed_records'])==14;save(ROOT/'positive_reconstruction.json',proof);negatives=[]
    def reject(label,image,baseline,config):
        initial=(image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))
        try:owned.apply_release(image,baseline,config)
        except (AssertionError,ValueError) as e:assert (image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))==initial;negatives.append(dict(case=label,rejected_before_mutation=True,error=str(e)))
        else:raise AssertionError(label)
    reject('repeated_application',test,base,positive)
    for label,path in [('wrong_SC2',owned.PATH),('wrong_ARM9','/__arm9__.bin')]:
        im=NdsImage.open(PARENT);v=bytearray(im.read_file(path));v[256]^=1;im.replace_file(path,bytes(v));reject(label,im,base,positive)
    altered=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');v=bytearray(altered.read_file(owned.PATH));v[256]^=1;altered.replace_file(owned.PATH,bytes(v));reject('wrong_canonical',NdsImage.open(PARENT),altered,positive)
    config_edits=[('format',lambda c:c.update(format='wrong')),('clean_ROM_hash',lambda c:c.update(clean_ROM_sha256='0'*64)),('clean_SC2_hash',lambda c:c.update(clean_SC2_sha256='0'*64)),('target_file_hash',lambda c:c.update(target_SC2_sha256='0'*64)),('dependency_hash',lambda c:c['dependencies'].update({str(DOC):'0'*64}))]
    for label,edit in config_edits:c=deepcopy(conf);edit(c);cp=ROOT/(label+'_config.json');save(cp,c);reject(label,NdsImage.open(PARENT),base,cp)
    mutations=[
        ('lost_format_gate','manuscript',lambda d:d.update(formatting_review_pending=True)),
        ('wrong_locale','manuscript',lambda d:d.update(target_locale='en-GB')),
        ('old_policy','manuscript',lambda d:d.update(translation_policy='natural-dialogue-v1')),
        ('lost_record','manuscript',lambda d:d['records'].pop()),
        ('lost_context_gate','manuscript',lambda d:d['records'][0]['review'].update(context=False)),
        ('unapproved_prose','manuscript',lambda d:d['records'][0].update(english='{SPEAKER:02}Changed.')),
        ('lost_static_Camille9','manuscript',lambda d:next(r for r in d['records'] if r['source_selector']==9).update(source_selector=8)),
        ('lost_FI_substitution','manuscript',lambda d:next(r for r in d['records'] if r['source_record_index']==66).update(english='{SPEAKER:AB}Lil... Oh, this is...')),
        ('wrong_stored_parity','reference_map',lambda d:d['blocks'][0]['text_records'][0].update(parity_space_added=not d['blocks'][0]['text_records'][0]['parity_space_added'])),
        ('missing_external_refs','reference_map',lambda d:d.update(external_references_complete=False)),
        ('conflated_threshold900000','reference_map',lambda d:d.update(original_source_threshold_gold=900000)),
        ('wrong_payment_million','reference_map',lambda d:d.update(original_source_payment_gold=1000000)),
        ('missing_in_block_terminator','reference_map',lambda d:d.update(both_funding_paths_end_at_in_block0000_terminator=False)),
        ('invented_zero_tail_dependency','reference_map',lambda d:d.update(no_zero_cache_tail_dependency=False)),
        ('missing_relative_span','reference_map',lambda d:d['blocks'][0]['relative_skip_fixups'].pop()),
        ('wrong_relative_target','reference_map',lambda d:d['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=0)),
        ('wrong_mapped_command','reference_map',lambda d:d['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
        ('missing630A_gate','reference_map',lambda d:d.update(opaque630A_source_operand_and_original_boundary_preserved=False)),
        ('missing_C200_gate','reference_map',lambda d:d.update(C200_source_index0_nine_UI_writes_and_unowned_RAM_preserved=False)),
        ('wrong_entry','reference_map',lambda d:d.update(entry_point_offset=12)),
        ('wrong_target_block','reference_map',lambda d:d['blocks'][0].update(target_block_sha256='0'*64)),
        ('wrong_C200_index','relocated_control_proof',lambda d:d['relocated_C200_pairs'][0]['cases'][0]['source_owned_UI_request_words'].__setitem__(1,54)),
        ('lost_C200_write','relocated_control_proof',lambda d:d['relocated_C200_pairs'][0]['cases'][0]['source_owned_UI_writes'].pop()),
        ('unowned_money_write','relocated_control_proof',lambda d:d['relocated_financial_boundary_cases'][0]['relocated_payment'].update(all_other4MiB_actor_roster_event_RNG_models_ABI_input_owner_and_output_guards_exact=False)),
        ('wrong_equal_threshold_result','relocated_control_proof',lambda d:next(c for c in d['relocated_financial_boundary_cases'] if c['input_funds']==1000000)['relocated_source_predicate']['native_result'].__setitem__(1,2)),
        ('wrong_payment_delta','relocated_control_proof',lambda d:d['relocated_financial_boundary_cases'][-1]['relocated_payment'].update(after_funds=1000000)),
        ('missing_money_boundary','relocated_control_proof',lambda d:d['relocated_financial_boundary_cases'].pop()),
        ('missing_dispatch','relocated_control_proof',lambda d:d['relocated_dispatch_cases'].pop()),
        ('changed_predicate_operand','relocated_control_proof',lambda d:d['relocated_predicate_pairs'][0]['cases'][0].update(source_command_hex='0080ffff00000000')),
        ('missing_native_plane','native_font_proof',lambda d:d['cases'].pop()),
        ('missing_native_negative','native_font_proof',lambda d:d['source_bound_formatter_negatives'].pop()),
        ('wrong_VM_return','termination_proof',lambda d:d.update(original_VM_return_address=0x02023F50)),
        ('missing_VM_tail_case','termination_proof',lambda d:d['cases'].pop()),
        ('false_tail_canary_gate','termination_proof',lambda d:d.update(all36_original_parent_VM_tail_cases_return_before_unowned_cache_bytes=False)),
        ('jump_to_logical_end','termination_proof',lambda d:d.update(source_insufficient_jump_target=974)),
        ('invented_actual_B141_visit','representative_proof',lambda d:d.update(actual_selected_B141_IDs=['DK4_MES_B141_R0015'])),
        ('missing_representative_approval','representative_proof',lambda d:d.update(no_open_translation_specific_display_or_control_finding=False)),
        ('missing_stored_macro_cases','final_padding_proof',lambda d:d.update(current_final_padded_macro_alignment_cases=52))]
    for label,key,edit in mutations:
        c=deepcopy(conf);d=deepcopy(doc);m=deepcopy(mapping);value=d if key=='manuscript' else m if key=='reference_map' else read(d[key]);edit(value)
        if key not in ['manuscript','reference_map']:
            vp=ROOT/(label+'_proof.json');save(vp,value);d[key]=str(vp);d[key+'_sha256']=sha(vp.read_bytes());c['dependencies'][str(vp)]=sha(vp.read_bytes())
            if key in ['termination_proof','representative_proof']:m[key]=str(vp)
        mp=ROOT/(label+'_map.json');save(mp,m);d['reference_map']=str(mp);d['reference_map_sha256']=sha(mp.read_bytes());dp=ROOT/(label+'_manuscript.json');save(dp,d);c.update(manuscript=str(dp),reference_map=str(mp));c['dependencies'].update({str(mp):sha(mp.read_bytes()),str(dp):sha(dp.read_bytes())});cp=ROOT/(label+'_config.json');save(cp,c);reject(label,NdsImage.open(PARENT),base,cp)
    assert len(negatives)==9+len(mutations);save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_mutation=True))
    stage=b'''    lil_funding = profile_config.get('lil_B141_editorial')
    if lil_funding:
        from dk4tool.patch.lil_B141_editorial_v1 import apply_release as apply_lil_funding

        lil_funding_report = apply_lil_funding(candidate, baseline, lil_funding)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_funding_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B141_editorial'] = {
            'release_config': lil_funding,
            'release_config_sha256': sha256(Path(lil_funding).read_bytes()),
            'proof': lil_funding_report}
        more_batch = Path(lil_funding_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B141 must run once after the complete V3526 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B141_editorial')" not in before;after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[owned.__name__]
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage);save(owned.CONFIG,conf);profile=deepcopy(registry['profiles']['all-routes-unified-v3526']);profile.update(lil_B141_editorial=owned.CONFIG,status='experimental',description='Full V3526 cumulative stack plus14 reviewed Lil B141 funding speeches and13 exact source relative-span fixups;one-million threshold and900000 payment remain distinct.');registry['profiles'][PROFILE]=profile;builder.write_bytes(after);tmp=rp.with_suffix('.lil_B141.tmp');save(tmp,registry);os.replace(tmp,rp)
    assert read(rp)['accepted_layers']==read(ROOT/'registry_before_raw.json')['accepted_layers'] and read(rp)['latest_promoted_build']==read(ROOT/'registry_before_raw.json')['latest_promoted_build']
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v3526',parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),config=owned.CONFIG,config_sha256=sha(Path(owned.CONFIG).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(after),compiler_module=owned.__name__,compiler_sha256=sha(Path(owned.__file__).read_bytes()),exact_hook_AST_import_verified=True,negative_cases=len(negatives),all_rejected_before_mutation=True,expected_manifest_batches=527,accepted_layers=114,V1492_promotion_unchanged=True,full_goal_complete=False));print(dict(registered=PROFILE,negative_cases=len(negatives),expected_batches=527,accepted_layers=114,promotion_unchanged=True))
