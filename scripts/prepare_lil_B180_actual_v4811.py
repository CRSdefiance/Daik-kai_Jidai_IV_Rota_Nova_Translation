"""Prepare a conditional-path actual audit; never assert all alternatives execute."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B180_actual_tools_v4811')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/audit_lil_B179_actual_v4742.py').read_text(encoding='utf-8')
    start=source.index('        expected=[c[\'offset\']');end=source.index('        following_pending=[]',start)
    block='''        assert len(fixture['all37_stored_fixture_commands'])==37
        stored={c['offset']:c for c in fixture['all37_stored_fixture_commands']}
        cursor,last=8,0;expected=[];predicates=[];effect_offsets=[]
        for pair in selected:
            assert pair['offset']==cursor and cursor not in expected
            expected.append(cursor);command=stored[cursor];word=command['word']
            assert pair['word']==word
            if word==0:
                assert pair['result_words']==[0,0];break
            if word==0x8000:
                after_seed=(pair['before_seed']*0x41C64E6D+0x3039)&0xFFFFFFFF
                roll=((after_seed>>16)&0x7FFF)%1000
                result=0 if roll<500 else 1 if roll==500 else 2
                assert pair['after_seed']==after_seed and pair['result_words']==[2,result]
                last=result;predicates.append(dict(source_offset=pair['original_source_offset'],
                    fixture_offset=cursor,before_seed=pair['before_seed'],after_seed=after_seed,roll=roll,result=result,
                    actual_unforced_original_LCG_transition=True))
            elif word==0xA000 and pair.get('original_source_block')==180:effect_offsets.append(pair['original_source_offset'])
            if word in [0x100,0x200,0x300,0x400]:
                span=int.from_bytes(block[cursor+2:cursor+4],'little')
                taken=word==0x100 or (word==0x200 and last==0) or (word==0x300 and last==1) or (word==0x400 and last==2)
                extent=4+(span if taken else 0)
                assert pair['extent']==extent and pair['result_words']==[3,0]
            else:
                extent=command['native_extent'];assert pair['extent']==extent
            cursor+=extent
        assert selected[-1]['word']==0 and selected[-1]['original_source_offset']==572
        assert len(intervals)==len({r['id'] for r in intervals})==11
        assert [r['id'] for r in intervals]==[r['id'] for r in fixture['original_text_records']]
        assert sum(r['prefix']==254 for r in intervals)==1
        assert len(predicates) in [1,2] and predicates[0]['source_offset']==452
        assert len(effect_offsets)==1 and effect_offsets[0] in [472,504,516]
        effects=[r for r in selected if r.get('original_source_block')==180 and r['word']==0xA000]
        ui=[r for r in selected if r['word']==0xC200]
        assert len(ui)==1 and ui[0]['original_source_offset']==570 and ui[0]['result_words']==[3,0]
        assert ui[0]['UI_request_after'][0]==1 and ui[0]['UI_request_after'][2:]==[13,0,0,0,1]
        assert ui[0]['UI_pending_after']==1
        assert intervals[-1]['returned']<=ui[0]['start']<=ui[0]['returned']<=selected[-1]['start']
'''
    tools=[derive('scripts/audit_lil_B179_actual_v4742.py','scripts/audit_lil_B180_actual_v4811.py',{
        source[start:end]:block,
        'B179':'B180','actual_v4742':'actual_v4811','display_fixture_v4739':'display_fixture_v4808',
        'display_run_v4741':'display_run_v4810','display_v4741':'display_v4810',
        'work/analysis/lil_B179_native_approval_v4726/all14_native_progressive_FE_and_source_reconciliation.json':
        'work/analysis/lil_B180_fonts_v4794/all11_progressive_FE_native_planes_and88_alignment_cases.json',
        'source_event179_not_selected':'source_event180_not_selected',
        'all_source16_commands_13_progressive1_impersonal_FE_A000_and_single_end_no_C200_retained':
        'all_source28_commands_10_progressive1_FE_two_predicates_ten_branches_three_A000_C200_end_retained',
        "source['block']!=179":"source['block']!=180",'original_source_block=179':'original_source_block=180',
        "extent=row['decoded_length'],result_words=row['result_words'])":
        "extent=row['decoded_length'],result_words=row['result_words'],before_seed=entry['original_RNG_seed'],after_seed=row['original_RNG_seed'],UI_request_after=row['native_UI_request_words'],UI_pending_after=row['native_UI_pending_flag'])",
        'source_A000=effects,source_C200=ui,':'source_A000=effects,source_C200=ui,actual_predicate_transitions=predicates,',
        'single_source_end508_actually_reached':'single_source_end572_actually_reached',
        'len(actual)==14':'len(actual)==11','actual_all14_progressive_FE_A000_and_single_end_no_C200':'actual_all11_progressive_FE_RNG_effect_C200_and_single_end',
        'fresh_actual_unique_speech_panels=14':'fresh_actual_unique_speech_panels=11',
        'all16_source_commands_stored_and_all25_fixture_commands_actually_selected=True':
        'all28_source_commands_stored_and_actual_conditional_path_verified=True',
        'all14_speeches13_progressive1_impersonal_FE_observed':'all11_speeches10_progressive1_impersonal_FE_observed',
        'source_A000_and_single_end_actually_executed_without_source_omission_no_C200':
        'original_selected_effect_C200_and_single_end_executed_without_source_omission',
        'actual_source_event179_not_selected':'actual_source_event180_not_selected','actual_panels=14':'actual_panels=11'}))]
    ROOT.mkdir(parents=True);save(ROOT/'prepared_audit.json',dict(tools=tools,actual_conditional_path_not_all_alternatives_expected=True,
        original_RNG_seed_transitions_and_UI_fields_checked=True,full_goal_complete=False))
