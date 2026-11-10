"""Refine the complete clean exchange with measured names andbranches before current English."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_branch_gloss_v7979')
OLD=Path('work/analysis/Rafael_B47_clean_gloss_v7973/15_fresh_clean_glosses_complete_B37_context_before_current_English.json')
FLOW=Path('work/analysis/Rafael_B47_source_paths_v7978/625_source_result_compositions_six_text_paths_two_exclusive_alternatives.json')
NAMES=Path('work/analysis/Rafael_B47_names_v7976/four_static_speakers_eight_getters_clean_fields16_synthetic_macro_alignments.json')
BRANCH="""The exact current native source probes bind actor00 to Rafael Castor,04 to Janus Pasar,05 to Claudio Manaus and06 to Julio Erneco, with original voice classes2/0/4/5. Both original name getters return each full name. Janus's パサー/Pasar is distinct from パシャ/Pasha in the military-force references; no association follows from the similar romanizations. Catalogue UI,custom player names andthe wider207-name review remain open.

Source branch composition uses all24 measured relative sites andsix original raw8000 predicate sites. The three Janus speeches R17/R92/R122 share the exact04FE0030 operand. They are included only for raw result1; R92 additionally requires entering the main advice block. The main warning/advice block is entered only for result1 from000009A0. Within it,the Ottoman-only Rafael R63 is selected when000007A0 is not1;the combined Spanish Valdes/Ottoman Pasha alternative R70 is selected when it is1. They are mutually exclusive. The source A000 command at250 is independently gated by000C2170 result1;its effect is preserved without assigning unproved plot semantics.

Composing five structural result values for each ofthe four unique operands yields625 cases andsix distinct text paths of5,7,11 or14 speeches. Their union includesall15 speech objects andall48 commands. This is a native-result composition,not actual story selection orproof that every hypothetical combination is naturally reachable. Raw expression values are not generally assumed boolean. The unforced current opening values compose an11-speech path withR70 andwithout Janus's three lines;that doesnot prove naturalB47 activation oractual B47 gameplay. The private advice andevery variant must be reviewed in its own complete path."""
if __name__=='__main__':
    assert not ROOT.exists();old,flow,names=map(read,[OLD,FLOW,NAMES]);doc=deepcopy(old)
    assert flow['source_gloss_sha256']==names['source_gloss_sha256']==sha(OLD.read_bytes())
    assert flow['current_B47_English_still_unread'] and names['current_English_B47_bodies_still_unread']
    context=old['complete_source_exchange_context']
    before="Actor00 is Rafael and the source names Julio/Claudio in surrounding context; original source identity fields and native display consumers still need explicit binding for this batch, especially actor04. Use source selectors until that binding is approved."
    assert before in context
    context=context.replace(before,"The original source selectors are now bound to Rafael, Janus, Claudio and Julio by clean fields and both current native name getters. Font and actual-scene name/body display checks remain pending.")+'\n\n'+BRANCH
    for row in doc['records']:
        row['source_gloss']=row['source_gloss'].replace('Speaker06','Julio').replace('Speaker04','Janus').replace('Speaker05','Claudio')
        row.update(full_clean_exchange_context=context,source_branch_context_proof=str(FLOW),source_branch_context_proof_sha256=sha(FLOW.read_bytes()),
            source_name_proof=str(NAMES),source_name_proof_sha256=sha(NAMES.read_bytes()),
            native_branch_composition_ofstored_alternatives_pending=False,
            source_composed_text_paths=[i for i,p in enumerate(flow['representative_text_paths']) if row['id'] in p['source_speech_IDs']])
    rows={r['source_record_index']:r for r in doc['records']}
    rows[63]['source_gloss']="Within the main advice block, Rafael concludes that they should leave the Mediterranean, which is strongly influenced by the Ottoman Pasha forces, until later. This Ottoman-only alternative is selected when the exact000007A0 expression result is not1. It is never spoken together withR70."
    rows[70]['source_gloss']="Within the main advice block, Rafael concludes that they should leave the Mediterranean until later because of the strong influence of both Spain's Valdes forces and the Ottoman Pasha forces. This alternative is selected when000007A0 returns1. Preserve both powers and do not merge it withR63."
    rows[122]['source_gloss']="Janus politely and lightly wryly notes that things are getting busy, moving from the advice to the work ahead. This source-actor04 line occurs only when the same04FE0030 condition as his earlier remarks returns1; no new rank or relationship is supplied."
    doc.update(prior_gloss=str(OLD),prior_gloss_sha256=sha(OLD.read_bytes()),branch_context=BRANCH,
        complete_source_exchange_context=context,source_branch_proof=str(FLOW),source_branch_proof_sha256=sha(FLOW.read_bytes()),
        source_names=str(NAMES),source_names_sha256=sha(NAMES.read_bytes()),
        source_first_boundary_UTC=datetime.now(timezone.utc).isoformat(),
        source_branch_context_refined_before_current_English_exposure=True,
        all15_complete_clean_Japanese_speeches_read_before_current_English=True,
        all_source_bytes_references_selectors_andoriginal_conditional_controls_unchanged=True,
        native_control_andname_binding_now_complete_butactual_branch_selection_anddisplay_pending=True)
    for a,b in zip(old['records'],doc['records'],strict=True):
        assert all(a[k]==b[k] for k in ['id','source_hex','source_reference','source_Japanese','source_complete_preamble_hex'])
        assert b['current_English_body_unread']
    ROOT.mkdir(parents=True);save(ROOT/'15_fresh_glosses_six_source_paths_names_bound_before_current_English.json',doc)
    print('B47 fresh glosses refined before current English:four identities,six text paths,exclusiveR63/R70 andconditionalJanus lines;no invented plot-flag meanings.')
