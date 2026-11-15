"""All1492 current Palace/Inn printf-parent-selector-wrap contracts."""
from pathlib import Path
import inspect,struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/palace_inn_layouts_v2255')
DOC=Path('translations/palace_inn_contextual_editorial_manuscript_v1.json')
INPUTS=[Path('work/analysis/palace_integration_v797/production_layout.json'),Path('work/analysis/inn_integration_v803/production_layout.json')]
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True);doc=read(DOC);rows={r['message_id']:r for r in doc['records']};rom=NdsImage.open(doc['current_ROM']);arm,common=[rom.read_file(p)for p in('/__arm9__.bin','/COMMON/MESFILE.DK4')];entries=current_entries(common,arm)
    snapshot=read('work/analysis/item_context_v2235/native_context.json')['pre_fixture_snapshot'];raw=Path(snapshot['path']).read_bytes();assert sha(raw)==snapshot['sha256']
    for n,r in rows.items():assert entries[n].text==b' '+r['english'].removesuffix('{PAD}').encode('ascii')
    source=inspect.getsource(original.format_case);marker='    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)'
    replacement='''    n=row['message_id'];parent,key=row['native_binding']['parent'],row['native_binding']['table_or_ID']
    for at,value in ((0x264,parent),(0x270,0),(0x274,n),(0x27C,key)):
        u.mem_write(STACK+at,struct.pack('<I',value))
    call(u,0x01FFCF3C-BASE,(wrapped,output,0),instruction_limit=2000000)
    for p,value in zip(pointers,values):
        assert bytes(u.mem_read(p,len(value)+1))==value+bytes(1)
'''
    assert source.count(marker)==1;source=source.replace(marker,replacement);env=dict(original.__dict__);exec(compile(source,__file__,'exec'),env);(ROOT/'effective_formatter.py').write_text(source,encoding='utf-8')
    old=[c for p in INPUTS for c in read(p)['cases']];assert len(old)==1492;cases=[];findings=[];indices=[];seen=set()
    for i,c in enumerate(old):
        if i%64==0:u,_=get_machine(arm,raw)
        n=c['id'];r=rows[n];values=tuple(bytes.fromhex(v)for v in c['source_values_hex']);result=env['format_case'](u,r,values)
        assert result['formatted_hex']==c['formatted_hex'];result.update(index=i,message_ID=n,values_hex=result['English_values_hex'],template_hex=entries[n].text.hex(),native_binding=r['native_binding']);cases.append(result)
        if result['findings']:findings.append(dict(index=i,message_ID=n,findings=result['findings']))
        shape=(n,len(result['lines']),tuple(len(s.encode('cp932'))%2 for s in result['lines']),any(not v.isascii()for v in values),values[0]if n==1180 else None)
        if shape not in seen:seen.add(shape);indices.append(i)
    assert not findings and {r['message_ID']for r in cases}==set(range(1146,1200))
    save(ROOT/'all54_current_native_layouts.json',dict(ARM9_sha256=sha(arm),COMMON_sha256=sha(common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_snapshot=snapshot,input_matrices={str(p):sha(p.read_bytes())for p in INPUTS},case_count=1492,cases=cases,findings=findings,representative_full_font_indices=indices,all54_original_parent_table_and_ID_bindings_used=True,all1492_formatted_bytes_identical_historical=True,complete_native_printf_words_argument_copies_bounds_canaries_and_ABI=True,source_three_night_choices_3_10_30=True,source_contract_fee_and_item_monthly_domains_separately_verified=True,supplied23byte_name_and_extreme_prices_are_stress_not_all_eligible=True,full_font_visual_actual_and_reconciliation_pending=True,no_ROM_or_registry_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(layouts=1492,IDs=54,findings=0,full_font_indices=len(indices)))
