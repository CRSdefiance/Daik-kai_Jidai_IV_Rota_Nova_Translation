"""Stage the contextual Port resupply and departure dialogue review."""

from hashlib import sha256
from pathlib import Path
from types import FunctionType

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import (
    DIRECTORY_OFFSET,
    TABLE_OFFSET,
    common_message_entries,
)
from scripts import register_london_stockholm_dialogue_20261115 as parent
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_port_services_v761 import BINDINGS
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.stage_mutiny_review_v1 import compile_layouts, portrait_sheets, render_portrait
from scripts.verify_release_baseline import files

base = parent.base
ARM, COMMON, CLEAN, GATES = parent.stage.ARM, parent.stage.COMMON, parent.stage.CLEAN, parent.stage.GATES
ROOT = Path('work/port_supply_dialogue_20261115_v1')
ROM = ROOT / 'Port_Supply_Dialogue_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/port_supply_dialogue_20261115_v1.json')
REVISIONS = {
    806: "We'll throw out any extra food. Is that okay?",
    816: "You can't afford a full resupply. Want to buy what you can?",
    817: 'Change the mix of water and food?',
}
PHRASES = {
    806: ("We'll throw out any extra food.", 'Is that okay?'),
    813: ("You're running low on water.", 'Need to stock up?'),
    814: ('Your sailors look tired.', 'Why not let them rest at the inn?'),
    816: ("You can't afford a full resupply.", 'Want to buy what you can?'),
}
DETAILS = {
    49: ('Departure check after a low-supplies report.',
         'The port worker offers to resupply the fleet for the substituted number of gold coins.',
         'The direct price question follows the crew’s warning and uses gold naturally for any amount.'),
    806: ('Refilling water would leave too much food for the new mix. The worker asks before discarding it.',
          'The surplus food would be discarded, so the worker asks if that is all right.',
          'Use the worker’s conversational voice and give the complete consequence before the yes/no question.'),
    812: ('Refilling food would leave too much water for the new mix.',
          'The surplus water would be disposed of. The worker asks permission to proceed.',
          'Dumped suits the concrete action. Both the warning and the short confirmation already read in full.'),
    813: ('The worker notices a shortage before the player sees the disposal prompt or the bill.',
          'Water looks low. The worker offers to replenish it.',
          'Keep the worker’s brisk question and place it together on the next line.'),
    814: ('The port worker sees fatigue while the player is preparing to depart.',
          'The sailors look tired. The worker recommends resting at the inn.',
          'The soft suggestion respects the player’s choice. Keep “Why not” with the rest of the question.'),
    815: ('The player chooses a cargo action with no cargo aboard.',
          'The port worker points out that the player has no cargo.',
          'The matter-of-fact reply fits the immediate refusal. No extra greeting is needed.'),
    816: ('The wallet cannot cover the full refill, but the worker offers a smaller purchase.',
          'The player lacks funds for a full resupply. The worker asks if they want only what they can afford.',
          'Keep both the limit and the choice in the worker’s voice. Each lands as a complete sentence.'),
    817: ('The player opens the control that changes the proportions of the two supplies.',
          'The worker asks whether to change the water-to-food ratio.',
          'Mix names the proportion in plain language and keeps water and food together.'),
}


def digest(raw):
    return sha256(raw).hexdigest()


def encoded_changes(logical):
    compile_protected = FunctionType(
        compile_layouts.__code__, compile_layouts.__globals__ | {'PHRASES': PHRASES}
    )
    return compile_protected({n: {'english': REVISIONS.get(n, logical[n])} for n in REVISIONS.keys() | PHRASES.keys()})


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    ctx = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    arm, common = ctx.arm, ctx.common
    clean = base.NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    old = owned_entries(common, arm, digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    credited = {row['id'] for row in base.load(base.LEDGER)[base.CONTEXT]['integrated_record_keys']
                if row['file_path'] == COMMON}
    assert all(f'COMMON_MESSAGE_{n}' in credited for n in DETAILS)
    bindings = {n: BINDINGS[n] for n in DETAILS if n in BINDINGS}
    assert all(arm[start:end + 4] == clean_arm[start:end + 4] for start, end, _ in bindings.values())
    logical = {n: ' '.join(old[n].text.decode('ascii').split()) for n in DETAILS}
    edited = encoded_changes(logical)
    assert set(edited) == {806, 813, 814, 816, 817}
    assert all(body != old[n].text and b'%' not in body + source[n].text for n, body in edited.items())
    common_after, installed, slots = owned_deployment(common, arm, old, edited)
    tested = with_components(ctx, arm, common_after)
    cpu, get, provider = tested.machine(arm, common_after, tested.raw, tested.plan)
    raster, _, font = font_tools(ctx.image)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')
    rows, pages, variants = [], [], []
    for n, (context, meaning, note) in DETAILS.items():
        s, a, b = source[n], old[n], installed[n]
        substitutions = s.text.count(b'%s')
        assert substitutions == a.text.count(b'%s') == b.text.count(b'%s') == int(n == 49)
        location = get(0x5528C, n)
        assert bytes(cpu.mem_read(location, len(b.text) + 1)) == b.text + b'\0'
        layout = {}
        if n in edited:
            start, end, handler = bindings[n]
            consumer = 0x02053FCC if handler == 0x53F9C else 0x02054014
            before, old_lines = native_layout(cpu, a.text, n, (), parent=consumer)
            after, new_lines = native_layout(cpu, b.text, n, (), parent=consumer)
            assert old_lines != new_lines and all(new_lines)
            assert all(any(phrase in line for line in new_lines) for phrase in PHRASES.get(n, ()))
            before_plane, _ = render_portrait(raster, arm, kanji, before)
            after_plane, _ = render_portrait(raster, arm, kanji, after)
            pages.extend(((f'{n} before', before_plane), (f'{n} after', after_plane)))
            layout = {'before_lines': old_lines, 'visible_lines': new_lines, 'native_output_hex': after.hex(),
                      'native_plane_sha256': digest(after_plane), 'consumer': consumer,
                      'caller_span': [start, end + 4], 'original_caller_hex': arm[start:end + 4].hex()}
            variants.append({'n': n, **layout})
        decision = 'revision' if n in REVISIONS else 'wrap revision' if n in edited else 'retention'
        rows.append({'id': f'COMMON_MESSAGE_{n}', 'message_ID': n, 'file_path': COMMON, 'speaker': 'Port Worker',
                     'context': context, 'source_meaning': meaning, 'localization_note': note, 'decision': decision,
                     'english': REVISIONS.get(n, logical[n]), 'Japanese': s.text.decode('cp932'),
                     'previous_English': a.text.decode('ascii'), 'source_reference': reference(s),
                     'current_reference': reference(a), 'staged_reference': reference(b),
                     'source_hex': s.text.hex(), 'current_hex': a.text.hex(), 'staged_hex': b.text.hex(),
                     'preserved_substitutions': substitutions,
                     'review': dict.fromkeys(GATES, True) | {'formatting': False}, **layout})
    assert provider.reads and bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    ROOT.mkdir()
    image = base.NdsImage.open(parent.ROM)
    before = files(image)
    image.replace_file(COMMON, common_after)
    after = files(image)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {COMMON}
    image.save(ROM)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    sheets = portrait_sheets(ROOT, pages)
    base.save(MANUSCRIPT, {'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                          'encoder': 'dialogue-relocatable-v1', 'review_gates': list(GATES),
                          'previous_sha256': release['candidate_sha256'], 'clean_sha256': release['clean_input_sha256'],
                          'candidate_sha256': base.digest(ROM), 'records': rows})
    base.save(STORED, {'candidate_sha256': base.digest(ROM), 'previous_sha256': release['candidate_sha256'],
                       'target_ARM9_sha256': digest(arm), 'target_COMMON_sha256': digest(common_after),
                       'whole_parent_inverse': True, 'preserved_entries': len(installed) - len(edited),
                       'allocations': slots, 'sheets': sheets, 'font': font, 'native_cases': variants,
                       'manuscript_sha256': base.digest(MANUSCRIPT)})
    print(f'{len(rows)} exact records reviewed and {len(variants)} changed pages rendered.')


if __name__ == '__main__':
    main()
