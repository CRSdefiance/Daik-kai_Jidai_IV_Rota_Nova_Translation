"""Independently audit staged B182 coverage, then apply or verify exact six-file state."""
from copy import deepcopy
from pathlib import Path
import argparse
import gzip
import json
import os
from collections import Counter
from PIL import Image,ImageChops
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

CHECKPOINT=Path('work/analysis/lil_B182_reference_checkpoint_v4910')
ROOT=Path('work/analysis/editorial_handoff_verification_v4911')

def verify_evidence(obj):
    for p,h in obj.get('evidence',{}).items():assert sha(Path(p).read_bytes())==h,(p,'changed')

def audit_scene(entry,current):
    doc=read(entry['manuscript']);assert sha(Path(entry['manuscript']).read_bytes())==entry['manuscript_sha256']
    assert entry['records']==doc['records'] and entry['approved_uncredited_objects']==len(doc['records'])==8
    assert entry['source_prose_or_completion_credit_added']==doc['source_prose_or_completion_credit_added']==0
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':6,'retain-wording':2}
    verify_evidence(entry)
    image,clean=NdsImage.open(current['path']),NdsImage.open('work/clean.nds')
    assert sha(Path(current['path']).read_bytes())==current['sha256']==doc['current_ROM_sha256']
    jp,old=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[182] for im in [clean,image]]
    source=read(doc['source_context']);assert len(source['records'])==8 and source['source_native_commands']==25
    assert (source['source_predicates'],source['source_relative_sites'],source['source_A000'],source['source_C200'])==(2,10,3,1)
    assert source['source_selectors']==[166,167,254] and source['source_macro_counts']=={'FI':0,'FA':0,'FO':0}
    for row in doc['records']:
        assert all(row['review'].values()) and row['actual_B22_display_fixture_observed']
        assert not row['offline_only_native_display_checked'] and row['individual_actual_source_event_activation_not_claimed']
        for block,k,h in [(jp,'source_reference','source_hex'),(old,'current_reference','current_hex')]:
            at=row[k]['offset'];raw=bytes.fromhex(row[h]);assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
            assert block[at-5:at+1]==bytes.fromhex(row['source_complete_preamble_hex'])
        english=row['english'].split('}',1)[1]
        if row['editorial_decision']=='retain-wording':assert english==row['previous_paragraph'] and row['fresh_retained_wording_justification']
        else:assert english!=row['previous_paragraph']
        assert '\n' not in row['english'] and '{LB' not in row['english']
    native=read(doc['native_font_proof']);assert native['current_original_macro_alignment_calls']==64
    assert len(native['cases'])==8 and (native['complete_progressive_planes'],native['complete_FE_logical_and_physical_planes'])==(7,1)
    assert len(native['negative_controls'])==18 and all(r['rejected'] for r in native['negative_controls'])
    approval=read('work/analysis/lil_B182_native_approval_v4892/all8_source_prose_current_native_approval.json')
    assert len(approval['formatter_negatives'])==len(set(approval['formatter_negatives']))==28
    assert len(approval['reviewed_sheets'])==1 and approval['reviewed_sheets'][0]['viewed_in_full_current_turn']
    for r in native['cases']:assert sha(Path(r['preview']).read_bytes())==r['preview_sha256']
    mapping=read(doc['reference_map']);verify_evidence(mapping);b=mapping['blocks'][0]
    assert len(b['command_map'])==25 and len(b['text_records'])==8 and len(b['relative_skip_fixups'])==10 and len(b['target_native_skip_cases'])==50
    assert b['source_bytes']==b['source_logical_end']==636 and b['research_bytes']==b['research_logical_end']==652
    assert [(r['source_offset'],r['target_offset']) for r in b['original_declared_end_word_maps']]==[(632,648)]
    assert [(r['old_offset'],r['new_offset']) for r in b['command_map'] if r['word']==0x8000]==[(512,530),(544,562)]
    target=Path(b['research_block']).read_bytes();assert sha(target)==b['target_block_sha256']
    for r in b['text_records']:
        raw=bytes.fromhex(r['target_hex']);assert target[r['new_offset']:r['new_offset']+r['new_length']]==raw
        assert raw==bytes.fromhex(next(c['encoded_hex'] for c in native['cases'] if c['id']==r['id']))+(b' ' if r['parity_space_added'] else b'')
    stored=read(doc['final_padding_proof']);assert stored['current_final_stored_macro_alignment_cases']==32
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(16,16)
    scratch=read('work/analysis/lil_B182_predicate500_v4896/all24_aligned_and_unaligned_original500_ownership_cases.json')
    assert len(scratch['cases'])==24 and scratch['actual_emulator_seed_writes']==0
    assert Counter(r['native_result'][1] for r in scratch['cases'])=={0:12,1:6,2:6}
    assert sum(r['operand_pointer_unaligned'] for r in scratch['cases'])==8
    for r in scratch['cases']:
        expected=[]
        if r['operand_pointer_unaligned']:expected.append(dict(PC=0x0202A5D8,address=0x02279600,size=4,value=500))
        expected.append(dict(PC=0x020D984C,address=0x02168EB8,size=4,value=r['after_seed']))
        assert r['all_original_native_writes']==expected
        assert r['full4MiB_difference_exactly_original_owned_RNG_and_optional_operand_scratch']
        assert r['cleanup_restores_only_owned_seed_and_optional_scratch_and_recovers_all4MiB']
    visual=read(doc['postscene_native_state_proof']);verify_evidence(visual)
    assert visual['fixture_return_frames']==[4776,4775] and visual['exact_timing_difference_counts']==dict(total=13,speech=7,control_or_end=6)
    assert visual['postscene9001_PRNG_seeds']==[3723009301,403514907] and not visual['PRNG_equality']
    assert all(visual['postscene9001_native_component_equality'].values()) and visual['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert len(visual['all_actual_consumer_sheets_viewed'])==2 and len(visual['paired_full_screen_views'])==12
    for s in visual['all_actual_consumer_sheets_viewed']+visual['paired_full_screen_views']:
        assert s['viewed'] and s['review'] and sha(Path(s['path']).read_bytes())==s['sha256']
    actual=read(visual['actual_proof']);assert len(actual['actual_panels'])==actual['complete_matching_observations']==8 and not actual['failures']
    assert not actual['paired_region_differences'] and actual['all25_source_commands_stored_and_actual_conditional_path_verified']
    for record in actual['actual_panels']:
        expected=Image.open(next(r['preview'] for r in native['cases'] if r['id']==record['id'])).convert('RGB')
        hold=record['holds'][0];photo=Image.open(hold['capture']).convert('RGB').crop((16,296,16+expected.width,360))
        for ink in [(0,8,0),(98,97,98)]:
            assert [p==ink for p in photo.getdata()]==[p==ink for p in expected.getdata()]
    assert len(visual['all115_sampled_nontext_region_checks'])==115
    differences=[]
    for row in visual['all115_sampled_nontext_region_checks']:
        images=[]
        for p in [row['source'],row['English']]:
            assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'];images.append(Image.open(p['path']).convert('RGB'))
        a,c=images;assert a.crop((0,0,256,294)).tobytes()==c.crop((0,0,256,294)).tobytes()
        if row['frame']>4776:
            bbox=ImageChops.difference(a,c).getbbox()
            if bbox is not None:assert bbox==(224,360,240,376);differences.append(row['frame'])
        if row['frame']==9001:assert a.tobytes()==c.tobytes()
    assert differences==[r['frame'] for r in visual['sampled_postscene_whole_RGB_differences_unmasked']] and len(differences)==18
    assert visual['actual_new_cold_boot_runs']==2 and visual['total_frames']==18002
    for r in visual['terminal_reports']:assert r['receipt']['terminal'] and r['receipt']['observer_host_slots_restored']

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');p.add_argument('--post',action='store_true');args=p.parse_args()
    assert not(args.apply and args.post)
    plan=read(CHECKPOINT/'mutation_plan.json');files=plan['files'];assert len(files)==6
    old_bytes=gzip.decompress((CHECKPOINT/'ledger.before.json.gz').read_bytes());old=json.loads(old_bytes)
    lp=Path('translations/editorial_review_current_v1.json');ledger_row=next(r for r in files if Path(r['target'])==lp.resolve())
    new=read(ledger_row['staged']);inverse=deepcopy(new)
    inverse['latest_checkpoint']=inverse.pop(plan['previous_key']);entry=inverse.pop(plan['ledger_key']);assert inverse==old
    assert Path(ledger_row['staged']).read_bytes()==encode_ledger(new)
    assert tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(5933,5936,3758,2175)
    assert new['current_integrated_candidate']==old['current_integrated_candidate'] and new['goal_status']=='active' and new['full_goal_complete'] is False
    known={historical_key(r) for r in new['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert len(known)==5933 and not known&{historical_key(r) for r in entry['records']}
    verify_evidence(plan);audit_scene(entry,new['current_integrated_candidate'])
    current=new['current_integrated_candidate'];manifest=read(current['manifest']);reg=read('translations/release_stack.json')
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches'])==563 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(reg['accepted_layers'])==114 and reg['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    for r in files:
        assert sha(Path(r['staged']).read_bytes())==r['after_sha256']
        assert sha(Path(r['target']).read_bytes())==r['after_sha256' if args.post else 'before_sha256']
    ROOT.mkdir(parents=True,exist_ok=True)
    receipt=dict(ledger_sha256=ledger_row['after_sha256'],candidate=current['path'],candidate_sha256=current['sha256'],
        all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,
        approved_uncredited_B182_objects=8,revised=6,retained=2,exact_clean_current_runtime_native_and_actual_references_verified=True,
        all8_actual_text_planes115_nontext_samples_and18_indicator_differences_independently_checked=True,
        all24_exact_RNG_and_optional_operand_scratch_write_cases_verified=True,
        current563_manifest_batches114_accepted18_checks_and_promoted_main_preserved=True,
        full_goal_active=True,full_goal_complete=False,registered_integration_patch_and_startup_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()))
    if args.apply:
        assert not(ROOT/'verified_handoff.json').exists()
        save(ROOT/'pre_apply_audit.json',receipt)
        for r in files:assert sha(Path(r['target']).read_bytes())==r['before_sha256']
        for r in files:
            data=Path(r['staged']).read_bytes()
            with Path(r['target']).open('r+b') as stream:stream.write(data);stream.truncate();stream.flush();os.fsync(stream.fileno())
            assert sha(Path(r['target']).read_bytes())==r['after_sha256']
        save(ROOT/'applied_handoff.json',receipt)
    elif args.post:
        assert (ROOT/'applied_handoff.json').exists();save(ROOT/'verified_handoff.json',receipt)
    else:save(ROOT/'pre_apply_audit.json',receipt)
    print(dict(applied=args.apply,post_verified=args.post,metadata_files=6,uncredited_B182=8,all_history_preserved=True,full_goal_active=True))
