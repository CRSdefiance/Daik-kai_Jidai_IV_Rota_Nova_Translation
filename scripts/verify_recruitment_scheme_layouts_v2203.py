"""Current full native layouts for106 reviewed records and source-bound typed statuses."""
from pathlib import Path
from copy import deepcopy
import inspect,struct
from scripts import probe_tavern_conversations_v764 as original
from scripts.recruitment_runtime_research_v771 import STATUS_PHRASES,STATUS_SUFFIX
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from dk4tool.rom.nds import NdsImage
ROOT=Path('work/analysis/recruitment_scheme_layouts_v2203')
DOC=Path('translations/recruitment_schemes_contextual_editorial_manuscript_v1.json')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);doc=read(DOC);rows={r['message_id']:r for r in doc['records']};rom=NdsImage.open(doc['current_ROM']);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm);scheme=read('work/analysis/tavern_schemes_context_v2197b/native_context.json');snap=scheme['read_only_snapshot'];raw=Path(snap['path']).read_bytes();assert sha(raw)==snap['sha256']and sha(arm)==doc['current_ARM9_sha256']
 for n,row in rows.items():assert entries[n].text==b' '+row['english'].removesuffix('{PAD}').encode('ascii')
 source=inspect.getsource(original.format_case)
 marker="    for p, value in zip(pointers, values, strict=False): u.mem_write(p, value + b'\\0')"
 replacement="""    status_index = None
    if n in (905,906):
        status_pointers = struct.unpack('<13I', u.mem_read(0x02156430,52))
        labels = [bytes(u.mem_read(p,128)).split(b'\\\\0')[0] for p in status_pointers]
        status_index = labels.index(values[1])
        assert status_index < 12
        pointers[1] = status_pointers[status_index]
    for i,(p,value) in enumerate(zip(pointers,values)):
        if status_index is not None and i == 1:
            assert bytes(u.mem_read(p,len(value)+1)) == value+b'\\\\0'
        else:
            u.mem_write(p,value+b'\\\\0')
"""
 assert source.count(marker)==1;source=source.replace(marker,replacement)
 a=source.index('    parent = ');b=source.index('    u.mem_write(wrapped - 16',a)
 source=source[:a]+"""    parent = row['native_binding']['parent']
    table = pointers[1] if n in (905,906) else row['native_binding']['table_or_ID'] or 0
    for off,value in ((0x264,parent),(0x270,0),(0x274,n),(0x27C,table)):
        u.mem_write(STACK+off,struct.pack('<I',value))
"""+source[b:]
 marker="    assert b' '.join(result.split()) == b' '.join(expected.split()), (n, values, result, expected)"
 replacement="""    if n in (905,906):
        assert expected.endswith(values[-1]+STATUS_SUFFIX)
        expected=expected[:-len(values[-1])-len(STATUS_SUFFIX)]+STATUS_PHRASES[status_index].encode()+STATUS_SUFFIX
        assert bytes(u.mem_read(pointers[1],len(values[-1])+1))==values[-1]+b'\\\\0'
"""+marker
 assert source.count(marker)==1;source=source.replace(marker,replacement);env=dict(original.__dict__);env.update(STATUS_PHRASES=STATUS_PHRASES,STATUS_SUFFIX=STATUS_SUFFIX);exec(compile(source,__file__,'exec'),env);formatter=env['format_case']
 inputs=[];jobs={}
 for path,kind in(('work/analysis/recruitment_owned_v772/native_layout/matrix.json','recruitment-typed-status-and-number-stress'),('work/analysis/tavern_schemes_layout_v775_v3/native_layout_matrix.json','scheme-original-catalog'),('work/analysis/scheme_followup_editorial_v777/layouts_v1/native_layout_matrix.json','followup-original-catalog')):
  data=read(path);count=0
  for case in data['cases']:
   if case.get('synthetic_23_byte_faction_boundary'):continue
   key=(case['id'],tuple(bytes.fromhex(v)for v in case['English_values_hex']));jobs.setdefault(key,kind);count+=1
  inputs.append(dict(path=path,sha256=sha(Path(path).read_bytes()),supplied_cases=count))
 assert {n for n,values in jobs}==set(rows)
 cases=[];findings=[];samples=[];seen=set()
 for index,((n,values),kind)in enumerate(jobs.items()):
  if index%64==0:u,_=get_machine(arm,raw)
  result=formatter(u,rows[n],values);result.update(index=index,message_ID=n,template_hex=entries[n].text.hex(),supplied_input_kind=kind);cases.append(result)
  if result['findings']:findings.append(dict(index=index,message_ID=n,lines=result['lines'],values_hex=result['values_hex'],findings=result['findings']))
  status=values[1]if n in(905,906)else None
  shape=(n,len(result['lines']),tuple(len(v.encode('cp932'))%2 for v in result['lines']),any(any(b>=128 for b in v)for v in values),status)
  if shape not in seen:seen.add(shape);samples.append(index)
  if index%5000==0:print(dict(index=index,total=len(jobs),findings=len(findings)),flush=True)
 save(ROOT/'all106_current_native_layouts.json',dict(ARM9_sha256=sha(arm),COMMON_sha256=sha(common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_snapshot=snap,cases=cases,case_count=len(cases),findings=findings,representative_full_font_indices=samples,all106_original_source_parent_table_bindings_used=True,typed905_906_use_original_readonly_UI_label_pointers_and_private_phrases=True,all12_status_values_in_full_font_samples=True,original_faction_input_domain='20 fixed nonplayer names;editable player company excluded by original source filters',unsupported_23_byte_faction_stress_not_misrepresented_as_eligible=True,input_contract='work/analysis/current_scheme_filter_binding_v2200/source_filter_and_current_name_contract.json',all_native_printf_full_bytes_guarded_and_ABI_preserved=True,source_input_matrices_replayed_as_supplied_stress_not_all_earned_or_reachable=inputs,native_machine_reset_every64_cases=True,full_font_visual_and_actual_reconciliation_pending=True,no_ROM_or_registry_change=True,effective_formatter_sha256=sha(source.encode()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(cases=len(cases),findings=len(findings),font_samples=len(samples)),flush=True)
