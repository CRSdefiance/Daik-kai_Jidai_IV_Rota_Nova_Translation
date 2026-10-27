"""Independently bind the uncredited27-gloss B172 lead and preserved cumulative state."""
import gzip
import json
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4363')
CHECKPOINT=Path('work/analysis/lil_B172_clean_lead_v4362')

if __name__=='__main__':
    assert not ROOT.exists()
    receipt=read(CHECKPOINT/'checkpoint_receipt.json');lp=Path('translations/editorial_review_current_v1.json')
    raw=lp.read_bytes();ledger=json.loads(raw);before_bytes=gzip.decompress((CHECKPOINT/'ledger.before.json.gz').read_bytes());before=json.loads(before_bytes)
    assert sha(raw)==receipt['ledger_sha256'] and sha(before_bytes)==receipt['before_ledger_sha256']
    assert raw==encode_ledger(ledger) and len(raw)<100*1024*1024
    assert {k:v for k,v in ledger.items() if k!='lil_B172_clean_source_lead_v4362'}==before
    for key in ['updated_files','preserved_release_files']:
        for path,digest in receipt[key].items():assert sha(Path(path).read_bytes())==digest,(key,path)
    prior_path=Path(receipt['prior_verified_handoff']);prior=read(prior_path)
    assert sha(prior_path.read_bytes())==receipt['prior_verified_handoff_sha256'] and prior['ledger_sha256']==sha(before_bytes)
    record=ledger['lil_B172_clean_source_lead_v4362'];source_path=Path(record['source_context']);source=read(source_path)
    assert sha(source_path.read_bytes())==record['source_context_sha256']==receipt['source_context_sha256']
    assert sha(Path(source['source_transcript']).read_bytes())==record['source_transcript_sha256']==source['source_transcript_sha256']
    assert source['no_predecessor_English_exposed'] and source['all27_clean_source_read_and_individually_glossed_before_predecessor_English']
    assert source['source_prose_or_completion_credit_added']==source['new_emulator_runs']==0
    assert sha(Path(source['source_ROM']).read_bytes())==source['source_ROM_sha256']
    clean=NdsImage.open(source['source_ROM']);sc2=clean.read_file('/data/SC2.DK4')
    assert sha(sc2)==source['source_SC2_sha256'];block=IlnkContainer.parse(sc2).blocks[172];lead=source['block']
    assert len(block)==1884 and sha(block)==lead['clean_block_sha256']=='feb4596dcc453b242d6e13aedb93aa1908699ea00f2d23750ff230be457ca59e'
    assert len(lead['records'])==source['total_editorial_objects']==record['clean_source_objects']==27
    assert len({r['id'] for r in lead['records']})==27 and lead['source_selectors']==record['source_selectors']==[2,26,201]
    assert lead['source_macro_counts']=={'FI':0,'FA':0,'FO':0}
    assert not any(lead[key] for key in ['FE_panels','typed_menu_2100_commands','typed_actor_style_4100_commands','relative_sites'])
    commands=lead['complete_native_commands']
    assert len(commands)==38 and [c['word'] for c in commands if c['word']!=0x4000]==[0x6000,0x45FF,0x6329,0x4651,0x6340,0x4620,0x632A,0xC200,0xA000,0x6240,0]
    assert next(c['offset'] for c in commands if c['word']==0xC200)==1868
    assert next(c['offset'] for c in commands if c['word']==0xA000)==1870
    assert next(c['whole_command_hex'] for c in commands if c['word']==0xA000)==record['source_A000_hex']=='00a0ffff010cc960'
    assert [c['offset'] for c in commands if c['word']==0]==[1880]
    for c in commands:assert block[c['offset']:c['offset']+c['native_extent']].hex()==c['whole_command_hex']
    for row in lead['records']:
        at=row['source_reference']['offset'];body=bytes.fromhex(row['source_hex'])
        assert block[at:at+len(body)]==body and block[at+len(body)]==0
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex'] and body[1:].decode('cp932')==row['source_Japanese']
        assert row['fresh_source_gloss'] and row['whole_exchange_context']==source['whole_exchange_context']
        assert row['clean_source_complete_exchange_read_before_predecessor_English']
    for path,digest in source['evidence'].items():assert sha(Path(path).read_bytes())==digest,path
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5762,5762,0)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5762,5765,3659,2103)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    candidate=ledger['current_integrated_candidate'];promotion=read('translations/promoted_build.json')
    assert candidate['profile']=='all-routes-unified-v4353' and promotion['profile']=='all-routes-unified-v4303'
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==prior['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==prior['patch_sha256']
    conf=read('translations/lil_B171_editorial_release_v1.json')
    for path,digest in conf['dependencies'].items():assert sha(Path(path).read_bytes())==digest,path
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4362')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4362',ledger_sha256=sha(raw),ledger_bytes=len(raw),
        all_prior_JSON_values_B171_completions_and_wider_scope_preserved=True,complete27_clean_Japanese_speeches_glossed_before_current_English=True,
        all38_source_commands_11_leaves_C200_then_A000_and_single_end_bound=True,
        source_names_item_and_city_approved_bindings_pending=True,no_current_English_manuscript_orreview_credit_created=True,
        clean_source_lead=str(source_path),clean_source_lead_sha256=sha(source_path.read_bytes()),
        fresh_reread=5762,integrated=5762,pending=0,source_prose=5765,revised=3659,retained=2103,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        manifest_batches=547,accepted_layers=114,promoted_main_V4303_unchanged=True,new_source_prose_reviews=0,new_completed_records=0,new_emulator_runs=0,
        B172_clean_gloss_lead_objects=27,remaining_B173_B180_physical_speeches=134,remaining_choice_command_leads=0,
        all_jobs_terminal=True,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4363 audit passes:V4362,27 clean B172 glosses/unexposed English/no credit;5762 integrated/0 pending;V4353 candidate,V4303 main. Full goal active.')
