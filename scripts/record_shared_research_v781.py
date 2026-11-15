"""Record 50 reviewed drafts and native preview evidence, without release credit."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.context_shared_dialogue_v781 import ROOT, CURRENT
from scripts.review_shared_dialogue_v781 import MANUSCRIPT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/shared_dialogue_v781_research.md')
LEDGER = Path('translations/editorial_review_current_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V781 Shared prose research')


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert sha(source.read_bytes()) == sha(target.read_bytes())


def main():
    manuscript = read(MANUSCRIPT)
    context = read(ROOT/'native_context.json')
    layout = read(ROOT/'layouts_v2/verification.json')
    visual = read(ROOT/'layouts_v2/visual_review.json')
    latest = read('out/editorial_review_latest.json')
    digest = sha(CURRENT.read_bytes())
    assert digest == latest['sha256'] == context['candidate_sha256'] == layout['candidate_sha256']
    assert len(manuscript['records']) == 50
    assert [r['message_id'] for r in manuscript['records']] == list(range(1020, 1070))
    assert sum(r['decision'] == 'revise' for r in manuscript['records']) == 34
    assert sum(r['decision'] == 'retain' for r in manuscript['records']) == 16
    assert all(all(v for k, v in r['review'].items() if k != 'formatting') and not r['review']['formatting'] for r in manuscript['records'])
    assert layout['manuscript_sha256'] == sha(Path(MANUSCRIPT).read_bytes())
    assert layout['native_layouts'] == 857 and not layout['findings']
    assert len(layout['complete_font_planes']) == 83 and len(layout['sheets']) == 9
    assert visual['all_nine_sheets_visually_reviewed'] and visual['all83_native_font_planes_preserved_exactly_in_composites']
    assert visual['native_verification_sha256'] == sha((ROOT/'layouts_v2/verification.json').read_bytes())
    assert all(sha(Path(r['path']).read_bytes()) == r['sha256'] for r in layout['complete_font_planes']+layout['sheets'])
    assert len(context['all624_original_actor_voice_selections']) == 624
    assert len(context['all21_private_barmaid_speeches']) == 21
    assert len(context['all24_village_coordinate_providers_two_modes']) == 48
    assert len(context['all570_unknown_fleet_town_argument_fragments']) == 570
    assert len(context['native_headcount_strings']) == 10
    assert context['all50_context_IDs'] == list(range(1020, 1070))
    protected = dict(read('work/analysis/barmaid_integration_v780/checkpoint.json')['protected_files_unchanged'])
    protected[str(CURRENT)] = digest
    protected[str(CURRENT.with_suffix('.xdelta'))] = latest['patch_sha256']
    registry_sha = sha(Path('translations/release_stack.json').read_bytes())
    for path, pin in protected.items():
        assert sha(Path(path).read_bytes()) == pin, path
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 367
    assert ledger['records_revised_and_integrated'] == 259
    assert ledger['retained_wordings_editorially_completed'] == 108
    assert ledger['records_with_source_and_prose_pass'] in (370, 420)
    completed = {n for family in ledger['completed_editorial_families'] for n in family['native_message_IDs']}
    assert completed.isdisjoint(range(1020, 1070))
    if ledger['records_with_source_and_prose_pass'] == 370:
        save(ROOT/'editorial_ledger_before_v781.json', ledger)
    else:
        assert (ROOT/'editorial_ledger_before_v781.json').exists()
    ledger['records_with_source_and_prose_pass'] = 420
    ledger['records_with_source_prose_drafts'] = 420
    ledger['active_source_prose_drafts'] = {
        'native_message_IDs': [750, 751, 752, *range(1020, 1070)],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json', str(MANUSCRIPT)],
        'status': '750-752-context-unmapped;1020-1069-source-context-prose-and-prospective-layout-reviewed;production-and-gameplay-pending',
        'note': '50 new drafts receive no completion credit. All formatting approvals remain false until actual consumer eligibility, owned production routing, copies, registered integration, exact patch and representative gameplay pass.'}
    ledger['coverage_units'][0]['next'] = 'Close V781 original caller filters and role/portrait-core bindings, integrate 50 drafts through owned no-growth routing, and verify production layouts, copies, exact patch and actual scenes. Then continue COMMON 1070 onward, resolve 750-752, and review wider shared/all-route/player-facing prose. Preserve the separate graphics audit and older-record follow-up.'
    ledger['latest_checkpoint'] = 'V781 reviews 50 shared entries: 34 proposed revisions and 16 retained wordings. Original voice tables, roles, coordinate/town/count providers and 21 private barmaid topics are mapped. 857 prospective native layouts and 83 independent full font planes pass; nine preview sheets were reviewed. Two weak line endings were repaired through natural rephrasing. Production routing, caller eligibility and actual scenes remain pending. 420 source/prose passes, 53 active drafts and 367 completed entries; V780 remains the latest ROM. The full editorial goal and separate graphics audit remain unfinished.'
    checkpoint = {'id': 'V781-shared-source-prose-and-native-layout-research', 'documentation': str(DOC),
                  'new_source_prose_records': 50, 'draft_revisions': 34, 'retained_wordings': 16,
                  'new_editorially_completed': 0, 'new_ROM': False, 'manuscript': str(MANUSCRIPT),
                  'native_context': str(ROOT/'native_context.json'), 'prospective_layouts': str(ROOT/'layouts_v2/verification.json'),
                  'visual_review': str(ROOT/'layouts_v2/visual_review.json'),
                  'remaining_gates': ['Original caller filters and role/portrait-core bindings', 'Owned no-growth production routing',
                                      'Production layouts and complete native copies', 'Registered combined ROM and exact patch',
                                      'Representative actual scenes, control pixels and transitions'], 'full_goal_complete': False}
    if not any(r['id'] == checkpoint['id'] for r in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(checkpoint)
    save(LEDGER, ledger)
    latest['latest_research_checkpoint'] = str(DOC)
    save('out/editorial_review_latest.json', latest)
    DOC.write_text('''# V781: the next 50 shared dialogue entries reviewed

COMMON 1020–1069 now have clean Japanese, exact current references, source glosses
and editorial decisions: 34 proposed revisions and 16 retained wordings. These are
drafts. All 50 formatting approvals remain false until production and gameplay
verification. 420 entries have source/prose review, including 53 active drafts;
367 are completed (259 revised and 108 retained). V780 remains the latest ROM.
The full editorial goal and the separate graphics audit are still unfinished.

## Meaning and natural English

- 1020–1027 retain the natural missing-information and low-success warnings, with
  the original strength and voice distinctions. Four warning sites use the same
  role-2 voice table. They ask permission before the original scheme is scheduled.
- 1028–1034 distinguish village coordinates from town names, and a fleet's current
  anchorage from its destination. Unknown fleets are not newly called pirates or
  assigned a faction. Hearsay is retained where the source uses it.
- 1035–1048 replace padded fragments with complete conversational prompts. The
  speaker is the **barkeep**, who offers to recruit for the player's crew. Required
  crew shortfall is kept separate from spare cabin capacity. Number-neutral wording
  works for one as well as larger counts, without inventing a plural suffix.
- 1049–1069 restore personal details and natural voice: limited interest in romance,
  a wish to surpass Mom, pleasure in cooking, help for a hard-working mother after
  Dad left, daydreams, the wait for a sailor, a childhood wish to be a princess,
  younger siblings, strategic deference, an interest in steering a ship and the
  parrot that the player gave her. No death, retirement, wedding, new relative,
  collective escape for siblings or pet sex is invented. The complimentary drink
  is her original offer, not a new refund or game mechanic. Character opinions
  remain character dialogue. Already natural wording is retained.

All prose uses natural-dialogue-v2 and American English. Each record has its own
Japanese source, gloss, speaker/context note and editorial decision. Approved names
and every runtime actor name remain unchanged. No manual alignment or line break
is authored. Neighboring stored messages are not treated as sequential dialogue.

## Original context and providers

624 native selections cover all 208 actor/current-captain objects across three
original voice tables; three null fallbacks are also checked. Four original
low-success call sites, the no-information branch and both recruitment-continuation
call sites reach the unchanged original wrappers. The recruitment initializer
sets role 1 for both continuation prompts. Original ABF50 formats the difference
between the required crew or capacity and the recruited total. Twenty supplied
native difference fragments cover ten positive decimal-width examples.

Twenty-one actual barmaid catalog entries select all 21 private topics through
58F24, native actor index plus 863. This is the second chance branch in 591D0 after
the gift/relationship stage, distinct from the casual topics reviewed in V780.
48 original village fragments cover all 24 points in both NPC modes. 570 original
unknown-fleet fragments cover 114 town-name providers and all five variants.

These are original CPU fragments with declared town, count and mode inputs. They
establish meanings, arguments and callers, not earned events, complete eligibility
filters or actual player-visible scenes. Full caller/portrait-core eligibility is
still a release gate. All compared executable spans remain exact to clean source.

Two research assumptions were corrected before recording results: the role value
must be established through its original initializer, and B6618 returns a town
object rather than a numeric index. The village caller now uses the original town
object offset, with its bounds and stride checked. No ROM bytes were changed.

## Prospective formatting and visual review

857 native printf/layout cases preserve every expanded byte and complete word,
guards, argument copies and the saved-register contract. Cases cover the captured
town names and village coordinates, original full-width decimal counts and explicit
width stress values, including zero and a large signed-positive boundary. Stress
counts are not claims about physically available crew or the source branch's
positive-count eligibility. The existing native font correctly renders these
original numeric strings. Number-neutral prose avoids the one-sailor/plural trap.

Village coordinates contain a leading LF and alignment spaces. The CPU prototype
explicitly selects the existing scoped coordinate-compaction helper, preserving
complete N/S/E/W numbers and the source argument copies. This does not prove the
future dispatcher will select that helper for 1028/1029. The global coordinate
provider is not edited. Production ownership, exact membership and actual routing
must still be proved.

The first pass found two weak line endings, after an article and a preposition.
Natural rephrasing of Donna's daydream and Benazir's self-question repaired them
without dropping facts. The first manuscript, source programs and failed preview
artifacts are retained as research. The second pass has zero layout findings.

83 complete native font planes independently match the game font. All nine sheets
were visually reviewed for complete first/final letters, margins, bounds and fluent
line breaks. Every enlarged card is pixel-identical to its saved native plane;
three full-resolution standalone checks also confirm the leading letters. These
are CPU previews, not new in-game screenshots or production-formatting approval.

## Next gates and preservation

Finish original caller/filter and role/portrait-core eligibility; establish scoped
production routing without section, cache, arena or staged-payload growth; verify
all production outputs and complete native copies; build through the registered
combined release and reconstruct the exact clean-input patch. Then test warnings,
both recruitment continuations, rumors and personal topics with representative
actual conversations, controls and normal scene returns. User-approved fixtures
may make rare states reachable, with explicit provenance and protected donor copies.

All 50 drafts receive zero completed-entry credit until those gates pass. COMMON
1070 onward, drafts 750–752, all route scenes and other player-facing prose remain
in scope. The two older route leads observed in V780 remain queued. The separate
graphics audit, its 18 original plaques, excluded Online bodies and preserved brown
marks are unchanged. Revisit the older record-based checks at full goal completion.

V780, its exact patch, the registry, canonical base, clean ROM and original donors
remain unchanged. Research and previews are archived under E:/Rota Nova
translations/Editorial review/V781 Shared prose research. They are not promoted as
guide screenshots. No GitHub commit or push was performed.
''', encoding='utf-8')
    heading = '## V781: 50 shared dialogue drafts and native layout research'
    section = f'\n\n{heading}\n\n50 entries receive source/context/prose review: 34 proposed revisions and 16 retained wordings. Original roles, three voice tables, 624 actor selections, 21 barmaid topics, 48 village-coordinate and 570 town-name fragments are mapped. 857 prospective layouts and 83 complete independent font planes pass; nine sheets are visually reviewed. Two weak line endings were repaired naturally. Production routing, caller eligibility, copies, patch and gameplay remain required. 420 source/prose passes, 53 drafts and 367 completed entries; V780 stays current. Wider prose and the separate graphics audit remain open. See [V781 research](shared_dialogue_v781_research.md).\n'
    for name in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs')/name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip()+section, encoding='utf-8')
    save(ROOT/'checkpoint.json', {'research': checkpoint, 'latest_ROM_unchanged': latest,
                                  'registry_sha256': registry_sha, 'protected_files_unchanged': protected,
                                  'goal_status': 'active', 'full_goal_complete': False,
                                  'producer_sha256': sha(Path(__file__).read_bytes())})
    for path in ROOT.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE/'evidence'/path.relative_to(ROOT))
    for path in (MANUSCRIPT, LEDGER, DOC, Path('out/editorial_review_latest.json'),
                 Path('scripts/context_shared_dialogue_v781.py'), Path('scripts/review_shared_dialogue_v781.py'),
                 Path('scripts/probe_shared_layout_v781.py'), Path(__file__).resolve().relative_to(Path.cwd().resolve())):
        copy(path, ARCHIVE/path)
    files = {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
             if p.is_file() and p.name != 'archive_manifest.json'}
    save(ARCHIVE/'archive_manifest.json', {'latest_ROM_unchanged': latest, 'files': files, 'full_goal_complete': False})
    assert all(sha((ARCHIVE/p).read_bytes()) == pin for p, pin in files.items())
    assert sha(CURRENT.read_bytes()) == digest and sha(Path('translations/release_stack.json').read_bytes()) == registry_sha
    print('V781 archived: 50 drafts,420 source/prose passes,53 active drafts;367 completions and V780 remain unchanged.', flush=True)


if __name__ == '__main__':
    main()
