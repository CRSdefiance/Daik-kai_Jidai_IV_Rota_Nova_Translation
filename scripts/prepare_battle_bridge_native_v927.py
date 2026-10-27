"""Bind28 reviewed native previews and create strictly guarded Bridge successors."""
import ast
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_battle_bridge_prose_v925 import MANUSCRIPT,IDS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/battle_bridge_v928')
PRODUCTION=Path('translations/battle_bridge_editorial_manuscript_v2.json')

def rendered(source,target,pairs):
    source,target=Path(source),Path(target);before=source.read_bytes();text=source.read_text(encoding='utf-8')
    assert not target.exists()
    for old,new in pairs:
        assert old in text,(source,old)
        text=text.replace(old,new)
    ast.parse(text)
    return source,target,before,text

def main():
    packet=read('work/analysis/battle_bridge_v924/source_context_packet.json')
    module=rendered('dk4tool/patch/battle_finance_editorial.py','dk4tool/patch/battle_bridge_editorial.py',[
        ('Complete12 battle Finance','Complete28 battle Bridge'),
        ('battle_finance','battle_bridge'),
        ('from dk4tool.patch.battle_chapel_planning_editorial import current_entries as previous_entries','from dk4tool.patch.battle_finance_editorial import current_entries as previous_entries'),
        ('battle_bridge_layout_v920','battle_bridge_layout_v926'),('range(1669,1681)','range(1681,1709)'),
        ('95f7eec22db72fccab6e4395919e2732d1dc9a129254f2b21edd947a40cde7a4',packet['COMMON_sha256']),
        ('0f8356bac78ea70be55db653ab1d42f1022ceff051d6b0463d622eb86d79596c',packet['ARM9_sha256']),
        ('deck-battle-finance-visible-v1','deck-battle-bridge-visible-v1'),
        ('dk4-battle-finance-editorial-v1','dk4-battle-bridge-editorial-v1'),
        ('all3656_other_message_strings_exact','all3640_other_message_strings_exact'),
        ('all75_original_battle_helper_main_and_ordinary_control_selections','all162_original_battle_helper_main_and_ordinary_control_selections'),
        ('len(cases)==75','len(cases)==162'),('len(battle)==50 and len(ordinary)==25','len(battle)==108 and len(ordinary)==54'),
        ("        role=r['source_role_type'];assert role==20\n        suffix=8+r['actor_ID'] if r['actor_ID']<4 else r['native_voice_class']\n        first=1459 if r['case']=='main_ordinary_working_control' else 1669",
         "        role=r['source_role_type'];assert role in (5,6,4)\n        if role==5:assert r['actor_ID']<4\n        suffix=(r['actor_ID'] if role==5 else 8+r['actor_ID']) if r['actor_ID']<4 else r['native_voice_class']\n        first={5:1471,6:1475,4:1487}[role] if r['case']=='main_ordinary_working_control' else {5:1681,6:1685,4:1697}[role]"),
        ("len(fonts['cases'])==12","len(fonts['cases'])==28"),("len(audit['records'])==12","len(audit['records'])==28"),
        ('all12','all28'),('complete_financial_report1670_initial_I1675_and_all_source_words_pass','complete_Xien_Camille_Gerhard_initial_I_and_all_source_words_pass'),
        ("    assert supplement['financial_report1670_has_no_invented_reporting_period']\n    assert supplement['explicit_this_month1674_preserved']\n    assert supplement['sea_battle_not_all_sailing_scope1671_1676_preserved']",
         "    assert supplement['Captain5_has_no_NPC_alternatives']\n    assert supplement['established_terms']=={'シエン':'Xien','ゲルハルト':'Gerhard','カミル':'Camille','副官':'First Mate','停戦':'truce'}\n    assert supplement['Xien_evidence']['ordinary_message1498_source_and_current']['message_id']==1498"),
        ("    assert context['no_Sera_special_role15_override_for_role20']",
         "    assert context['Captain5_null_NPC_tables_preserved_and_never_called_as_supported_alternatives']\n    assert context['source_activity0_working_not_activity1_separate_helper126A8']\n    assert all(r['actor_ID']<4 for r in cases if r['source_role_type']==5)")])
    audit=rendered('scripts/audit_battle_finance_native_v922.py','scripts/audit_battle_bridge_native_v928.py',[
        ('battle_finance','battle_bridge'),('battle_bridge_layout_v920','battle_bridge_layout_v926'),
        ('probe_battle_bridge_fonts_v920','probe_battle_bridge_fonts_v926'),
        ('deck-battle-finance-visible-v1','deck-battle-bridge-visible-v1'),
        ('all75_original_battle_helper_main_and_ordinary_control_selections','all162_original_battle_helper_main_and_ordinary_control_selections'),
        ('==75','==162'),('all12','all28'),('==12','==28'),('12 records','28 records'),
        ('Battle Finance native-consumer audit','Battle Bridge native-consumer audit')])
    ROOT.mkdir(parents=True,exist_ok=True)
    font_path=Path('work/analysis/battle_bridge_v926/native_font_proof.json');fonts=read(font_path)
    assert fonts['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert tuple(c['message_id'] for c in fonts['cases'])==IDS
    for case in fonts['cases']:assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    visual=Path('work/analysis/battle_bridge_v926/visual_review.json')
    assert not visual.exists() and not PRODUCTION.exists()
    save(visual,{'native_font_proof':str(font_path),'native_font_proof_sha256':sha(font_path.read_bytes()),
        'review_sheet':fonts['review_sheet'],'review_sheet_sha256':fonts['review_sheet_sha256'],
        'all28_previews_visually_reviewed':True,'native_IDs':list(IDS),'visual_review_pending':False,
        'findings':'All28 native body previews reviewed. Complete words,letters and punctuation start at x0 and fit216x36. Barrage1682 and Gerhard1706 use three full rows;Camille1683 begins with complete ASCII I;Xien1684 is intact;1704 fills36 cells on its second row. No alignment padding,stray text,split words,missing edge glyphs or extra pages. Actual panels and normal returns remain required.',
        'CPU_only_font_scope_no_actual_gameplay_credit':True,'full_goal_complete':False})
    doc=deepcopy(read(MANUSCRIPT));doc['reviewed_research_manuscript']=str(MANUSCRIPT)
    doc['reviewed_research_manuscript_sha256']=sha(MANUSCRIPT.read_bytes())
    for key,path in [('native_font_proof',font_path),('visual_review_proof',visual)]:doc[key]=str(path);doc[key+'_sha256']=sha(path.read_bytes())
    doc['formatting_review_pending']=False;doc['review_gates']=['source','context','localization','naturalness','formatting']
    doc['status']='28-source-prose-native-font-and-visual-reviewed-registered-release-and-actual-pending'
    for row in doc['records']:row['review']['formatting']=True
    save(PRODUCTION,doc);provenance=[]
    for source,target,before,text in (module,audit):
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==before
        provenance.append({'source':str(source),'source_before_sha256':sha(before),'source_after_sha256':sha(source.read_bytes()),'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    save(ROOT/'native_successor_provenance.json',{'files':provenance,'all_source_hashes_unchanged':True,'all_successor_replacements_preflighted_before_output':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('28 previews reviewed;production manuscript and strict Bridge module/auditor created.',flush=True)
if __name__=='__main__':main()
