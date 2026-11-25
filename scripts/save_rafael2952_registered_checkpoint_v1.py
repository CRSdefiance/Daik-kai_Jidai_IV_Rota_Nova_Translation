"""Record the verified cumulative release and the next clean-only intake."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.finalize_rafael_B201_B220_research_v1 import ROOT as RESEARCH, checksum
from scripts.qualify_rafael_B221_B240_clean_v1 import OUT as NEXT
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint


A=Path('work/analysis')
ROOT=A/'Rafael2952_extended_release_verified_v1_20261106'
RELEASE=ROOT/'registered_release_verification.json'
CREDIT=ROOT/'completion_checkpoint.json'
PACKAGE=A/'Weekend_testing_package_Rafael2549_20261106/package_verification.json'
REGISTRY=Path('translations/release_stack.json')
READY=RESEARCH/'research_completion.json'
ACTUAL=RESEARCH/'actual_review.json'
NEXT_KEY='Rafael_SC0_B221_B240_clean_20261106'


def main():
    release,credit,package,ready,next_batch=map(load,(RELEASE,CREDIT,PACKAGE,READY,NEXT))
    assert credit['new_credit']==403 and credit['counts']==dict(completed=14797,revised=8706,retained=6091)
    assert (release['complete_stack_entries'],release['accepted_layers'],release['passing_release_checks'])==(689,114,26)
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert release['all_eight_registered_final_stages_preserved']
    assert release['only_owned_SC0_blocks_changed']==list(range(201,221))
    assert release['parent_sha256']==package['ROM_sha256']
    assert (ready['actual_pages'],ready['actual_menus'],ready['offline_only_source_variants'])==(174,6,209)
    assert next_batch['clean_objects']==270 and next_batch['independently_drafted_records']==30
    assert next_batch['source_only_no_current_English_extracted'] and next_batch['zero_already_credited_keys']
    summary=(
        "Rafael B201–B220 is registered and credited once, with 299 revisions and 104 justified retentions. "
        f"Experimental {release['candidate_sha256'][:8]} passed 689 entries, all 114 accepted layers, eight final stages, "
        "26 release checks, exact clean-input reconstruction and its own Rafael startup. Integrated total is 14,797. "
        "The next clean intake has 270 records across B221–B240, with 30 independent drafts. Rafael2549 remains the weekend package."
    )
    doc=f"""# Rafael B201–B220 registered checkpoint

{summary}

The {link('cumulative experimental ROM',release['candidate'])} and {link('clean-input patch',release['patch'])} reconstruct byte for byte. The first build attempt stopped at a full C drive during the final stages. The verified retry ran on the project’s E-drive analysis volume and preserved the earlier outputs. The registered ASCII right-bound correction and original B146 percent-relocation proof are bound in the manifest. {link('Registered release verification',RELEASE)}.

All 383 pages, 21 captions and 41 name or role bindings passed offline checks. Three initialized emulator fixtures displayed 174 pages, 33 headers, both staged panels and all seven forecasts. Six selected menus showed 13 captions and ordinary A returns. The remaining 209 speeches and eight captions are offline-only. Natural activation, alternate player selections, event outcomes and physical hardware remain open. {link('Five-gate receipt',READY)}. {link('Focused emulator scope',ACTUAL)}.

The next batch contains 234 speeches, 29 physical style alternatives and seven menu captions. B231 is control-only. The letter and red-sword rumor have 30 clean-first drafts, including 15 voice variants. Complete the remaining 240 drafts before opening current English. Review the letter's source-staged signature independently from the B216 layout. Rafael and tutorials remain first. Deferred artwork and the later technical re-audit remain separate. {link('Next clean census',NEXT)}. {link('Rafael2549 weekend package',package['zip'])}.
"""
    evidence={str(p):checksum(p) for p in (RELEASE,CREDIT,PACKAGE,READY,ACTUAL,NEXT,Path(__file__))}
    checkpoint(
        mutation=ROOT/'registered_documentation_v1',
        batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Rafael B221–B240 clean-first dialogue intake.',
            next_action='Draft the remaining 240 clean objects, then compare against registered Rafael2952.',
            current_batch_not_yet_integrated=True,native_job_live=False,registered_build_live=False,guide_photos=False),
        new_entries={NEXT_KEY:dict(new_credit=0,source_records=270,ordinary_speeches=234,physical_style_alternatives=29,
            typed_captions=7,source_only=True,independently_drafted_records=30,independent_draft_blocks=[221,222],
            remaining_clean_meanings_anddrafts=240,remaining_current_comparisons=270,current_comparisons=0,
            full_intake_not_complete=True,evidence=evidence)},
        summary=summary,document='docs/editorial_Rafael_B201_B220_registered_20261106.md',
        document_text=doc,completed=14797,protected={str(REGISTRY):release['registry_sha256'],
            release['canonical_base']:release['canonical_sha256'],release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'],release['parent']:release['parent_sha256'],
            package['zip']:package['zip_sha256']},
    )
    print('Recorded Rafael2952 and the 270-object clean-only intake.')


if __name__=='__main__':
    main()

