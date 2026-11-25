"""Replace one live-noticed stiff retention while preserving the source stammer,food enthusiasm andsea acceptance."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

PARENT=Path('translations/rafael_B81_B84_contextual_editorial_manuscript_v1.json')
OUTPUT=Path('translations/rafael_B81_B84_contextual_editorial_manuscript_v2.json')
ROOT=Path('work/analysis/Rafael_Emilio_food_acceptance_20261105')
IDENT='DK4_MES_B81_R0220'

if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=load(PARENT);original=deepcopy(doc);row=next(r for r in doc['records'] if r['id']==IDENT)
    assert row['decision']=='retention' and row['english']=='Lots of every kind? Then count me in! Sea or anywhere!'
    assert row['source_Japanese']=='そ、そおかあ\nいろいろが、いっぱいかあ\nじゃあいく！\u3000うみでもどこでも！'
    row.update(english="R-really? All kinds, and lots of it? Then I'm in! I'll go anywhere, even to sea!",decision='revision',retention_reason=None,
        source_meaning='Stammering,Emilio reacts to plenty of different foods,then agrees to go—even to sea,oranywhere.',
        finding='Live complete-exchange review found Sea or anywhere! stiff despite the earlier retention. Restore the source stammer,retain the plentiful variety of food,andmake his eager acceptance of even the sea natural. The preceding food discussion supplies the collective it;no new relationship,rank,destination orguaranteed food supply is asserted.',
        prior_macro_normalized_comparison=None,earlier_retention_superseded_by_live_contextual_finding=True,
        prior_reviewed_wording=original['records'][next(i for i,r in enumerate(original['records']) if r['id']==IDENT)]['english'])
    row['localization_note']=row['finding'];row['planned_English_markup']='{SPEAKER:0E}'+row['english']
    row['review']=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
    doc.update(proposed_revisions=174,wording_retentions=156,previous_manuscript=str(PARENT),previous_manuscript_sha256=sha(PARENT.read_bytes()),
        single_live_contextual_prose_revision_ID=IDENT,all_other_329_reviewed_prose_objects_unchanged=True,new_credit=0)
    assert len(doc['records'])==330 and sum(r['decision']=='revision' for r in doc['records'])==174 and sum(r['decision']=='retention' for r in doc['records'])==156
    assert all(a==b for a,b in zip(original['records'],doc['records'],strict=True) if a['id']!=IDENT)
    ROOT.mkdir();save(OUTPUT,doc)
    subset=deepcopy(doc);subset.update(records=[row],blocks=[81],physical_speech_objects=1,ordinary_speech_objects=1,FE_speech_objects=0,
        typed_choice_objects=0,typed_choice_commands=0,subset_of=str(OUTPUT),subset_of_sha256=sha(OUTPUT.read_bytes()),
        original_full_manuscript=str(PARENT),original_full_manuscript_sha256=sha(PARENT.read_bytes()))
    save(ROOT/'fresh_manuscript_v2.json',subset);save(ROOT/'preferences_v2.json',dict(records={}))
    save(ROOT/'source_context_andretention_reconsideration_v2.json',dict(id=IDENT,source_reference=row['source_reference'],current_reference=row['current_reference'],
        exact_Japanese=row['source_Japanese'],current_English=row['current_English'],previous_retention=row['prior_reviewed_wording'],revised_English=row['english'],finding=row['finding'],
        preceding_full_exchange_ids=['DK4_MES_B81_R0206','DK4_MES_B81_R0209','DK4_MES_B81_R0213','DK4_MES_B81_R0216'],following_full_exchange_ids=['DK4_MES_B81_R0224','DK4_MES_B81_R0228','DK4_MES_B81_R0231'],
        original_51_speech_full_source_and49_speech_actual_branch_reviews_retained=True,
        every_other_reviewed_prose_object_unchanged=True,fresh_native_stored_andfocused_actual_pending=True,new_credit=0))
    print('Refined one stiff Emilio retention from the full live exchange;330 total now174 revisions/156 retentions. Fresh page checks pending.')
