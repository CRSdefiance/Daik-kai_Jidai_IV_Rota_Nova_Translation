"""Record25 reviewed previews and create source-preserving native successors."""

from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_battle_cooking_livestock_prose_v907 import MANUSCRIPT,IDS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_cooking_livestock_v910')
PRODUCTION=Path('translations/battle_cooking_livestock_editorial_manuscript_v2.json')


def replace(text,old,new):
    assert old in text,old
    return text.replace(old,new)


def successor(source,target,changes,provenance):
    source,target=Path(source),Path(target)
    assert not target.exists()
    before=source.read_bytes();text=source.read_text(encoding='utf-8')
    for old,new in changes:text=replace(text,old,new)
    with target.open('x',encoding='utf-8') as f:f.write(text)
    assert source.read_bytes()==before
    provenance.append({'source':str(source),'source_before_sha256':sha(before),'source_after_sha256':sha(source.read_bytes()),
        'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    font_path=Path('work/analysis/battle_cooking_livestock_v908/native_font_proof.json');fonts=read(font_path)
    assert fonts['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert tuple(c['message_id'] for c in fonts['cases'])==IDS
    for c in fonts['cases']:assert sha(Path(c['preview']).read_bytes())==c['preview_sha256']
    visual=Path('work/analysis/battle_cooking_livestock_v908/visual_review.json')
    assert not visual.exists() and not PRODUCTION.exists()
    save(visual,{'native_font_proof':str(font_path),'native_font_proof_sha256':sha(font_path.read_bytes()),
        'review_sheet':fonts['review_sheet'],'review_sheet_sha256':fonts['review_sheet_sha256'],
        'all25_previews_visually_reviewed':True,'native_IDs':list(IDS),'visual_review_pending':False,
        'findings':'All25 native body previews reviewed. Every row begins at x0;all complete words and punctuation fit216x36 with no split words,padding gaps,stray text or extra pages. Initial I and final exclamation1639,complete Sera1632,first-person cooking1629 and second-row I1634 are intact. These are CPU-only font proofs;actual scenes and normal transitions remain required.',
        'CPU_only_font_scope_no_actual_gameplay_credit':True,'full_goal_complete':False})
    doc=deepcopy(read(MANUSCRIPT));doc['reviewed_research_manuscript']=str(MANUSCRIPT)
    doc['reviewed_research_manuscript_sha256']=sha(MANUSCRIPT.read_bytes())
    for key,p in [('native_font_proof',font_path),('visual_review_proof',visual)]:doc[key]=str(p);doc[key+'_sha256']=sha(p.read_bytes())
    doc['formatting_review_pending']=False;doc['review_gates']=['source','context','localization','naturalness','formatting']
    doc['status']='25-source-prose-native-font-and-visual-reviewed-registered-release-and-actual-pending'
    for row in doc['records']:row['review']['formatting']=True
    save(PRODUCTION,doc)
    provenance=[]
    successor('dk4tool/patch/battle_repair_medical_editorial.py','dk4tool/patch/battle_cooking_livestock_editorial.py',[
        ('Complete24 gunnery/deck comments','Complete25 battle cooking/livestock comments'),
        ('from dk4tool.patch.battle_personal_editorial import current_entries as previous_entries','from dk4tool.patch.battle_repair_medical_editorial import current_entries as previous_entries'),
        ('battle_repair_medical_layout_v902','battle_cooking_livestock_layout_v908'),
        ('battle_repair_medical_editorial','battle_cooking_livestock_editorial'),
        ('from dk4tool.patch.battle_cooking_livestock_editorial import current_entries as previous_entries','from dk4tool.patch.battle_repair_medical_editorial import current_entries as previous_entries'),
        ('range(1596,1620)','range(1620,1645)'),
        ('4168b52812ce30b8d03ccb6fe0f9df8b1caff57071c477f5a0962a1ea3fae135','00f2b25402b22003d051901e5102ad0ff3c6a13c3bc7f737bc6d4e069438ab77'),
        ('1c2382455732761a6bb569bfb89ffe9afacefe133d111147dd62c75cffad59bd','32977c36c7035ae3d3c94176c6e0faf51c1263cf52b166e3f6ad983d59cba7a7'),
        ('deck-battle-repair-medical-visible-v1','deck-battle-cooking-livestock-visible-v1'),
        ('dk4-battle-repair-medical-editorial-v1','dk4-battle-cooking-livestock-editorial-v1'),
        ('all3644_other_message_strings_exact','all3643_other_message_strings_exact'),
        ("'native_pronoun_proof')","'ordinary_context_supplement')"),
        ('role in (13,14)','role in (15,17)'),
        ('first=(1386 if role==13 else 1398)', 'first=(1410 if role==15 else 1423)'),
        ('else (1596 if role==13 else 1608)','else (1620 if role==15 else 1633)'),
        ("        assert r['selected_message_ID']==first+suffix", "        expected=(1422 if r['case']=='main_ordinary_working_control' else 1632) if role==15 and r['actor_ID']==24 else first+suffix\n        assert r['selected_message_ID']==expected\n        assert r['Sera_specific_Galley_override_executed']==(role==15 and r['actor_ID']==24)"),
        ("    terms=read(doc['native_pronoun_proof']);assert terms['IC_is_first_person_not_actor_name']\n    assert terms['source1610_means_I_am_here_so_do_not_worry']\n    assert len(terms['all25_current_and_clean_parser_control_cases'])==25\n    assert terms['source1610_hex']==next(r['source_hex'] for r in doc['records'] if r['message_id']==1610)",
         "    supplement=read(doc['ordinary_context_supplement'])\n    assert supplement['candidate_sha256']==doc['current_ROM_sha256']\n    assert supplement['pig_grooming_interpretation_supported_by1424_and1636']\n    assert supplement['first_person_pig_protest_supported_by1429_and_source_oira1639']\n    assert context['Sera_role15_battle1632_and_ordinary1422_overrides_proved']\n    assert context['additional_original_mood_response_control']['selected_message_ID']==1833\n    assert sum(r['Sera_specific_Galley_override_executed'] for r in cases)==3"),
        ("len(fonts['cases'])==24","len(fonts['cases'])==25"),
        ("len(audit['records'])==24","len(audit['records'])==25"),('all24','all25'),
        ('complete_ASCII_initial_I1610_and_all_source_words_pass','complete_ASCII_initial_I1639_Sera1632_and_all_source_words_pass')],provenance)
    successor('scripts/audit_battle_repair_medical_native_v904.py','scripts/audit_battle_cooking_livestock_native_v910.py',[
        ('battle_repair_medical','battle_cooking_livestock'),('battle_cooking_livestock_layout_v902','battle_cooking_livestock_layout_v908'),
        ('probe_battle_cooking_livestock_fonts_v902','probe_battle_cooking_livestock_fonts_v908'),
        ('deck-battle-repair-medical-visible-v1','deck-battle-cooking-livestock-visible-v1'),
        ('all24','all25'),('==24','==25'),('24 records','25 records'),
        ('Battle repair and medical native-consumer audit','Battle cooking and livestock native-consumer audit')],provenance)
    module=Path('dk4tool/patch/battle_cooking_livestock_editorial.py')
    text=module.read_text(encoding='utf-8')
    assert "r['actor_ID']==24" in text and "r['actor_ID']==25" not in text
    assert 'native_pronoun_proof' not in text and 'source1610' not in text
    save(ROOT/'native_successor_provenance.json',{'files':provenance,'all_source_hashes_unchanged':True,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print('25 native previews reviewed;production manuscript and strict source-preserving module/auditor created.',flush=True)


if __name__=='__main__':main()
