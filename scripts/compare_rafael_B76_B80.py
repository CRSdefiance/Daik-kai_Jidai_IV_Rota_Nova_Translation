"""Review Mediterranean alternatives without changing the direct defeat or inventing rank."""
from pathlib import Path
from scripts.compare_sealed_dialogue_v1 import compare

ROOT=Path('work/analysis/Rafael_B61_B80_clean_20261104')
RETAIN={
76:{
7:'The surprised respectful greeting naturally uses the established Admiral Hayreddin name.',
12:'The praise, Ottoman/Pasha identification, extraordinary strength and unfinished confidence in the crew are natural and accurate.',
27:'The concise firm warning naturally preserves not letting their guard down.',
31:'Old man is Claudio deliberately irreverent familiar address to the established older admiral, not Grandpa or kinship. The contrast with Rafael formal address and Hayreddin amused reply supports retaining that characterization.',
34:'The amused short laugh and goodbye naturally convey the farewell.',
37:'The respectful goodbye and established name already work.',
},
77:{
10:'The painful direct loss to Valdes is already accurate. The following victory refers to overall Mediterranean supremacy; retain the encouragement without reversing the battle result.',
},
78:{
9:'The stammered hesitant hope naturally responds to Claudio confidence.',
13:'Ruler of the seas is source-supported enthusiastic praise here, not a formal coronation; the pride encouragement already works.',
17:'The hesitant agreement and familiar thanks naturally accept the encouragement.',
21:'The admiral reminder, near-goal encouragement and Stay strong fit Claudio supportive voice.',
},
79:{
10:'The relieved At last naturally conveys that reaching this point took a long time.',
32:'The puzzled contrast accurately preserves the cloth pattern looking nothing like a map.',
},
80:{
13:'The relieved identification check and explicit king-of-Portugal summons are natural and add no messenger rank.',
},
}
FINDINGS={
76:{
15:'Remove the invented internal instruction be confident; preserve the nervous affirmative, unelaborated self-correction and firmer reply.',
20:'Restore the conditional if they manage to defeat Pasha forces rather than commanding a guaranteed defeat or narrowing the source forces to a fleet.',
23:'Correct collective We to Rafael personal promise to remember the Alexandria priest.',
},
77:{
5:'Make the achieved faction supremacy natural and explicit rather than the headline-like tops the Mediterranean.',
13:'Restore the specific source-defined Estado overseas trading-network objective instead of the vague invented conquer the rest instruction.',
},
78:{
5:'Restore being the strongest regional power rather than ruling all its seas, and explicit support for restoring the Portuguese royal house rather than generic crown support.',
24:'Make the renewed rally natural and energetic with Let us go/Let us contraction rather than a stiff proclamation.',
29:'Localize the drawn-out affirmative cheer as a natural English cheer rather than an ambiguous Ooooooh reaction.',
},
79:{
5:'Remove invented Lord rank while preserving respectful surname address, Mediterranean supremacy and the offered object.',
22:'Restore the confident map inference and qualified recollection of some kind of crown in natural sentences; name no specific crown.',
29:'Restore the collective decision to search and a natural departure prompt rather than a clipped command plus stiff Let us.',
},
80:{
19:'Remove invented Lord rank and make the enthusiastic homecoming/king summons natural without changing the alternative event.',
},
}

if __name__=='__main__':
    flatten=lambda rows:{(b,i):text for b,items in rows.items() for i,text in items.items()}
    compare(draft_path=ROOT/'B76_B80_26_logical_English_drafts_v1.json',
        current_path='work/analysis/Rafael_B61_B80_latest_runtime_20261104/all539_current_effective_qualified_v1.json',
        output=ROOT/'B76_B80_26_whole_exchange_comparison_v1.json', retain=flatten(RETAIN),
        findings=flatten(FINDINGS), producer=Path(__file__),
        context='Complete Hayreddin warning/contact exchange, alternative Mediterranean supremacy outcomes, restoration rally, priest cloth-map handover and two Portugal royal summons paths. Preserve the explicit painful direct loss to Valdes, source-defined overseas trading-network objective, conditional Alexandria contact, unnamed crown inference and rhetorical sea-dominance praise without inventing royal rank. Native controls, source alternatives, all prior evidence and fresh display/stored/gameplay requirements remain.',
        extra=dict(all539_prose_comparisons_now_available=True,
            Estado_term_qualified_from_clean_B152_B164_B166=True,
            original_direct_battle_loss_wording_justifiably_retained=True))
