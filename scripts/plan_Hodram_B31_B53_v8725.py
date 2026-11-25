"""Automatic full-usable-width mixed Hodram paragraphs; unchanged prose and original QA."""
from dataclasses import replace
from types import FunctionType
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_Rafael_B45_layout_v7881b as previous
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B31_B53_layout_v8725')
DOC=Path('translations/hodram_B31_B53_editorial_manuscript_v1.json')
LOGICAL=Path('work/analysis/Hodram_B31_B53_logical_v8724/logical_paragraphs.json')
MEASUREMENT=previous.MEASUREMENT

def get_profile(row):
    assert row['kind']=='progressive' and row['source_selector'] in [34,113]
    p=get_dialogue_profile('hodram-story-live')
    assert p.window_width_px==216 and p.max_lines==4 and p.default_ascii_width==6 and p.default_multibyte_width==12
    assert p.macro_ascii_lengths==dict(FI=6,FA=9,FO=15) and p.guard_linebreaks and p.pair_phase_safe_breaks
    return replace(p,leading_speaker_bytes=frozenset({row['source_selector']}))

def display(text):return text.replace('{MACRO:FI}','Hodram').replace('{MACRO:FA}','Bergstrom').replace('{MACRO:FO}','Bergstrom Fleet')

ADAPTER=checked_text(previous.ADAPTER,{
    "row['source_selector'] in [0,6]":"row['source_selector'] in [34,113]",
    "profile.macro_ascii_lengths=={'FI':6,'FA':6,'FO':10} and profile.macro_widths['FA']==36":"profile.macro_ascii_lengths=={'FI':6,'FA':9,'FO':15} and profile.macro_widths['FA']==54",
    'Rafael B45 plan:':'Hodram B31/B53 plan:',
    'Rafael-B45-RESEARCH-ONLY:':'Hodram-B31-B53-RESEARCH-ONLY:',
})
PAIRS=previous.previous.ENV['PAIRS']|{('found','it'),('it','already'),('beat','me'),("you'd",'better'),('anyone','else'),('the','best'),('best','in'),('in','the'),('the','world'),("won't",'settle'),('settle','for'),('for','less'),('lil','argot'),("ullr's",'bow'),('too','bad'),('in','amsterdam'),('oh','well')}|{('southern','mediterranean'),('my','advice'),('better','off'),('off','leaving'),('bad','news'),('your','own'),('own','good'),('another','sea'),('what','do'),('do','you'),('you','mean')}|{("hayreddin's",'outfit'),('death','wish')}|{('will','you?'),('take','you'),('you','on'),('ottoman','empire'),("you'd",'better')}
ENV={**previous.ENV,'get_profile':get_profile,'display':display,'PAIRS':PAIRS,'BOUND_ZERO_SOURCE_BODIES':frozenset()}
exec(compile(ADAPTER,__file__+'::source-qualified-Hodram-full-usable-width','exec'),ENV);plan=ENV['plan']
base_qa=FunctionType(previous.base_qa.__code__,{**previous.base_qa.__globals__,'get_profile':get_profile},argdefs=previous.base_qa.__defaults__)

if __name__=='__main__':
    assert not ROOT.exists();doc,logical,measured=map(read,[DOC,LOGICAL,MEASUREMENT])
    assert logical['manuscript_sha256']==sha(DOC.read_bytes()) and logical['fresh_native_alignment_cases']==12 and len(doc['records'])==3
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    _,_,oracle=bind(image);assert oracle['whole12byte_name_inverse_to_previous_font_oracle_ARM9'] and measured['ARM9_sha256']==previous.bound['current_ARM9_sha256']
    rows=[];failures=[]
    for row in doc['records']:
        try:
            assert not row['review']['formatting'];planning=dict(row);planning['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english']
            p=plan(planning);assert ' '.join(p['lines'])==row['english'];raw=bytes.fromhex(p['encoded_hex']);assert raw[0]==row['source_selector'] and b'\0' not in raw[1:]
            p.update(file_path=doc['file_path'],block=row['block'],source_record_index=row['source_record_index'],source_selector=row['source_selector'],kind=row['kind'],logical_English=row['english'],planning_record=planning,
                base_QA=base_qa(planning,p),original_consumer_usable_text_width_px=216,original_consumer_bitmap_width_px=228 if row['kind']=='system-FE' else 216)
            rows.append(p)
        except (AssertionError,ValueError) as exc:failures.append(dict(id=row['id'],error_type=type(exc).__name__,error=str(exc)))
    ROOT.mkdir(parents=True);save(ROOT/'automatic_plans.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),logical=str(LOGICAL),logical_sha256=sha(LOGICAL.read_bytes()),records=rows,failures=failures,
        source_owned_planner=ADAPTER,source_owned_profile_function=__import__('inspect').getsource(get_profile),source_owned_display_function=__import__('inspect').getsource(display),coherent_pairs=sorted(PAIRS),
        all_words_punctuation_andzero_source_macros_preserved_without_shortening=True,prose_manual_breaks_authored=False,automatic_compiler_breaks_not_manual_prose=True,
        all_progressive216_bitmap_andusable_width_no_FE_panel=True,earlier_boundary_measurement=str(MEASUREMENT),earlier_boundary_measurement_sha256=sha(MEASUREMENT.read_bytes()),target_font_oracle_inverse_binding=oracle,
        original_QA_warnings_errors_infos_retained_without_waiver=True,formatting_gate_native_glyphs_stored_actual_andrelease_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,LOGICAL,MEASUREMENT,Path(previous.__file__),Path('scripts/Hodram_FE_font_oracles_v8315.py'),Path(__file__)]}))
    for p in rows:print(p['id'],p['expected_native_pages'],p['lines'],[(i['severity'],i['code']) for i in p['base_QA']['issues']])
    assert not failures and len(rows)==3
