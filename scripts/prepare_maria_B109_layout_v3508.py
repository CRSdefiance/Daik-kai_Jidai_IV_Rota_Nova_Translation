"""Prepare Maria-specific layout/native-plane tools;source UI actual proof remains required."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B109_layout_tools_v3508')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('work/analysis/maria_B109_source_v3498/all26_clean_current_complete_context.json');packet=read(source);control=Path('work/analysis/maria_B109_controls_v3502/source_restored_UI_prefix_pause_C200_and34_commands_contract.json');contract=read(control);profile=Path('dk4tool/dialogue/maria_B109_profile.py');assert not profile.exists()
    deps=[source,control,Path('work/analysis/maria_B109_voices_v3499/current_four_Maria_static_names_voices_and_native_context.json'),Path('work/analysis/maria_B109_dispatches_v3500/all26_source_current_Maria_dispatches_and_catalog.json'),Path('work/analysis/maria_B109_entry_v3501/source_EV3_B109_action_dependency_and_native_getter_binding.json'),Path('work/analysis/maria_B109_terms_v3504b/current_approved_Admiral_Ming_Netherlands_and_source_culture.json'),Path('work/analysis/maria_B109_macro_profile_v3507/four_static_actors_default_macro_lengths16_alignment_cases.json')]
    hashes=[packet['blocks'][0]['clean_block_sha256'],packet['blocks'][0]['current_block_sha256'],contract['control_restored_draft_sha256']]
    text='''"""Exact B109 progressive metrics,with separate source UI restoration/actual gates."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=%r
BLOCKS=frozenset(%r)
SELECTORS=frozenset({3,11,21,74})
DEPENDENCIES=%r
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS or consumer!='progressive':raise ValueError('Exact Maria B109 source/current block and progressive runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Maria B109 source contract changed:'+path)
    base=get_dialogue_profile('maria-story-shared-events-live')
    return replace(base,name='maria-B109-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,balanced_wrapping=True,literal_prefix_policy='native-guard-v255',macro_widths={'FI':30,'FA':12,'FO':42,'I':12},macro_ascii_lengths={'FI':5,'FA':2,'FO':7},metrics_source=base.metrics_source+';B10926 progressive speeches,four static actors in actual Maria captain3 context.52 native dispatches and16 default macro cases bind5/2/7 lengths;source macros0. Original CS0101/4500/4684 prefix restoration,pause andC200 are separate source controls;focused actual display/transition approval remains required.')
'''%(packet['current_ARM9_sha256'],hashes,{str(p):sha(p.read_bytes()) for p in deps})
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8');pairs=[]
    def make(a,b,changes,transform=None):
        a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in changes:assert x in t,x;t=t.replace(x,y)
        if transform:t=transform(t)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append(dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())))
    make('dk4tool/dialogue/lil_B139_B140_layout_v2.py','dk4tool/dialogue/maria_B109_layout_v1.py',[
      ('lil-B139-B140-progressive-runtime-bound-v1','maria-B109-progressive-runtime-bound-v1'),('frozenset({2,4,9,16,20,21,171})','frozenset({3,11,21,74})'),("[('FI',3),('FA',5),('FO',9)]","[('FI',5),('FA',2),('FO',7)]"),('source-bound B139/B140 profile','source-bound Maria B109 profile'),('def _word(value):',"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('zheng','he'),('indian','ocean'),('western','european'),('european','powers'),('maritime','ban'),(\"ming's\",'policies'),('trading','profits'),('place','at'),('at','sea'),('all','of'),('of','a'),('a','sudden'),('run','out'),('of','france'),('time','of'),('of','my'),('my','life'),('your','leadership'),('your','skill'),('tougher','parts'),('parts','to'),('to','play')})\n\ndef _word(value):")])
    make('scripts/plan_lil_B139_B140_layout_v3473.py','scripts/plan_maria_B109_layout_v3508.py',[
      ('plan67','plan26'),('lil_B139_B140_layout_v3473','maria_B109_layout_v3508'),('lil_remaining_B139_B140_source_v3456','maria_B109_source_v3498'),('next67_B139_B140_clean_current_context','all26_clean_current_complete_context'),('lil_B139_B140_profile','maria_B109_profile'),('lil_B139_B140_layout_v2','maria_B109_layout_v1'),('lil_B139_B140_editorial_manuscript_v4','maria_B109_editorial_manuscript_v1'),('lil_B139_B140_editorial_manuscript_v5','maria_B109_editorial_manuscript_v2'),('/data/SC2.DK4','/data/SC3.DK4'),('all67','all26'),('len(reports)==67','len(reports)==26'),('plans=67','plans=26'),("dialogue_profile='lil-opening-editorial-native-v1'","dialogue_profile='maria-story-shared-events-live'")])
    def native_expand(t):
        start=t.index('def expand(');end=t.index("if __name__=='__main__':",start);return t[:start]+'from scripts.prove_maria_B109_macro_profile_v3507 import expand\n\n'+t[end:]
    make('scripts/verify_lil_B139_B140_fonts_v3472.py','scripts/verify_maria_B109_fonts_v3509.py',[
      ('Current536 macro calls,67 progressive planes and67 full paragraph QA.','Current208 logical/compiled macro cases,26 native planes and26 paragraph QA.'),('lil_B139_B140_profile','maria_B109_profile'),('lil_B139_B140_layout_v1','maria_B109_layout_v1'),('lil_B139_B140_fonts_v3472','maria_B109_fonts_v3509'),('lil_B139_B140_editorial_manuscript_v4','maria_B109_editorial_manuscript_v2'),('/data/SC2.DK4','/data/SC3.DK4'),('len(cases)==67 and len(qa_reports)==67 and macro_calls==536','len(cases)==26 and len(qa_reports)==26 and macro_calls==208'),('blocks[139]','blocks[109]'),('blocks[137]','blocks[108]'),('selectors=[2,4,9,16,20,21,171]','selectors=[3,11,21,74]'),('format(4 if selector==2 else 2','format(11 if selector==3 else 3'),('len(negatives)==23','len(negatives)==17'),('all67','all26'),('current_original_macro_alignment_calls=536','current_original_macro_alignment_calls=208'),('actual_selected_B139_B140_IDs','actual_selected_B109_IDs'),('67 complete progressive planes,536 macro cases,67 QA plans and23source-consumer','26 complete progressive planes,208 macro cases,26 QA plans and17 source-consumer'),('nine sheets','four sheets'),("expected=wrapped.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')","expected=wrapped.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan')")],native_expand)
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),tools=pairs,source_UI_prefix_restoration_and_focused_actual_display_separate_required=True,source_macros0_default_macro_lengths5_2_7_verified16_cases=True,producer_sha256=sha(Path(__file__).read_bytes()),all_prior_artifacts_preserved=True,full_goal_complete=False))
