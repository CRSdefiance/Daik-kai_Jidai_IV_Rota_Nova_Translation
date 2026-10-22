"""Record source/prose progress with unfinished native UI and release gates."""

from copy import deepcopy
from pathlib import Path
from shutil import copy2

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.finish_refit_display_v712 import load
from scripts.prepare_personal_chatter_v835 import ROOT, ROM, MANUSCRIPT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/personal_chatter_v835_checkpoint.md')
LEDGER = Path('translations/editorial_review_current_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V835 Personal chatter source and context')


def main():
    assert not DOC.exists()
    ledger, doc, plan = read(LEDGER), read(MANUSCRIPT), read(ROOT / 'Rafael_context_run_plan.json')
    assert ledger['records_editorially_completed'] == 646 and ledger['records_with_source_and_prose_pass'] == 649
    assert sha(ROM.read_bytes()) == ledger['current_integrated_candidate']['sha256'] == plan['ROM_sha256']
    assert len(doc['records']) == 25 and sum(r['editorial_decision'] == 'revise' for r in doc['records']) == 18
    assert all(all(v for k, v in r['review'].items() if k != 'formatting') and not r['review']['formatting'] for r in doc['records'])
    assert all(r['english'] == ' '.join(r['english'].split()) and r['english'].isascii() for r in doc['records'])
    assert sha(Path(doc['native_context_proof']).read_bytes()) == doc['native_context_proof_sha256']
    assert sha(Path(doc['normal_activity_context_proof']).read_bytes()) == doc['normal_activity_context_proof_sha256']
    report, shots, receipt = load(Path(plan['folder']), plan['ROM_sha256'], 16800)
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    assert sha(Path(plan['source_donor']).read_bytes()) == sha(Path(plan['disposable_source']).read_bytes()) == plan['source_donor_sha256']
    assert report['battery_save_preloaded']['source_sha256'] == plan['source_donor_sha256']
    for row in report['read_only_capture_RAM_snapshots'] + report['read_only_pause_RAM_snapshots']:
        assert row['read_only_export'] and sha(Path(row['path']).read_bytes()) == row['sha256']
    old = []
    for tag, path in [('canonical', Path('out/raphael_natural_v2_accepted_base.nds')), ('V92', Path('out/all_routes_combined_v92_candidate.nds'))]:
        rom = NdsImage.open(path)
        entries = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), clean=False)
        old.append({'baseline': tag, 'path': str(path), 'sha256': sha(path.read_bytes()),
                    'entries': [{'message_id': n, 'text_hex': entries[n].text.hex(), 'English': entries[n].text.decode('ascii')} for n in (1365, 1366)]})
    save(ROOT / 'historical_defect_baselines.json', {'baselines': old,
        'same_unrelated_split_lookout_sentence_already_in_both_baselines': old[0]['entries'] == old[1]['entries'],
        'not_a_new_V834_regression': True})
    selected = [9600, 10400, 11200, 14000, 15200, 16800]
    sheet = Image.new('RGB', (768, 824), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, f in enumerate(selected):
        x, y = i % 3 * 256, i // 3 * 412
        draw.text((x + 5, y + 6), f'Current V834 baseline {f}', fill='white')
        sheet.paste(shots[f], (x, y + 28))
    image_path = ROOT / 'ordinary_Deck_navigation_baseline.png'
    sheet.save(image_path)
    save(ROOT / 'baseline_context_verification.json', {
        'current_ROM': str(ROM), 'ROM_sha256': plan['ROM_sha256'], 'capture_receipt': receipt,
        'terminal16800_frame_cold_boot_no_savestate_or_new_RAM_code_fixture': True,
        'original_and_disposable_source_saves_unchanged': True,
        'actual_scope': 'Port supply-dialog cancellations,ordinary quick-menu Deck entry,room navigation,Helm personnel picker and normal return. No actual1361-1385 activity-line activation or revised words claimed.',
        'initial_Hodram_schedule_reached_Rafael_supply_flow_and_was_navigated_normally': True,
        'native_selector_is_a_distinct_embedded_consumer_not_portrait_modal': True,
        'review_sheet': str(image_path), 'review_sheet_sha256': sha(image_path.read_bytes()),
        'visual_review_pending': True, 'no_editorial_completion_credit': True})
    save(ROOT / 'editorial_ledger_before_checkpoint.json', ledger)
    native_ids = list(range(1361, 1386))
    prior_ids = set(ledger['active_source_prose_drafts']['native_message_IDs'])
    assert not prior_ids.intersection(native_ids)
    ledger['records_with_source_and_prose_pass'] = 674
    ledger['records_with_source_prose_drafts'] = 674
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4'] = 673
    ledger['reviewed_but_incomplete_COMMON_IDs'] = sorted(prior_ids | set(native_ids))
    ledger['active_source_prose_drafts']['native_message_IDs'] = sorted(prior_ids | set(native_ids))
    ledger['active_source_prose_drafts']['manuscripts'].append(str(MANUSCRIPT))
    ledger['active_source_prose_drafts'].update(status='three-older-context-unmapped-and25-actor-chatter-native-UI-release-pending',
        note='28 reviewed pending drafts are not the full remaining scope. All unreviewed shared/route/player prose and raw native coverage remain.')
    finding = {'id': 'COMMON1365-1366-unrelated-split-lookout-sentence',
        'native_message_IDs': [1365, 1366], 'status': 'source-and-native-actor-context-mapped-repair-pending',
        'detail': 'Janus4 should acknowledge a good story;Claudio5 should count99-102 with exertion. Current text instead splits an unrelated lookout report across independent actor messages. Both canonical baseline and V92 already have the defect. Proposed repairs are source-reviewed but not yet in a registered ROM.',
        'source_context': str(ROOT / 'native_context.json'), 'normal_activity_context': str(ROOT / 'normal_activity_path.json'),
        'historical_evidence': str(ROOT / 'historical_defect_baselines.json'), 'no_completion_credit': True}
    assert not any(f.get('id') == finding['id'] for f in ledger['findings'])
    ledger['findings'].append(finding)
    checkpoint = (
        'V835 source/prose-reviews25 independent actor comments1361-1385:18 proposed revisions and7 justified retentions. '
        'Native original selector1361+actor is proved for all25,with25 activity-function and25 normal state1 calls beyond the initial25 parameter3 controls. '
        'Janus1365 and Claudio1366 contain an unrelated split lookout report already present in V92/canonical;their correct source meanings and speakers are mapped. '
        'The25 drafts restore counts,exertion,source sounds,training and other omitted meaning in natural English. '
        'A terminal16800-frame ordinary current-ROM Rafael test-save cold boot maps Deck entry,room navigation,personnel picker and normal return without new RAM/code fixtures;no affected activity line or revised wording is claimed displayed. '
        'Distinct embedded Deck bounds,automatic wrapping/full native fonts,actual revised activity samples,registered combined ROM/patch and completion credit remain pending. '
        'V834 remains current with646 complete;674 source/prose reviewed and28 reviewed drafts pending,not the full remaining scope. '
        'All remaining shared/route/player prose,raw native coverage and separate graphics/all18 plaques remain open;full goal active.')
    ledger['personal_chatter_v835'] = {'status': doc['status'], 'manuscript': str(MANUSCRIPT),
        'source_context': str(ROOT / 'native_context.json'), 'normal_activity_path': str(ROOT / 'normal_activity_path.json'),
        'baseline_context': str(ROOT / 'baseline_context_verification.json'), 'documentation': str(DOC),
        'remaining_gates': doc['remaining_gates'], 'no_completed_entry_credit': True}
    ledger['latest_checkpoint'] = checkpoint
    ledger.setdefault('research_checkpoints', []).append({'id': 'V835-actor-specific-Deck-comments',
        'native_message_IDs': native_ids, 'manuscript': str(MANUSCRIPT), 'documentation': str(DOC),
        'source_prose_pass': True, 'formatting_and_release_pending': True, 'completed_entries_added': 0})
    before = read(ROOT / 'editorial_ledger_before_checkpoint.json')
    assert ledger['unresolved_graphics_work'] == before['unresolved_graphics_work']
    assert ledger['current_integrated_candidate'] == before['current_integrated_candidate']
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values()) == 674
    assert not ledger['full_goal_complete'] and ledger['records_editorially_completed'] == 646
    save(LEDGER, ledger)
    DOC.write_text('''# V835: actor-specific Deck comment review

Twenty-five independent comments1361-1385 are reviewed from the clean Japanese
against current V834. The v2 manuscript records faithful glosses,individual
source/context/localization/naturalness gates and18 proposed revisions/7
retentions. Every formatting gate stays false. No ROM or release profile changes.

## Inherited source defects

Janus4's1365 is an affirmative comment about a good story/account. Claudio5's1366
counts99,100,101 and strains to reach102. Current English instead splits an
unrelated lookout report between the two independent selections. The exact same
bad strings exist in both the canonical baseline and V92. This is an inherited
content defect,not evidence that V834 introduced new text corruption.

Other proposals restore exertion,slurred delight,humming,realization,habitual
appraisal,the constant-training resolve,medicine mixing,nodding sleep and other
omitted meaning. Lil's approved Camille spelling and seven natural existing lines
are retained. Character voice is localized in simple natural American English.
Nothing is shortened to imitate an old allocation,and no line positions are authored.

## Native context and distinct renderer

Original12104 initially proves1361+actor for parameter3 and actors0-24. A further
source trace proves original12838 selects the same25 independent IDs and is
reached by the normal12104 state1 branch in the captured global context. Those50
complete native ABI calls also pass. COMMON copy is intercepted only after ID
selection;these are selector proofs,not actual text/display/eligibility evidence.
The initial parameter3 probe is supplementary,not the sole normal-path argument.

The normal Deck list callback0201CB6C forwards state through02013DCC,
02015948,02015334 and02015478. The selected text is expanded through original
02053914 with the same actor object and drawn at020154CC through embedded
020D5404. It is not the ordinary progressive portrait dialogue consumer. The
draw suppliesY60 inside its own window;absolute text origin,bounds,wrapping,
palette,crops and full first/final letters still need native/actual calibration.
Global context fields are not labeled day/night without further evidence.
The captured Fernando name8265+ernando is valid CP932 fullwidth F plus ernando;
the initial ASCII-only diagnostic was misleading and no name defect is claimed.

## Current-ROM navigation baseline

A terminal16800-frame ordinary cold boot uses a disposable copy of the retained
Rafael V440 test donor. Earned progression/unlocks are not inferred. The reused
Hodram schedule initially reaches Rafael's supply flow;ordinary cancellations
then reach the quick menu,Deck,room navigation,Helm personnel picker and normal
town return. No new RAM/code fixture or savestate is used. Original donor and
disposable source hashes remain exact. Captures and RAM receipts are on E:.
No1361-1385 activity line or revised wording is claimed activated. This baseline
is context research,not formatting or whole-family gameplay approval.

## Next work

Map the embedded text rectangle and automatic wrap/font behavior;prove complete
glyphs and bounds for all25;exercise Janus/Claudio activity cases through the
normal source consumer using disclosed fixtures if needed;integrate through a
new registered combined profile with exact clean-input patch and unchanged
earlier content/code allocations. Then update completion credit and guide images.
The current-ROM baseline screenshots are not promoted as final localized guide art.

''' + checkpoint + '\n', encoding='utf-8')
    paragraph = '\n\n## V835: actor-specific Deck source/prose review\n\n' + checkpoint + ' See [V835 context](personal_chatter_v835_checkpoint.md).\n'
    for p in ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md', 'docs/known_issues.md'):
        with Path(p).open('a', encoding='utf-8') as f:
            f.write(paragraph)
    sources = {Path(__file__), Path('scripts/prepare_personal_chatter_v835.py'), Path('scripts/extend_personal_context_v835.py'),
               Path('scripts/run_personal_chatter_context_v835.py'), MANUSCRIPT, DOC, LEDGER,
               *ROOT.glob('*.json'), *ROOT.glob('*.png')}
    sources.update(map(Path, ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md', 'docs/known_issues.md')))
    archived = []
    for source in sorted(sources):
        target = ARCHIVE / source.absolute().relative_to(Path.cwd())
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        archived.append({'source': str(source), 'archive': str(target), 'sha256': sha(target.read_bytes())})
    save(ROOT / 'archive_manifest.json', {'archive': str(ARCHIVE), 'files': archived,
        'all_copies_hash_verified': True, 'previous_goal_turn_classification': 'progress:V83412 Refit dialogue entries completed',
        'this_goal_turn_classification': 'progress:25 source/prose reviews,75 native selector cases,inherited defect mapped,ordinary Deck baseline',
        'whole_goal_complete': False})
    print('V835 checkpoint saved:646 complete,674 source/prose reviewed,28 reviewed drafts pending. V834 remains current;25 embedded-format/release gates remain open.', flush=True)


if __name__ == '__main__':
    main()
