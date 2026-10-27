"""Eight complete current direct-defender pipelines/fonts without roster fixtures."""
from pathlib import Path
OLD=Path('scripts/verify_aftermath_fled_fonts_v2542.py')
if __name__=='__main__':
 source=OLD.read_text()
 changes={
  'else255':'else 255','aftermath_fled_fonts_v2542':'aftermath_city_fonts_v2566','aftermath_fled_contextual':'aftermath_city_contextual',
  'range(2046,2052)':'range(2038,2046)','0x02117900':'0x021178C0',
  '  if n==2046:assigned,fixture=raw,None\n  else:\n   r=representatives[n];assigned,fixture=assigned_role_raw(arm,raw,r[\'actor_ID\'],r[\'actor_object\']);fixtures.append(fixture)':"  r=representatives[n];actor=r['actor_object'];assigned,fixture=raw,None",
  '0x53D44,1,0x021178C0,None':'0x53F0C,actor,0x021178C0,None',
  "result['parent']==0x02053DB8 and result['selector_offset']==0x27C":"result['parent']==0x02053F40 and result['selector_offset']==0x274",
  'source_role=1,role_fixture=fixture':'source_actor_ID=r["actor_ID"],source_actor_object=actor,original_direct_parent=0x02053F40,original_table_stack_offset=0x274,CPU_actor_or_roster_fixture=None',
  '(936,462)':'(936,616)','all6_current_fled_victory_native_fonts':'all8_current_direct_city_native_fonts',
  'len(cases)==6 and len(copies)==12':'len(cases)==8 and len(copies)==16',
  'all6_complete_native_cases':'all8_complete_native_cases','all12_native_cold_warm_copies':'all16_native_cold_warm_copies',
  'all6_source_numeric_selection_complete_ABI_words_and_visible_ink_pass':'all8_source_numeric_selection_complete_ABI_words_and_visible_ink_pass',
  'all6_original_role1_pipelines':'all8_original_direct_defender_pipelines','all_five_CPU_original_single_roster_byte_fixtures':'CPU_actor_or_roster_fixtures',
  'complete_native_font_cases=6':'complete_native_font_cases=8','current_role1_font':'current_direct_defender_font','current role1 portrait font':'current direct defender font',
  'current original role1 pipeline':'current original direct-defender pipeline',
  'Current isolated CPU original53D44 role1 selection':'Current isolated CPU original53F0C direct defender selection',
  'Five alternatives use original setter82BB8 on one empty duty byte in CPU copies;all actor IDs and remaining4MiB model bytes stay exact.':'Existing original actor objects are passed directly;no actor or roster fixture is applied,and all actor-model bytes stay exact.',
  'Six current role1 pipelines,full native fonts and12 cold/warm copies':'Eight current direct-defender pipelines,full native fonts and16 cold/warm copies',
 }
 for a,b in changes.items():
  assert a in source,a
  source=source.replace(a,b)
 source=source.replace(' def current_machine(a,c,r,p):',' last_model={}\n def current_machine(a,c,r,p):')
 a='  cpu,get,provider=machine(a,c,r,p);executed=set()'
 b=a+"\n  assert get(0xCB184)==root\n  last_model.update(cpu=cpu,before=bytes(cpu.mem_read(root,0x1A04)))"
 assert source.count(a)==1;source=source.replace(a,b)
 a='  assert result[\'input_hex\']==text.hex()'
 assert source.count(a)==1;source=source.replace(a,"  assert bytes(last_model['cpu'].mem_read(root,0x1A04))==last_model['before']\n"+a)
 a=' ROOT.mkdir(parents=True);save('
 assert source.count(a)==1
 extra=''' import inspect
 nativecode=inspect.getsource(native_layout)
 for before,after in [('0x02053DB8','0x02053F40'),("struct.pack('<I',n)","struct.pack('<I',table)"),("struct.pack('<I',table))\\n    call","struct.pack('<I',0))\\n    call")]:
  assert nativecode.count(before)==1
  nativecode=nativecode.replace(before,after)
 nativeenv=dict(native_layout.__globals__);exec(compile(nativecode,__file__,'exec'),nativeenv);native_layout=nativeenv['native_layout']
'''
 source=source.replace(a,extra+a)
 source=source.replace('complete_native_font_cases=8,findings=findings,','complete_native_font_cases=8,findings=findings,effective_direct_native_layout_sha256=sha(nativecode.encode()),all_original_actor_model_bytes_unchanged=True,no_actor_or_roster_fixture=True,')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
