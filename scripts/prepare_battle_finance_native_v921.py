"""Bind12 reviewed native previews and create source-preserving Finance successors."""

from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_battle_finance_prose_v919 import MANUSCRIPT,IDS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_finance_v922')
PRODUCTION=Path('translations/battle_finance_editorial_manuscript_v2.json')


def rendered(source,target,pairs):
    source,target=Path(source),Path(target);before=source.read_bytes();text=source.read_text(encoding='utf-8')
    assert not target.exists()
    for old,new in pairs:
        assert old in text,(source,old)
        text=text.replace(old,new)
    return source,target,before,text


def main():
    module=rendered('dk4tool/patch/battle_chapel_planning_editorial.py','dk4tool/patch/battle_finance_editorial.py',[
        ('Complete24 battle Chapel/Planning','Complete12 battle Finance'),
        ('battle_chapel_planning_editorial','battle_finance_editorial'),
        ('from dk4tool.patch.battle_cooking_livestock_editorial import current_entries as previous_entries','from dk4tool.patch.battle_chapel_planning_editorial import current_entries as previous_entries'),
        ('battle_chapel_planning_layout_v914','battle_finance_layout_v920'),('range(1645,1669)','range(1669,1681)'),
        ('edd4ac2e494d4d829a2a68d0c36f6e182b173c0f55d7b22520bee4bcdb8e43b8','95f7eec22db72fccab6e4395919e2732d1dc9a129254f2b21edd947a40cde7a4'),
        ('b0ed8242f75648ef1dd5dc62358436d754d466612365e1088ef4b55f5c7c69f2','0f8356bac78ea70be55db653ab1d42f1022ceff051d6b0463d622eb86d79596c'),
        ('deck-battle-chapel-planning-visible-v1','deck-battle-finance-visible-v1'),
        ('dk4-battle-chapel-planning-editorial-v1','dk4-battle-finance-editorial-v1'),
        ('all3644_other_message_strings_exact','all3656_other_message_strings_exact'),
        ('all150_original_battle_helper_main_and_ordinary_control_selections','all75_original_battle_helper_main_and_ordinary_control_selections'),
        ('len(cases)==150','len(cases)==75'),('len(battle)==100 and len(ordinary)==50','len(battle)==50 and len(ordinary)==25'),
        ('role in (18,19)','role==20'),
        ("first=(1435 if role==18 else 1447) if r['case']=='main_ordinary_working_control' else (1645 if role==18 else 1657)",
         "first=1459 if r['case']=='main_ordinary_working_control' else 1669"),
        ("len(fonts['cases'])==24","len(fonts['cases'])==12"),("len(audit['records'])==24","len(audit['records'])==12"),
        ('all24','all12'),('complete_Claudio1653_Marine_Barracks1666_and_all_source_words_pass','complete_financial_report1670_initial_I1675_and_all_source_words_pass'),
        ("    assert supplement['Claudio_nickname_expansion_consistent_with_completed1409']\n    assert supplement['casualty_loss_1652_is_documented_contextual_inference_not_native_casualty_count']\n    assert supplement['native_ARM9_Schemes_caption_hex']=='536368656d657300'",
         "    assert supplement['financial_report1670_has_no_invented_reporting_period']\n    assert supplement['explicit_this_month1674_preserved']\n    assert supplement['sea_battle_not_all_sailing_scope1671_1676_preserved']"),
        ('no_Sera_special_role15_override_for_roles18_or19','no_Sera_special_role15_override_for_role20')])
    audit=rendered('scripts/audit_battle_chapel_planning_native_v916.py','scripts/audit_battle_finance_native_v922.py',[
        ('battle_chapel_planning','battle_finance'),('battle_finance_layout_v914','battle_finance_layout_v920'),
        ('probe_battle_finance_fonts_v914','probe_battle_finance_fonts_v920'),
        ('deck-battle-chapel-planning-visible-v1','deck-battle-finance-visible-v1'),
        ('all150_original_battle_helper_main_and_ordinary_control_selections','all75_original_battle_helper_main_and_ordinary_control_selections'),
        ('==150','==75'),('all24','all12'),('==24','==12'),('24 records','12 records'),
        ('Battle Chapel and Planning native-consumer audit','Battle Finance native-consumer audit')])
    ROOT.mkdir(parents=True,exist_ok=True)
    font_path=Path('work/analysis/battle_finance_v920/native_font_proof.json');fonts=read(font_path)
    assert fonts['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert tuple(c['message_id'] for c in fonts['cases'])==IDS
    for case in fonts['cases']:assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    visual=Path('work/analysis/battle_finance_v920/visual_review.json')
    assert not visual.exists() and not PRODUCTION.exists()
    save(visual,{'native_font_proof':str(font_path),'native_font_proof_sha256':sha(font_path.read_bytes()),
        'review_sheet':fonts['review_sheet'],'review_sheet_sha256':fonts['review_sheet_sha256'],
        'all12_previews_visually_reviewed':True,'native_IDs':list(IDS),'visual_review_pending':False,
        'findings':'All12 native body previews reviewed. Every row starts at x0 with complete words/letters/punctuation inside216x36. The full three-row financial report1670,month/startle1674,initial I1675,and Purser\'s Office1679 are intact. No split words,padding gaps,stray text or extra pages. Actual panels and normal transitions remain required.',
        'CPU_only_font_scope_no_actual_gameplay_credit':True,'full_goal_complete':False})
    doc=deepcopy(read(MANUSCRIPT));doc['reviewed_research_manuscript']=str(MANUSCRIPT)
    doc['reviewed_research_manuscript_sha256']=sha(MANUSCRIPT.read_bytes())
    for key,path in [('native_font_proof',font_path),('visual_review_proof',visual)]:doc[key]=str(path);doc[key+'_sha256']=sha(path.read_bytes())
    doc['formatting_review_pending']=False;doc['review_gates']=['source','context','localization','naturalness','formatting']
    doc['status']='12-source-prose-native-font-and-visual-reviewed-registered-release-and-actual-pending'
    for row in doc['records']:row['review']['formatting']=True
    save(PRODUCTION,doc);provenance=[]
    for source,target,before,text in (module,audit):
        with target.open('x',encoding='utf-8') as stream:stream.write(text)
        assert source.read_bytes()==before
        provenance.append({'source':str(source),'source_before_sha256':sha(before),'source_after_sha256':sha(source.read_bytes()),
            'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    save(ROOT/'native_successor_provenance.json',{'files':provenance,'all_source_hashes_unchanged':True,
        'all_successor_replacements_preflighted_before_output':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('12 native previews reviewed;production manuscript and strict Finance module/auditor created.',flush=True)


if __name__=='__main__':main()
