"""Review all four player answers as paired alternatives before exposing old captions."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.gloss_rafael_B51_B59_clean import ROOT

if __name__=='__main__':
    source=ROOT/'B60_two_choices_clean_v1.json';output=ROOT/'B60_four_choice_drafts_v1.json'
    assert not output.exists();doc=load(source)
    assert doc['object_count']==2 and doc['caption_count']==4
    meanings=[
        'Identify Spain,the power that took Portugal,as their true enemy.',
        'Admit uncertainty about the identity of their true enemy.',
        'Propose defeating Kuhn first as the cooperative strategy.',
        'Entrust handling Kuhn to Pereira while Rafael departs for Europe.',
    ]
    english=["Spain. They took Portugal from us.","...I'm not sure.","Let's defeat Kuhn first.","I'll leave Kuhn to you."]
    records=[]
    for row,meaning,text in zip(doc['records'],meanings,english,strict=True):
        r=deepcopy(row);r.update(source_meaning=meaning,english=text,speaker='Rafael/player answer',
            context='Complete paired answers in Pereira’s B60 negotiation:the true-enemy question andthe subsequent anti-Kuhn strategy. Each pair selects an alternative path;no answer ispresented as preceding the other.',
            localization_note='Natural selectable answer preserves this intent: '+meaning,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            current_English_comparison_pending=True,native_choice_mapping_anddisplay_pending=True)
        records.append(r)
    save(output,dict(format='dk4-clean-choice-drafts-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=records,source=str(source),source_sha256=sha(source.read_bytes()),
        earlier_current_English_captions_unconsulted=True,all_four_meanings_anddrafts_saved_before_current_caption_comparison=True,
        new_credit=0,guide_photos=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Saved4 source-first player answer drafts across2 complete alternatives;comparison/display pending.')
