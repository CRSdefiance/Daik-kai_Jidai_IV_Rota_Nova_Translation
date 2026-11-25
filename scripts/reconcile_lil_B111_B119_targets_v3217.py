"""Split reachable Lil prose from an unowned appended canonical Maria copy."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B111_B119_source_v3217')
OLD=Path('work/analysis/lil_B111_B119_source_v3210b/complete182_clean_current_native_context.json')
CLASSIFICATION=Path('work/analysis/lil_B115_tail_classification_v3216/source_return0_graph_and_canonical_Maria_copy_classification.json')
CONTEXT=Path('work/analysis/lil_B111_B119_clean_context_v3213b/all182_complete_clean_exchange_context_notes.json')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=deepcopy(read(OLD));classification=read(CLASSIFICATION)
    assert classification['source_context_sha256']==sha(OLD.read_bytes())
    assert classification['all12_original_VM_return0_cases_stop_before_cursor_advance']
    assert classification['all_original_prefix_branch_results_cannot_reach_appended_SC0_SC1_SC2_copies']
    omitted=[r for r in doc['records'] if r['block']==115 and r['source_reference']['offset']>=440]
    assert len(omitted)==32
    excluded={r['id'] for r in omitted}
    doc['records']=[r for r in doc['records'] if r['id'] not in excluded]
    for b in doc['blocks']:
        b['records']=[r for r in b['records'] if r['id'] not in excluded]
        if b['block']==115:
            b['unowned_appended_Maria_copy_records']=omitted
            b['unowned_appended_copy_original_offset']=440
            b['unowned_appended_copy_current_hex']=classification['copies'][2]['versions'][1]['tail_sha256']
            b['unowned_copy_metadata_value_above_is_sha256_not_body_hex']=True
            b['preserve_all_current_appended_copy_bytes_during_relocation']=True
            b['canonical_player_facing_region_file']='/data/SC3.DK4'
            b['canonical_player_facing_region_block']=97
    assert len(doc['records'])==116 and sum(r['kind']=='system-FE' for r in doc['records'])==1
    assert len(doc['typed_actor_style_records'])==34
    doc.update(previous_physical_source_packet=str(OLD),previous_physical_source_packet_sha256=sha(OLD.read_bytes()),
        classification_proof=str(CLASSIFICATION),classification_proof_sha256=sha(CLASSIFICATION.read_bytes()),
        total_editorial_objects=150,speech_objects=116,ordinary_source_speeches=115,system_FE_panels=1,
        total_stored_physical_source_objects_including_unreachable_copies=182,
        total_stored_physical_speeches_including_unreachable_copies=148,
        unowned_appended_Maria_copy_records=omitted,unowned_appended_Maria_copy_record_count=32,
        canonical_Maria_followup_records=classification['canonical_Maria_source_record_aliases'],
        canonical_Maria_SC3_B97_32_records_remain_in_full_editorial_goal=True,
        all305_physical_native_commands_must_survive_inverse_restoration=True,
        active_Lil_review_targets150_not182=True,all182_clean_objects_previously_read_before_any_oldEnglishcomparison=True,
        complete_clean_context_notes=str(CONTEXT),complete_clean_context_notes_sha256=sha(CONTEXT.read_bytes()),
        whole_clean_exchange_context_read=True,older_English_editorial_comparison_pending=True,
        scope='150reachable Lil editorialtargets acrossB111-B119:116speech(115ordinary/oneFE24000gold) and34storedactor-style alternatives/6objects48slots. Thephysical182packet includes32appended Maria copy speeches aftersource0000;12nativeVMreturns andconservativeprefixgraphs proveordinaryLilentrydoesnotreachthem. Their exact1886byteJapanese counterpartisordinaryentrySC3B97andall32remainqueuedinthefullMariaeditorialscope. Preserve thecurrent SC2copybyteforbyte asunowneddatawhenmovingtheblock. No dead-copy translation orcompletioncredit isclaimed. All305physicalcommands/64spans remainmapped;current roles/voices/macros/predicates/query,oldEnglishcomparison,gloss/prose/retentions,native/reference/representative/release gates stillpending.',
        source_prose_credit_added=0,completion_credit_added=0,new_emulator_runs=0)
    doc['evidence'][str(OLD)]=sha(OLD.read_bytes())
    doc['evidence'][str(CLASSIFICATION)]=sha(CLASSIFICATION.read_bytes())
    doc['evidence'][str(CONTEXT)]=sha(CONTEXT.read_bytes())
    doc['evidence'][str(Path(__file__))]=sha(Path(__file__).read_bytes())
    ROOT.mkdir(parents=True)
    save(ROOT/'complete150_reachable_Lil_clean_current_context.json',doc)
    save(ROOT/'canonical_Maria32_deferred_source_lead.json',dict(
        classification=str(CLASSIFICATION),classification_sha256=sha(CLASSIFICATION.read_bytes()),
        current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],
        file_path='/data/SC3.DK4',block=97,source_speech_count=32,
        records=classification['canonical_Maria_source_record_aliases'],
        complete_clean_dialogue_already_read_as_exact_duplicate=True,
        current_Maria_route_actor_company_macros_and_all_editorial_native_release_gates_pending=True,
        retained_in_full_editorial_goal_not_completed_or_discarded=True,
        source_prose_or_completion_credit_added=0,new_emulator_runs=0,full_goal_complete=False))
    print('Reconciled150reachable Lil targets;32canonical MariaSC3B97speeches queued,notdiscarded. Preserveunowned appendedcopy bytes/all305commands. Zero neweditorialcredit.')
