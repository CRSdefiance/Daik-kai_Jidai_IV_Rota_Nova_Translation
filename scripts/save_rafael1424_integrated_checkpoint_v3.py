"""Save the verified release and the next clean-source editorial starting point."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

A=Path('work/analysis')
ROOT=A/'Rafael1424_extended_release_verified_v2_20261105'
INTAKE=A/'Rafael_B161_B180_clean_20261105'
CENSUS=INTAKE/'clean_source_census_v1.json'
READY=A/'Rafael557_research_final_v1_20261105/research_completion.json'
FORMAT=A/'Rafael557_story_percent_relocation_v1_20261105/qualification.json'
PACKAGE=A/'Weekend_testing_package_v1_20261105/package_verification.json'

if __name__=='__main__':
    rp=ROOT/'registered_release_verification.json';cp=ROOT/'completion_checkpoint.json'
    release,credit,census,ready,percent,package=map(load,[rp,cp,CENSUS,READY,FORMAT,PACKAGE])
    assert credit['new_credit']==557 and credit['counts']==dict(completed=13269,revised=7518,retained=5751)
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert release['complete_stack_entries']==682 and release['accepted_layers']==114 and release['passing_release_checks']==26
    assert release['all_eight_registered_final_stages_preserved'] and release['exact_all_integrated_references_bound']
    assert len(percent['relocated_source25_records'])==5 and all(r['rejected'] for r in percent['negative_cases'])
    assert census['source_objects']==741 and census['clean_meanings_andindependent_drafts']==29
    assert census['zero_already_credited_keys'] and census['zero_overlap_with_pending_or_integrated_B141_B160']
    summary=('Rafael B141–B160 is integrated and credited once: 557 reviews (235 revisions, 322 justified retentions). '
        'Cumulative 5d40f920 passed 682 manifest entries, 114 accepted layers, all eight final stages, 26 release checks, exact clean-input patch reconstruction and its own Rafael startup. '
        'The two Castor Co. punctuation fixes are included; 188 variants/193 pages were observed in targeted fixtures, and 361 variants remain offline-only. '
        'Integrated total: 13,269. Main and weekend ZIP unchanged. Next Rafael B161–B180: 741 unique clean records inventoried and the complete 29-record sailing lesson independently drafted. No current English opened for this intake.')
    detail=f'''# Registered Rafael1424 checkpoint — November 5, 2026

**557 additional records are integrated and credited once: 235 revisions and 322 justified retentions.** The ledger now records **13,269 = 7,518 revisions + 5,751 retentions**. The final manuscript, exact source/current/target bindings, findings and five individual gates are in `translations/rafael557_integrated_final_review_v1.json`. Historical source/prose count is 13,272. No other coverage credit changed.

Registered experimental candidate: `{release['candidate']}`. SHA-256: `{release['candidate_sha256']}`. Its manifest has **682 entries, all 114 accepted layers, eight final stages and 26 passing release checks**. The adjacent patch `{release['patch']}` reconstructs this exact image from the clean Japanese input. Proof: `{rp}`. All 20 owned B141–B160 blocks are present; only those SC0 blocks differ from 3bf3. All other files/components, artwork, fonts, names and runtime fixes, including the ASCII right-bound correction, are unchanged. Main 3cb8 and the delivered weekend ZIP are unchanged.

Reuse [the 557 research checkpoint](editorial_Rafael557_research_ready_20261105.md) and `{READY}` for the complete editorial, glyph, wrapping, allocation and representative scene checks. Both corrected Castor Co. lines are included. The disclosed fixtures observed 188 speech variants/193 pages, 13 of the 20 scoped names, six FE notices, both FU substitutions and all eight captions across four default menus. Another 361 variants are offline-only. The exact registered ROM passed a separate 4,001-frame cold boot to Rafael's opening, ten exact RGB pairs, own captain 0/route 0 and both original Fernan name getters. This does not establish natural conditional activation, original locations, earned chronology, a full route or hardware coverage.

The verified 673-entry prefix was reused; the new transaction and all eight original stage bodies ran. Preserve both pre-ROM failures: the first lacked a callable nested entrypoint; the second exposed five false positives from relocated source-leading 0x25 speaker selectors. The v6 final check rebinds only those exact source/target records and still executes the four-archive format-command checks, rejecting a real injected %s and all three bad binding cases. Both original and derived safety source hashes are in the final manifest. Proof: `{FORMAT}`. Keep this exact qualified source mapping for unchanged B146 in later cumulative builds. The first startup capture requested extra frames; the second reused the exact request contract, and all required pixels matched. All artifacts are preserved; no live jobs remain.

Continue with **Rafael B161–B180**, prioritizing the remaining tutorials. The clean census `{CENSUS}` has **741 unique source records (733 speeches and eight captions)**, including four two-choice menus, 14 label-free controls and no personality objects. No keys overlap earlier credit or B141–B160. The complete **29-record B180 sailing lesson** has clean meanings and independent drafts at `{INTAKE/'B180_sailing_lesson_clean_drafts_v1.json'}`, including both responses to the instructor and the explanation of sails, attachments and wind angle. Current comparisons, approved nautical/UI terms and all gates remain pending. Continue substantial complete exchanges from the clean packet. Do not relabel old wording or draft coverage as new approval.

Every other storyline, shared shop/town/random exchange, name and player-facing text remains in scope. The two full-catalogue particle fixes, deferred graphics artwork and the later older-record technical re-audit remain separate. No guide photography, pruning or main promotion.
'''
    checkpoint(mutation=A/'Rafael1424_integrated_documentation_checkpoint_v3_20261105',batch_key=credit['family'],
        batch_updates=dict(new_credit=0,registered=True,experimental_not_promoted=True,exact_clean_patch_verified=True,own_startup_verified=True),
        new_entries={'Rafael_SC0_B161_B180_clean_20261105':dict(new_credit=0,source_objects=741,speeches=733,typed_captions=8,
            complete_blocks=list(range(161,181)),clean_census=str(CENSUS),clean_census_sha256=sha(CENSUS.read_bytes()),
            clean_source_packet=str(INTAKE/'clean_source_packet.json'),clean_choice_objects=str(INTAKE/'clean_choice_objects.json'),
            independently_drafted_records=29,independent_draft_blocks=[180],remaining_clean_meanings_anddrafts=712,
            all_current_comparisons_andfive_gates_pending=True,source_only_no_current_English_extracted=True)},
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Rafael B161–B180 clean source census; 29-record sailing lesson drafted.',
            next_action='Draft and compare remaining complete Rafael exchanges, prioritizing the sailing and related tutorials. Bind exact current UI terms, macros and names after clean-first drafts.',
            current_batch_not_yet_integrated=True,previous_Rafael557_batch_integrated=True,
            registered_integration_pending=False,registered_build_live=False,native_job_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Rafael1424_registered_checkpoint_v3_20261105.md',document_text=detail,completed=13269,
        protected={'translations/release_stack.json':release['registry_sha256'],'dk4tool/rom/nds.py':'27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963',
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
            release['candidate']:release['candidate_sha256'],release['parent']:release['parent_sha256'],package['zip']:package['zip_sha256']})
    print('Saved verified Rafael1424/13269 checkpoint and 741-record clean intake. All prior work, main and weekend ZIP preserved.')
