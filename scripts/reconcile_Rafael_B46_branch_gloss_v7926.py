"""Refine the fresh source gloss with measured conditional context before current English."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_branch_gloss_v7926')
OLD=Path('work/analysis/Rafael_B46_clean_gloss_v7920b/24_speeches2_choices_fresh_clean_glosses_before_current_English.json')
FLOW=Path('work/analysis/Rafael_B46_menu_flow_v7925/two_choice_native_forwarding_four_relative_sites_accept22_decline7_source_scope.json')
if __name__=='__main__':
    assert not ROOT.exists();old,flow=map(read,[OLD,FLOW]);doc=deepcopy(old)
    assert flow['source_gloss_sha256']==sha(OLD.read_bytes()) and flow['no_current_English_B46_body_orchoice_read']
    shared="""Claudio's relief and Rafael's subdued answer lead into Julio's concern that an enemy may challenge them sooner than expected, and his offer to explain other sea actions. The two polite menu options accept or decline the offer. In the measured source menu dispatch, option0 is forwarded as state2/value0 and option1 as state2/value1. Composing those values with the four independently executed native relative-site cases gives an acceptance path of22 speeches and a decline path of7 speeches, covering all24 distinct stored speech objects together.

Acceptance skips the0300 object, enters Julio's overview and12 distinct FE information panels, and reaches his understanding check and Rafael's thanks. The outer0100 then skips the caution/acknowledgment nested inside it. Declining executes0300 and jumps directly inside that outer0100 to Julio's 'I see'/emphatic caution and Rafael's brief acknowledgment, bypassing the tutorial and understanding/thanks. The nested empty0100 ends at the shared unfinished private thought. Thus Julio's caution is the decline response, not a warning spoken after the tutorial on every path.

This path description composes exact native menu/relative results. The modal input loop was bridged only in the isolated VM tests; it is not an actual controller choice, complete interpreter execution or proof of natural event activation. Both original branch-specific exchanges need representative actual tests later. No text/condition/branch/result/seed has been forced in gameplay."""
    context=old['records'][0]['full_clean_exchange_context']
    before="Julio then checks understanding, receives Rafael's polite thanks, warns him not to relax at sea, and receives a short acknowledgment."
    assert before in context
    context=context.replace(before,"The understanding check and thanks belong to the acceptance path; the caution and acknowledgment belong to the decline path.")+'\n\n'+shared
    accept,decline=flow['source_paths']
    for row in doc['records']+doc['menu_choices']:
        row['full_clean_exchange_context']=context
        row['source_branch_context_proof']=str(FLOW);row['source_branch_context_proof_sha256']=sha(FLOW.read_bytes())
        if row.get('kind')=='typed-menu-2100-choice':
            row['source_choice_response_context']="Rafael's selectable polite response to Julio's offer; raw menu has no speech selector. Preserve two-option order and native selection0/1; no forced actual choice."
        else:
            row['source_composed_paths']=[p['menu_selection'] for p in flow['source_paths'] if row['id'] in p['source_speech_IDs']]
    rows={r['source_record_index']:r for r in doc['records']}
    rows[95]['source_gloss']="On the acceptance path only, Julio asks how that was and whether Rafael understood the explanation. This checks understanding rather than asserting demonstrated mastery."
    rows[98]['source_gloss']="On the acceptance path only, Rafael politely says yes and thanks Julio for the explanation. Preserve respectful appreciation without adding a family or military title."
    rows[105]['source_gloss']="On the decline path only, Julio acknowledges Rafael's saying he can manage now, then emphatically warns him not to let his guard down at sea. 'I see' responds to the declined offer, not to thanks after an explanation."
    rows[109]['source_gloss']="On the decline path only, Rafael briefly acknowledges Julio's caution. Do not insert this reply into the acceptance path or add a promise the source does not supply."
    doc.update(previous_source_gloss=str(OLD),previous_source_gloss_sha256=sha(OLD.read_bytes()),
        branch_context=shared,source_paths=flow['source_paths'],source_branch_proof=str(FLOW),source_branch_proof_sha256=sha(FLOW.read_bytes()),
        source_branch_context_refined_before_current_English_exposure=True,
        source_first_boundary_UTC=datetime.now(timezone.utc).isoformat(),
        previous_gloss_linear_caution_context_superseded_not_deleted=True,
        all_source_texts_controls_menu_order_andsource_references_unchanged=True,
        names_proof_reused_by_exact_same_source_selectors_andfields_no_rerun=True)
    for previous,current in zip(old['records']+old['menu_choices'],doc['records']+doc['menu_choices'],strict=True):
        for key in ['id','source_hex','source_reference','source_Japanese']:
            assert previous[key]==current[key]
        assert current['current_English_body_unread']
    assert [len(p['source_speech_IDs']) for p in doc['source_paths']]==[22,7]
    ROOT.mkdir(parents=True)
    save(ROOT/'24_speeches2_choices_fresh_branch_context_before_current_English.json',doc)
    print('Fresh source gloss refined before current English: tutorial/check/thanks on accept; caution/acknowledgment on decline; shared unfinished thought.')
