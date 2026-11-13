"""Independent two-file reconstruction and pre-commit negative controls for the release adapter."""
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import shachihoko_item116_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_atomic_v6108')
DOC=Path('translations/shachihoko_item116_editorial_manuscript_v2.json')
SEAL=Path('work/analysis/shachihoko_approval_v6106/coordinated_title_description_source_native_actual_approval.json')
BIND=Path('work/analysis/shachihoko_description_consumers_v6092/current218_live_description_getters_two_item_callers_and_exact_owned_representations.json')
NATIVE=Path('work/analysis/shachihoko_native_v6098/all218_live_descriptions_and218_item_names_rebound_to_actual_target.json')
BOOT=Path('work/analysis/shachihoko_boot_v6099/source_bound_growth_boot_input_and_native_allocation_verification.json')
FONTS=Path('work/analysis/shachihoko_detail_fonts_v6101/both_detail_consumers_three_items_two_modes_complete_native_planes.json')
ACTUAL=Path('work/analysis/shachihoko_actual_menu_v6105/actual_menu_two_holds_eight_complete_native_text_fields_and_return.json')
NAMES=Path('work/analysis/shachihoko_combined_name_glyphs_v6107/actual_coordinated_card_and_generated_notice_complete_glyphs.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists();doc=read(DOC);parent=Path(doc['current_ROM']);assert sha(parent.read_bytes())==doc['current_ROM_sha256'];image=NdsImage.open(parent);baseline=NdsImage.open(doc['canonical_baseline']);clean=NdsImage.open(doc['source_ROM'])
    deps={DOC,SEAL,BIND,NATIVE,BOOT,FONTS,ACTUAL,NAMES,Path(__file__).relative_to(Path.cwd()),Path(owned.__file__).relative_to(Path.cwd()),Path('dk4tool/patch/shachihoko_item116_research_v1.py'),Path('dk4tool/patch/shachihoko_item_name_data_v1.py'),Path(doc['target_ARM9']),Path(doc['target_COMMON'])}
    for p in [DOC,SEAL,BIND,NATIVE,BOOT,FONTS,ACTUAL,NAMES]:
        for q,h in read(p).get('evidence',{}).items():assert sha(Path(q).read_bytes())==h;deps.add(Path(q))
    for r in read(SEAL)['viewed_sheets']:assert sha(Path(r['path']).read_bytes())==r['sha256'];deps.add(Path(r['path']))
    for r in read(ACTUAL)['eight_complete_actual_title_description_field_matches']:
        assert sha(Path(r['PNG']).read_bytes())==r['PNG_sha256'];deps.add(Path(r['PNG']))
    for r in read(NAMES)['cases']:assert sha(Path(r['PNG']).read_bytes())==r['PNG_sha256'];deps.add(Path(r['PNG']))
    conf=dict(format=owned.FORMAT,manuscript=str(DOC),approval=str(SEAL),bindings=str(BIND),native=str(NATIVE),boot=str(BOOT),fonts=str(FONTS),actual=str(ACTUAL),actual_names=str(NAMES),
        source_ARM9_sha256=doc['current_ARM9_sha256'],source_COMMON_sha256=doc['current_COMMON_sha256'],target_ARM9_sha256=doc['native_data_plan']['target_ARM9_sha256'],target_COMMON_sha256=doc['native_data_plan']['target_COMMON_sha256'],
        clean_ROM=doc['source_ROM'],clean_ROM_sha256=doc['source_ROM_sha256'],clean_ARM9_sha256=sha(clean.read_file(owned.ARM)),canonical_ARM9_sha256=sha(baseline.read_file(owned.ARM)),
        source_files={p:sha(v) for _,p,v in image.iter_files()},source_components={p:sha(v) for p,v in image.iter_components()},dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps,key=str)},full_goal_complete=False)
    ROOT.mkdir(parents=True);config=ROOT/'positive_config.json';save(config,conf);calls=[];replace=image.replace_file;image.replace_file=lambda *a,**k:(calls.append(a[0]),replace(*a,**k))[1]
    positive=owned.apply_release(image,baseline,config);assert calls==[owned.ARM,owned.COMMON];reference=NdsImage.open(doc['native_reference_ROM']);assert {p:v for p,v in image.iter_components()}=={p:v for p,v in reference.iter_components()} and {p:v for _,p,v in image.iter_files()}=={p:v for _,p,v in reference.iter_files()}
    save(ROOT/'positive_reconstruction.json',positive);negatives=[];original_load=owned.load
    def reject(label,path,change):
        value=deepcopy(read(path));change(value);candidate=NdsImage.open(parent);writes=[];replace=candidate.replace_file;candidate.replace_file=lambda *a,**k:(writes.append(a[0]),replace(*a,**k))[1]
        owned.load=lambda p:value if Path(p)==Path(path) else original_load(p)
        try:
            try:owned.apply_release(candidate,baseline,config)
            except (AssertionError,ValueError,KeyError) as exc:reason=str(exc) or type(exc).__name__
            else:raise RuntimeError('Rejected-control accepted:'+label)
        finally:owned.load=original_load
        assert not writes and candidate.read_file(owned.ARM)==NdsImage.open(parent).read_file(owned.ARM) and candidate.read_file(owned.COMMON)==NdsImage.open(parent).read_file(owned.COMMON)
        negatives.append(dict(label=label,rejected_before_any_image_mutation=True,reason=reason))
    for key in ['source_ARM9_sha256','source_COMMON_sha256','target_ARM9_sha256','target_COMMON_sha256','canonical_ARM9_sha256','clean_ROM_sha256']:
        reject('wrong-'+key,config,lambda v,k=key:v.update({k:'0'*64}))
    reject('lost-route-ancestry',config,lambda v:v['source_files'].update({'/data/SC2.DK4':'0'*64}))
    reject('lost-ARM7-ancestry',config,lambda v:v['source_components'].update({'/__arm7__.bin':'0'*64}))
    for key,value in [('translation_policy','natural-dialogue-v1'),('target_locale','en-GB'),('full_goal_complete',True),('all207_names_all_storylines_and_full_editorial_goal_preserved',False),('no_duplicate_name_dialogue_or_generic_notice_credit',False)]:reject('wrong-'+key,DOC,lambda v,k=key,x=value:v.update({k:x}))
    for i in range(2):
        for gate in ['source','context','localization','naturalness','formatting']:reject(f'record{i}-lost-{gate}',DOC,lambda v,i=i,g=gate:v['records'][i]['review'].update({g:False}))
    reject('invented-extra-record',DOC,lambda v:v['records'].append(deepcopy(v['records'][0])))
    reject('changed-clean-description',DOC,lambda v:v['records'][1].update(source_hex='00'))
    reject('unapproved-guaranteed-effect',DOC,lambda v:v['records'][1].update(english='This figurehead guarantees protection from every storm.'))
    for path,key in [(NATIVE,'all_actual123264_deployed_payload_bytes_and_executed_target_instructions_exact'),(BOOT,'all31_actual_same_input_whole_RGB_frames_equal_V6050'),(BOOT,'complete_actual123264_payload_native_copy_reservation_and_cacheline_extents_verified'),
        (FONTS,'all24_native_field_word_glyph_pixel_bounds_and_parent_crop_cases_pass'),(ACTUAL,'no_RAM_inventory_money_roster_condition_or_RNG_fixture'),(ACTUAL,'all_changed_title_and134_character_description_exact_native_independent_glyphs_and_original_parent_positions'),(NAMES,'no_glyph_or_source_substitution_loss')]:reject('missing-'+key,path,lambda v,k=key:v.update({k:False}))
    reject('incomplete-actual-field-holds',ACTUAL,lambda v:v['eight_complete_actual_title_description_field_matches'].pop())
    reject('unviewed-sheet',SEAL,lambda v:v['viewed_sheets'][0].update(viewed=False))
    save(ROOT/'negative_cases.json',negatives);save(ROOT/'atomic_validation_receipt.json',dict(config=str(config),config_sha256=sha(config.read_bytes()),positive_proof=str(ROOT/'positive_reconstruction.json'),positive_proof_sha256=sha((ROOT/'positive_reconstruction.json').read_bytes()),
        positive_records=2,negative_count=len(negatives),all_negatives_reject_before_any_image_mutation=True,negative_cases=str(ROOT/'negative_cases.json'),parent_ROM=str(parent),parent_ROM_sha256=sha(parent.read_bytes()),locked_dependencies=len(deps),
        exactly_two_image_replacements_after_all_guards=True,all_reference_files_and_components_reconstruct_exactly=True,no_registry_or_ledger_mutation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(records=2,precommit_negative_controls=len(negatives),locked_dependencies=len(deps),all_reject_before_any_mutation=True,reference_components_and_files_exact=True))
