"""Retain every source name substitution through natural address andfaithful reported quotation."""
from copy import deepcopy
from scripts.draft_rafael_B157_B160_clean_v1 import DATA as original,CONTEXT
from scripts.seal_clean_independent_drafts_v1 import seal

DATA=deepcopy(original)
for index,draft in {
47:'FI... She told me, "I think about FI every day, too."',
60:"If you hadn't felt anything for her, FI, I would have kept this to myself.",
76:"She's worried about your background, FI. You come from an old, respected family.",
129:'"FI, I hope your country will be restored, too. When it is...',
}.items():DATA[159][index]=(DATA[159][index][0],draft)

if __name__=='__main__':
    seal('work/analysis/Rafael_B141_B160_clean_20261105','B157_B160_meanings_andindependent_drafts_v2.json',
        DATA,CONTEXT,{},__file__,72)
