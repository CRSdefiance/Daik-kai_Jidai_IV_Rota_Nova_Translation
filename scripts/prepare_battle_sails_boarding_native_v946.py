"""Bind24 native previews and guarded SailHandling/Boarding successors."""
import ast
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch import battle_survey_lookout_editorial as parent
from scripts.prepare_battle_sails_boarding_prose_v944 import MANUSCRIPT,IDS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/battle_sails_boarding_v947')
PRODUCTION=Path('translations/battle_sails_boarding_editorial_manuscript_v2.json')
def rendered(source,target,pairs):
    source,target=Path(source),Path(target);before=source.read_bytes();text=source.read_text(encoding='utf-8');assert not target.exists()
    for old,new in pairs:
        assert old in text,(source,old)
        text=text.replace(old,new)
    ast.parse(text)
    return source,target,before,text

def main():
    packet=read('work/analysis/battle_sails_boarding_v940/source_context_packet.json')
    old_supplement="    assert supplement['established_roles']=={'Survey':3,'Lookout':1}\n    assert supplement['source1720_agent_unstated_preserved']\n    assert supplement['source1718_measurement_also_matters_not_fighting_is_unimportant']\n    assert supplement['source1725_helmsman_relied_upon_not_promoted_to_command']"
    new_supplement="""    assert supplement['established_roles']=={'SailHandling':0,'Boarding':7}
    assert supplement['mast_crew_metonymy_supported_by_help125']
    assert supplement['source1736_conditional_expected_evasion_not_invulnerability']
    assert supplement['source1739_risk_not_guaranteed_hit']
    assert supplement['source1754_personal_tactical_judgment_not_universal_duel_rule']
    pronoun_path=Path(supplement['source_pronoun_proof'])
    assert sha(pronoun_path.read_bytes())==supplement['source_pronoun_proof_sha256']
    pronouns=read(pronoun_path)
    assert pronouns['candidate_sha256']==doc['current_ROM_sha256'] and pronouns['ARM9_sha256']==SOURCE_ARM
    assert pronouns['source1747_hex']==next(r['source_hex'] for r in doc['records'] if r['message_id']==1747)
    assert pronouns['IC_is_first_person_not_actor_name'] and pronouns['source1747_first_person_leads_hand_to_hand_combat']
    assert pronouns['four_genuine_captain_states_no_actor_ID_replacement']
    assert pronouns['producer_sha256']==sha(Path('scripts/probe_battle_boarding_pronoun_v943.py').read_bytes())
    assert [r['actor_ID'] for r in pronouns['all25_current_and_clean_parser_control_cases']]==list(range(25))
    for r in pronouns['all25_current_and_clean_parser_control_cases']:
        assert len(r['variants'])==2 and all(v['source_output_guards_and_ABI_pass'] for v in r['variants'])"""
    module=rendered('dk4tool/patch/battle_survey_lookout_editorial.py','dk4tool/patch/battle_sails_boarding_editorial.py',[
        ('Complete24 battle Survey/Lookout','Complete24 battle SailHandling/Boarding'),('battle_survey_lookout','battle_sails_boarding'),
        ('from dk4tool.patch.battle_bridge_editorial import current_entries as previous_entries','from dk4tool.patch.battle_survey_lookout_editorial import current_entries as previous_entries'),
        ('battle_sails_boarding_layout_v936','battle_sails_boarding_layout_v945'),('range(1709,1733)','range(1733,1757)'),
        (parent.SOURCE_COMMON,packet['COMMON_sha256']),(parent.SOURCE_ARM,packet['ARM9_sha256']),
        ('deck-battle-survey-lookout-visible-v1','deck-battle-sails-boarding-visible-v1'),('dk4-battle-survey-lookout-editorial-v1','dk4-battle-sails-boarding-editorial-v1'),
        ('role in (3,1)','role in (0,7)'),('{3:1499,1:1511}','{0:1523,7:1535}'),('{3:1709,1:1721}','{0:1733,7:1745}'),
        ('complete_measurement_and_boarding_sniping_and_all_source_words_pass','complete_windward_mast_coordination_IC_I_duel_and_all_source_words_pass'),
        (old_supplement,new_supplement),('no_Sera_special_role15_override_for_roles3_or1','no_Sera_special_role15_override_for_roles0_or7'),
        ("        authored[n]=compiled(row)","        assert row['source_native_macros']==(['IC'] if n==1747 else [])\n        authored[n]=compiled(row)")])
    audit=rendered('scripts/audit_battle_survey_lookout_native_v938.py','scripts/audit_battle_sails_boarding_native_v947.py',[
        ('battle_survey_lookout','battle_sails_boarding'),('battle_sails_boarding_layout_v936','battle_sails_boarding_layout_v945'),('probe_battle_sails_boarding_fonts_v936','probe_battle_sails_boarding_fonts_v945'),('deck-battle-survey-lookout-visible-v1','deck-battle-sails-boarding-visible-v1'),('Battle Survey/Lookout native-consumer audit','Battle SailHandling/Boarding native-consumer audit')])
    ROOT.mkdir(parents=True,exist_ok=True);font_path=Path('work/analysis/battle_sails_boarding_v945/native_font_proof.json');fonts=read(font_path)
    assert fonts['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and tuple(c['message_id'] for c in fonts['cases'])==IDS
    for case in fonts['cases']:assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    visual=Path('work/analysis/battle_sails_boarding_v945/visual_review.json');assert not visual.exists() and not PRODUCTION.exists()
    save(visual,{'native_font_proof':str(font_path),'native_font_proof_sha256':sha(font_path.read_bytes()),'review_sheet':fonts['review_sheet'],'review_sheet_sha256':fonts['review_sheet_sha256'],'all24_previews_visually_reviewed':True,'native_IDs':list(IDS),'visual_review_pending':False,
        'findings':'All24 full native body previews reviewed. Complete words/letters/punctuation start at x0 inside216x36. Conditional evasion1736 has a complete35cell continuation;drill1742 has34cell first row;IC1747 has complete ASCII I and hand-to-hand continuation after17cell first row;feast1751 and three-row fewer-casualty duel1754 are intact. No manual alignment,padding gaps,stray text,word splits,edge-letter loss or extra pages. Actual panels/normal returns remain required.','CPU_only_font_scope_no_actual_gameplay_credit':True,'full_goal_complete':False})
    doc=deepcopy(read(MANUSCRIPT));doc.update(reviewed_research_manuscript=str(MANUSCRIPT),reviewed_research_manuscript_sha256=sha(MANUSCRIPT.read_bytes()),formatting_review_pending=False,review_gates=['source','context','localization','naturalness','formatting'],status='24-source-prose-native-font-and-visual-reviewed-registered-release-and-actual-pending')
    for key,path in [('native_font_proof',font_path),('visual_review_proof',visual)]:doc[key]=str(path);doc[key+'_sha256']=sha(path.read_bytes())
    for row in doc['records']:row['review']['formatting']=True
    save(PRODUCTION,doc);provenance=[]
    for source,target,before,text in (module,audit):
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==before
        provenance.append({'source':str(source),'source_before_sha256':sha(before),'source_after_sha256':sha(source.read_bytes()),'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    save(ROOT/'native_successor_provenance.json',{'files':provenance,'all_source_hashes_unchanged':True,'all_successor_replacements_preflighted_before_output':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('24 previews reviewed;production manuscript and strict SailHandling/Boarding module/auditor created.',flush=True)
if __name__=='__main__':main()
