"""Exercise independent complete source/current/final bindings before any atomic commit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B54_B60_profile_v1 import contract,validate_approved_batch,validate_runtime
from dk4tool.patch.hodram_B54_B60_references_v1 import reconstruct_and_bind
from scripts.review_Hodram_B54_B60_actual_v8825 import PROOFS
from scripts.verify_village_wrap_v608 import read,save
PROOFS={**PROOFS,'relocation':'work/analysis/Hodram_B54_B60_references_v8814/source_current_final_map.json','current':'work/analysis/Hodram_B54_B60_current_v8799/current_effective.json','source_controls':'work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json'}
ROOT=Path('work/analysis/Hodram_B54_B60_reference_validation_v8836')
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v4.json')
MODULE=Path('dk4tool/patch/hodram_B54_B60_references_v1.py')
def require(value,label):
    if not value:raise ValueError('B54-B60 production references: '+label)
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);data={k:read(p) for k,p in PROOFS.items()};frozen=contract();validate_approved_batch(doc)
    parent,clean,reference=[NdsImage.open(p) for p in [doc['current_ROM'],'work/clean.nds',doc['reference_ROM']]];validate_runtime(parent)
    protected={Path(p) for p in frozen['dependencies']}|{DOC,MODULE,Path(__file__),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),Path(doc['current_ROM']),Path(doc['reference_ROM']),Path('work/clean.nds')}
    before={str(p):sha(p.read_bytes()) for p in protected};before_rom=bytes(parent.rom.save());before_object=parent.rom
    result=reconstruct_and_bind(parent,clean,reference,doc,data,require)
    assert set(result['target_blocks'])==set(range(54,61)) and result['summary']['editorial_references']==82 and result['summary']['commands']==152 and result['summary']['unowned_blocks']==318
    assert parent.rom is before_object and bytes(parent.rom.save())==before_rom
    cases=[]
    def reject(label,mutate):
        candidate=dict(doc=deepcopy(doc),data=deepcopy(data));mutate(candidate)
        assert candidate['doc']!=doc or candidate['data']!=data,label
        try:reconstruct_and_bind(parent,clean,reference,candidate['doc'],candidate['data'],require)
        except ValueError as error:
            text=str(error);assert 'Native dependency changed' not in text and 'Frozen Hodram-B54-B60 contract changed' not in text,(label,text)
            cases.append(dict(label=label,actual_changed_input=True,rejected=True,diagnostic=text))
        else:raise AssertionError('Changed reference input accepted:'+label)
        assert parent.rom is before_object and bytes(parent.rom.save())==before_rom
    for field,part in [('source_reference','offset'),('current_reference','offset'),('final_reference','offset'),('source_reference','header_offset'),('source_reference','block'),('current_reference','bytes'),('final_reference','record_index')]:
        reject(field+':'+part,lambda d,f=field,p=part:d['doc']['records'][0][f].__setitem__(p,d['doc']['records'][0][f][p]+1))
    reject('final-target-block-digest',lambda d:d['doc']['records'][0]['final_reference'].__setitem__('target_block_sha256','0'*64))
    reject('final-body-byte',lambda d:d['doc']['records'][0].__setitem__('final_hex',d['doc']['records'][0]['final_hex']+'20'))
    reject('complete-six-byte-preamble',lambda d:d['doc']['records'][0].__setitem__('source_complete_preamble_hex','0040ffff00ff'))
    reject('wrong-archive-owner',lambda d:d['data']['current'].__setitem__('file_path','/data/SC0.DK4'))
    reject('missing-source-group',lambda d:d['data']['source_controls']['groups'].pop())
    reject('missing-target-group',lambda d:d['data']['relocation']['groups'].pop())
    reject('duplicate-canonical-record',lambda d:d['doc']['records'].__setitem__(1,deepcopy(d['doc']['records'][0])))
    reject('truncated-target-end',lambda d:d['data']['relocation']['groups'][1]['all_target_commands'][-1].__setitem__('native_extent',2))
    reject('wrong-source-command-opcode',lambda d:d['data']['current']['groups'][0]['all_source_commands'][0].__setitem__('word',0x6000))
    reject('wrong-native-source-command-extent',lambda d:d['data']['source_controls']['groups'][0]['all_original_source_commands'][0].__setitem__('native_extent',4))
    nested=next(i for i,c in enumerate(data['relocation']['groups'][4]['all_target_commands']) if c['ancestor_0100_offsets'])
    reject('nested-command-owner',lambda d:d['data']['relocation']['groups'][4]['all_target_commands'][nested].__setitem__('ancestor_0100_offsets',[]))
    query=next(i for i,c in enumerate(data['relocation']['groups'][4]['all_target_commands']) if c['word']==0x8000)
    reject('raw-query-command-bytes',lambda d:d['data']['relocation']['groups'][4]['all_target_commands'][query].__setitem__('whole_command_hex','0080ffff12fe0130'))
    reject('stored-record-boundary',lambda d:d['data']['relocation']['groups'][0]['text_records'][0].__setitem__('new_record_index',d['data']['relocation']['groups'][0]['text_records'][0]['new_record_index']+1))
    for ident in ['DK4_MES_B56_R0010','DK4_MES_B57_R0007','DK4_MES_B55_R0006','DK4_MES_B59_R0023','DK4_MES_B60_R0012']:
        index=next(i for i,r in enumerate(doc['records']) if r['id']==ident)
        reject(ident+':distinct-consumer-final-offset',lambda d,i=index:d['doc']['records'][i]['final_reference'].__setitem__('offset',d['doc']['records'][i]['final_reference']['offset']+1))
    assert len(cases)==25 and len({r['label'] for r in cases})==25
    assert {str(p):sha(p.read_bytes()) for p in protected}==before and parent.rom is before_object and bytes(parent.rom.save())==before_rom
    ROOT.mkdir(parents=True);save(ROOT/'independent_reference_validation.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),reference_summary=result['summary'],
        positive_complete152command_native_inventories_and82disjoint_source_current_final_references=True,
        positive_entire_archive_whole_reference_ROM_all318_unownedblocks_files_components_andallinverses=True,
        negative_cases=cases,negative_count=25,every_negative_actual_input_changed_andsemantic_guard_rejected=True,
        original_NDS_object_identity_andwhole_bytes_unchanged_afterpositive_andallnegative_cases=True,
        all_frozen_guards_active_protected_files_ROMs_registry_ledger_andinputs_hash_exact=True,protected_hashes=before,
        production_controls_loaders_actual_comparison_readers_atomic_registered_patch_startup_andcredit_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,MODULE,Path(__file__)]}))
    print('Independent production references:all152commands/82canonical source-current-final refs/wholearchive/wholeNDS andinverses pass;25semantic defects reject withzero mutation.No ROMcommit orcredit.',flush=True)
