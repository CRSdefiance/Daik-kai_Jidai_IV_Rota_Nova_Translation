"""Validate production reconstruction against the independent blocks/ROM and real defects."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B31_B53_profile_v1 import contract,validate_approved_batch,validate_runtime
from dk4tool.patch.hodram_B31_B53_reconstruction_v1 import reconstruct
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_reconstruction_validation_v8752')
DOC=Path('translations/hodram_B31_B53_editorial_manuscript_v5.json')
MAP=Path('work/analysis/Hodram_B31_B53_references_v8738/source_current_final_map.json')
CURRENT=Path('work/analysis/Hodram_B31_B53_current_v8722/current_effective.json')
CONTROL=Path('work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json')
INDEPENDENT=Path('work/analysis/Hodram_B31_B53_independent_v8734/independent_reconstruction.json')
REFERENCE=Path('work/analysis/Hodram_B31_B53_reference_v8736/research_image_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,mapping,packet,controls,independent,reference=map(read,[DOC,MAP,CURRENT,CONTROL,INDEPENDENT,REFERENCE]);frozen=contract();validate_approved_batch(doc)
    image=NdsImage.open(doc['current_ROM']);validate_runtime(image);archive=image.read_file('/data/SC1.DK4');bank=IlnkContainer.parse(archive).blocks
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==reference['parent_sha256']
    protected={Path(p) for p in frozen['dependencies']}|{DOC,MAP,CURRENT,CONTROL,INDEPENDENT,REFERENCE,Path(__file__),Path('dk4tool/patch/hodram_B31_B53_reconstruction_v1.py'),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),Path(doc['current_ROM']),Path(reference['research_ROM']),Path('work/clean.nds')}
    before={str(p):sha(p.read_bytes()) for p in protected};positives=[];cases=[];blocks=list(bank)
    for group in mapping['groups']:
        number=group['block'];p=next(g for g in packet['groups'] if g['block']==number);c=next(g for g in controls['groups'] if g['block']==number)
        original=dict(old=bank[number],clean=bytes.fromhex(p['clean_block_hex']),group=group,packet=p,rows=[r for r in doc['records'] if r['block']==number],edges=c['operands_requiring_adjustment_when_resizing'])
        target=reconstruct(**original);expected=Path(group['target_block']).read_bytes()
        assert target==expected and sha(target)==group['target_block_sha256']==next(g for g in independent['groups'] if g['block']==number)['target_block_sha256']
        blocks[number]=target;positives.append(dict(block=number,target_block_sha256=sha(target),target_bytes=len(target),target_tail_bytes=group['target_tail_bytes'],entire_independently_reconstructed_block_byte_exact=True))
        def reject(label,mutate):
            changed=deepcopy(original);mutate(changed);assert changed!=original,label
            try:reconstruct(**changed)
            except ValueError as error:cases.append(dict(block=number,label=label,actual_changed_input=True,rejected=True,diagnostic=str(error)))
            else:raise AssertionError(f'Changed B{number} reconstruction input accepted:'+label)
        reject('wrong-file-owner',lambda d:d['group'].__setitem__('file_path','/data/SC0.DK4'))
        reject('wrong-block-owner',lambda d:d['group'].__setitem__('block',53 if number==31 else 31))
        reject('wrong-current-block',lambda d:d.__setitem__('old',bytes([d['old'][0]^1])+d['old'][1:]))
        reject('wrong-clean-block',lambda d:d.__setitem__('clean',bytes([d['clean'][0]^1])+d['clean'][1:]))
        reject('record-missing',lambda d:d['rows'].pop())
        reject('record-duplicate',lambda d:d['rows'].append(deepcopy(d['rows'][0])))
        reject('unapproved-menu',lambda d:d['group']['choice_commands'].append(dict(word=0x2100)))
        reject('speaker-preamble',lambda d:d['rows'][0].__setitem__('source_complete_preamble_hex','0040ffff00ff'))
        reject('current-body-reference',lambda d:d['rows'][0]['current_reference'].__setitem__('offset',d['rows'][0]['current_reference']['offset']+2))
        reject('source-body-reference',lambda d:d['rows'][0]['source_reference'].__setitem__('offset',d['rows'][0]['source_reference']['offset']+2))
        reject('final-body-reference',lambda d:d['rows'][0]['final_reference'].__setitem__('offset',d['rows'][0]['final_reference']['offset']+2))
        reject('final-reference-recordindex',lambda d:d['rows'][0]['final_reference'].__setitem__('record_index',d['rows'][0]['final_reference']['record_index']+1))
        reject('compiled-missing-final-glyph',lambda d:d['rows'][0].__setitem__('compiled_hex',d['rows'][0]['compiled_hex'][:-2]))
        reject('parity-space',lambda d:d['group']['text_records'][0].__setitem__('parity_space_added',not d['group']['text_records'][0]['parity_space_added']))
        reject('wrong-target-header',lambda d:d['group'].__setitem__('target_header_hex','4353000100000000'))
        reject('wrong-tail',lambda d:d['group'].__setitem__('target_tail_bytes',d['group']['target_tail_bytes']+2))
        reject('truncated-full-end',lambda d:d['group']['all_target_commands'][-1].__setitem__('native_extent',2))
        reject('changed-full-end-word',lambda d:d['group']['all_target_commands'][-1].__setitem__('whole_command_hex','00000080'))
        reject('wrong-original-end-location',lambda d:d['packet']['all_current_commands'][-1].__setitem__('offset',d['packet']['all_current_commands'][-1]['offset']+2))
        reject('target-command-missing',lambda d:d['group']['all_target_commands'].pop(0))
        opaque=next(i for i,v in enumerate(group['all_target_commands']) if v['word'] not in [0,0x4000,0x100,0x200,0x300,0x400,0x8000])
        reject('opaque-complete-command-byte',lambda d:d['group']['all_target_commands'][opaque].__setitem__('whole_command_hex','ffff'))
        if number==31:
            reject('missing-relative-site',lambda d:d['edges'].pop())
            reject('missing-relative-fixup',lambda d:d['group']['relative_fixups'].pop())
            reject('relative-target-endpoint',lambda d:d['group']['relative_fixups'][0].__setitem__('new_matched_skip_target',d['group']['relative_fixups'][0]['new_matched_skip_target']+2))
            reject('relative-source-span',lambda d:d['edges'][0].__setitem__('source_span',d['edges'][0]['source_span']+2))
            reject('relative-target-span',lambda d:d['group']['relative_fixups'][0].__setitem__('target_span',d['group']['relative_fixups'][0]['target_span']+2))
            nested=next(i for i,v in enumerate(group['all_target_commands']) if v['ancestor_0100_offsets'])
            reject('nested-source-scope',lambda d:d['group']['command_map'][nested].__setitem__('source_0100_ancestors',[]))
            reject('nested-target-scope',lambda d:d['group']['all_target_commands'][nested].__setitem__('ancestor_0100_offsets',[]))
            query=next(i for i,v in enumerate(group['all_target_commands']) if v['word']==0x8000)
            reject('raw-query-body',lambda d:d['group']['all_target_commands'][query].__setitem__('whole_command_hex','0080ffff12fe0130'))
        else:
            reject('invented-relative-site',lambda d:d['edges'].append(dict(block=53,offset=8)))
        print('RECONSTRUCTION_PASS',number,'negativecases',len(cases),flush=True)
    rebuilt=IlnkContainer(blocks).to_bytes();assert rebuilt==Path(mapping['target_archive']).read_bytes() and sha(rebuilt)==mapping['target_archive_sha256']==independent['target_archive_sha256']
    restored=IlnkContainer.parse(rebuilt);assert [i for i,(a,b) in enumerate(zip(bank,restored.blocks,strict=True)) if a!=b]==[31,53]
    for i in [31,53]:restored.blocks[i]=bank[i]
    assert restored.to_bytes()==archive
    planned=deepcopy(image);planned.replace_file('/data/SC1.DK4',rebuilt);assert sha(bytes(planned.rom.save()))==reference['research_ROM_sha256']==independent['independently_reconstructed_complete_target_ROM_sha256']
    assert [p for _,p,v in image.iter_files() if planned.read_file(p)!=v]==['/data/SC1.DK4'] and all(planned.read_file(p)==v for p,v in image.iter_components())
    planned.replace_file('/data/SC1.DK4',archive);assert bytes(planned.rom.save())==bytes(image.rom.save())
    assert len(positives)==2 and len(cases)==51 and len({(c['block'],c['label']) for c in cases})==51
    assert {str(p):sha(p.read_bytes()) for p in protected}==before
    ROOT.mkdir(parents=True);save(ROOT/'independent_reconstruction_validation.json',dict(positive_blocks=positives,positive_complete_archive_andwhole_NDS=True,
        target_archive_sha256=sha(rebuilt),whole_target_ROM_sha256=reference['research_ROM_sha256'],negative_cases=cases,negative_count=len(cases),
        every_negative_actual_input_changed_andguard_rejected=True,complete18commands3preambles4relatives_query8opaquecontrols_fullends_separate_tail_andallinverses_preserved=True,
        all_frozen_guards_enabled_no_protected_file_orROM_mutation=True,protected_hashes=before,
        production_native_actual_reference_control_loader_evidence_atomic_andregistered_stage_pending=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,MAP,CURRENT,CONTROL,INDEPENDENT,REFERENCE,Path('dk4tool/patch/hodram_B31_B53_reconstruction_v1.py'),Path(__file__)]}))
    print('Production reconstruction:2blocks/wholearchive/wholeNDS equalindependent reviewedreference;51changed semantic defects reject withfrozen guardsactive. No ROMcommit orcredit.',flush=True)
