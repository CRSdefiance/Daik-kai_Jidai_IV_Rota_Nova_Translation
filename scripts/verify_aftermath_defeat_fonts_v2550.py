"""Fourteen current source-role1 pipelines and full native defeat-report fonts."""
from pathlib import Path
OLD=Path('scripts/verify_aftermath_fled_fonts_v2542.py')
if __name__=='__main__':
 source=OLD.read_text()
 changes={
 'else255':'else 255','aftermath_fled_fonts_v2542':'aftermath_defeat_fonts_v2550','aftermath_fled_contextual':'aftermath_defeat_contextual',
 "context['all208_original_voice_selections']":"context['all416_original_selected_voice_choices']",
 'set(range(2046,2052))':'{*range(2016,2022),*range(2138,2146)}',
 'if n==2046:':'if n in(2016,2138):',
 '0x53D44,1,0x02117900,None':'0x53D44,1,row["source_table"],None',
 "result['selector']==0x02117900":"result['selector']==row['source_table']",
 'text,n,None,0x02117900':'text,n,None,row["source_table"]',
 "(936,462)":"(936,1078)",
 'all6_current_fled_victory_native_fonts':'all14_current_paired_defeat_native_fonts',
 'for n in range(2046,2052)':'for n in [*range(2016,2022),*range(2138,2146)]',
 'len(cases)==6 and len(copies)==12':'len(cases)==14 and len(copies)==28',
 'all6_complete_native_cases':'all14_complete_native_cases','all12_native_cold_warm_copies':'all28_native_cold_warm_copies',
 'all6_source_numeric_selection_complete_ABI_words_and_visible_ink_pass':'all14_source_numeric_selection_complete_ABI_words_and_visible_ink_pass',
 'all6_original_role1_pipelines':'all14_original_role1_pipelines','all_five_CPU_original_single_roster_byte_fixtures':'all_twelve_CPU_original_single_roster_byte_fixtures',
 'complete_native_font_cases=6':'complete_native_font_cases=14','Five alternatives':'Twelve alternatives',
 'Six current role1 pipelines,full native fonts and12 cold/warm copies':'Fourteen current role1 pipelines,full native fonts and28 cold/warm copies',
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
