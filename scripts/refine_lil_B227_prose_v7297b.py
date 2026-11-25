"""Preserve the first draft; clarify two spoken sentences without losing source meaning."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B227_prose_v7297b');OLD=Path('translations/lil_B227_editorial_manuscript_v1.json');OUT=Path('translations/lil_B227_editorial_manuscript_v1b.json')
EDITS={15:("But if you're scared of the blade and hesitate as you step in, you could get hurt even worse. That's why being fearless matters.",'Preserve fear of the blade,the hesitant step in,the counterproductive risk of serious injury,andthe importance of a fearless state of mind. This makes the causal explanation easier to say aloud than the first draft\'s repeated you clauses. Being fearless expresses物事をおそれない精神力 naturally in the immediate martial context;no statistic,actual injury orunconditional guarantee is added. The earlier generic afraid/hurt wording lost the concrete advance. This is a complete source-meaning review,not deletion toimitate the old allocation.'),28:('Oops! My teacher would scold me for relying on gear. They\'d say, "Train yourself first!"','Keep the self-correction,the remembered respectful teacher,the warning against depending on equipment,andthe entire quoted self-training admonition. Placing the conversational quote tag before the quotation avoids the first draft\'s redundant That\'s what they\'d say. Teacher avoids anunproved naval/social rank;they avoids the earlier translation\'s unsupported teacher gender. The source speaker continues throughout the quote;no new actor,name,family relationship orpresent teacher is invented.')}
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists();old=read(OLD);doc=deepcopy(old);changed=[]
    for row in doc['records']:
        index=row['source_record_index']
        if index not in EDITS:continue
        text,reason=EDITS[index];before=deepcopy(row);assert row['editorial_decision']=='revise' and all(row['review'][k] for k in ['source','context','localization','naturalness']) and not row['review']['formatting']
        row.update(english=row['english'].split('}',1)[0]+'}'+text,localization_note=reason,editorial_finding=reason,historical_first_prose_draft=dict(manuscript=str(OLD),manuscript_sha256=sha(OLD.read_bytes()),english=before['english'],localization_note=before['localization_note'],editorial_finding=before['editorial_finding']),whole_exchange_reread_after_sentence_refinement=True);changed.append(row['id'])
    assert len(changed)==2 and doc['revised']==7 and doc['retained']==2
    doc.update(previous_prose_draft=str(OLD),previous_prose_draft_sha256=sha(OLD.read_bytes()),only_R15_R28_prose_refined_with_all_source_meaning_preserved=True)
    ROOT.mkdir(parents=True);save(OUT,doc);save(ROOT/'two_contextual_sentence_refinements.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),historical_manuscript=str(OLD),historical_manuscript_sha256=sha(OLD.read_bytes()),changed_IDs=changed,all9_reread_as_complete_exchange=True,all_source_facts_voice_andemotional_progression_preserved=True,all_other7_rows_exact=True,no_ROM_or_registry_ledger_orcredit_change=True,formatting_native_actual_andrelease_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B227:R15 causal warning andR28 quotation refined;all9 reread;7 revisions/2 retentions unchanged;all drafts preserved.')
