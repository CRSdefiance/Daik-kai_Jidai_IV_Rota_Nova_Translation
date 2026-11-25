"""Correct an inverted scope label without repeating or changing header comparisons."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    source=Path('work/analysis/Rafael_B36_B41_progressive_names_20261104/actual_header_verification.json')
    target=source.with_name('actual_header_verification_v2.json');assert not target.exists()
    proof=load(source);assert proof.pop('two_catalogue_middle_field_proposals_deferred_not_approved') is False
    assert proof['full_catalogue_UI_unvisited'] and proof['no_name_data_change']
    proof.update(catalogue_field_proposals_not_deployed_or_approved_by_this_proof=True,
        clarification='The initial scope field used an inverted boolean label. This proof covers unchanged progressive nameplates only. Both catalogue-field proposals remain pending deployment/acceptance; their separate offline qualification is preserved.',
        exact_header_comparisons_reused_without_reexecution=True,prior_header_proof=str(source),prior_header_proof_sha256=sha(source.read_bytes()),
        clarification_producer_sha256=sha(Path(__file__).read_bytes()))
    save(target,proof)
    print('Progressive-only header scope clarified;all40 comparisons unchanged;initial evidence preserved.')
