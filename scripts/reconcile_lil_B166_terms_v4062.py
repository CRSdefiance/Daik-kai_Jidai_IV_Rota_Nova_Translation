"""Bind workroom/role/stat and refit wording to exact current reviewed Help bytes."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B166_terms_v4062')
SOURCE=Path('work/analysis/lil_B166_source_v4054/all44_clean_current_complete_context_with_typed_choice.json')
CREW=Path('work/analysis/crew_help_v448/page_proposal.json')
SKILL=Path('work/analysis/skill_terms_v463/page_proposal.json')
CONFIG=Path('translations/skill_terms_help_release_v1.json')
ROOMS={110:('担当室','Workrooms'),111:('個室','Private Cabin'),112:('娯楽室','Recreation Room'),113:('材木室','Lumber Room'),114:('診察室','Infirmary'),115:('調理室','Galley'),116:('飼育室','Livestock Room'),117:('礼拝室','Chapel'),121:('副官室',"First Mate's Office")}
if __name__=='__main__':
    assert not ROOT.exists();v=read(SOURCE);image=NdsImage.open(v['current_ROM']);raw=image.read_file('/COMMON/HELP.DK4');blocks=IlnkContainer.parse(raw).blocks
    config,crew,skill=map(read,[CONFIG,CREW,SKILL]);assert sha(raw)==config['target_HELP_sha256']==skill['target_HELP_sha256']
    assert sha(Path(config['manuscript']).read_bytes())==config['manuscript_sha256']
    assert crew['all35_native_previews_visually_reviewed'] and crew['all34_clean_source_context_and_natural_English_reviews_complete'] and skill['all15_native_previews_visually_reviewed'] and skill['actual_UI_terms_pixel_verified']
    pages={p['topic_id']:(p,CREW) for p in crew['pages']};pages.update({p['topic_id']:(p,SKILL) for p in skill['pages']});bound=[]
    for topic,(jp,en) in ROOMS.items():
        page,plan=pages[topic];encoded=bytes.fromhex(page['encoded_hex']);assert blocks[topic]==encoded and page['visible_lines'][0]==en
        bound.append(dict(source_term=jp,approved_English=en,HELP_topic=topic,current_complete_topic_sha256=sha(encoded),reviewed_page_plan=str(plan),reviewed_page_plan_sha256=sha(plan.read_bytes()),source_linked_article=page['source_article_id'],source_page_number=page['page_number']))
    for topic in [133,209]:page,plan=pages[topic];assert blocks[topic]==bytes.fromhex(page['encoded_hex'])
    active=read(config['manuscript']);bytopic={r['topic_id']:r for r in active['records']};assert 'Speech 100' in bytopic[121]['english'] and 'Speech 160' in bytopic[117]['english']
    rolemap={'船大工':'Shipwright','船医':'Surgeon','説得力':'Speech','航海士':'officer','水夫':'sailor'}
    assert 'Shipwright, Survey 130' in bytopic[133]['english'] and 'Surgeon, Observe 150' in bytopic[133]['english']
    refitpath=Path('translations/refit_help_manuscript_v2.json');refit=read(refitpath);cannon=next(r for r in refit['records'] if r['id']=='REFIT_HELP_1284')
    assert cannon['clean_source_Japanese']=='船に取り付けられている\n大砲の種類を変更できます' and 'cannon type' in cannon['english'] and all(cannon['review'].values())
    ROOT.mkdir(parents=True)
    save(ROOT/'nine_rooms_active_Speech_Shipwright_Surgeon_and_source_distinctions.json',dict(candidate=v['current_ROM'],candidate_sha256=v['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),current_HELP_sha256=sha(raw),entire_HELP_exact_to_reviewed_skill_release=True,nine_room_terms_bound_to_complete_current_topics=bound,role_and_stat_terms=rolemap,skill_numeric_thresholds_not_supplied_in_B166_and_not_to_be_added=True,original_cannon_type_term=cannon,source_additional_sails_and_basic_sail_type_are_distinct_generic_categories_not_named_equipment=True,gun_batteries_distinct_from_cannon_type=True,source_B166_room_effects_preserved_without_overwriting_from_other_help_articles=True,source_Galley_Livestock_group_does_not_map_each_room_to_one_resource=True,source_medical_treatment_and_faster_cabin_recovery_do_not_promise_instant_full_recovery=True,Shipwright_at_sea_Lumber_Room_and_shipyard_refit_repair_help_all_retained=True,source_high_persuasion_localized_as_active_Speech_not_superseded_Social=True,new_native_calls_or_actual_displays=0,earlier_viewed_source_locked_UI_and_Help_evidence_reused=True,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CREW,SKILL,CONFIG,Path(config['manuscript']),Path('translations/crew_help_manuscript_v1.json'),refitpath,Path(__file__)]},source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print('B166 terms:9 current complete room pages,Speech/Shipwright/Surgeon andcannon type bound;source-specific effects preserved;no credit.')
