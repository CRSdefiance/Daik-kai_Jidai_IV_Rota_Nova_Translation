"""Close one complete-exchange naturalness finding without reopening329 good decisions."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

PARENT=Path('translations/rafael_B81_B84_contextual_editorial_manuscript_v2.json')
OUTPUT=Path('translations/rafael_B81_B84_contextual_editorial_manuscript_v3.json')
ROOT=Path('work/analysis/Rafael_food_assurance_v3_20261105')
ID='DK4_MES_B81_R0216'

if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=load(PARENT);original=deepcopy(doc)
    row=next(r for r in doc['records'] if r['id']==ID)
    assert row['decision']=='revision' and row['english']=="That's right! All kinds of food. There must be!"
    assert row['source_Japanese']=='そうさ。いろんな食べ物があるんだよ\nきっとね'
    previous=row['english'];row['english']="That's right! There must be all kinds of food out there!"
    reason=('Reading the complete nine-speech food/recruitment exchange exposed the stranded There must be! '
        'as stiff. Join the assurance andits complement into one natural sentence;must expresses Rafael’s '
        'optimistic inference fromきっとね rather than certain firsthand knowledge. Out there follows '
        'his immediately preceding all-over-the-world proposal. Preserve the food hook andEmilio’s eager response;'
        'no new destination,relationship,rank orfood guarantee.')
    row.update(prior_reviewed_wording=previous,finding=reason,localization_note=reason,
        planned_English_markup='{SPEAKER:00}'+row['english'],live_exchange_naturalness_refinement=True)
    row['review']=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
    doc.update(previous_manuscript=str(PARENT),previous_manuscript_sha256=sha(PARENT.read_bytes()),
        single_live_contextual_prose_revision_ID=ID,all_other_329_reviewed_prose_objects_unchanged=True,new_credit=0)
    assert sum(r['decision']=='revision' for r in doc['records'])==174
    assert all(a==b for a,b in zip(original['records'],doc['records'],strict=True) if a['id']!=ID)
    ROOT.mkdir();save(OUTPUT,doc)
    subset=deepcopy(doc);subset.update(records=[row],blocks=[81],physical_speech_objects=1,
        ordinary_speech_objects=1,FE_speech_objects=0,typed_choice_objects=0,typed_choice_commands=0,
        subset_of=str(OUTPUT),subset_of_sha256=sha(OUTPUT.read_bytes()))
    save(ROOT/'fresh_manuscript.json',subset);save(ROOT/'preferences.json',dict(records={}))
    save(ROOT/'context_finding.json',dict(id=ID,Japanese=row['source_Japanese'],previous=previous,
        revised=row['english'],reason=reason,preceding='DK4_MES_B81_R0213',following='DK4_MES_B81_R0220',
        actual_context='work/analysis/Rafael_Emilio_food_actual_pixels_v2_20261105/focused_actual_pixels.json',
        every_other329_object_unchanged=True,fresh_checks_pending=True,new_credit=0))
    print('Repaired one stiff assurance;174 revisions/156 retentions unchanged. Fresh checks pending.')
