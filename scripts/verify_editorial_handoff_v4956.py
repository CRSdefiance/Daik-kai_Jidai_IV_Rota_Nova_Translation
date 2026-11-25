"""Audit B183 source/native/reference facts and lossless six-file checkpoint application."""
from copy import deepcopy
from pathlib import Path
from collections import Counter
import argparse,gzip,json,os,struct
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue import lil_B183_layout_v3 as codec
from dk4tool.dialogue.lil_B183_profile import profile_for
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

CHECKPOINT=Path('work/analysis/lil_B183_checkpoint_v4955')
ROOT=Path('work/analysis/editorial_handoff_verification_v4956')

def audit(entry,current):
    doc=read(entry['manuscript']);assert sha(Path(entry['manuscript']).read_bytes())==entry['manuscript_sha256']
    assert entry['records']==doc['records'] and len(doc['records'])==entry['approved_uncredited_objects']==25
    assert entry['source_prose_or_completion_credit_added']==doc['source_prose_or_completion_credit_added']==0
    assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':16,'retain-wording':9}
    for p,h in entry['evidence'].items():assert sha(Path(p).read_bytes())==h
    image,clean=NdsImage.open(current['path']),NdsImage.open('work/clean.nds')
    assert sha(Path(current['path']).read_bytes())==current['sha256']==doc['current_ROM_sha256']
    arm=image.read_file('/__arm9__.bin');assert sha(arm)==doc['required_runtime_ARM9_sha256']
    blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    japanese=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[183];old=blocks[183]
    source=read(doc['source_context']);assert (source['source_native_commands'],source['speech_objects'],source['ordinary_source_speeches'],source['system_FE_panels'])==(28,25,23,2)
    assert source['source_static_actor_selectors']==[85,110,132,148,153] and source['source_macro_counts']=={'FI':0,'FA':0,'FO':0}
    assert (source['source_predicates'],source['source_relative_sites'],source['source_A000'],source['source_C200'])==(0,0,1,1)
    font=read(doc['native_font_proof']);cases={r['id']:r for r in font['cases']}
    assert len(cases)==25 and font['current_original_macro_alignment_calls']==200
    assert (font['complete_progressive_planes'],font['complete_FE_logical_and_physical_planes'])==(23,2)
    assert len(font['negative_controls'])==24 and all(r['rejected'] for r in font['negative_controls'])
    assert Counter(r['kind'] for r in doc['records'])=={'progressive':23,'system-FE':2}
    for row in doc['records']:
        assert all(row['review'].values()) and row['source_meaning'] and row['localization_note']
        for data,k,h in [(japanese,'source_reference','source_hex'),(old,'current_reference','current_hex')]:
            at=row[k]['offset'];raw=bytes.fromhex(row[h]);assert data[at:at+len(raw)]==raw and data[at+len(raw)]==0
            assert data[at-5:at+1].hex()==row['source_complete_preamble_hex']
        if row['editorial_decision']=='retain-wording':assert row['english'].split('}',1)[1]==row['previous_paragraph'] and row['fresh_retained_wording_justification']
        profile=profile_for(arm,old,'FE-paper' if row['kind']=='system-FE' else 'progressive')
        encoded=codec.encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile)
        c=cases[row['id']];assert encoded.encoded.hex()==row['compiled_hex']==c['encoded_hex']
        qa=codec.audit_relocatable_dialogue_record(bytes.fromhex(row['source_hex']),row['english'],profile)
        assert not [r for r in qa['issues'] if r['severity'] in ['error','warning'] and not
            (r['severity']=='warning' and r['code']=='line-break-count' and row.get('qa_waivers')==['line-break-count'] and row.get('qa_waiver_reason'))]
        assert c['all_first_final_internal_glyphs_in_order_and_unique_cells'] and c['all_visible_origins_zero_and_within_four_rows'] and c['one_native_page_consumes_complete_target']
        assert sum(len(p['cases']) for p in c['current_native_macro_pipelines'])==8
        for pipe in c['current_native_macro_pipelines']:
            if row['kind']=='system-FE':assert all(r['null_source_actor'] for r in pipe['cases'])
        assert sha(Path(c['preview']).read_bytes())==c['preview_sha256']
        assert Image.open(c['preview']).size==((228,64) if row['kind']=='system-FE' else (216,64))
    approval=read('work/analysis/lil_B183_native_approval_v4946/all25_source_prose_current_native_approval.json')
    assert approval['manuscript_sha256']==entry['manuscript_sha256']
    assert len(approval['formatter_negatives'])==len(set(approval['formatter_negatives']))==28
    assert len(approval['reviewed_sheets'])==4 and all(r['viewed_in_full_current_turn'] for r in approval['reviewed_sheets'])
    for s in approval['reviewed_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    wrap=read(doc['source_bound_wrap_refinement_proof']);assert sha(Path(doc['source_bound_wrap_refinement_proof']).read_bytes())==doc['source_bound_wrap_refinement_proof_sha256']
    assert wrap['only_changed_record_IDs']==['DK4_MES_B183_R0035'] and wrap['all25_words_controls_and_prose_unchanged']
    assert wrap['all24_other_compiled_targets_and_native_planes_exact']
    for p,h in wrap['evidence'].items():assert sha(Path(p).read_bytes())==h
    r=cases['DK4_MES_B183_R0035'];assert [s.strip() for s in bytes.fromhex(r['encoded_hex'])[1:].decode('ascii').splitlines()]==[
        'What are you two talking about?','That one over there','is obviously better!']
    names=read(doc['source_nameplate_consumer_proof']);assert names['progressive_nameplate_values']=={
        '85':'Square Shopkeeper','110':'Shipwright','132':'Priest','148':'Guildmaster','153':'Sailor'}
    assert names['full_catalogue_values']=={**names['progressive_nameplate_values'],'153':'Retainer'}
    assert len(names['native_ten_consumer_cases']['rows'])==10 and all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['all_actor_models_and_unowned4MiB_exact'] for r in names['native_ten_consumer_cases']['rows'])
    voice=read(doc['actor_voice_contract']);assert {r['actor_ID']:r['original_voice_class'] for r in voice['fresh5_actor_names']['rows']}=={85:0,110:0,132:0,148:0,153:4}
    terms=read(doc['actor_terminology_reconciliation']);assert terms['commodity_index']==57 and terms['commodity']=='Artwork' and terms['city']=='Basra'
    assert [r['text'] for r in terms['two_source_current_city_aliases']]==['Basra','Basra'] and terms['commodity_binding']['text']=='Artwork'
    plan=read('work/analysis/lil_B183_relocation_v4947/nested_source_relocation_research.json');b=plan['blocks'][0]
    assert b['block']==183 and (b['source_bytes'],b['source_logical_end'],b['research_bytes'],b['research_logical_end'])==(956,956,1056,1054)
    target=Path(b['research_block']).read_bytes();assert sha(target)==b['research_block_sha256']
    assert target[1050:1054]==bytes(4) and target[1054:]==bytes(2) and 8+struct.unpack_from('<H',target,4)[0]==1054
    assert len(b['command_map'])==28 and len(b['text_records'])==25 and not b['relative_skip_fixups'] and not b['target_native_skip_cases']
    assert [(c['word'],c['old_offset'],c['new_offset']) for c in b['command_map'] if c['word']!=0x4000]==[(0xA000,8,8),(0xC200,950,1048),(0,952,1050)]
    restored=bytearray(target[:1054]);struct.pack_into('<H',restored,4,948)
    for r in sorted(b['text_records'],key=lambda r:r['new_offset'],reverse=True):
        at=r['new_offset'];value=bytes.fromhex(r['target_hex']);assert target[at:at+len(value)]==value
        c=cases[r['id']];assert value==bytes.fromhex(c['encoded_hex'])+(b' ' if r['parity_space_added'] else b'')
        restored[at:at+len(value)]=old[r['old_offset']:r['old_offset']+r['old_length']]
    assert bytes(restored)==old
    stored=read('work/analysis/lil_B183_stored_v4948/all25_final_stored_targets100_macro_cases_and_complete_planes.json')
    assert len(stored['final_target_parity_cases'])==25 and stored['current_final_stored_macro_alignment_cases']==100
    assert (stored['new_parity_macro_alignment_cases'],stored['exact_byte_identical_reused_macro_alignment_cases'])==(64,36)
    assert all(r['complete_final_target_native_plane_equals_reviewed_plane'] and r['tail_padding_consumed_without_blank_page_or_lost_glyph'] for r in stored['final_target_parity_cases'])
    research=read('work/analysis/lil_B183_research_v4950/research_image_receipt.json');rp=Path(research['research_ROM']);reference=NdsImage.open(rp)
    assert sha(rp.read_bytes())==research['research_ROM_sha256'] and research['parent_sha256']==current['sha256']
    after=IlnkContainer.parse(reference.read_file('/data/SC2.DK4')).blocks
    assert len(after)==336 and [i for i,(a,c) in enumerate(zip(blocks,after,strict=True)) if a!=c]==[183] and after[183]==target
    assert [p for _,p,v in image.iter_files() if reference.read_file(p)!=v]==['/data/SC2.DK4']
    assert all(reference.read_file(p)==v for p,v in image.iter_components())
    pins=read('translations/rom_retention_pins.json');assert any(Path(r['path']).resolve()==rp.resolve() for r in pins)
    loader=read('work/analysis/lil_B183_loader_v4951/whole_SC2_and_B183_initial_entry_proof.json')
    assert loader['fresh_research_whole_SC2_loads']==336 and loader['fresh_parent_modes']==672
    assert loader['exact_parent_reused_whole_SC2_loads']==336 and loader['exact_parent_reused_modes']==672
    for row in loader['versions']:
        assert row['ROM_sha256']==(current['sha256'] if row['label']=='current' else research['research_ROM_sha256'])
        for k in ['load','parent']:assert sha(Path(row[k+'_proof']).read_bytes())==row[k+'_sha256']
    census=read('work/analysis/lil_B183_reference_census_v4952/all28_commands_no_relative_sites_and_shipped_entry_census.json')
    assert len(census['native_call_census'])==3 and len(census['blocks'][0]['mapped_commands'])==28
    ends=read('work/analysis/lil_B183_ends_v4953/two_declared_tail_end_decodes_no_relative_sites.json')
    assert ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and [(r['version'],r['end_offset']) for r in ends['cases']]==[('current',952),('research',1050)]
    control=read('work/analysis/lil_B183_relocated_controls_v4954/all25_progressive_FE_dispatches_A000_C200_pairs_and3_leaves.json')
    assert len(control['relocated_dispatch_cases'])==25 and sum(r['resolved_actor_ID'] is None for r in control['relocated_dispatch_cases'])==2
    assert len(control['all3_source_current_target_nonrelative_nonspeech_leaves'])==3 and len(control['relocated_C200_pairs'])==len(control['relocated_A000_structural_pairs'])==1
    assert entry['new_emulator_runs']==0 and entry['new_research_ROMs']==1 and entry['actual_sealing_compiler_registered_patch_and_startup_pending']

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');p.add_argument('--post',action='store_true');args=p.parse_args();assert not(args.apply and args.post)
    plan=read(CHECKPOINT/'mutation_plan.json');files=plan['files'];assert len(files)==6
    old_bytes=gzip.decompress((CHECKPOINT/'ledger.before.json.gz').read_bytes());old=json.loads(old_bytes)
    lp=Path('translations/editorial_review_current_v1.json');row=next(r for r in files if Path(r['target'])==lp.resolve());new=read(row['staged'])
    inverse=deepcopy(new);inverse['latest_checkpoint']=inverse.pop(plan['previous_key']);entry=inverse.pop(plan['ledger_key']);assert inverse==old
    assert Path(row['staged']).read_bytes()==encode_ledger(new) and Path(row['staged']).stat().st_size<100*1024*1024
    assert tuple(new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(5941,5944,3764,2177)
    assert new['current_integrated_candidate']==old['current_integrated_candidate'] and new['goal_status']=='active' and new['full_goal_complete'] is False
    known={historical_key(r) for r in new['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert len(known)==5941 and not known&{historical_key(r) for r in entry['records']}
    for path,h in plan['evidence'].items():assert sha(Path(path).read_bytes())==h
    audit(entry,new['current_integrated_candidate'])
    current=new['current_integrated_candidate'];manifest=read(current['manifest']);registry=read('translations/release_stack.json')
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches'])==564 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    for r in files:
        assert sha(Path(r['staged']).read_bytes())==r['after_sha256'] and sha(Path(r['target']).read_bytes())==r['after_sha256' if args.post else 'before_sha256']
    ROOT.mkdir(parents=True,exist_ok=True)
    receipt=dict(ledger_sha256=row['after_sha256'],candidate=current['path'],candidate_sha256=current['sha256'],
        all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,approved_uncredited_B183_objects=25,revised=16,retained=9,
        all_exact_source_current_runtime_native_relocation_and_offline_reference_bindings_verified=True,
        early_wrap_corrected_without_word_width_guard_or_other24_plane_changes=True,
        both_FE_consumers_Sailor_catalogue_distinction_and_voice4_preserved=True,
        all564_manifest_batches114_accepted18_checks_and_promoted_main_preserved=True,
        actual_sealing_registered_integration_patch_and_startup_pending=True,full_goal_active=True,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes()))
    if args.apply:
        assert not(ROOT/'verified_handoff.json').exists();save(ROOT/'pre_apply_audit.json',receipt)
        for r in files:assert sha(Path(r['target']).read_bytes())==r['before_sha256']
        for r in files:
            data=Path(r['staged']).read_bytes()
            with Path(r['target']).open('r+b') as stream:stream.write(data);stream.truncate();stream.flush();os.fsync(stream.fileno())
            assert sha(Path(r['target']).read_bytes())==r['after_sha256']
        save(ROOT/'applied_handoff.json',receipt)
    elif args.post:
        assert (ROOT/'applied_handoff.json').exists();save(ROOT/'verified_handoff.json',receipt)
    else:save(ROOT/'pre_apply_audit.json',receipt)
    print(dict(applied=args.apply,post_verified=args.post,files=6,uncredited_B183=25,all_history_preserved=True,full_goal_active=True))
