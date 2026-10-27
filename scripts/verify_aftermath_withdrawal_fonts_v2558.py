"""Eight current role1 withdrawal pipelines and complete native fonts."""
from pathlib import Path
OLD=Path('scripts/verify_aftermath_fled_fonts_v2542.py')
if __name__=='__main__':
 source=OLD.read_text()
 changes={
  'else255':'else 255','aftermath_fled_fonts_v2542':'aftermath_withdrawal_fonts_v2558','aftermath_fled_contextual':'aftermath_withdrawal_contextual',
  'range(2046,2052)':'range(2114,2122)','if n==2046:':'if n==2114:','0x02117900':'0x02117D00',
  '(936,462)':'(936,616)','all6_current_fled_victory_native_fonts':'all8_current_withdrawal_native_fonts',
  'len(cases)==6 and len(copies)==12':'len(cases)==8 and len(copies)==16',
  'all6_complete_native_cases':'all8_complete_native_cases','all12_native_cold_warm_copies':'all16_native_cold_warm_copies',
  'all6_source_numeric_selection_complete_ABI_words_and_visible_ink_pass':'all8_source_numeric_selection_complete_ABI_words_and_visible_ink_pass',
  'all6_original_role1_pipelines':'all8_original_role1_pipelines','all_five_CPU_original_single_roster_byte_fixtures':'all_seven_CPU_original_single_roster_byte_fixtures',
  'complete_native_font_cases=6':'complete_native_font_cases=8','Five alternatives':'Seven alternatives',
  'Six current role1 pipelines,full native fonts and12 cold/warm copies':'Eight current role1 pipelines,full native fonts and16 cold/warm copies',
 }
 for a,b in changes.items():
  assert a in source,a
  source=source.replace(a,b)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
