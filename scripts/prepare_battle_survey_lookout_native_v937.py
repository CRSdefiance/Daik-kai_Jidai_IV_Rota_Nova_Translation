"""Bind24 native previews and source-preserving Survey/Lookout successors."""
import ast
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_battle_survey_lookout_prose_v934 import MANUSCRIPT,IDS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/battle_survey_lookout_v938')
PRODUCTION=Path('translations/battle_survey_lookout_editorial_manuscript_v2.json')

def rendered(source,target,pairs):
    source,target=Path(source),Path(target);before=source.read_bytes();text=source.read_text(encoding='utf-8');assert not target.exists()
    for old,new in pairs:
        assert old in text,(source,old)
        text=text.replace(old,new)
    ast.parse(text)
    return source,target,before,text

def main():
    packet=read('work/analysis/battle_survey_lookout_v933/source_context_packet.json')
    module=rendered('dk4tool/patch/battle_bridge_editorial.py','dk4tool/patch/battle_survey_lookout_editorial.py',[
        ('Complete28 battle Bridge','Complete24 battle Survey/Lookout'),('battle_bridge','battle_survey_lookout'),
        ('from dk4tool.patch.battle_finance_editorial import current_entries as previous_entries','from dk4tool.patch.battle_bridge_editorial import current_entries as previous_entries'),
        ('battle_survey_lookout_layout_v926','battle_survey_lookout_layout_v936'),('range(1681,1709)','range(1709,1733)'),
        ('8013f94caf8fd04b6482b6f73405a9e9a3347cf4ddf38ba238d83ec75028585a',packet['COMMON_sha256']),
        ('57b07085e354e51fbbd6b36b1b0cd8befafbf3b12ef207c3fa85b04598db2e13',packet['ARM9_sha256']),
        ('deck-battle-bridge-visible-v1','deck-battle-survey-lookout-visible-v1'),('dk4-battle-bridge-editorial-v1','dk4-battle-survey-lookout-editorial-v1'),
        ('all3640_other_message_strings_exact','all3644_other_message_strings_exact'),
        ('all162_original_battle_helper_main_and_ordinary_control_selections','all150_original_battle_helper_main_and_ordinary_control_selections'),
        ('len(cases)==162','len(cases)==150'),('len(battle)==108 and len(ordinary)==54','len(battle)==100 and len(ordinary)==50'),
        ("        role=r['source_role_type'];assert role in (5,6,4)\n        if role==5:assert r['actor_ID']<4\n        suffix=(r['actor_ID'] if role==5 else 8+r['actor_ID']) if r['actor_ID']<4 else r['native_voice_class']\n        first={5:1471,6:1475,4:1487}[role] if r['case']=='main_ordinary_working_control' else {5:1681,6:1685,4:1697}[role]",
         "        role=r['source_role_type'];assert role in (3,1)\n        suffix=8+r['actor_ID'] if r['actor_ID']<4 else r['native_voice_class']\n        first={3:1499,1:1511}[role] if r['case']=='main_ordinary_working_control' else {3:1709,1:1721}[role]"),
        ("len(fonts['cases'])==28","len(fonts['cases'])==24"),("len(audit['records'])==28","len(audit['records'])==24"),('all28','all24'),
        ('complete_Xien_Camille_Gerhard_initial_I_and_all_source_words_pass','complete_measurement_and_boarding_sniping_and_all_source_words_pass'),
        ("    assert supplement['Captain5_has_no_NPC_alternatives']\n    assert supplement['established_terms']=={'シエン':'Xien','ゲルハルト':'Gerhard','カミル':'Camille','副官':'First Mate','停戦':'truce'}\n    assert supplement['Xien_evidence']['ordinary_message1498_source_and_current']['message_id']==1498",
         "    assert supplement['established_roles']=={'Survey':3,'Lookout':1}\n    assert supplement['source1720_agent_unstated_preserved']\n    assert supplement['source1718_measurement_also_matters_not_fighting_is_unimportant']\n    assert supplement['source1725_helmsman_relied_upon_not_promoted_to_command']"),
        ("    assert context['Captain5_null_NPC_tables_preserved_and_never_called_as_supported_alternatives']\n    assert context['source_activity0_working_not_activity1_separate_helper126A8']\n    assert all(r['actor_ID']<4 for r in cases if r['source_role_type']==5)",
         "    assert context['no_Sera_special_role15_override_for_roles3_or1']\n    assert context['source_activity0_working_not_activity1_separate_helper126A8']")])
    audit=rendered('scripts/audit_battle_bridge_native_v928.py','scripts/audit_battle_survey_lookout_native_v938.py',[
        ('battle_bridge','battle_survey_lookout'),('battle_survey_lookout_layout_v926','battle_survey_lookout_layout_v936'),('probe_battle_survey_lookout_fonts_v926','probe_battle_survey_lookout_fonts_v936'),('deck-battle-bridge-visible-v1','deck-battle-survey-lookout-visible-v1'),('all162_original_battle_helper_main_and_ordinary_control_selections','all150_original_battle_helper_main_and_ordinary_control_selections'),('==162','==150'),('all28','all24'),('==28','==24'),('28 records','24 records'),('Battle Bridge native-consumer audit','Battle Survey/Lookout native-consumer audit')])
    ROOT.mkdir(parents=True,exist_ok=True);font_path=Path('work/analysis/battle_survey_lookout_v936/native_font_proof.json');fonts=read(font_path)
    assert fonts['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and tuple(c['message_id'] for c in fonts['cases'])==IDS
    for case in fonts['cases']:assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    visual=Path('work/analysis/battle_survey_lookout_v936/visual_review.json');assert not visual.exists() and not PRODUCTION.exists()
    save(visual,{'native_font_proof':str(font_path),'native_font_proof_sha256':sha(font_path.read_bytes()),'review_sheet':fonts['review_sheet'],'review_sheet_sha256':fonts['review_sheet_sha256'],'all24_previews_visually_reviewed':True,'native_IDs':list(IDS),'visual_review_pending':False,
        'findings':'All24 complete native body previews reviewed. Every row begins at x0 and fits216x36. Position1710,unglamorous1714 and also-matters1718 have complete three-row text;1713 fills36 cells. Initial I in1721/1728 and full boarding-action1722 are intact. Revised phrase hints keep during a battle and taking these measurements together and give1712 two whole clauses. No stray text,padding gaps,missing edge letters,word splits or extra pages. Actual scenes and normal returns remain required.','CPU_only_font_scope_no_actual_gameplay_credit':True,'full_goal_complete':False})
    doc=deepcopy(read(MANUSCRIPT));doc.update(reviewed_research_manuscript=str(MANUSCRIPT),reviewed_research_manuscript_sha256=sha(MANUSCRIPT.read_bytes()),formatting_review_pending=False,review_gates=['source','context','localization','naturalness','formatting'],status='24-source-prose-native-font-and-visual-reviewed-registered-release-and-actual-pending')
    for key,path in [('native_font_proof',font_path),('visual_review_proof',visual)]:doc[key]=str(path);doc[key+'_sha256']=sha(path.read_bytes())
    for row in doc['records']:row['review']['formatting']=True
    save(PRODUCTION,doc);provenance=[]
    for source,target,before,text in (module,audit):
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==before
        provenance.append({'source':str(source),'source_before_sha256':sha(before),'source_after_sha256':sha(source.read_bytes()),'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    save(ROOT/'native_successor_provenance.json',{'files':provenance,'all_source_hashes_unchanged':True,'all_successor_replacements_preflighted_before_output':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('24 native previews reviewed;production manuscript and strict Survey/Lookout module/auditor created.',flush=True)
if __name__=='__main__':main()
