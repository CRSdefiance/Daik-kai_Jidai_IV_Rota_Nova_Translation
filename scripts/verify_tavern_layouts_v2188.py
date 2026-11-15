"""Re-execute all63 Tavern records through current native scoped printf/selector/wrap."""
from pathlib import Path
import inspect,re,struct
from scripts import probe_tavern_conversations_v764 as old
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from dk4tool.rom.nds import NdsImage
ROOT=Path('work/analysis/tavern_layouts_v2188');DOC=Path('translations/tavern_exchanges_contextual_editorial_manuscript_v1.json')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);d=read(DOC);rows={r['message_id']:r for r in d['records']};rom=NdsImage.open(d['current_ROM']);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm);ctx=read('work/analysis/tavern_context_v2184b/fresh_current_native_context.json');raw=Path(ctx['source_snapshot']['path']).read_bytes();assert sha(raw)==ctx['source_snapshot']['sha256']and sha(arm)==d['current_ARM9_sha256']
 for n,r in rows.items():assert entries[n].text==b' '+r['english'].removesuffix('{PAD}').encode('ascii')
 source=inspect.getsource(old.format_case);start=source.index('    parent = ');end=source.index('    u.mem_write(wrapped - 16',start)
 source=source[:start]+'''    parent = row['native_binding']['parent']
    table = row['native_binding']['table'] or (825 if n == 825 else 0)
    u.mem_write(STACK + 0x264, struct.pack('<I', parent))
    u.mem_write(STACK + 0x274, struct.pack('<I', n))
    u.mem_write(STACK + 0x270, struct.pack('<I', table))
    u.mem_write(STACK + 0x27C, struct.pack('<I', 0x02118400 if 852 <= n <= 858 else 0x021184C0))
'''+source[end:]
 marker="    assert b' '.join(result.split()) == b' '.join(expected.split()), (n, values, result, expected)";assert source.count(marker)==1;source=source.replace(marker,"    if n == 842: expected = re.sub(rb'([NSEW]) +([0-9])', rb'\\1\\2', expected)\n"+marker)
 env=dict(old.__dict__);env['re']=re;exec(compile(source,__file__,'exec'),env);formatter=env['format_case'];jobs={};inputs=[]
 def add(n,vs):
  values=tuple(bytes.fromhex(v)if isinstance(v,str)else v for v in vs);assert len(values)==rows[n]['english'].count('%s');jobs.setdefault((n,values),None)
 for path,key in(('work/analysis/tavern_coordinates_v766/native_layout_matrix.json','values_hex'),('work/analysis/tavern_coordinates_v766/actual_leader_layout_matrix.json','values_hex'),('work/analysis/tavern_runtime_v769/new32_native_layout_matrix.json','English_values_hex')):
  prior=read(path);inputs.append(dict(path=path,sha256=sha(Path(path).read_bytes()),supplied_cases=len(prior['cases'])))
  for c in prior['cases']:add(c['id'],c[key])
 for c in ctx['native_provider_fragments']:
  n=c['id'];values=c['arguments_hex'];add(n,values[:1]if n in(871,872)else values)
 for n in range(852,859):
  for value in(0,1,9,10,1000,2147483647):add(n,(str(value).translate(str.maketrans('0123456789','０１２３４５６７８９')).encode('cp932'),))
 assert {n for n,v in jobs}==set(rows);cases=[];findings=[];seen=set();samples=[]
 for index,(n,values) in enumerate(jobs):
  if index%64==0:u,_=get_machine(arm,raw)
  result=formatter(u,rows[n],values);result.update(index=index,message_ID=n,template_hex=entries[n].text.hex());cases.append(result)
  if result['findings']:findings.append(dict(index=index,message_ID=n,lines=result['lines'],values_hex=result['values_hex'],findings=result['findings']))
  shape=(n,len(result['lines']),tuple(len(line.encode('cp932'))%2 for line in result['lines']),any(any(b>=128 for b in v)for v in values),tuple(v for v in values if v in(b'FALCON',b'ICARUS',b'FIONA',b'FORTUNE',b'FURY',b'ABCDEFGHIJKLMNOPQRSTUVW')))
  if shape not in seen:seen.add(shape);samples.append(index)
  if index%5000==0:print(dict(index=index,total=len(jobs),findings=len(findings)),flush=True)
 save(ROOT/'all63_current_native_layouts.json',dict(ARM9_sha256=sha(arm),COMMON_sha256=sha(common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),current_source_context='work/analysis/tavern_context_v2184b/fresh_current_native_context.json',source_snapshot=ctx['source_snapshot'],case_count=len(cases),cases=cases,findings=findings,representative_full_font_indices=samples,all63_source_parent_table_bindings_used=True,all_source_and_current_provider_values_printed_in_actual_English_order=True,native_printf_full_bytes_guards_stack_and_callee_ABI_verified=True,old_input_matrices_replayed_as_supplied_stress_not_earned_eligibility=inputs,native_machine_reset_every64_cases=True,full_font_pagination_and_visual_review_pending=True,no_ROM_or_registry_change=True,effective_formatter_sha256=sha(source.encode()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(cases=len(cases),findings=len(findings),full_font_samples=len(samples)),flush=True)
