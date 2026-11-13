"""Record the verified Rafael3222 release and exact next clean-only scope."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.checkpoint_rafael_B221_B240_contextual_v1 import PACKAGE, REGISTRY, RELEASE as PARENT
from scripts.checkpoint_rafael_B221_B240_research_v1 import ACTUAL, READY
from scripts.qualify_rafael_B241_B260_clean_v2 import OUT as NEXT
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.write_rafael_B221_B240_contextual_v1 import digest

ROOT = Path('work/Rafael3222_extended_release_verified_v1_20261106')
RELEASE = ROOT/'registered_release_verification.json'
CREDIT = ROOT/'completion_checkpoint.json'
FAILURE = Path('work/analysis/Rafael3222_extended_build_gc_v1_20261106/completion.json')
NEXT_KEY = 'Rafael_SC0_B241_B260_clean_20261106'


def main():
    release, credit, package, ready, next_batch, parent, failure = map(load, (RELEASE, CREDIT, PACKAGE, READY, NEXT, PARENT, FAILURE))
    assert credit['new_credit'] == 270 and credit['counts'] == dict(completed=15067,revised=8927,retained=6140)
    assert (release['complete_stack_entries'],release['accepted_layers'],release['passing_release_checks']) == (690,114,26)
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert release['all_eight_registered_final_stages_preserved'] and release['parent_sha256'] == parent['candidate_sha256']
    assert release['only_owned_SC0_blocks_changed'] == [n for n in range(221,241) if n != 231]
    assert (ready['actual_pages'],ready['actual_menus'],ready['offline_only_source_variants']) == (94,3,177)
    assert (next_batch['clean_objects'],next_batch['new_eligible_objects'],next_batch['independently_drafted_records']) == (310,292,94)
    assert next_batch['source_only_no_current_English_extracted'] and next_batch['no_duplicate_credit']
    assert next_batch['prior_completed_block_byte_identical_in_current_Rafael2952']
    assert failure['terminal'] and not failure['driver_completed_without_exception']
    summary = (
        'Rafael B221–B240 is registered and credited once, with 221 revisions and 49 justified retentions. '
        f'Experimental {release["candidate_sha256"][:8]} passed 690 entries, 114 accepted layers, eight final stages, '
        '26 release checks, exact clean-input reconstruction and its own Rafael startup. Integrated coverage is 15,067. '
        'The next intake has 292 eligible records and 94 independent drafts. B246 retains its 18 earlier reviews.'
    )
    doc = f"""# Rafael B221–B240 registered checkpoint

{summary}

The {link('experimental cumulative ROM',release['candidate'])} and {link('clean-input patch',release['patch'])} reconstruct byte for byte. The first attempt ran out of space on E while writing the final ROM. The verified retry and reconstruction are on C. The registered ASCII right-bound correction and the B146 percent-relocation proof remain bound. {link('Registered release verification',RELEASE)}.

All 279 dialogue pages, seven captions and 26 public name or role bindings passed offline checks. The two initialized emulator fixtures displayed 86 speech variants across 94 pages and 16 distinct nameplates. They included three signatures, all three swan panels, all four voice commands at default class 4 and all seven captions at the default cursor. A returned to the next fixture speech in each menu. The other 177 speech variants passed offline checks. Original conditional activation, alternate selections, event outcomes and hardware remain unobserved. {link('Five-gate receipt',READY)}. {link('Focused emulator scope',ACTUAL)}.

The B241–B260 census contains 310 clean objects. The 18 already-integrated B246 records match their previously reviewed block byte for byte and remain available for context. Complete the 198 remaining independent drafts before comparing the 292 new objects against Rafael3222. B244 contains only controls. Preserve deferred artwork, the later older-record technical re-audit and the existing {link('Rafael2549 weekend package',package['zip'])}. {link('Next clean census',NEXT)}.
"""
    evidence = {str(path):digest(path) for path in (RELEASE,CREDIT,PACKAGE,READY,ACTUAL,NEXT,PARENT,FAILURE,Path(__file__))}
    checkpoint(mutation=ROOT/'registered_documentation_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Rafael B241–B260 clean-first intake.',
            next_action='Finish the 198 clean drafts. Preserve B246’s earlier review, then compare 292 eligible records against Rafael3222.',
            current_batch_not_yet_integrated=True,native_job_live=False,registered_build_live=False,guide_photos=False),
        new_entries={NEXT_KEY:dict(new_credit=0,source_records=292,full_clean_census_records=310,
            ordinary_speeches=272,physical_style_alternatives=14,typed_captions=6,prior_reviewed_records=18,
            prior_reviewed_context_only_blocks=[246],source_only=True,independently_drafted_records=94,
            independent_draft_blocks=next_batch['complete_draft_blocks'],remaining_clean_meanings_anddrafts=198,
            remaining_current_comparisons=292,current_comparisons=0,full_intake_not_complete=True,evidence=evidence)},
        summary=summary,document='docs/editorial_Rafael_B221_B240_registered_20261106.md',document_text=doc,completed=15067,
        protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],
            release['parent']:release['parent_sha256'],package['zip']:package['zip_sha256']})
    print('Recorded Rafael3222, the 292 eligible next records, and 94 clean-only drafts.')


if __name__ == '__main__':
    main()

