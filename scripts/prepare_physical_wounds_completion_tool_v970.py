"""Preflight an evidence-bound wound completion successor;credit remains gated by actual tests."""
from pathlib import Path
import ast
from scripts.prepare_physical_fatigue_native_v961 import rendered
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/physical_wounds_v970')
CHECKPOINT='V970 completes13 wound comments1794-1806 for original conditions2/3 in registered V969:11 revisions and2 retentions. All150 original direct/main battle/ordinary selections,25 healthy and25 prior-fatigue controls,52 full native font cases,7336 copies and178 cache sequences pass. Eight active-widget bitmap/RGB holds verify complete initial I1796,Julios35cell continuation1799,genuine captain retained1803 and Sera24 special1806. Four normal returns preserve scoped state through first Back;original battle time resumes on exit. Explicit room assignments follow observed native combat0/1,and a one-byte condition2/3 fixture is applied after Deck opens. Seven ordinary startup/New Game captures and title match V962. Exact clean-input patch preserves471 batches,114 layers,3655 unselected strings,all graphics/routes,native code,single8KiB cache,216x36 crop and123040 staged bytes.1092 entries complete (817 revised/275 retained),1095 source/prose reviewed. Other physical states,older750-752,mood1833,special1885-1888,raw abandon-caption0x134E54,remaining shared/routes/player prose/raw coverage,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;canonical not promoted;full goal active.'


def main():
    source=Path('scripts/record_physical_fatigue_completion_v964.py').read_text(encoding='utf-8')
    checkpoint_line=next(line for line in source.splitlines() if line.startswith('    checkpoint='))
    doc_start=source.index("    with DOC.open('x'");doc_end=source.index("    for p in map(Path,('docs/translation_progress.md'",doc_start)
    document='''    with DOC.open('x',encoding='utf-8') as f:
        f.write('# V970: physical wound editorial completion\\n\\n'+checkpoint+'\\n\\n## Source and English\\n\\nEleven revisions and two justified retentions cover13 independent wound responses. The clean Japanese restores personal reassurance,hesitant unfinished thoughts,Rafaels ongoing bleeding and But I,Lils pain and responsibility as admiral,and Seras natural brief reassurance. Conditions2/3 share the same dialogue alternatives,but their other effects are not asserted identical. The rough spit remedy remains character speech. All13 clean sources have no IC macro;literal Japanese first-person wording becomes natural English. Exact clean/canonical/current references and all five natural-dialogue-v2 gates are retained.\\n\\n## Formatting and actual scenes\\n\\nAll13 complete native-font previews match independent words at x0 in52 ordinary/battle condition2/3 controls. Maria1805 now breaks after Dont worry,and the continuation keeps about a little wound like this intact. The two prior soft-hint attempts are preserved;no prose or manual line breaks were changed. Source fonts and native bounds cover Rafael1802s full35cell first-person fragment and Lils personal admiral line1804. The general story audit rejects this COMMON format;the dedicated original-consumer audit passes with zero errors and unwaived warnings. Four bad-format and11 glyph-deletion controls reject offline.\\n\\n'+gameplay['scope']+'\\n\\n## Registered candidate\\n\\nExperimental profile all-routes-unified-v969 rebuilds471 batches and114 accepted layers from canonical out/raphael_natural_v2_accepted_base.nds,SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe. Only COMMON/MESFILE.DK4 and ARM9 selection metadata differ from V962. Native code,all other prose,graphics/routes/HELP/ARM7/overlays,sections/BSS,cache arenas and123040 staged bytes are exact. The xdelta reconstructs every candidate byte from clean Japanese SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d. Explicit user cold-boot acceptance is still required for canonical promotion.\\n\\nROM SHA256 '+candidate['sha256']+'\\nPatch SHA256 '+candidate['patch_sha256']+'\\n')
'''
    s,t,b,text=rendered('scripts/record_physical_fatigue_completion_v964.py','scripts/record_physical_wounds_completion_v970.py',[
        (source[doc_start:doc_end],document),
        ('fatigue reviews','wound reviews'),('physical_fatigue','physical_wounds'),
        ('from dk4tool.patch.battle_gunnery_deck_editorial import current_entries as previous_entries','from dk4tool.patch.physical_fatigue_editorial import current_entries as previous_entries'),
        ('physical_wounds_layout_v960','physical_wounds_layout_v968b'),('prepare_physical_wounds_release_v962','prepare_physical_wounds_release_v969'),('verify_physical_wounds_gameplay_v964','verify_physical_wounds_gameplay_v970b'),
        ('physical_wounds_v964','physical_wounds_v970'),('V964 Physical Fatigue','V970 Physical Wounds'),
        ("assert ledger['records_editorially_completed']==1066 and ledger['records_with_source_and_prose_pass']==1082","assert ledger['records_editorially_completed']==1079 and ledger['records_with_source_and_prose_pass']==1095"),
        ('{1783,1784,1790,1793}','{1796,1799,1803,1806}'),('Camille_ASCII_I_Cristina_Recreation_Room_genuine_captain_and_Sera_special_pass','Camille_ASCII_I_Julio35cell_continuation_genuine_captain_and_Sera_special_pass'),
        ('whole256x384_title_menu_at1100_exact_to_V954','whole256x384_title_menu_at1100_exact_to_V962'),
        ('all75_original_direct_main_battle_and_ordinary_fatigue_selections','all150_original_direct_main_battle_and_ordinary_wound_selections'),('==75','==150'),
        ("context['Sera24_special_ID']==1793 and context['job_role_and_mood_not_queried_in_physical_status_branch']","context['Sera24_special_ID']==1806 and context['job_role_and_mood_getters_not_called'] and len(context['all25_condition1_prior_fatigue_discriminating_controls'])==25"),
        ("fonts['complete_native_font_cases']==26","fonts['complete_native_font_cases']==52"),('all-routes-unified-v962','all-routes-unified-v969'),
        ('complete_ASCII_I1783_aligned_Recreation_Room1784_retained1790_and_Sera1793_reviewed','complete_ASCII_I1796_35cell_strength1799_retained1803_and_Sera1806_reviewed'),
        ('all13_fonts26_cases75_source25_healthy50_pronoun7336_copies178_sequences_pass','all13_fonts52_cases150_source25_healthy25_fatigue7336_copies178_sequences_pass'),
        ('ordinary_and_battle_font_controls','condition2_3_ordinary_and_battle_font_controls'),("'editorial_decision']=='revise' for r in records)==10","'editorial_decision']=='revise' for r in records)==11"),
        ('Shared-Physical-Condition1-Fatigue1781-1793','Shared-Physical-Conditions2-3-Wounds1794-1806'),
        ('records_editorially_completed=1079,records_revised_and_integrated=806,retained_wordings_editorially_completed=273','records_editorially_completed=1092,records_revised_and_integrated=817,retained_wordings_editorially_completed=275'),
        ("['/COMMON/MESFILE.DK4']=1078","['/COMMON/MESFILE.DK4']=1091"),('previous_current_integrated_candidate_V954','previous_current_integrated_candidate_V962'),
        ('experimental-physical-fatigue13','experimental-physical-wounds13'),
        ('13 condition1 fatigue comments.','13 condition2/3 wound comments.'),
        ('13 full native fonts in26 ordinary/battle controls,eight full-word/actual-RGB holds,four normal returns and15 offline rejection controls. Complete ASCII I1783,aligned Recreation Room1784,retained captain1790 and Sera1793 pass. No game-wide guarantee.','13 full native fonts in52 condition2/3 ordinary/battle controls,eight full-word/actual-RGB holds,four normal returns and15 offline rejection controls. Complete initial I1796,35cell continuation1799,retained captain1803 and Sera1806 pass. No game-wide guarantee.'),
        ('work/analysis/battle_gunnery_deck_v955/user676_677_current_preservation.json','work/analysis/physical_fatigue_v964/user676_677_current_preservation.json'),
        (checkpoint_line,'    checkpoint='+repr(CHECKPOINT)),
        ('V964-Physical-Fatigue13-complete','V970-Physical-Wounds13-complete'),
        ('13 source/prose reviews,50 first-person expansions,26 native fonts,registered V962/exact patch,four actual scenes/returns and13 completed entries','13 source/prose reviews,200 original selectors,52 native fonts,registered V969/exact patch,four actual scenes/returns and13 completed entries'),
        ("values())==1079 and sum(ledger['source_prose_reviewed_counts_by_file'].values())==1082","values())==1092 and sum(ledger['source_prose_reviewed_counts_by_file'].values())==1095"),
        ('V964: physical fatigue editorial completion','V970: physical wound editorial completion'),
        ('physical_wounds_v970_962','physical_wounds_v970_969'),('V962.png','V969.png'),('Actual V962 cold boot with declared coordinates,room assignment and officer-condition1 fixture','Actual V969 cold boot with declared coordinates,room assignment and late officer-condition2/3 fixture'),
        ('range(957,965)','(965,966,967,968,\'968b\',969,970)'),
        ('work/analysis/physical_wounds_v962/standard_story_audit.log','work/analysis/physical_wounds_v969/standard_story_audit.log'),
        ('13 reviews complete:1079 total (806 revised/273 retained),1082 source/prose','13 reviews complete:1092 total (817 revised/275 retained),1095 source/prose')])
    ast.parse(text)
    with t.open('x',encoding='utf-8') as f:f.write(text)
    assert s.read_bytes()==b
    save(ROOT/'completion_tool_provenance.json',{'source':str(s),'source_before_sha256':sha(b),'source_after_sha256':sha(s.read_bytes()),'source_unchanged':True,'successor':str(t),'successor_sha256':sha(t.read_bytes()),'all_replacements_preflighted_before_output':True})
    print('Wound completion successor created;all native,actual,visual and patch gates remain required.',flush=True)


if __name__=='__main__':main()
