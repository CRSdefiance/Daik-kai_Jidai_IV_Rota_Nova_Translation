"""Preserve unapplied8265 staging; replace inherited old actual/font fields with explicitly scoped current evidence."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_overlay_scope_tools_v8267')
if __name__=='__main__':
    assert not ROOT.exists()
    extra="""            font=next(r for r in read(PROOFS['body_fonts'])['records'] if r['id']==row['id'])
            actualscope='Revised English complete body/name holds in initialized wholeB74 orfocused B27 intro display fixtures;byte-identical approved reference;not natural activation in registered V8259.'
            holds=[dict(scope=o['scope'],**hold) for o in row['actual_display_observations'] if o['version']=='revised_English' for hold in o['speech']['complete_holds']]
            assert holds
            put(base+['actual_proof'],PROOFS['actual'])
            put(base+['actual_holds'],holds)
            put(base+['individually_activated_in_current_build'],False)
            put(base+['current_observation_scope'],actualscope)
            put(base+['formatting_scope'],'Complete native/stored/actual first/internal/final glyph masks,216px/fourrows/onepage,all sourcecontrols andstoredparity;'+actualscope)
            if 'native_complete_font_plane_sha256' in record:put(base+['native_complete_font_plane_sha256'],font['pages'][0]['native_plane_sha256'])
            if 'native_font_proof_case' in record:put(base+['native_font_proof_case'],font)
            if 'native_control_proof' in record:put(base+['native_control_proof'],PROOFS['final_controls'])
            if 'representative_actual_proof' in record:put(base+['representative_actual_proof'],PROOFS['actual'])
            if 'individually_observed_original_context' in record:put(base+['individually_observed_original_context'],False)
            if 'offline_scope' in record:put(base+['offline_scope'],'Complete independent source/control/relative/whole inverse checks;actual conditional selection limits retained separately in current_observation_scope.')
"""
    receipt=derive('scripts/complete_Gerhard_overlay_v8265.py','scripts/complete_Gerhard_overlay_v8267.py',{
      'Gerhard_registered_overlay_v8265':'Gerhard_registered_overlay_v8267','editorial_handoff_verification_v8266':'editorial_handoff_verification_v8268',
      'Gerhard_Adernkatz_registered_V8259_Hodram28_pending_stored_names_actual_policy_release_v8265':'Gerhard_Adernkatz_registered_V8259_Hodram28_pending_stored_names_actual_policy_release_v8267',
      'unfinished_editorial_scope_v8265':'unfinished_editorial_scope_v8267','latest_integrated_editorial_overlay_v8265':'latest_integrated_editorial_overlay_v8267',
      " 'policy_tests':":" 'body_fonts':'work/analysis/Gerhard_pages_v8206/5_complete_native_paragraphs5_pages20_compiled_alignments.json',\n 'actual':'work/analysis/Gerhard_actual_v8229/six_paired_runs_actual_five_surname_bodies_headers_conditions_andnormal_returns.json',\n 'final_controls':'work/analysis/Gerhard_final_controls_v8214/5_final_dispatches51_controls30_raw_evaluations150_seeded_ends.json',\n 'policy_tests':",
      "            overlays.append({k:v for k,v in overlay.items() if k!='previous_credited_record_preserved'})":extra+"            overlays.append({k:v for k,v in overlay.items() if k!='previous_credited_record_preserved'})",
      'V8265':'V8267','verifiedV8266':'verifiedV8268','VerifiedV8266':'VerifiedV8268',
    })
    ROOT.mkdir(parents=True);save(ROOT/'exact_scoped_overlay_successor.json',dict(derivation=receipt,
        prior8265_staging_preserved_andnever_applied=True,
        reason='Do not carry older natural-activation/font proof fields forward under a new candidate SHA;preserve the entire old record snapshot andscope every current actual/font field explicitly.',
        no_ROM_registry_orcompletion_credit_change=True,full_goal_complete=False))
