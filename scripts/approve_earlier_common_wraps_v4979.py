"""Approve viewed source/context/native findings and construct one exact COMMON reflow."""
from copy import deepcopy
from pathlib import Path
from functools import cache
from dk4tool.dialogue.earlier_market_letters_reflow_v2 import compile_letter,PARAGRAPH
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/earlier_common_wraps_approval_v4979')
INPUT=Path('work/analysis/earlier_common_wraps_review_v4978/whole_context_four_retentions_two_reflows_and8_native_planes.json')
DOC=Path('translations/earlier_common_wraps_editorial_manuscript_v1.json')

def partitions(text,rows):
    words=text.split(' ')
    @cache
    def solve(start,row):
        if row==rows:return [()] if start==len(words) else []
        results=[]
        for stop in range(start+1,len(words)+1):
            line=' '.join(words[start:stop]);limit=35 if row==rows-1 else 34
            if len(line)>limit:break
            results.extend((line,*tail) for tail in solve(stop,row+1))
        return results
    return solve(0,0)

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();d=read(INPUT)
    assert d['visual_review_pending'] and d['retained_exact_layout_IDs']==[682,764,774] and d['proposed_reflow_IDs']==[775]
    assert len(d['records'])==4 and not d['changed_prose_IDs'] and d['actual_new_emulator_runs']==0
    for p,h in d['dependencies'].items():assert sha(Path(p).read_bytes())==h
    assert sha(Path(d['review_sheet']).read_bytes())==d['review_sheet_sha256']
    for r in d['records']:
        assert len(r['native_cases'])==2 and r['source_meaning'] and r['fresh_retained_wording_justification'] and r['layout_review_reason']
        for c in r['native_cases']:assert sha(Path(c['preview']).read_bytes())==c['preview_sha256'] and c['full_independent_228x64_plane_equal']
    intro=next(r for r in d['records'] if r['message_id']==774)['english'].removesuffix('{PAD}')
    intro_plans={str(n):partitions(intro,n) for n in [1,2,3]};assert not any(intro_plans.values())
    assert partitions(intro,4) and len("Oh, I know! I'll write you a letter")==35
    proposed,allocation=compile_letter(775,PARAGRAPH,105)
    assert allocation['lines']==["And I'll write you a letter",'of recommendation to thank you for','selling us so many popular goods.']
    assert allocation['generated_terminal_spaces']==2 and allocation['generated_even_pre_LF_allocation_spaces']==[0,0]
    assert len(partitions(PARAGRAPH,2))==0 and partitions(PARAGRAPH,3)
    negatives=[]
    inputs=[(n,PARAGRAPH,105) for n in [682,764,774,776]]
    inputs.extend((775,t,105) for t in [PARAGRAPH+'{LB}',PARAGRAPH+'{PAD}{PAD}',PARAGRAPH+' ',PARAGRAPH.replace('recommendation','introduction'),PARAGRAPH.replace('so many','those'),PARAGRAPH.replace('popular','scarce')])
    inputs.extend((775,PARAGRAPH,n) for n in [0,104,106,512])
    for index,args in enumerate(inputs):
        try:compile_letter(*args)
        except ValueError as e:negatives.append(dict(case=index,arguments=args,rejected=True,reason=str(e)))
        else:raise AssertionError('Unsafe or unowned layout accepted')
    assert len(negatives)==14
    image=NdsImage.open(d['current_ROM']);arm,common=image.read_file('/__arm9__.bin'),image.read_file('/COMMON/MESFILE.DK4')
    assert sha(common)==d['current_COMMON_sha256'] and sha(arm)==d['current_ARM9_sha256']
    before=owned_entries(common,arm,d['directory_sha256']);old=before[775]
    selected=next(r for r in d['records'] if r['message_id']==775);assert selected['target_hex']==proposed.hex() and selected['current_hex']==old.text.hex()
    container=IlnkContainer.parse(common);blocks=list(container.blocks);body=bytearray(blocks[old.block])
    assert body[old.block_offset:old.block_offset+106]==old.text+b'\0'
    body[old.block_offset:old.block_offset+105]=proposed;blocks[old.block]=bytes(body);target=IlnkContainer(blocks).to_bytes()
    after=owned_entries(target,arm,d['directory_sha256']);assert len(target)==len(common)
    for a,b in zip(before,after,strict=True):
        assert (a.message_id,a.block,a.block_offset,a.copy_end,a.record_index,a.start,a.end)==(b.message_id,b.block,b.block_offset,b.copy_end,b.record_index,b.start,b.end)
        assert b.text==(proposed if a.message_id==775 else a.text)
    assert [i for i,(a,b) in enumerate(zip(container.blocks,blocks,strict=True)) if a!=b]==[10]
    inverse=bytearray(blocks[10]);inverse[old.block_offset:old.block_offset+105]=old.text
    restored=list(blocks);restored[10]=bytes(inverse);assert IlnkContainer(restored).to_bytes()==common
    rows=deepcopy(d['records'])
    for r in rows:
        r.update(speaker=r['historical_record']['speaker'],context=r['historical_record']['context']+' Reopened whole-context formatting review;the clean/current conditional graph is preserved.',
            localization_note=r['fresh_retained_wording_justification']+' '+r['layout_review_reason'],review=dict(source=True,context=True,localization=True,naturalness=True,formatting=True),
            status='source-context-wording-native-approved;representative-and-registered-integration-pending',
            native_display_scope='Viewed complete current/reviewed228x64 planes from the current ARM9,1px font offset,existing original expansion/wrapper and row pitch16. No actual emulator coverage added.')
    doc=dict(format='dk4-earlier-common-wrap-editorial-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-fixed-v1',
        review_gates=['source','context','localization','naturalness','formatting'],records=rows,current_ROM=d['current_ROM'],current_ROM_sha256=d['current_ROM_sha256'],
        source_context_proof=str(INPUT),source_context_proof_sha256=sha(INPUT.read_bytes()),retained_wordings=4,retained_exact_layout_IDs=[682,764,774],reflow_IDs=[775],
        source_prose_or_completion_credit_added=0,formatting_reopened_without_duplicate_credit=True,actual_new_emulator_runs=0,registered_integration_pending=True,full_goal_complete=False)
    validate_natural_dialogue_batch(doc);ROOT.mkdir(parents=True);save(DOC,doc)
    tp=ROOT/'target_COMMON_RESEARCH_ONLY.bin';tp.write_bytes(target)
    save(ROOT/'four_retentions_one_reflow_source_native_approval.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        input_proof=str(INPUT),input_proof_sha256=sha(INPUT.read_bytes()),viewed_sheet=d['review_sheet'],viewed_sheet_sha256=d['review_sheet_sha256'],all8_current_and_reviewed_complete_native_planes_viewed=True,
        only_changed_message_IDs=[775],retained_exact_layout_IDs=[682,764,774],all_four_wordings_retained_with_individual_reasons=True,
        intro774_exhaustive_complete_word_partitions_at1_2_3_rows=intro_plans,intro774_four_rows_possible=True,
        initial774_three_row_assumption_disproved=True,diagnostic_proofs_and_executed_producers_preserved=True,
        target_COMMON=str(tp),target_COMMON_sha256=sha(target),source_COMMON_sha256=sha(common),source_ARM9_sha256=sha(arm),directory_sha256=d['directory_sha256'],
        all3668_message_boundaries_NULs_and_unselected_payloads_exact=True,all_other_blocks_exact=True,inverse_restores_every_current_COMMON_byte=True,
        compiler_module='dk4tool/dialogue/earlier_market_letters_reflow_v2.py',compiler_module_sha256=sha(Path('dk4tool/dialogue/earlier_market_letters_reflow_v2.py').read_bytes()),
        negative_controls=negatives,all14_unsafe_or_unowned_inputs_rejected=True,viewed_in_full=True,
        source_prose_or_completion_credit_added=0,new_emulator_runs=0,new_ROMs=0,registered_integration_pending=True,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [INPUT,DOC,tp,Path(__file__),'dk4tool/dialogue/earlier_market_letters_reflow_v2.py']},full_goal_complete=False))
    print(dict(reviewed_wording_retentions=4,exact_layout_retentions=[682,764,774],native_approved_reflow=[775],negative_controls=14,
        all3668_boundaries_exact=True,ROMs_created=0,new_editorial_credit=0))
