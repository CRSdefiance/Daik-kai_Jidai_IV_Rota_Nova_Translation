"""Record24 reviewed native previews;create strict source-preserving successors."""

from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_battle_chapel_planning_prose_v913 import MANUSCRIPT,IDS
from scripts.prepare_battle_cooking_livestock_native_v909 import successor
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_chapel_planning_v916')
PRODUCTION=Path('translations/battle_chapel_planning_editorial_manuscript_v2.json')


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    font_path=Path('work/analysis/battle_chapel_planning_v914/native_font_proof.json');fonts=read(font_path)
    assert fonts['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert tuple(c['message_id'] for c in fonts['cases'])==IDS
    for c in fonts['cases']:assert sha(Path(c['preview']).read_bytes())==c['preview_sha256']
    visual=Path('work/analysis/battle_chapel_planning_v914/visual_review.json')
    assert not visual.exists() and not PRODUCTION.exists()
    save(visual,{'native_font_proof':str(font_path),'native_font_proof_sha256':sha(font_path.read_bytes()),
        'review_sheet':fonts['review_sheet'],'review_sheet_sha256':fonts['review_sheet_sha256'],
        'all24_previews_visually_reviewed':True,'native_IDs':list(IDS),'visual_review_pending':False,
        'findings':'All24 complete native body previews reviewed. Uniform x0 row starts,complete letters and punctuation,no split words or padding gaps,and all ink inside216x36. Claudio1653 continuation after25 characters,initial ASCII I1648,all three1663/1667 rows and full35-character Marine Barracks1666 continuation are intact. Actual panels and normal transitions remain required.',
        'CPU_only_font_scope_no_actual_gameplay_credit':True,'full_goal_complete':False})
    doc=deepcopy(read(MANUSCRIPT));doc['reviewed_research_manuscript']=str(MANUSCRIPT)
    doc['reviewed_research_manuscript_sha256']=sha(MANUSCRIPT.read_bytes())
    for key,p in [('native_font_proof',font_path),('visual_review_proof',visual)]:doc[key]=str(p);doc[key+'_sha256']=sha(p.read_bytes())
    doc['formatting_review_pending']=False;doc['review_gates']=['source','context','localization','naturalness','formatting']
    doc['status']='24-source-prose-native-font-and-visual-reviewed-registered-release-and-actual-pending'
    for row in doc['records']:row['review']['formatting']=True
    save(PRODUCTION,doc);provenance=[]
    successor('dk4tool/patch/battle_cooking_livestock_editorial.py','dk4tool/patch/battle_chapel_planning_editorial.py',[
        ('Complete25 battle cooking/livestock','Complete24 battle Chapel/Planning'),
        ('battle_cooking_livestock_editorial','battle_chapel_planning_editorial'),
        ('battle_chapel_planning_editorial_release_v2.json','battle_chapel_planning_editorial_release_v1.json'),
        ('from dk4tool.patch.battle_repair_medical_editorial import current_entries as previous_entries','from dk4tool.patch.battle_cooking_livestock_editorial import current_entries as previous_entries'),
        ('battle_cooking_livestock_layout_v908','battle_chapel_planning_layout_v914'),
        ('range(1620,1645)','range(1645,1669)'),
        ('00f2b25402b22003d051901e5102ad0ff3c6a13c3bc7f737bc6d4e069438ab77','edd4ac2e494d4d829a2a68d0c36f6e182b173c0f55d7b22520bee4bcdb8e43b8'),
        ('32977c36c7035ae3d3c94176c6e0faf51c1263cf52b166e3f6ad983d59cba7a7','b0ed8242f75648ef1dd5dc62358436d754d466612365e1088ef4b55f5c7c69f2'),
        ('deck-battle-cooking-livestock-visible-v1','deck-battle-chapel-planning-visible-v1'),
        ('dk4-battle-cooking-livestock-editorial-v1','dk4-battle-chapel-planning-editorial-v1'),
        ('all3643_other_message_strings_exact','all3644_other_message_strings_exact'),
        ('role in (15,17)','role in (18,19)'),
        ('first=(1410 if role==15 else 1423)','first=(1435 if role==18 else 1447)'),
        ('else (1620 if role==15 else 1633)','else (1645 if role==18 else 1657)'),
        ("        expected=(1422 if r['case']=='main_ordinary_working_control' else 1632) if role==15 and r['actor_ID']==24 else first+suffix\n        assert r['selected_message_ID']==expected\n        assert r['Sera_specific_Galley_override_executed']==(role==15 and r['actor_ID']==24)",
         "        assert r['selected_message_ID']==first+suffix"),
        ("len(fonts['cases'])==25","len(fonts['cases'])==24"),
        ("len(audit['records'])==25","len(audit['records'])==24"),('all25','all24'),
        ('complete_ASCII_initial_I1639_Sera1632_and_all_source_words_pass','complete_Claudio1653_Marine_Barracks1666_and_all_source_words_pass'),
        ("    assert supplement['pig_grooming_interpretation_supported_by1424_and1636']\n    assert supplement['first_person_pig_protest_supported_by1429_and_source_oira1639']\n    assert context['Sera_role15_battle1632_and_ordinary1422_overrides_proved']\n    assert context['additional_original_mood_response_control']['selected_message_ID']==1833\n    assert sum(r['Sera_specific_Galley_override_executed'] for r in cases)==3",
         "    assert supplement['Claudio_nickname_expansion_consistent_with_completed1409']\n    assert supplement['casualty_loss_1652_is_documented_contextual_inference_not_native_casualty_count']\n    assert supplement['native_ARM9_Schemes_caption_hex']=='536368656d657300'\n    for name,digest in supplement['established_term_documents'].items():assert sha(Path(name).read_bytes())==digest\n    assert context['no_Sera_special_role15_override_for_roles18_or19']")],provenance)
    successor('scripts/audit_battle_cooking_livestock_native_v910.py','scripts/audit_battle_chapel_planning_native_v916.py',[
        ('battle_cooking_livestock','battle_chapel_planning'),('battle_chapel_planning_layout_v908','battle_chapel_planning_layout_v914'),
        ('probe_battle_chapel_planning_fonts_v908','probe_battle_chapel_planning_fonts_v914'),
        ('deck-battle-cooking-livestock-visible-v1','deck-battle-chapel-planning-visible-v1'),
        ('all25','all24'),('==25','==24'),('25 records','24 records'),
        ('Battle cooking and livestock native-consumer audit','Battle Chapel and Planning native-consumer audit')],provenance)
    save(ROOT/'native_successor_provenance.json',{'files':provenance,'all_source_hashes_unchanged':True,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print('24 native previews reviewed;production manuscript and strict native module/auditor created.',flush=True)


if __name__=='__main__':main()
