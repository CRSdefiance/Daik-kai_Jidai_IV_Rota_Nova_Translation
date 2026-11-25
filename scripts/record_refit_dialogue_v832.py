"""Record source/context/prose progress; keep unverified release gates open."""

from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.context_refit_dialogue_v832 import IDS, ROOT, ROM
from scripts.review_refit_dialogue_v832 import MANUSCRIPT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/refit_dialogue_v832_context.md')
LEDGER = Path('translations/editorial_review_current_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V832 Refit dialogue source and context')


def main():
    assert not DOC.exists()
    ledger, manuscript = read(LEDGER), read(MANUSCRIPT)
    context, actual = read(ROOT / 'native_context.json'), read(ROOT / 'actual_rename_context.json')
    assert ledger['records_editorially_completed'] == 634 and ledger['records_with_source_and_prose_pass'] == 637
    assert ledger['current_integrated_candidate']['sha256'] == context['candidate_sha256'] == actual['candidate_sha256'] == sha(ROM.read_bytes())
    assert len(context['all208_native_voice_selections']) == 208
    assert len(context['all256_duration_byte_argument_contracts']) == 256
    assert len(context['percentage_argument_contracts']) == 10
    assert sha(Path(actual['contact_sheet']).read_bytes()) == actual['contact_sheet_sha256']
    actual.update(visual_review_pending=False, visual_review={
        'five_screen_question_selection_invitation_keyboard_cancel_sheet_opened': True,
        '1264_1265_complete_visible_letters_and_alignment_reviewed': True,
        'keyboard_Japanese_input_characters_preserved_as_functional_choices': True,
        'no_new_translated_wording_or_helper_discount_scene_claimed': True})
    save(ROOT / 'actual_rename_context.json', actual)
    rom, clean, canonical = [NdsImage.open(p) for p in (ROM, 'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    manuscript.update(current_COMMON_sha256=sha(rom.read_file('/COMMON/MESFILE.DK4')),
                      current_ARM9_sha256=sha(rom.read_file('/__arm9__.bin')),
                      source_clean_COMMON_sha256=sha(clean.read_file('/COMMON/MESFILE.DK4')),
                      source_canonical_COMMON_sha256=sha(canonical.read_file('/COMMON/MESFILE.DK4')))
    assert tuple(r['message_id'] for r in manuscript['records']) == IDS
    assert all(not r['review']['formatting'] for r in manuscript['records'])
    assert all(all(r['review'][g] for g in ('source', 'context', 'localization', 'naturalness')) for r in manuscript['records'])
    save(MANUSCRIPT, manuscript)
    prose = read(ROOT / 'source_review.json')
    prose['manuscript_sha256'] = sha(MANUSCRIPT.read_bytes())
    save(ROOT / 'source_review.json', prose)
    capacity = read(ROOT / 'runtime_capacity_research.json')
    capacity.update(later_registered_owners=[
        'dk4tool/patch/recruitment_quantity_runtime.py:compact Thumb quantity helper',
        'dk4tool/patch/recruitment_editorial_runtime.py:consolidated dispatch and status data',
        'dk4tool/patch/tavern_editorial_runtime.py:literal GATE at0214797C',
        'dk4tool/patch/inn_editorial_runtime.py:latest compact parent/ID contract table'],
        current_scope_contract_note='Inn table uses142 of144 bytes. Adding a direct1263-1267 range and original queued table8680 requires additional exact memberships;find proven owned capacity/encoding rather than broadening IDs or overwriting old code.',
        current_quantity_contract_note='Existing compact helper is private to six price callers and one day caller. New return02017B90 must be explicitly recognized as days,not the default gold coins. Preserve all seven old caller results and closure tests.',
        old_bank_tails_not_free=True)
    save(ROOT / 'runtime_capacity_research.json', capacity)
    corrections = read(ROOT / 'research_corrections.json')
    corrections['raster_probe_signature_correction'] = 'Use raster(ARM9,text,01FFCE40-BASE,size=(228,64));228 and64 are not its entry/tracking arguments. Original captured frames were not rerun or retimed.'
    corrections['old_runtime_reuse_assumption_rejected'] = 'Current quantity/dispatcher/literal bytes differ from the initial Shipyard assembler because later registered consumers own those spans. No restoration or runtime patch was applied.'
    save(ROOT / 'research_corrections.json', corrections)
    save(ROOT / 'ledger_before_V832.json', ledger)
    entry = {
        'documentation': str(DOC), 'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'native_message_IDs': list(IDS), 'proposed_revisions': 11, 'justified_retained_wordings': 1,
        'native_context_proof': str(ROOT / 'native_context.json'),
        'actual_rename_context': str(ROOT / 'actual_rename_context.json'),
        'runtime_capacity_research': str(ROOT / 'runtime_capacity_research.json'),
        'status': '12-source-context-prose-reviewed-format-units-integration-helper-scene-pending',
        'remaining_gates': [
            'Extend exact current direct/queued formatter memberships without erasing later registered runtime work',
            'Scoped number-plus-day/days argument at original02017B90;preserve earlier seven callers',
            'All generated layouts/native fonts/scope and negative controls',
            'Registered combined ROM,exact clean-input patch,and actual revised helper/discount/duration and rename samples'],
        'no_completed_entry_credit': True, 'current_ROM_unchanged': str(ROM), 'full_goal_complete': False}
    ledger['refit_dialogue_v832'] = entry
    ledger['research_checkpoints'].append({'id': 'V832-Refit-dialogue-source-context-and-rename', **entry})
    ledger['records_with_source_and_prose_pass'] = 649
    ledger['records_with_source_prose_drafts'] = 649
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4'] = 648
    ledger['reviewed_but_incomplete_COMMON_IDs'] = [750, 751, 752, *IDS]
    ledger['active_source_prose_drafts'] = {
        'native_message_IDs': [750, 751, 752, *IDS],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json', str(MANUSCRIPT)],
        'status': 'three-older-context-unmapped-and12-Refit-runtime-release-pending',
        'note': 'These15 are reviewed drafts only,not the full remaining goal. Unreviewed shared/route/player prose and raw-source coverage stay open.'}
    ledger['findings'].append({'id': 'COMMON1256-1267-Refit-source-voice-units-and-prose',
                               'file': '/COMMON/MESFILE.DK4', 'native_message_IDs': list(IDS),
                               'status': entry['status'], 'proof': entry['native_context_proof'],
                               'detail': 'Restore Admiral and voice-specific refit offers,calculation bridge and complete selection questions. IC is first person;native duration argument lacks a unit. Old runtime tails already belong to later features.',
                               'no_completion_credit': True})
    ledger['latest_checkpoint'] = (
        'V832 freshly reviews12 shared Shipwright/refit messages1256-1267:11 proposed revisions andone justified retention. '
        'All208 native actor voice selections,original missing-slot fallback,10 source discount arithmetic/argument cases andall256 duration-byte arguments are mapped. '
        'Two ordinary14000/14600-frame cold boots prove original1264/1265 visible complete glyphs,the separate ship-selection/name invitation/keyboard sequence and normal cancel;five ship names and25975 funds remain exact. '
        'Current V831 stays unchanged. The proposed duration needs a scoped day/days argument and current formatter membership extension;initial old-bank reuse assumptions were rejected because later Tavern/recruitment/Inn code owns those spans. '
        '634 completed entries remain;649 source-prose reviewed;15 reviewed drafts pending,not a full remaining-work count. '
        'All other shared/route/player prose,raw-record coverage and separate graphics/all18-plaque work remain open;full goal active.')
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values()) == 649
    assert ledger['records_revised_and_integrated'] == 456 and ledger['retained_wordings_editorially_completed'] == 178
    save(LEDGER, ledger)
    DOC.write_text('''# V832: Refit dialogue source/context review

Twelve original COMMON messages1256-1267 are freshly reviewed:11 proposed
revisions andone justified retention. The manuscript is natural-dialogue-v2 with
individual source/context/localization/naturalness reviews. Formatting remains
false on every record: these are not production-approved translations yet.

## Source and voices

The original role13 is 船大工, displayed as Shipwright. Positive refit cost,
an assigned officer and native ability at least25 gate the helper offer. The
original eight-slot table at02118680 selects1256,missing,1257-1262. All208 native
actor lookups pass. The missing voice1 slot falls back to1256; it is not silence.
Seven distinct offers preserve Admiral, additive offers, confidence, a measured
older voice and hesitation without invented kinship or caricature. IC is the
character-dependent first-person pronoun (僕/アタシ), not an omitted actor name.

Original source fragments prove ten supplied ability/discount cases and all256
duration-byte arguments. The discount is ability divided by5; the refit price is
reduced before the separate final-price confirmation. These supplied-register
contracts do not establish earned eligibility or actual helper activation.
1263 retains its percentage and the following calculation bridge.1267 currently
receives only a full-width number. Its proposed The refit will take %s requires
a narrowly scoped number-plus-day/days argument before release; never ship that
draft with the current bare-number argument.

## Actual Rename context

Separate14000/14600-frame ordinary cold boots use disposable copies of the
existing Copenhagen fixture save. No new code/RAM fixture or savestate. Actual
1264 asks which ship to rename; after ship selection1265 invites a desired name,
then native keyboard entry appears. Both prompts have complete matching native,
independent and actual glyph planes at x22/y296. Cancellation returns normally,
all five ship names/Hull/Crew model states remain unchanged and funds stay25975.
The five-screen sheet was visually reviewed. The keyboard's hiragana are input
character choices, not untranslated dialogue; controls remain English. No new
draft wording or helper/discount/duration scene is claimed tested.

## Next implementation

Preserve the current runtime. Exact comparisons rejected reusing initial V759
shipyard bytes: later registered Tavern/recruitment and Inn code occupies those
banks. The existing compact dispatcher contract uses142 of144 bytes; add exact
new direct1263-1267 and queued02118680 memberships through a proven allocation or
encoding change. Do not broaden to unrelated IDs to make the table fit.

The compact quantity helper is private to six price callers and one duration
caller. A new caller at original return02017B90 must explicitly select days;
merely routing it to that helper would select the default gold-coin unit. Preserve
all seven earlier callers and prove new scope/closure, native glyphs, generated
wraps, buffers and ABI. No section, staged123040-byte payload, cache, BSS or
allocator growth is authorized by this research. No runtime bytes were changed.

Native probes corrected an initial missing-slot/silent assumption, the displayed
role label, a mistaken call to a literal pointer, and a raster-helper signature.
The corrections and earlier drafts are retained. Captures were not restarted or
retimed to accommodate failed verifier assumptions.

Current integrated candidate remains V831.634 entries are completed;649 have
source/prose review;15 reviewed drafts await further work, including older750-752.
Those counts do not enumerate all remaining shared/route/player prose. Registered
integration, exact patch, actual revised helper/discount/duration and Rename
samples remain. Graphics and all18 plaques remain separately unfinished.
''', encoding='utf-8')
    paragraph = '\n\n## V832: Refit dialogue source/context review\n\n' + ledger['latest_checkpoint'] + ' See [V832 evidence](refit_dialogue_v832_context.md).\n'
    for path in ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md'):
        with Path(path).open('a', encoding='utf-8') as handle:
            handle.write(paragraph)
    sources = [Path(__file__), DOC, LEDGER, MANUSCRIPT,
               *map(Path, ('scripts/context_refit_dialogue_v832.py', 'scripts/review_refit_dialogue_v832.py',
                           'scripts/run_refit_rename_context_v832.py', 'scripts/run_refit_name_entry_v832.py',
                           'scripts/verify_refit_rename_context_v832.py',
                           'docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md')),
               *ROOT.glob('*.json'), *ROOT.glob('*.png')]
    save(ROOT / 'source_program_manifest.json', {str(p): sha(p.read_bytes()) for p in sources})
    sources.append(ROOT / 'source_program_manifest.json')
    archive = []
    for source in sources:
        target = ARCHIVE / source.absolute().relative_to(Path.cwd())
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        archive.append({'source': str(source), 'archive': str(target), 'sha256': sha(target.read_bytes())})
    save(ROOT / 'archive_manifest.json', {'archive': str(ARCHIVE), 'files': archive,
                                         'all_copies_hash_verified': True, 'not_guide_promoted':'Source-wording context captures only;new wording not integrated.',
                                         'previous_goal_turn_classification':'progress:V831 integrated31 Refit descriptions and verified native/actual/patch',
                                         'this_goal_turn_classification':'progress:12 source/prose reviews,native voices/arguments,actual Rename context and current-runtime ownership diagnosis'})
    copy2(ROOT / 'archive_manifest.json', ARCHIVE / 'archive_manifest.json')
    print('V832 recorded:634 completed/649 source-prose/15 reviewed drafts pending. V831 unchanged;E archive verified;goal active.', flush=True)


if __name__ == '__main__':
    main()
