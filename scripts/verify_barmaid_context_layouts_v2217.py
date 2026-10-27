"""Current real parent/ID dispatcher, literal name origins and complete273 layouts."""
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from scripts.verify_barmaid_scoped_layout_v780 import formatter
from scripts.audit_barmaid_name_layout_v779 import origins
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/barmaid_context_layouts_v2217')
DOC=Path('translations/barmaid_contextual_editorial_manuscript_v1.json')
SOURCE=Path('work/analysis/barmaid_editorial_v779/layouts_v1/native_layout_matrix.json')

if __name__=='__main__':
    assert not ROOT.exists()
    ROOT.mkdir(parents=True)
    doc=read(DOC);rows={r['message_id']:r for r in doc['records']}
    rom=NdsImage.open(doc['current_ROM']);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    entries=current_entries(common,arm)
    for n,r in rows.items():assert entries[n].text==b' '+r['english'].removesuffix('{PAD}').encode('ascii')
    context=read('work/analysis/barmaid_context_v2213/native_context.json');snapshot=context['pre_fixture_snapshot'];raw=Path(snapshot['path']).read_bytes()
    assert sha(raw)==snapshot['sha256']and context['current_ARM9_sha256']==sha(arm)
    run,program=formatter();(ROOT/'effective_formatter.py').write_text(program,encoding='utf-8')
    old=read(SOURCE);assert len(old['cases'])==273
    cases=[];unresolved=[];classified=[];indices=[];seen=set()
    for index,case in enumerate(old['cases']):
        if index%64==0:u,_=get_machine(arm,raw)
        n=case['id'];r=rows[n]
        result=run(u,r,tuple(bytes.fromhex(v)for v in case['source_values_hex']))
        result.update(index=index,message_ID=n,values_hex=result['English_values_hex'],template_hex=entries[n].text.hex(),original_parent=0x02054014)
        if result['findings']:
            words=origins(r,result)
            assert result['findings']==['weak_line_end']and words and all(w['entire_word_is_literal_captain_name']for w in words),(n,result)
            classified.append(dict(index=index,message_ID=n,word_origins=words,resolution='All bytes of the apparent article/initial are the original captain first-name argument. No prose or rendering waiver.'))
        result['unresolved_findings']=[]
        shape=(n,len(result['lines']),tuple(len(s.encode('cp932'))%2 for s in result['lines']),any(not bytes.fromhex(v).isascii()for v in result['source_values_hex']))
        if shape not in seen:seen.add(shape);indices.append(index)
        cases.append(result)
    assert len(classified)==5 and {r['message_ID']for r in cases}==set(range(989,1020))
    example=cases[classified[0]['index']];r=deepcopy(rows[example['id']]);values=[bytes.fromhex(v)for v in example['source_values_hex']]
    assert example['id']==989
    r['english']=r['english'].replace('Your name is... %s','Your name is... '+values[1].decode('ascii'))
    r['source_native_arguments']=['barmaid'];r['English_argument_source_indices']=[0]
    literal=deepcopy(example);literal['English_values_hex']=[values[0].hex()]
    negative=origins(r,literal)
    assert negative and not any(w['entire_word_is_literal_captain_name']for w in negative)
    save(ROOT/'all31_current_native_layouts.json',dict(ARM9_sha256=sha(arm),COMMON_sha256=sha(common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_snapshot=snapshot,input_matrix=str(SOURCE),input_matrix_sha256=sha(SOURCE.read_bytes()),case_count=len(cases),cases=cases,findings=unresolved,raw_name_initial_diagnostics=classified,literal_prose_negative_control_rejected=True,no_blanket_weak_end_or_name_waiver=True,representative_full_font_indices=indices,current_original_direct_parent_ID_dispatcher_used=True,all_native_printf_bytes_complete_guards_bounds_and_callee_ABI=True,first_name_capacity16bytes_and17byte_NUL_contract_bound=True,supplied_name_boundaries_not_every_arbitrary_user_string=True,native_machine_reset_every64_cases=True,full_font_visual_and_actual_reconciliation_pending=True,no_ROM_or_registry_change=True,effective_formatter_sha256=sha(program.encode()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(cases=len(cases),raw_typed_name_diagnostics=len(classified),unresolved=0,font_samples=len(indices)),flush=True)
