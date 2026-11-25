"""Current original parent/key dispatch, coordinate copy preservation and full857 layouts."""
from pathlib import Path
import inspect,re
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/shared_context_layouts_v2229')
DOC=Path('translations/shared_contextual_editorial_manuscript_v1.json')
SOURCE=Path('work/analysis/shared_editorial_v781/layouts_v2/native_layout_matrix.json')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    doc=read(DOC);rows={r['message_id']:r for r in doc['records']}
    rom=NdsImage.open(doc['current_ROM']);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
    for n,r in rows.items():assert entries[n].text==b' '+r['english'].removesuffix('{PAD}').encode('ascii')
    snapshot=read('work/analysis/shared_context_v2224/native_context.json')['pre_fixture_snapshot'];raw=Path(snapshot['path']).read_bytes()
    assert sha(raw)==snapshot['sha256']and sha(arm)==doc['current_ARM9_sha256']
    source=inspect.getsource(original.format_case)
    marker='    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)'
    replacement='''    n=row['message_id']
    parent,key=row['native_binding']['parent'],row['native_binding']['table_or_ID']
    for off,value in ((0x264,parent),(0x270,0),(0x274,n),(0x27C,key)):
        u.mem_write(STACK+off,struct.pack('<I',value))
    call(u,0x01FFCF3C-BASE,(wrapped,output,0),instruction_limit=2000000)
    for p,value in zip(pointers,values):
        assert bytes(u.mem_read(p,len(value)+1))==value+bytes(1)
    if n in (1028,1029):
        expected=re.sub(rb'([NSEW]) +(?=[0-9])',rb'\\1',expected)
'''
    assert source.count(marker)==1;source=source.replace(marker,replacement)
    env={**original.__dict__,'re':re};exec(compile(source,__file__,'exec'),env)
    (ROOT/'effective_formatter.py').write_text(source,encoding='utf-8')
    old=read(SOURCE);assert old['count']==857 and not old['findings']
    cases=[];findings=[];indices=[];seen=set()
    for index,c in enumerate(old['cases']):
        if index%64==0:u,_=get_machine(arm,raw)
        n=c['id'];result=env['format_case'](u,rows[n],tuple(bytes.fromhex(v)for v in c['source_values_hex']))
        result.update(index=index,message_ID=n,values_hex=result['English_values_hex'],template_hex=entries[n].text.hex(),native_binding=rows[n]['native_binding'])
        if result['findings']:findings.append(dict(index=index,message_ID=n,findings=result['findings'],lines=result['lines']))
        shape=(n,len(result['lines']),tuple(len(s.encode('cp932'))%2 for s in result['lines']),any(not bytes.fromhex(v).isascii()for v in result['source_values_hex']))
        if shape not in seen:seen.add(shape);indices.append(index)
        cases.append(result)
    assert not findings and {r['message_ID']for r in cases}==set(range(1020,1070))
    save(ROOT/'all50_current_native_layouts.json',dict(ARM9_sha256=sha(arm),COMMON_sha256=sha(common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_snapshot=snapshot,input_matrix=str(SOURCE),input_matrix_sha256=sha(SOURCE.read_bytes()),case_count=len(cases),cases=cases,findings=findings,representative_full_font_indices=indices,all50_original_parent_table_and_ID_bindings_used=True,all_original_raw_coordinate_town_and_headcount_arguments_remain_byte_exact=True,coordinate_display_normalization_is_in_selected_native_path_not_authored_prose=True,native_printf_bytes_words_guards_bounds_and_callee_ABI_complete=True,supplied_numeric_size_stress_not_earned_or_all_reachable=True,native_machine_reset_every64_cases=True,full_font_visual_and_actual_reconciliation_pending=True,no_ROM_or_registry_change=True,effective_formatter_sha256=sha(source.encode()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(cases=len(cases),findings=len(findings),font_samples=len(indices)),flush=True)
