"""Keep the Maria-calibrated full-width planner and all330 exact source/current bindings."""
from scripts import plan_maria328_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'work/Maria_B73_B95_clean_20261109':'work/Maria_B96_B124_clean_20261109',
    "doc['physical_speech_objects']==313":"doc['physical_speech_objects']==328",
    "doc['blocks']==[73,74,75,76,77,78,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95]":
        "doc['blocks']==[96,98,99,100,101,102,103,104,105,106,107,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124]",
    "len(bound)==len(original)==len(doc['records'])==328":"len(bound)==len(original)==len(doc['records'])==330",
    "row['source_word']==0x2200":"row['source_word']==0x2100 and row['source_count']==2",
    'assert len(bindings)==313':'assert len(bindings)==328',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-full-width-source-controls-phase-andpagination-contract330','exec'),globals())
