"""Audit, apply and postverify the lossless B186 checkpoint without adding coverage."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
import argparse,gzip,json,os,struct
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

CHECKPOINT=Path('work/analysis/lil_B186_checkpoint_v5173')
ROOT=Path('work/analysis/editorial_handoff_verification_v5174')

def audit(entry,current):
    doc=read(entry['manuscript']);assert sha(Path(entry['manuscript']).read_bytes())==entry['manuscript_sha256']
    assert len(doc['records'])==len(entry['records'])==entry['approved_uncredited_objects']==12
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':7,'retain-wording':5}
    assert entry['source_prose_or_completion_credit_added']==doc['source_prose_or_completion_credit_added']==0
    for path,digest in entry['evidence'].items():assert sha(Path(path).read_bytes())==digest
    image,clean=NdsImage.open(current['path']),NdsImage.open('work/clean.nds')
    blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    japanese=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[186];old=blocks[186]
    assert sha(Path(current['path']).read_bytes())==current['sha256']==doc['current_ROM_sha256']
    assert sha(image.read_file('/__arm9__.bin'))==doc['required_runtime_ARM9_sha256']
    font=read(doc['native_font_proof']);cases={r['id']:r for r in font['cases']}
    assert len(cases)==12 and font['current_original_macro_alignment_calls']==96
    assert (font['complete_progressive_planes'],font['complete_FE_logical_and_physical_planes'])==(11,1)
    assert len(font['negative_controls'])==18 and all(r['rejected'] for r in font['negative_controls'])
    native=read('work/analysis/lil_B186_native_approval_v5156/all12_source_prose_current_native_approval.json')
    assert len(native['formatter_negatives'])==len(set(native['formatter_negatives']))==28
    assert len(native['reviewed_sheets'])==2 and all(r['viewed_in_full_current_turn'] for r in native['reviewed_sheets'])
    for compact,row in zip(entry['records'],doc['records'],strict=True):
        assert all(row['review'].values()) and row['actual_B22_display_fixture_observed']
        for key in ['id','file_path','block','source_reference','current_reference','source_hex','current_hex','source_Japanese','english','source_selector','source_complete_preamble_hex','speaker','source_meaning','localization_note','editorial_decision','review']:
            assert compact[key]==row[key]
        for data,key,hexkey in [(japanese,'source_reference','source_hex'),(old,'current_reference','current_hex')]:
            at=row[key]['offset'];value=bytes.fromhex(row[hexkey])
            assert data[at:at+len(value)]==value and data[at+len(value)]==0
            assert data[at-5:at+1].hex()==row['source_complete_preamble_hex']
        case=cases[row['id']];assert case['encoded_hex']==row['compiled_hex']
        assert case['all_first_final_internal_glyphs_in_order_and_unique_cells'] and case['one_native_page_consumes_complete_target']
        assert case['all_visible_origins_zero_and_within_four_rows']
        assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
        if row['editorial_decision']=='retain-wording':
            assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and compact['fresh_retained_wording_justification']
        if row['source_record_index']==13:
            assert len(row['reviewed_ordinary_boundaries'])==2 and compact['reviewed_ordinary_boundaries']==row['reviewed_ordinary_boundaries']
        else:assert not compact.get('reviewed_ordinary_boundaries')
    wrap=read(doc['source_bound_wrap_refinement_proof'])
    assert wrap['only_changed_record_IDs']==['DK4_MES_B186_R0013'] and wrap['all12_words_controls_and_prose_unchanged']
    assert wrap['eleven_other_compiled_targets_exact'] and wrap['eleven_other_native_planes_exact']
    assert len(wrap['exact_source_and_prose_mutation_controls'])==6
    assert [s.strip() for s in bytes.fromhex(cases['DK4_MES_B186_R0013']['encoded_hex'])[1:].decode('ascii').splitlines()]==[
        "Yes! The customers won't be",'satisfied with a flavor this','light. It has to be sweeet! Sweet!']
    terms=read(doc['actor_terminology_reconciliation'])
    assert terms['approved_prose_names']=={'174':'Owner','175':'Cook'}
    assert [r['text'] for r in terms['two_source_current_city_aliases']]==['アレキサンドリア','Alexandria']
    assert terms['one_current_alias_still_Japanese_and_caller_unreviewed']
    assert terms['Sweets_is_broad_source_supported_collective_not_a_single_commodity_ID_or_new_UI_category']
    assert not terms['no_predecessor_English_exposed'] and terms['exposure_disclosure']
    mapping=read(doc['reference_map']);spec=mapping['blocks'][0];target=Path(spec['research_block']).read_bytes()
    assert (spec['block'],spec['source_bytes'],spec['source_logical_end'],spec['research_bytes'],spec['research_logical_end'])==(186,652,650,584,582)
    assert sha(old)==spec['source_block_sha256'] and sha(target)==spec['target_block_sha256']
    assert old[650:]==target[582:]==bytes(2) and old[646:650]==target[578:582]==bytes(4)
    assert len(spec['text_records'])==12 and len(spec['relative_skip_fixups'])==6 and len(spec['target_native_skip_cases'])==30
    assert len(spec['mapped_native_commands'])==len(spec['command_map'])==24
    restored=bytearray(target[:582]);struct.pack_into('<H',restored,4,642)
    for edge in spec['relative_skip_fixups']:struct.pack_into('<H',restored,edge['new_offset']+2,edge['source_span'])
    for row in sorted(spec['text_records'],key=lambda r:r['new_offset'],reverse=True):
        at=row['new_offset'];value=bytes.fromhex(row['target_hex']);assert target[at:at+len(value)]==value
        restored[at:at+len(value)]=old[row['old_offset']:row['old_offset']+row['old_length']]
    assert bytes(restored)+old[650:]==old
    stored=read(doc['final_padding_proof'])
    assert len(stored['final_target_parity_cases'])==12 and stored['current_final_stored_macro_alignment_cases']==48
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(36,12)
    controls=read(doc['relocated_control_proof'])
    assert len(controls['relocated_dispatch_cases'])==12 and len(controls['all6_exact_nonrelative_leaves'])==6
    assert len(controls['all5_source_and_relocated_structural_paths_identical'])==5
    assert [(r['old_offset'],r['new_offset']) for r in controls['predicate_pairs']]==[(540,478)]
    ownership=read('work/analysis/lil_B186_predicate700_v5159/all12_aligned_and_unaligned_original700_ownership_cases.json')
    assert len(ownership['cases'])==12 and ownership['unforced_cases']==3 and ownership['CPU_only_boundary_fixture_cases']==9
    assert ownership['actual_emulator_seed_writes']==0
    assert all(r['threshold']==700 and r['full4MiB_difference_exactly_original_owned_RNG_and_optional_operand_scratch'] for r in ownership['cases'])
    assert {r['roll'] for r in ownership['cases'] if not r['unforced_current_snapshot']}=={699,700,701}
    research=read('work/analysis/lil_B186_research_v5161/research_image_receipt.json')
    assert research['parent_sha256']==current['sha256'] and sha(Path(research['research_ROM']).read_bytes())==research['research_ROM_sha256']
    loader=read('work/analysis/lil_B186_loader_v5162/whole_SC2_and_B186_initial_entry_proof.json')
    assert (loader['fresh_research_whole_SC2_loads'],loader['fresh_parent_modes'],loader['exact_parent_reused_whole_SC2_loads'],loader['exact_parent_reused_modes'])==(336,672,336,672)
    for version in loader['versions']:
        for k in ['load','parent']:assert sha(Path(version[k+'_proof']).read_bytes())==version[k+'_sha256']
    visual=read(doc['postscene_native_state_proof'])
    assert not visual['visual_review_pending'] and visual['all47_complete_native_holds_and115_paired_nontext_samples_pass']
    assert visual['fixture_return_frames']==[5735,5737] and visual['exact_timing_difference_counts']==dict(total=10,speech=4,control_or_end=6)
    assert len(visual['sampled_postscene_whole_RGB_differences_unmasked'])==4
    assert visual['postscene9001_PRNG_seeds']==[1803218166,2467799992] and not visual['PRNG_equality']
    assert visual['whole_RGB_final9001_equal'] and all(visual['postscene9001_native_component_equality'].values())
    assert visual['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert len(visual['all_actual_consumer_sheets_viewed'])==2 and len(visual['paired_full_screen_views'])==5
    assert sum(len(s['frames'])*2 for s in visual['paired_full_screen_views'])==20
    assert all(s['viewed_after_image_return'] for s in visual['all_actual_consumer_sheets_viewed']+visual['paired_full_screen_views'])
    assert visual['reaped_tool_sessions']==[17715,18367] and visual['total_frames']==18002
    assert entry['atomic_compiler_registered_patch_and_current_startup_pending']
    assert entry['new_emulator_runs']==2 and entry['new_research_ROMs']==3
    fixture=read('work/analysis/lil_B186_display_fixture_v5166/complete_B186_B22_fixtures.json')
    pins=read('translations/rom_retention_pins.json')
    for p in [research['research_ROM'],*[f['research_ROM'] for f in fixture['fixtures']]]:
        assert any(Path(r['path']).resolve()==Path(p).resolve() for r in pins)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');parser.add_argument('--post',action='store_true')
    args=parser.parse_args();assert not(args.apply and args.post)
    planpath=CHECKPOINT/'mutation_plan.json';plan=read(planpath);files=plan['files'];assert len(files)==6
    old_bytes=gzip.decompress((CHECKPOINT/'ledger.before.json.gz').read_bytes());old=json.loads(old_bytes)
    lp=Path('translations/editorial_review_current_v1.json')
    row=next(r for r in files if Path(r['target'])==lp.resolve());new=read(row['staged'])
    inverse=deepcopy(new);inverse['latest_checkpoint']=inverse.pop(plan['previous_key']);entry=inverse.pop(plan['ledger_key']);assert inverse==old
    assert Path(row['staged']).read_bytes()==encode_ledger(new) and Path(row['staged']).stat().st_size<100*1024*1024
    assert tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6015,6018,3811,2204)
    assert new['current_integrated_candidate']==old['current_integrated_candidate'] and new['goal_status']=='active' and not new['full_goal_complete']
    known={historical_key(r) for r in new['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert len(known)==6015 and not known&{historical_key(r) for r in entry['records']}
    for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
    current=new['current_integrated_candidate'];audit(entry,current)
    prior=read('work/analysis/editorial_handoff_verification_v5128/verified_handoff.json')
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    manifest=read(current['manifest']);registry=read('translations/release_stack.json')
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches'])==569 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    workspace=Path.cwd().resolve()
    for r in files:
        assert Path(r['target']).is_relative_to(workspace) and Path(r['staged']).is_relative_to(CHECKPOINT.resolve())
        assert sha(Path(r['staged']).read_bytes())==r['after_sha256']
        assert sha(Path(r['target']).read_bytes())==r['after_sha256' if args.post else 'before_sha256']
    ROOT.mkdir(parents=True,exist_ok=True)
    receipt=dict(ledger_sha256=row['after_sha256'],candidate=current['path'],candidate_sha256=current['sha256'],
        patch=prior['patch'],patch_sha256=prior['patch_sha256'],mutation_plan_sha256=sha(planpath.read_bytes()),
        all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,
        completed=6015,source_prose=6018,revised=3811,retained=2204,SC2=4130,SC3=96,reviewed_routes=4416,completed_routes=4416,
        approved_uncredited_B186_objects=12,B186_revised=7,B186_retained=5,
        exact_source_current_native_relocation_and_representative_actual_proofs_bound=True,
        R13_early_wrap_corrected_without_words_font_width_guards_or_other11_plane_changes=True,
        actual_unique_speeches=12,actual_complete_holds=47,actual_nontext_pairs=115,viewed_fullscreens=20,
        ten_timing_four_indicator_and_unequal_RNG_differences_preserved=True,
        all569_manifest_batches114_accepted18_checks_preserved_without_rerun=True,main_V4701_preserved=True,
        all_sessions_terminal_and_reaped=True,atomic_compiler_registered_integration_patch_and_current_startup_pending=True,
        full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
    if args.apply:
        pre=read(ROOT/'pre_apply_audit.json');assert pre['mutation_plan_sha256']==receipt['mutation_plan_sha256']
        assert not(ROOT/'applied_handoff.json').exists()
        # Validate every target and staged digest before the first write.
        for r in files:
            assert sha(Path(r['target']).read_bytes())==r['before_sha256']
            assert sha(Path(r['staged']).read_bytes())==r['after_sha256']
        for r in files:
            data=Path(r['staged']).read_bytes()
            with Path(r['target']).open('r+b') as stream:stream.write(data);stream.truncate();stream.flush();os.fsync(stream.fileno())
            assert sha(Path(r['target']).read_bytes())==r['after_sha256']
        save(ROOT/'applied_handoff.json',receipt)
    elif args.post:
        assert read(ROOT/'applied_handoff.json')['mutation_plan_sha256']==receipt['mutation_plan_sha256']
        assert not(ROOT/'verified_handoff.json').exists();save(ROOT/'verified_handoff.json',receipt)
    else:
        assert not(ROOT/'pre_apply_audit.json').exists();save(ROOT/'pre_apply_audit.json',receipt)
    print(dict(applied=args.apply,post_verified=args.post,files=6,uncredited_B186=12,all_history_preserved=True,full_goal_active=True))
