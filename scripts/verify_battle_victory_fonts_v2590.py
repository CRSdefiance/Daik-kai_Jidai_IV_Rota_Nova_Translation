"""Eight current legacy victory pipelines;exact ordered glyphs and pair blank."""
from pathlib import Path
if __name__=='__main__':
 outer=Path('scripts/verify_flagship_capture_fonts_v2582.py').read_text();needle="\n exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})";assert outer.count(needle)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(needle,'\n captured=source'),__file__,'exec'),env);source=env['captured']
 changes={
  'flagship_capture_fonts_v2582':'battle_victory_fonts_v2590','flagship_capture_contextual':'battle_victory_contextual',
  'out/all_routes_combined_v1364_candidate.nds':'out/all_routes_combined_v1404_candidate.nds',
  'from scripts.review_flagship_capture_context_v2581 import compiled':'from scripts.battle_victory_native_plan_v1396 import compiled',
  'work/analysis/flagship_precision_fonts_v1357/native_font_proof.json':'work/analysis/battle_victory_fonts_v1397b/native_font_proof.json',
  '0x02117740':'0x02117EE0','range(2011,2016)':'range(2130,2138)',
  'len(copies)==10':'len(copies)==16','all5_complete_native_cases':'all8_complete_native_cases',
  'all10_native_cold_warm_copies':'all16_native_cold_warm_copies',
  'all5_source_numeric_selection_complete_ABI_words_and_visible_ink_pass':'all8_source_numeric_selection_complete_ABI_words_and_visible_ink_pass',
  'unique_native_reports=5':'unique_native_reports=8','[2011,2011,2012,2011,2011,2013,2014,2015]':'list(range(2130,2138))',
  'all8_current_flagship_capture_native_fonts':'all8_current_battle_victory_native_fonts',
  'five full native reports and10 cold/warm copies':'eight full native reports and16 cold/warm copies',
  'from pathlib import Path':'from pathlib import Path\nfrom copy import deepcopy',
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 source=source.replace(' def current_machine(a,c,r,p):',' checked_machines=[]\n def current_machine(a,c,r,p):')
 source=source.replace('cpu,get,provider=machine(a,c,r,p);executed=set()','cpu,get,provider=machine(a,c,r,p);executed=set();checked_machines.append((cpu,bytes(cpu.mem_read(root,0x1A04))))')
 needle='  assert result[\'input_hex\']==text.hex()'
 assert needle in source;source=source.replace(needle,"  last,beforemodels=checked_machines[-1];assert bytes(last.mem_read(root,0x1A04))==beforemodels\n"+needle)
 source=source.replace('  models=bytes(check.mem_read(root,0x1A04))\n','')
 needle="  pixels=raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)"
 replacement="""  assert formatted==b' '+text and b'\\n'not in formatted and not text.startswith(b' ')
  events=[];pixels=raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000,glyph_events=events)
  expected_codes=list(formatted)+([32]if len(formatted)%2 else [])
  assert [e['code']for e in events]==expected_codes
  assert [(e['x'],e['y'],e['style'])for e in events]==[(6*i,0,1)for i in range(len(expected_codes))]
  assert events[1]['x']==6 and events[-1]['x']+6<=228 and not any(pixels[228*11:])
"""
 assert needle in source;source=source.replace(needle,replacement)
 source=source.replace('native_font_sha256=sha(pixels),native_pipeline=result,','native_font_sha256=sha(pixels),complete_glyph_events=events,original_leading_cell_count=1,original_odd_pair_trailing_blank_cells=len(expected_codes)-len(formatted),actor_models_unchanged_after_complete_pipeline=True,native_pipeline=result,')
 old=Path('scripts/probe_battle_victory_fonts_v1397.py').read_text();a=old.index('    invalid = []');b=old.index('    sheet = ',a)
 block='\n'.join(line[3:]if line.startswith('   ')else line for line in old[a:b].splitlines()).replace('rows[2132]','records_by_ID[2132]')+'\n'
 needle=" sheet=Image.new('RGB',(936,616)";assert needle in source;source=source.replace(needle,block+needle)
 source=source.replace('unique_native_reports=8,findings=findings,','unique_native_reports=8,findings=findings,invalid_compiler_inputs_rejected=invalid,all8_original_legacy_leading_cells_ordered_glyphs_odd_pair_blanks_and_unchanged_actor_models_verified=True,')
 source=source.replace('Current isolated CPU original53D44 role1 selection','Current isolated CPU original53D44 role1 legacy victory selection;compiler emits no leading guard,original formatter supplies one cell and native ASCII pairs preserve the exact optional trailing blank')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
