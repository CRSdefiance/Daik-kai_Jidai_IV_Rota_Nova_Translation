"""Reject three worse projections andretain a complete phrasal verb at a line ending."""
from copy import deepcopy
from pathlib import Path
from scripts.refine_rafael_B51_B60_layout import ROOT
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    original=ROOT/'visual_preferences_v2.json';output=ROOT/'visual_preferences_v3.json';assert not output.exists()
    doc=deepcopy(load(original));rejected=[]
    reasons={
        'DK4_MES_B58_R0068':'Keeping the entire item title in one row projected a sparse opening andan extra page ending only Proof of Conquest.The original four-row page remains complete andreadable;the title continues across adjacent rows.',
        'DK4_MES_B60_R0374':'Forcing who’d-be together projected a new page containing only to-do-it.Keep the original complete four-row question within one page.',
        'DK4_MES_B60_R0451':'Forcing there’ll-be together projected a new page containing only to-stop-him.Keep the original complete four-row explanation within one page.',
    }
    for ident,reason in reasons.items():
        rejected.append(dict(id=ident,rejected_preference=doc['records'].pop(ident),reason=reason))
    r=doc['records']['DK4_MES_B56_R0077']
    r['QA_line_ending_retention']=dict(exact_line='The whole town chipped in,',
        reason='In is the particle completing chipped-in,not an unattached preposition.The complete clause ends naturally before and;retaining this boundary fixes the prior chipped/in split.')
    doc['records']['DK4_MES_B60_R0486']['page_clause']="that little mustached bastard, you won't beat Kuhn in a hundred years!"
    doc['records']['DK4_MES_B60_R0486']['reason']='Keep the complete insult noun phrase on the successor page,after the first-page if-you-can’t-beat lead-in;avoid both the original orphan bastard andthe revised isolated is row.'
    doc.update(previous_preferences=str(original),previous_preferences_sha256=sha(original.read_bytes()),
        rejected_worse_planner_projections_not_native_ROM_failures=rejected,
        short_nonterminal_middle_rows_penalized_without_geometry_changes=True,
        phrasal_verb_QA_retention_source_andtext_bound=True,producer_sha256=sha(Path(__file__).read_bytes()))
    save(output,doc);print('Retained3 original one-page layouts;38 scoped preferences andone grammatical QA retention ready.')
