"""Preserve v1 and correct the Chapel branch label in a successor manuscript."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
OLD=Path('translations/battle_chapel_planning_contextual_editorial_manuscript_v1.json')
NEW=Path('translations/battle_chapel_planning_contextual_editorial_manuscript_v1b.json')
ROOT=Path('work/analysis/battle_chapel_planning_metadata_v2408c')
if __name__=='__main__':
 assert not NEW.exists()and not ROOT.exists();d=read(OLD);corrections=[]
 for r in d['records']:
  prior=r['context'];head,tail=prior.split(' activity comment.',1);assert head==('Independent Battle Planning19'if r['role_ID']==18 else'Independent Planning19');r['context']='Independent battle '+('Chapel18'if r['role_ID']==18 else'Planning19')+' activity comment.'+tail
  corrections.append(dict(message_ID=r['message_id'],prior_context=prior,corrected_context=r['context'],prose_source_gloss_retention_reason_and_speaker_unchanged=True))
 d.update(context_metadata_successor_of=str(OLD),context_metadata_successor_of_sha256=sha(OLD.read_bytes()),context_label_corrections_only=True);ROOT.mkdir(parents=True);save(NEW,d);save(ROOT/'context_metadata_corrections.json',dict(prior=str(OLD),prior_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),corrections=corrections,role_IDs18_19_and_all_English_unchanged=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(corrected_role_labels=24,English_changes=0))
