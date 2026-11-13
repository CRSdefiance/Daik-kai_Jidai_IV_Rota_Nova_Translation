"""Register26 guarded reviews after the complete V3487 cumulative stack."""
import ast,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import maria_B109_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B109_registration_v3525')
PROFILE='all-routes-unified-v3526'
PARENT=Path('out/all_routes_combined_v3487_candidate.nds')
DOC=Path('translations/maria_B109_editorial_manuscript_v10.json')
MAP=Path('translations/maria_B109_editorial_relocation_map_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert sha(raw)=='d7c2eb57f3b914aa3f87932fb3085a0eb03394170fb7ba42cbd9f2c55d3993ae' and PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    parent,base=NdsImage.open(PARENT),NdsImage.open('out/raphael_natural_v2_accepted_base.nds');doc,mapping=map(read,[DOC,MAP]);assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']
    deps={str(DOC),str(MAP),str(Path(owned.__file__).relative_to(Path.cwd())),str(Path(__file__).relative_to(Path.cwd())),'dk4tool/dialogue/maria_B109_layout_v2.py','dk4tool/dialogue/maria_B109_profile.py','dk4tool/dialogue/layout.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','docs/editorial_testing_scope_v1870.md','work/analysis/maria_B109_checkpoint_v3524/checkpoint_receipt.json','work/analysis/maria_B109_reference_approval_v3523/approval_receipt.json','work/analysis/maria_B109_loader_v3521/whole_SC3_and_B109_initial_entry_proof.json'}
    deps.update(doc[k] for k in ['source_context','native_font_proof','native_progressive_proof','final_padding_proof','relocated_control_proof','representative_proof','actor_voice_contract','effective_current_comparison','whole_exchange_context_notes'])
    deps.update(mapping[k] for k in ['source_plan','target_block'])
    pending=list(deps);seen=set()
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
    font=read(doc['native_font_proof']);deps.update(s['path'] for s in font['review_sheets']);deps.update(c['preview'] for c in font['cases'])
    actual=read(doc['representative_proof']);deps.update(s['path'] for s in actual['representative_contact_sheets'])
    for r in font['source_and_English_immediate_normal_Hangzhou_return_exact']:deps.add(r['capture'])
    conf=dict(format='dk4-maria-B109-editorial-release-v1',manuscript=str(DOC),reference_map=str(MAP),required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),source_SC3_sha256=mapping['source_SC3_sha256'],target_SC3_sha256=mapping['target_SC3_sha256'],canonical_SC3_sha256=mapping['canonical_SC3_sha256'],clean_SC3_sha256=mapping['clean_SC3_sha256'],clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf);test=NdsImage.open(PARENT);proof=owned.apply_release(test,base,positive)
    research=read('work/analysis/maria_B109_reference_approval_v3523/approval_receipt.json');expected=NdsImage.open(research['research_ROM'])
    assert test.read_file(owned.PATH)==expected.read_file(owned.PATH) and len(proof['changed_records'])==26
    save(ROOT/'positive_reconstruction.json',proof);negatives=[]
    def reject(label,image,baseline,config):
        initial=(image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))
        try:owned.apply_release(image,baseline,config)
        except (AssertionError,ValueError) as error:
            assert (image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))==initial;negatives.append(dict(case=label,rejected_before_mutation=True,error=str(error)))
        else:raise AssertionError(label)
    reject('repeated_application',test,base,positive)
    for label,path in [('wrong_SC3',owned.PATH),('wrong_ARM9','/__arm9__.bin')]:
        im=NdsImage.open(PARENT);v=bytearray(im.read_file(path));v[256]^=1;im.replace_file(path,bytes(v));reject(label,im,base,positive)
    altered=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');v=bytearray(altered.read_file(owned.PATH));v[256]^=1;altered.replace_file(owned.PATH,bytes(v));reject('wrong_canonical',NdsImage.open(PARENT),altered,positive)
    config_edits=[('format',lambda c:c.update(format='wrong')),('clean_ROM_hash',lambda c:c.update(clean_ROM_sha256='0'*64)),('clean_SC3_hash',lambda c:c.update(clean_SC3_sha256='0'*64)),('target_file_hash',lambda c:c.update(target_SC3_sha256='0'*64)),('missing_dependency_hash',lambda c:c['dependencies'].update({str(DOC):'0'*64}))]
    for label,edit in config_edits:
        c=deepcopy(conf);edit(c);cp=ROOT/(label+'_config.json');save(cp,c);reject(label,NdsImage.open(PARENT),base,cp)
    mutations=[
        ('lost_format_gate','manuscript',lambda d:d.update(formatting_review_pending=True)),
        ('wrong_locale','manuscript',lambda d:d.update(target_locale='en-GB')),
        ('old_policy','manuscript',lambda d:d.update(translation_policy='natural-dialogue-v1')),
        ('lost_record','manuscript',lambda d:d['records'].pop()),
        ('lost_context_gate','manuscript',lambda d:d['records'][0]['review'].update(context=False)),
        ('unapproved_prose','manuscript',lambda d:d['records'][0].update(english='{SPEAKER:0B}Changed.')),
        ('lost_static_Ian21','manuscript',lambda d:next(r for r in d['records'] if r['source_selector']==21).update(source_selector=20)),
        ('changed_ellipsis','manuscript',lambda d:next(r for r in d['records'] if r['source_record_index']==68).update(english='{SPEAKER:03}!')),
        ('wrong_prefix_reference','reference_map',lambda d:d['source_owned_control_repair'].update(offset=9)),
        ('invented_prefix_name','reference_map',lambda d:d['source_owned_control_repair'].update(after=owned.BAD_PREFIX.hex())),
        ('missing_source_controls','reference_map',lambda d:d.update(all34_source_command_boundaries26_complete_preambles8_source_non_speech_commands_verified=False)),
        ('missing_actual_gate','reference_map',lambda d:d.update(focused_actual_B109_content_in_B33_entry_fixture_approved=False)),
        ('wrong_entry','reference_map',lambda d:d.update(entry_point_offset=12)),
        ('invented_relative_span','reference_map',lambda d:d.update(relative_skip_fixups=[{}])),
        ('wrong_mapped_command','reference_map',lambda d:d['mapped_native_commands'][0].update(new_offset=10)),
        ('wrong_target_block','reference_map',lambda d:d.update(target_block_sha256='0'*64)),
        ('missing_stored_object','reference_map',lambda d:d['text_records'].pop()),
        ('wrong_stored_parity','reference_map',lambda d:d['text_records'][0].update(parity_space_added=not d['text_records'][0]['parity_space_added'])),
        ('false_natural_activation','reference_map',lambda d:d.update(source_event109_natural_activation_not_claimed=False)),
        ('wrong_loader_gate','relocated_control_proof',lambda d:d.update(all303_loader_cache_hits606_parent_modes_each_image=False)),
        ('wrong_C200_index','relocated_control_proof',lambda d:d['relocated_C200']['source_owned_UI_request_words'].__setitem__(1,0)),
        ('missing_C200_write','relocated_control_proof',lambda d:d['relocated_C200']['source_owned_UI_writes'].pop()),
        ('unowned_C200_write','relocated_control_proof',lambda d:d['relocated_C200'].update(all_other4MiB_actor_roster_event_RNG_and_models_exact=False)),
        ('missing_native_plane','native_font_proof',lambda d:d['cases'].pop()),
        ('lost_glyph_order_gate','native_font_proof',lambda d:d.update(wordless_three_periods_complete_at_origin=False)),
        ('missing_native_negative','native_font_proof',lambda d:d['source_bound_formatter_negatives'].pop()),
        ('unmatched_actual_glyph','representative_proof',lambda d:d.update(unmatched_capture_planes=[dict(missing=1)])),
        ('missing_actual_panel','representative_proof',lambda d:d.update(complete_matching_panels=25)),
        ('false_actual_scope','representative_proof',lambda d:d.update(source_event109_not_selected_or_earned=False)),
        ('missing_stored_macro_case','final_padding_proof',lambda d:d.update(stored_target_macro_alignment_cases=100))]
    for label,key,edit in mutations:
        c=deepcopy(conf);d=deepcopy(doc);m=deepcopy(mapping)
        value=d if key=='manuscript' else m if key=='reference_map' else read(d[key]);edit(value)
        if key not in ['manuscript','reference_map']:
            vp=ROOT/(label+'_proof.json');save(vp,value);d[key]=str(vp);d[key+'_sha256']=sha(vp.read_bytes());c['dependencies'][str(vp)]=sha(vp.read_bytes())
            linked={'relocated_control_proof':'reference_proof','representative_proof':'actual_display_proof','final_padding_proof':'stored_target_proof'}
            if key in linked:m[linked[key]]=str(vp)
        mp=ROOT/(label+'_map.json');save(mp,m);d['reference_map']=str(mp);d['reference_map_sha256']=sha(mp.read_bytes());dp=ROOT/(label+'_manuscript.json');save(dp,d)
        c.update(manuscript=str(dp),reference_map=str(mp));c['dependencies'].update({str(dp):sha(dp.read_bytes()),str(mp):sha(mp.read_bytes())});cp=ROOT/(label+'_config.json');save(cp,c);reject(label,NdsImage.open(PARENT),base,cp)
    assert len(negatives)==39;save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_mutation=True))
    stage=b'''    maria_more = profile_config.get('maria_B109_editorial')
    if maria_more:
        from dk4tool.patch.maria_B109_editorial_v1 import apply_release as apply_maria_more

        maria_more_report = apply_maria_more(candidate, baseline, maria_more)
        grouped.setdefault('/data/SC3.DK4', [])
        changed_records.setdefault('/data/SC3.DK4', []).extend(row['id'] for row in maria_more_report['changed_records'])
        relocation_checks.setdefault('/data/SC3.DK4', {})['maria_B109_editorial'] = {
            'release_config': maria_more,
            'release_config_sha256': sha256(Path(maria_more).read_bytes()),
            'proof': maria_more_report}
        more_batch = Path(maria_more_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('Maria B109 must run once after the complete V3487 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('maria_B109_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');imports=[n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)];assert imports==[owned.__name__]
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(owned.CONFIG,conf);profile=deepcopy(registry['profiles']['all-routes-unified-v3487']);profile.update(maria_B109_editorial=owned.CONFIG,status='experimental',description='Full V3487 cumulative stack plus26 source/context/native reviewed Maria B109 speeches and exact numeric UI-prefix restoration;B33-entry content fixture disclosed.');registry['profiles'][PROFILE]=profile
    builder.write_bytes(after);tmp=rp.with_suffix('.maria_B109.tmp');save(tmp,registry);os.replace(tmp,rp)
    assert read(rp)['accepted_layers']==read(ROOT/'registry_before_raw.json')['accepted_layers'] and read(rp)['latest_promoted_build']==read(ROOT/'registry_before_raw.json')['latest_promoted_build']
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v3487',parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),config=owned.CONFIG,config_sha256=sha(Path(owned.CONFIG).read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),builder_before_sha256=sha(before),builder_after_sha256=sha(after),compiler_module=owned.__name__,compiler_sha256=sha(Path(owned.__file__).read_bytes()),exact_hook_AST_import_verified=True,negative_cases=len(negatives),all_rejected_before_mutation=True,expected_manifest_batches=526,accepted_layers=114,V1492_promotion_unchanged=True,full_goal_complete=False))
    print('Registered V3526 after full V3487;39 negatives pass before mutation,114 accepted layers and V1492 preserved.')
