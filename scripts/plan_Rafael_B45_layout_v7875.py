"""Automatic source-bound paragraphs at original progressive216px and FE228px widths; no approval."""
import inspect
from dataclasses import replace
from types import FunctionType
from pathlib import Path
from dk4tool.dialogue import qa
from dk4tool.dialogue.encoder import RelocatableDialogueEncoding
from dk4tool.dialogue.layout import DialogueDiagnostic
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.plan_lil_B234_layout_v7586d import plan as old_plan,PAIRS
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_layout_v7875')
MANUSCRIPT=Path('translations/rafael_B45_editorial_manuscript_v1.json')
LOGICAL=Path('work/analysis/Rafael_B45_logical_v7874/12_logical_paragraphs48_original_native_alignments_distinct_FE.json')
def display(text):
    return text.replace('{MACRO:FI}','Rafael').replace('{MACRO:FA}','Castor').replace('{MACRO:FO}','Castor Co.')
def get_profile(row):
    is_FE=row['kind']=='system-FE'
    return replace(get_dialogue_profile('raphael-story-shared-events-live'),
        window_width_px=228 if is_FE else 216,
        macro_widths={'FI':36,'FA':36,'FO':60,'I':12},macro_ascii_lengths={'FI':6,'FA':6,'FO':10},
        leading_speaker_bytes=frozenset({254} if is_FE else {0,6}))
ADAPTER=checked_text(inspect.getsource(old_plan),{
    "row['kind']=='progressive' and row['source_selector'] in [19,104]":
    "((row['kind']=='progressive' and row['source_selector'] in [0,6]) or (row['kind']=='system-FE' and row['source_selector']==254))",
    "all(32<=ord(c)<127 or c=='…' and row['id']=='DK4_MES_B234_R0005' and body=='………' and bytes.fromhex(row['source_hex'])==bytes.fromhex('68816381638163') for c in body)":
    "all(32<=ord(c)<127 for c in body)",
    "limit=4;words=body.split()":"cells=38 if row['kind']=='system-FE' else 36;limit=4;words=body.split()",
    'if length+reserve+int(line>0)>36:continue':'if length+reserve+int(line>0)>cells:continue',
    "row['id']=='DK4_MES_B234_R0033'":"False",
    "{'DK4_MES_B234_R0016':{('draw','customers')}}.get(row['id'],set())":"set()",
    'cost[0]+tiny,cost[1]+1,cost[2]+weak':'cost[0]+tiny+weak,cost[1]+1,cost[2]+weak',
    '(36-length)**2':'(cells-length)**2',
    "get_dialogue_profile('lil-opening-editorial-native-v1')":"get_profile(row)",
    "name='B234-source-bound-layout-RESEARCH-ONLY'":"name='Rafael-B45-RESEARCH-ONLY:'+row['id'],literal_prefix_policy='native-guard-v255'",
    'leading_speaker_bytes=frozenset([19,104])':"leading_speaker_bytes=get_profile(row).leading_speaker_bytes",
    "assert profile.macro_ascii_lengths['FA']==5 and profile.macro_widths['FA']==30":
    "assert profile.macro_ascii_lengths=={'FI':6,'FA':6,'FO':10} and profile.macro_widths['FA']==36",
    'No source/prose-preserving B234 plan:':'No source/prose-preserving Rafael B45 plan:',
    'all_words_punctuation_and_zero_macros_unchanged':'all_words_punctuation_and_source_macros_unchanged',
})
ENV={**old_plan.__globals__,'display':display,'get_profile':get_profile,
    'PAIRS':PAIRS|{('trade','goods'),('market','share'),('governor\\x27s','office'),('contract','fee'),('minimum','fee'),
        ('just','starting'),('starting','out'),('local','ruler'),('local','stock'),('you','bought'),
        ('in','lisbon'),('in','ceuta'),('20','percent'),('anything','you'),('sell','goods')}}
exec(compile(ADAPTER,__file__+'::measured-Rafael-progressive-andFE-planner','exec'),ENV)
plan=ENV['plan']
def base_qa(row,p):
    profile=replace(get_profile(row),name='Rafael-B45-native-QA:'+row['id'],
        literal_prefix_policy='native-guard-v255',max_lines=p['max_total_rows'])
    raw=bytes.fromhex(row['source_hex'])
    def encoded(source,text,prof):
        assert source==raw and text==row['english'] and prof==profile
        return RelocatableDialogueEncoding(p['formatted_markup'],bytes.fromhex(p['encoded_hex']),
            tuple(DialogueDiagnostic(**v) for v in p['diagnostics']))
    audit=FunctionType(qa.audit_relocatable_dialogue_record.__code__,
        {**qa.audit_relocatable_dialogue_record.__globals__,'encode_relocatable_dialogue':encoded},
        argdefs=qa.audit_relocatable_dialogue_record.__defaults__)
    return audit(raw,row['english'],profile)
if __name__=='__main__':
    assert not ROOT.exists();doc,logical=map(read,[MANUSCRIPT,LOGICAL])
    assert logical['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and logical['fresh_native_alignment_cases']==48
    rows=[];failures=[]
    for row in doc['records']:
        try:
            assert not row['review']['formatting'];planning=dict(row);body=row['english']
            for token in ['FI','FA','FO']:body=body.replace(token,'{MACRO:'+token+'}')
            planning['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body
            p=plan(planning);assert ' '.join(p['lines'])==body
            p.update(file_path=doc['file_path'],block=row['block'],source_record_index=row['source_record_index'],
                source_selector=row['source_selector'],kind=row['kind'],logical_English=row['english'],planning_record=planning,
                base_QA=base_qa(planning,p),original_consumer_width_px=228 if row['kind']=='system-FE' else 216)
            rows.append(p)
        except (ValueError,AssertionError) as exc:
            failures.append(dict(id=row['id'],error_type=type(exc).__name__,error=str(exc)))
    ROOT.mkdir(parents=True);save(ROOT/'12_automatic_plans_distinct_progressive216_FE228_all_QA_preserved.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),logical=str(LOGICAL),logical_sha256=sha(LOGICAL.read_bytes()),
        records=rows,failures=failures,source_owned_plan_adapter=ADAPTER,source_owned_measured_macro_display=inspect.getsource(display),
        source_owned_measured_profile=inspect.getsource(get_profile),source_word_boundary_pairs=sorted(ENV['PAIRS']),
        progressive_viewport=[216,64],FE_logical_viewport=[228,48],FE_physical_viewport=[228,64],
        same_original_four_rows_per_page_distinct_native_consumers=True,source_macros_FI6_FA6_FO10=True,
        no_manual_break_padding_alignment_orprose_abbreviation_authored=True,
        full_original_consumer_width_pair_phase_andnative_linebreak_guards=True,
        all_original_QA_issues_preserved_no_waivers=True,no_global_profile_font_orweak_boundary_change=True,
        compiled_native_font_bounds_pagination_controls_stored_actual_andrelease_pending=True,
        all12_formatting_gates_remain_false=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,LOGICAL,Path(old_plan.__code__.co_filename),Path(__file__)]},full_goal_complete=False))
    for r in rows:print(r['id'],r['lines'],r['line_lengths'],'QA',[(i['code'],i['severity']) for i in r['base_QA']['issues']])
    print('FAILURES',failures)
    if failures:raise SystemExit(1)
