"""Independently verify current B176 pending coverage, relocation and retained history."""
import gzip
import struct
from collections import Counter
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4578')
CHECKPOINT=Path('work/analysis/lil_B176_relocation_checkpoint_v4577')
DOC=Path('translations/lil_B176_editorial_manuscript_v3.json')
PLAN=Path('work/analysis/lil_B176_relocation_v4575/nested_source_relocation_research.json')
STORED=Path('work/analysis/lil_B176_stored_v4576/all10_final_stored_targets40_macro_cases_and_complete_planes.json')


def main():
    output=ROOT/'independent_verified_handoff.json'
    assert not output.exists()
    receipt=read(CHECKPOINT/'checkpoint_receipt.json')
    lp=Path('translations/editorial_review_current_v1.json')
    ledger=read(lp)
    assert sha(lp.read_bytes())==receipt['ledger_sha256']
    old_bytes=gzip.decompress((CHECKPOINT/'ledger.before.json.gz').read_bytes())
    import json
    before=json.loads(old_bytes)
    allowed={'latest_checkpoint','lil_B176_reversible_relocation_v4577'}
    assert not (allowed-{'latest_checkpoint'}) & set(before)
    assert {k:v for k,v in before.items() if k not in allowed}=={k:v for k,v in ledger.items() if k not in allowed}
    assert lp.read_bytes()==encode_ledger(ledger) and lp.stat().st_size<100*1024*1024
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert tuple(ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass',
        'records_revised_and_integrated','retained_wordings_editorially_completed'])==(5865,5878,3728,2137)
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert tuple(fresh[k] for k in ['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated',
        'fresh_pass_records_pending_native_actual_release'])==(5875,5865,10)
    assert len(fresh['record_keys'])==len({historical_key(r) for r in fresh['record_keys']})==5875
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==4022
    scope=ledger['unfinished_editorial_scope_v4573']
    assert scope['canonical_Maria32_pending_uncredited'] and scope['remaining_B177_B180_physical_speeches']==48
    assert scope['incomplete_route_source_prose']==10
    assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    doc,plan,stored=map(read,[DOC,PLAN,STORED])
    validate_natural_dialogue_batch(doc)
    rows=doc['records']
    assert len(rows)==10 and Counter(r['editorial_decision'] for r in rows)=={'revise':5,'retain-wording':5}
    assert fresh['pending_record_keys']==[{'file_path':'/data/SC2.DK4','id':r['id']} for r in rows]
    assert plan['manuscript_sha256']==stored['manuscript_sha256']==sha(DOC.read_bytes())
    font=read(doc['native_font_proof'])
    assert sha(Path(doc['native_font_proof']).read_bytes())==doc['native_font_proof_sha256']
    assert len(font['cases'])==10 and font['current_original_macro_alignment_calls']==80
    assert (font['progressive_planes'],font['FE_planes'])==(9,1)
    assert len(font['review_sheets'])==2 and all(s['viewed_in_full_current_turn'] for s in font['review_sheets'])
    for sheet in font['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert sum(len(font[k]) for k in ['source_consumer_negative_controls','source_bound_formatter_negatives','source_macro_preservation_negatives'])==49
    assert (stored['current_final_stored_macro_alignment_cases'],stored['new_parity_macro_alignment_cases'],
            stored['exact_byte_identical_reused_macro_alignment_cases'])==(40,16,24)
    assert stored['relocation_plan_sha256']==sha(PLAN.read_bytes())
    image=NdsImage.open(doc['current_ROM'])
    current=IlnkContainer.parse(image.read_file('/data/SC2.DK4'))
    clean=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4'))
    b=plan['blocks'][0]
    assert len(plan['blocks'])==1 and b['block']==176
    source=current.blocks[176]
    target=Path(b['research_block']).read_bytes()
    assert (len(source),len(target),b['source_logical_end'],b['research_logical_end'])==(392,404,390,404)
    assert sha(source)==b['source_block_sha256'] and sha(target)==b['research_block_sha256']
    assert len(b['command_map'])==13 and len(b['text_records'])==10
    assert not b['relative_skip_fixups'] and not b['target_native_skip_cases']
    assert [(m['word'],m['old_offset'],m['new_offset']) for m in b['command_map'] if m['word']!=0x4000]==[(0xA000,8,8),(0xC200,384,398),(0,386,400)]
    assert source[8:16]==target[8:16]==bytes.fromhex('00a0ffff010a0da1')
    assert source[384:390]==target[398:404]==bytes.fromhex('00c200000000')
    lookup={r['id']:r for r in rows}
    for moved,case in zip(b['text_records'],stored['final_target_parity_cases'],strict=True):
        r=lookup[moved['id']]
        assert r['id']==case['id'] and all(r['review'].values())
        for block,ref,value in [(clean.blocks[176],r['source_reference'],r['source_hex']),
                                (source,r['current_reference'],r['current_hex'])]:
            at=ref['offset'];raw=bytes.fromhex(value)
            assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
            assert block[at-5:at+1].hex()==r['source_complete_preamble_hex']
        value=bytes.fromhex(moved['target_hex']);at=moved['new_offset']
        assert target[at:at+len(value)]==value and target[at+len(value)]==0
        assert target[:at].count(b'\0')==moved['new_record_index']
        assert case['complete_final_target_native_plane_equals_reviewed_plane'] and case['tail_padding_consumed_without_blank_page_or_lost_glyph']
        if r['editorial_decision']=='retain-wording':
            assert r['english'].split('}',1)[1]==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification']
    restored=bytearray(target)
    struct.pack_into('<H',restored,4,382)
    for moved in reversed(b['text_records']):
        restored[moved['new_offset']:moved['new_offset']+moved['new_length']]=source[moved['old_offset']:moved['old_offset']+moved['old_length']]
    assert bytes(restored)==source[:390]
    prospective=IlnkContainer.parse(Path(plan['target_SC2']).read_bytes())
    assert len(prospective.blocks)==len(current.blocks)==336
    assert [i for i,(a,z) in enumerate(zip(current.blocks,prospective.blocks,strict=True)) if a!=z]==[176]
    assert prospective.blocks[176]==target
    for path,digest in {**receipt['evidence'],**receipt['preserved_release_files']}.items():
        assert sha(Path(path).read_bytes())==digest,path
    main=read('translations/promoted_build.json')
    assert main['profile']=='all-routes-unified-v4541' and main['main_build']
    assert main['rom_sha256']==sha(Path(main['rom']).read_bytes())==doc['current_ROM_sha256']
    for row in read(CHECKPOINT/'mutation_plan.json'):
        assert Path(row['target']).read_bytes()==Path(row['planned']).read_bytes()
    result={**receipt,'independent_audit':True,'all10_source_current_stored_references_and5_retentions_verified':True,
        'all49_negatives80_logical_compiled_and40_stored_cases_bound':True,
        'source_A000_C200_single_end_byte_exact_and_uninterpreted':True,
        'pending_draft_credit_added_once_and_historical_completions_unchanged':True,
        'original_checkpoint_producer':receipt['evidence'],
        'independent_producer_sha256':sha(Path(__file__).read_bytes())}
    save(output,result)
    print('V4577 independently verified:5875 reread/5865 completed/10 pending;all source/current/stored references,40 stored cases,inverse and full history exact. Main V4541 preserved.')


if __name__=='__main__':
    main()
