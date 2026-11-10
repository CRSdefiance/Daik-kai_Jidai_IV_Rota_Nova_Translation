"""Retain the calibrated full-width planner for373 bodies andboth qualified menu types."""
from scripts.plan_maria335_B137_B151_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/Maria_B137_B151_clean_20261109':'work/Maria_B152_B175_clean_20261109',
    "doc['physical_speech_objects']==333":"doc['physical_speech_objects']==373",
    "doc['blocks']==list(range(137,152))":"doc['blocks']==list(range(152,176))",
    "len(bound)==len(original)==len(doc['records'])==335":"len(bound)==len(original)==len(doc['records'])==390",
    "row['source_word']==0x2100 and row['source_count']==2":
        "row['source_word'] in (0x2100,0x2200) and row['source_count']=={0x2100:2,0x2200:3}[row['source_word']]",
    'assert len(bindings)==333':'assert len(bindings)==373',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-source-current-controls-word-width-phase-andpagination-contract','exec'),globals())
