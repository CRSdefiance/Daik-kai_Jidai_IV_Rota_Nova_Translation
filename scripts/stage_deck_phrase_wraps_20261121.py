"""Source-bound wrap review of ten early-break Deck comments."""

from hashlib import sha256
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageDraw

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_bubble_portrait_wraps_20261120 as parent
from scripts import work_comments_layout_v843 as formatter
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.prepare_work_comments_v842 import snapshot
from scripts.probe_battle_finance_fonts_v920 import prepare_mode
from scripts.probe_physical_wounds_fonts_v968b import prepare_condition
from scripts.probe_work_fonts_v843 import execute, prepare_model
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_deck_comments_20261119 import current_pixels
from scripts.stage_shared_notices_storage_v1 import relocate


base, CLEAN = parent.base, Path('work/clean.nds')
ARM, COMMON = '/__arm9__.bin', '/COMMON/MESFILE.DK4'
ROOT = Path('work/deck_phrase_wraps_20261121/staged_v2')
ROM, PROOF = ROOT / 'Deck_Phrase_Wraps_STAGED.nds', ROOT / 'staged.json'
PATCH, REBUILT = ROOT / 'translation.xdelta', ROOT / 'clean_rebuilt.nds'
TRIAGE = Path('translations/editorial_checkpoints/SharedText_20261110_v1/shared_ascii_early_break_triage_20261120_v1.json')
HISTORIES = {
    1524: 'sails_boarding', 1535: 'sails_boarding', 1584: 'battle_personal',
    1599: 'battle_repair_medical', 1670: 'battle_finance', 1698: 'battle_bridge',
    1754: 'battle_sails_boarding', 1763: 'battle_gunnery_deck', 1805: 'physical_wounds',
    1807: 'illness_critical',
}
EDIT = {
    1524: ('We need to pick sails for the wind: fore-and-aft or square.',
           'Keep the need to match two named types of sail to the wind. Put the selection before the two alternatives.'),
    1535: ('I train like this regularly.',
           'The polite voice describes a routine. The complete statement reads plainly without breaking the training phrase.'),
    1584: ('I should put away my prized model...',
           'Cesare is thinking about putting away the model he values. Keep the complete action and his trailing thought together.'),
    1599: ("If the hull gets damaged, I'll fix it right away!",
           'Keep the source condition and quick response in two whole clauses. The shipwright speaks about prospective damage.'),
    1670: ('I could work on the financial report while I have the chance...',
           'The purser considers what to do while time is available. Keep the tentative wording, the full report name and the trailing thought.'),
    1698: ('Just watch me dodge those shots!',
           'The helmsman confidently offers to show that they can evade the incoming shots. The whole boast fits together.'),
    1754: ("To win with fewer casualties, we'll have to fight a duel...",
           'Hodram makes the duel necessary to win with fewer casualties. Keep that purpose clause and the measured conclusion intact.'),
    1763: ('Watch me sink their flagship!',
           'The gunner makes a simple, energetic boast. The action and its target stay together.'),
    1805: ("It's a minor wound. Don't worry.",
           'Maria assesses the wound and reassures the listener in two composed beats on one row.'),
    1807: ("I think I've caught something.",
           'The speaker suspects an illness without naming it. The complete thought fits together.'),
}
VOICE_ACTORS = {0: 4, 1: 16, 3: 7, 6: 14}
SATISFIES = ('complete_native_copy_macro_draw_and_ABI', 'full252x96_native_and_independent_canvas_equal',
             'bitmap_and_input_guards_exact', 'independent_authored_words_at_x0_12px_rows_match_every_pixel')


def ordered_layout(text):
    layout = FunctionType(formatter.layout.__code__, formatter.layout.__globals__ | {
        'KEEP_TOGETHER': formatter.KEEP_TOGETHER | {('financial', 'report'), ("we'll", 'have')},
    })
    return layout(text)


def source_rows(clean, previous, ledger):
    clean_arm, arm = clean.read_file(ARM), previous.read_file(ARM)
    original = common_message_entries(clean.read_file(COMMON), clean_arm)
    directory = sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    installed = owned_entries(previous.read_file(COMMON), arm, directory)
    flagged = {r['message_ID']: r for r in base.load(TRIAGE)['records']}
    assert base.load(TRIAGE)['candidate_sha256'] == base.digest(parent.ROM)
    histories = {name: Path(f'translations/{name}_contextual_final_review_v1.json') for name in set(HISTORIES.values())}
    history_rows = {name: {r['message_id']: r for r in base.load(path)['records']} for name, path in histories.items()}
    credited = {(r['file_path'], r['id']) for r in ledger[base.CONTEXT]['integrated_record_keys']}
    rows, storage = {}, {}
    for n, family in HISTORIES.items():
        old, current, prior = original[n], installed[n], history_rows[family][n]
        assert (COMMON, prior['id']) in credited and all(prior['review'].values())
        assert old.text.hex() == flagged[n]['clean_hex'] == prior['source_hex']
        assert current.text.hex() == flagged[n]['current_hex']
        assert reference(old) == flagged[n]['clean_reference'] and reference(current) == flagged[n]['current_reference']
        assert prior['native_argument_count'] == 0 and all(b'%' not in r.text for r in (old, current))
        old_lines = [line.rstrip() for line in current.text.decode('ascii').split('\n')]
        assert ' '.join(old_lines) == prior['english']
        assert old.text.decode('cp932') == prior['source_Japanese']
        english, note = EDIT[n]
        lines = ordered_layout(english)
        storage[n] = formatter.serialize(lines)
        assert ' '.join(lines) == english and 0 < len(lines) <= 3 and max(map(len, lines)) <= 36
        rows[n] = {key: prior.get(key) for key in (
            'id', 'speaker', 'context', 'source_meaning', 'role_ID', 'voice_class', 'protagonist_ID')}
        rows[n].update(message_ID=n, file_path=COMMON, source_Japanese=prior['source_Japanese'],
                       previous_English=prior['english'], english=english, localization_note=note,
                       decision='revision', finding='wrap and prose', previous_visible_lines=old_lines,
                       visible_lines=lines, new_pages=1, source_reference=reference(old),
                       current_reference=reference(current), source_hex=old.text.hex(), current_hex=current.text.hex(),
                       prior_review=str(histories[family]), original_substitution_count=0,
                       review=dict.fromkeys(REQUIRED_REVIEW_GATES, True))
    return rows, storage, directory


def draw_pages(image, context, arm, rows, rebound):
    sources = {
        'widget': ('personal_cabin_v840_838_Charles_after', 4600),
        'npc': ('personal_cabin_v840_838_Charles_after', 3200),
        'battle': ('battle_personal_v897_893_Julio', 14700),
        'hodram': ('battle_survey_lookout_v939_938_CaptainSurvey', 16500),
        'maria': ('ceremony_Maria_approach_v825', 26000),
    }
    loaded = {key: snapshot(*value) for key, value in sources.items()}
    draw_ranges = ((0xD16B4, 0xD1898), (0x125A20, 0x126000))
    assert all(context.raw[a:b] == arm[a:b] for a, b in draw_ranges)
    paint = FunctionType(execute.__code__, execute.__globals__ | {'expected_pixels': current_pixels})
    first = Image.new('RGB', (900, 5 * 103), '#293340')
    draw = ImageDraw.Draw(first)
    cases = {}
    for i, (n, row) in enumerate(rows.items()):
        role, hero, voice = (row[k] for k in ('role_ID', 'protagonist_ID', 'voice_class'))
        if n == 1584:
            actor, key = 13, 'battle'
        elif hero is not None:
            actor, key = hero, {1: 'hodram', 3: 'maria'}[hero]
        else:
            actor, key = VOICE_ACTORS[voice], 'npc' if n <= 1535 or n >= 1807 else 'battle'
        scene, snapshot_receipt = loaded[key]
        fixture, assignment = prepare_model(arm, scene, actor, role, loaded['widget'][0])
        if n in (1805, 1807):
            conditions = (2, 3) if n == 1805 else (5,)
            states = [prepare_condition(arm, fixture, actor, mode, status)
                      for status in conditions for mode in ((0, 0), (0, 1))]
        elif n >= 1584:
            states = [prepare_mode(arm, fixture)]
        else:
            states = [(fixture, {'ordinary_captured_mode': True})]
        variants, planes = [], []
        for raw, mode in states:
            raw = bytearray(raw)
            for start, end in draw_ranges:
                raw[start:end] = context.raw[start:end]
            case, plane = paint(image, bytes(raw), actor, role, n, rebound[n].text, row['visible_lines'])
            assert all(case[name] for name in SATISFIES)
            assert not any(plane[y*252+x] for y in range(60, 96) for x in range(216, 252))
            variants.append(case | {'mode': mode, 'complete_ink_inside_216x36': True})
            planes.append(plane)
        assert all(plane == planes[0] for plane in planes)
        cases[n] = dict(snapshot=snapshot_receipt, assignment=assignment, controls=variants)
        body = Image.frombytes('L', (252, 96), bytes(0 if v else 255 for v in planes[0])).crop((0, 60, 216, 96))
        x, y = 10 + (i % 2) * 450, (i // 2) * 103
        draw.text((x, y + 3), f"COMMON {n}  {row['speaker']}", fill='white')
        first.paste(body.resize((432, 72), Image.Resampling.NEAREST), (x, y + 21))
        print(f'{n} {row["visible_lines"]}', flush=True)
    path = ROOT / 'deck_phrase_wraps_native.png'
    first.save(path)
    return cases, path


def main():
    assert not PROOF.exists()
    release, ledger, pending = map(base.load, (parent.RELEASE, base.LEDGER, parent.PENDING))
    parent_sha = base.digest(parent.ROM)
    assert parent_sha == release['candidate_sha256'] == ledger['current_integrated_candidate']['sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256'] == pending['clean_sha256']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    clean, image = map(base.NdsImage.open, (CLEAN, parent.ROM))
    rows, storage, directory = source_rows(clean, image, ledger)
    arm, common = image.read_file(ARM), image.read_file(COMMON)
    repack = FunctionType(relocate.__code__, relocate.__globals__ | {'DIRECTORY': directory})
    target_common, target_arm, rebound, allocation = repack(common, arm, rows, storage)
    assert allocation['all_41_blocks_fit_8KiB'] and allocation['changed_visible_templates'] == list(rows)
    for row in pending['records']:
        entry = rebound[row['message_ID']]
        assert row['current_reference'] == reference(entry) and row['current_hex'] == entry.text.hex()
    for n, row in rows.items():
        row.update(staged_reference=reference(rebound[n]), staged_hex=rebound[n].text.hex())
    image.replace_file(ARM, target_arm)
    image.replace_file(COMMON, target_common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True, exist_ok=True)
    if ROM.exists():
        assert ROM.read_bytes() == target
    else:
        ROM.write_bytes(target)
    image = base.NdsImage.open(ROM)
    context = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    stage = with_components(context, target_arm, target_common)
    cpu, get, provider = stage.machine(target_arm, target_common, stage.raw, stage.plan)
    for visit in range(2):
        for n in rows:
            text = rebound[n].text + b'\0'
            assert bytes(cpu.mem_read(get(0x5528C, n), len(text))) == text
    assert provider.reads
    cases, sheet = draw_pages(image, stage, target_arm, rows, rebound)
    if not PATCH.exists():
        make_xdelta(CLEAN, ROM, PATCH)
    if not REBUILT.exists():
        apply_xdelta(CLEAN, PATCH, REBUILT)
    assert REBUILT.read_bytes() == target
    proof = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
                 review_gates=sorted(REQUIRED_REVIEW_GATES), records=list(rows.values()),
                 candidate_sha256=base.digest(ROM), parent_sha256=parent_sha,
                 exact_clean_patch_reconstruction=True, patch_sha256=base.digest(PATCH),
                 parent_runtime=context.receipt(), complete_parent_inverse=True,
                 target_COMMON_sha256=sha256(target_common).hexdigest(),
                 target_ARM9_sha256=sha256(target_arm).hexdigest(), allocation=allocation,
                 native_display=cases, warm_and_cold_loader_checks=2*len(rows), unchanged_pending=len(pending['records']),
                 native_sheet={'path': str(sheet), 'sha256': base.digest(sheet)},
                 actual_gameplay_observed=False, visual_review_pending=True)
    validate_natural_dialogue_batch(proof)
    base.save(PROOF, proof)


if __name__ == '__main__':
    main()


