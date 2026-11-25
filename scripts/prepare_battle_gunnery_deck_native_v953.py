"""Bind24 native previews and guarded Gunnery/DeckCleaning successors."""
import ast
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch import battle_sails_boarding_editorial as parent
from scripts.prepare_battle_gunnery_deck_prose_v951 import MANUSCRIPT,IDS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/battle_gunnery_deck_v954')
PRODUCTION=Path('translations/battle_gunnery_deck_editorial_manuscript_v2.json')
def rendered(source,target,pairs):
    source,target=Path(source),Path(target);before=source.read_bytes();text=source.read_text(encoding='utf-8');assert not target.exists()
    for old,new in pairs:
        assert old in text,(source,old)
        text=text.replace(old,new)
    ast.parse(text)
    return source,target,before,text

def main():
    packet=read('work/analysis/battle_gunnery_deck_v950/source_context_packet.json')
    source=Path('dk4tool/patch/battle_sails_boarding_editorial.py').read_text()
    start=source.index("    assert supplement['established_roles']");end=source.index('    for name,digest in supplement',start)
    old_supplement=source[start:end]
    new_supplement="""    assert supplement['established_roles']=={'Gunnery':8,'DeckCleaning':2}
    assert supplement['Aim_and_Gun_Batteries_terms_source_bound']
    assert supplement['source1759_says_more_firing_not_independently_measured_shot_formula']
    assert supplement['source1768_loading_order_not_already_loaded_state']
    assert supplement['source1770_conditional_deference_not_boarding_order']
    assert supplement['no_IC_native_macro_in_selected_Japanese']
    help_rows={r['topic_id']:r for r in supplement['reference_help']}
    assert {126,129,173}<=set(help_rows)
    assert help_rows[129]['heading']=='Gun Batteries' and help_rows[173]['heading']=='Aim'
"""
    module=rendered('dk4tool/patch/battle_sails_boarding_editorial.py','dk4tool/patch/battle_gunnery_deck_editorial.py',[
        ('Complete24 battle SailHandling/Boarding','Complete24 battle Gunnery/DeckCleaning'),('battle_sails_boarding','battle_gunnery_deck'),
        ('from dk4tool.patch.battle_survey_lookout_editorial import current_entries as previous_entries','from dk4tool.patch.battle_sails_boarding_editorial import current_entries as previous_entries'),
        ('battle_gunnery_deck_layout_v945','battle_gunnery_deck_layout_v952'),('range(1733,1757)','range(1757,1781)'),
        (parent.SOURCE_COMMON,packet['COMMON_sha256']),(parent.SOURCE_ARM,packet['ARM9_sha256']),
        ('deck-battle-sails-boarding-visible-v1','deck-battle-gunnery-deck-visible-v1'),('dk4-battle-sails-boarding-editorial-v1','dk4-battle-gunnery-deck-editorial-v1'),
        ('role in (0,7)','role in (8,2)'),('{0:1523,7:1535}','{8:1547,2:1559}'),('{0:1733,7:1745}','{8:1757,2:1769}'),
        ('complete_windward_mast_coordination_IC_I_duel_and_all_source_words_pass','complete_Aim_loading_orders_personal_cleaning_and_all_source_words_pass'),
        (old_supplement,new_supplement),('no_Sera_special_role15_override_for_roles0_or7','no_Sera_special_role15_override_for_roles8_or2'),
        ("row['source_native_macros']==(['IC'] if n==1747 else [])","row['source_native_macros']==[]")])
    audit=rendered('scripts/audit_battle_sails_boarding_native_v947.py','scripts/audit_battle_gunnery_deck_native_v954.py',[
        ('battle_sails_boarding','battle_gunnery_deck'),('battle_gunnery_deck_layout_v945','battle_gunnery_deck_layout_v952'),('probe_battle_gunnery_deck_fonts_v945','probe_battle_gunnery_deck_fonts_v952'),('deck-battle-sails-boarding-visible-v1','deck-battle-gunnery-deck-visible-v1'),('Battle SailHandling/Boarding native-consumer audit','Battle Gunnery/DeckCleaning native-consumer audit')])
    ROOT.mkdir(parents=True,exist_ok=True);font_path=Path('work/analysis/battle_gunnery_deck_v952/native_font_proof.json');fonts=read(font_path)
    assert fonts['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and tuple(c['message_id'] for c in fonts['cases'])==IDS
    for case in fonts['cases']:assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    visual=Path('work/analysis/battle_gunnery_deck_v952/visual_review.json');assert not visual.exists() and not PRODUCTION.exists()
    save(visual,{'native_font_proof':str(font_path),'native_font_proof_sha256':sha(font_path.read_bytes()),'review_sheet':fonts['review_sheet'],'review_sheet_sha256':fonts['review_sheet_sha256'],'all24_previews_visually_reviewed':True,'native_IDs':list(IDS),'visual_review_pending':False,
        'findings':'All24 full native previews reviewed. Complete words/letters/punctuation start at x0 inside216x36. Aim1759,retained1776 and first row1778 fill36cells. Conditional orders1770 have35cell first row;personal I1775 and three-row Lil1779 are intact. Phrase review keeps Ive built and until the boarding together. No authored alignment,padding gaps,stray text,word splits,missing edge letters or extra pages. Actual panels/normal returns remain required.','CPU_only_font_scope_no_actual_gameplay_credit':True,'full_goal_complete':False})
    doc=deepcopy(read(MANUSCRIPT));doc.update(reviewed_research_manuscript=str(MANUSCRIPT),reviewed_research_manuscript_sha256=sha(MANUSCRIPT.read_bytes()),formatting_review_pending=False,review_gates=['source','context','localization','naturalness','formatting'],status='24-source-prose-native-font-and-visual-reviewed-registered-release-and-actual-pending')
    for key,path in [('native_font_proof',font_path),('visual_review_proof',visual)]:doc[key]=str(path);doc[key+'_sha256']=sha(path.read_bytes())
    for row in doc['records']:row['review']['formatting']=True
    save(PRODUCTION,doc);provenance=[]
    for source,target,before,text in (module,audit):
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==before
        provenance.append({'source':str(source),'source_before_sha256':sha(before),'source_after_sha256':sha(source.read_bytes()),'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    save(ROOT/'native_successor_provenance.json',{'files':provenance,'all_source_hashes_unchanged':True,'all_successor_replacements_preflighted_before_output':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('24 previews reviewed;production manuscript and strict Gunnery/DeckCleaning module/auditor created.',flush=True)
if __name__=='__main__':main()
