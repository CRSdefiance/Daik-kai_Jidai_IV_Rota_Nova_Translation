"""Review the visible Online captions using the observed original page owners."""

from collections import Counter
from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.gallery_caption_bounds import validate as gallery_captions
from scripts import checkpoint_online_and_scene_consumers_v1 as pending
from scripts import observe_online_gallery_common_v1 as observed
from scripts import register_ancient_map_hint_label_v1 as parent
from scripts import stage_ancient_map_hint_label_v1 as hint
from scripts.materialize_extras_menu_v1 import ARM9_RECORDS
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask


base, ARM = parent.base, parent.ARM
ROOT = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
OUTPUT = ROOT / 'visible_online_captions_context_v1.json'
CONSUMERS = ROOT / 'online_and_gallery_observed_consumers_v1.json'
BASE, COLOR = 0x02000000, (0, 8, 0)
DESCRIPTORS = (0x12F88C, 0x12F898, 0x12F8A4, 0x12F8B0)
CATEGORIES = ('Overview', 'Careers', 'First Steps', 'Create a Story')
DECISIONS = (
    (None, 'The call to chart unknown waters suits the opening ocean view and the map metaphor.'),
    ('Many lives, many stories', 'The page invites the player to meet and work with others. The parallel phrasing keeps the range of people and their stories in a natural caption.'),
    (None, 'The short invitation preserves player freedom and matches the play-style examples.'),
    (None, 'Royal orders preserves the sovereign authority behind the page’s invitation to further adventures.'),
    ("A sailor's life around the world", 'Use an idiomatic title for the promise of a sailor’s life with the world as its setting.'),
    ('Sail far. Make your mark!', 'Making a mark preserves the invitation to earn renown without promising a place in history.'),
    (None, 'The line preserves the variety of goods and the chance to earn a profit without promising a fortune.'),
    (None, 'The caption carries the excitement of the original sea battle alongside its image.'),
    (None, 'The choice of nation has a major effect on the story. The active caption already expresses that relationship.'),
    (None, 'The caption carries the new excitement that follows changes without adding a particular event or cause.'),
    ('Set sail with new companions!', 'The page describes forming a fleet with people the player meets. Companions fits that relationship without implying a political alliance.'),
    (None, 'The caption preserves the emphasis on the player’s own ship and the scope of the voyage.'),
    (None, 'The vast adventure and its enthusiasm carry the closing caption’s meaning.'),
)


def capture(case, sha):
    folder = observed.ROOT / case
    terminal = folder / 'terminal.json'
    receipt = base.load(terminal)
    assert receipt['ROM_sha256'] == sha
    assert all(base.digest(path) == digest for path, digest in receipt['evidence'].items())
    requests = base.load(folder / 'requests.json')
    assert not requests['errors'] and requests['mismatches'] == 0
    assert requests['all_host_slots_restored_and_core_file_exact']
    assert receipt['caption_calls'] == requests['rows']
    return receipt, requests, base.load(folder / 'capture/capture_report.json'), terminal


def caption_rows(clean, arm, receipt, report, page_resources):
    font = GameAsciiFont.from_arm9(arm)
    calls = {row['pointer']: row for row in receipt['caption_calls']}
    assert len(calls) == len(receipt['caption_calls']) == 13
    resources = {(row['category_index'], row['page_index']): row for row in page_resources}
    source_notes = {offset: (n, jp) for n, offset, jp, _, c in ARM9_RECORDS if c == 'Online overview caption'}
    records, holds = [], []
    for i, offset in enumerate(DESCRIPTORS):
        data, table, count = unpack_from('<3I', clean, offset)
        assert count == (4, 4, 2, 3)[i] and arm[offset:offset+12] == clean[offset:offset+12]
        for index in range(count):
            field = table - BASE + 4 * index
            ptr = unpack_from('<I', clean, field)[0]
            assert arm[field:field+4] == clean[field:field+4]
            at = ptr - BASE
            rid, japanese = source_notes[at]
            original = japanese.encode('cp932') + b'\0'
            assert clean[at:at+len(original)] == original
            current = arm[at:at+len(original)]
            previous = current.split(b'\0', 1)[0].decode('ascii')
            assert current == previous.encode('ascii').ljust(len(original), b'\0')
            event = calls[ptr]
            assert event['PC'] == observed.ONLINE and event['text'] == previous
            assert event['x'] == 128 - len(previous) * 3
            frame = next(row for row in report['frames_captured'] if row['frame'] >= event['frame'] + 60)
            assert base.digest(frame['path']) == frame['PNG_sha256']
            image = Image.open(frame['path']).convert('RGB')
            ink, bounds = complete_mask(font, previous, image, event['x'], 205, COLOR)
            holds.append(dict(id=rid, original_pointer=ptr, screenshot=frame, complete_native_ink=ink, bounds=bounds))
            draft, note = DECISIONS[len(records)]
            english = draft or previous
            assert len(english.encode('ascii')) < len(original)
            x = 128 - len(english) * 3
            assert 28 <= x and x + 6 * len(english) <= 228
            page = resources[i, index]
            records.append(dict(id=rid, file_path=ARM, source_Japanese=japanese,
                source_reference=dict(offset=at, pointer=ptr, original_hex=original.hex()),
                current_reference=dict(offset=at, pointer=ptr, stored_hex=current.hex(), field=field),
                current_English=previous, english=english, decision='revision' if draft else 'retention',
                localization_note=note, speaker='Online guide caption',
                context=f'Online Version, {CATEGORIES[i]}, page {index + 1} of {count}.',
                original_category=i, original_page=index, background=page['background']['path'],
                original_substitution_count=0, output_origin=[x, 205],
                review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
    return records, holds


def main():
    assert not OUTPUT.exists() and not CONSUMERS.exists()
    proof, release = map(base.load, (hint.PROOF, parent.RELEASE))
    assert base.digest(parent.ROM) == proof['candidate_sha256'] == release['candidate_sha256']
    earlier = base.NdsImage.open(observed.parent.ROM)
    arm = base.NdsImage.open(parent.ROM).read_file(ARM)
    clean = base.NdsImage.open(parent.CLEAN).read_file(ARM)
    assert hint.transform(earlier.read_file(ARM), clean) == arm
    inherited = base.digest(observed.parent.ROM)
    sound, online, gallery = (capture(case, inherited) for case in ('sound', 'online', 'gallery'))
    assert [(r['PC'], r['message_ID'], r['caller_LR']) for r in sound[1]['source_requests']] == [
        (0x0205528C, 3251, 0x02109278), (0x020534F4, 3251, 0x02109278)]
    assert all(not run[1]['source_requests'] and not run[0]['target_COMMON_calls'] for run in (online, gallery))
    resources = Path('work/analysis/online_resource_pages_v189.json')
    records, holds = caption_rows(clean, arm, online[0], online[2], base.load(resources)['pages'])
    native_gallery = {row['field']: row for row in gallery_captions(arm)}
    gallery_matches = []
    for event in gallery[0]['caption_calls']:
        field = event['gallery_table'] - BASE + 4 * event['gallery_position']
        row = native_gallery[field]
        assert event['PC'] == observed.GALLERY and event['pointer'] == row['pointer']
        assert event['text'] == row['English'] and event['x'] == row['bounds'][0]
        gallery_matches.append(row | dict(observed_frame=event['frame']))
    assert Counter(row['route'] for row in gallery_matches) == dict.fromkeys(range(4), 3)
    source_map = base.load(pending.OUTPUT)
    assert source_map['candidate_sha256'] == inherited
    base.save(CONSUMERS, dict(current_ROM_sha256=release['candidate_sha256'], observer_ROM_sha256=inherited,
        observed_online_caption_masks=holds, observed_gallery_caption_owners=gallery_matches,
        independent_gallery_titles_checked_for_arrow_bounds=len(native_gallery),
        original_native_COMMON_positive_control=sound[1]['source_requests'],
        online_and_gallery_observed_COMMON_requests=0, original_pending_COMMON_IDs_in_scope=245,
        independent_online_and_gallery_caption_paths=True, other_COMMON_consumers_pending=True,
        credit_added=0, evidence={str(path): base.digest(path) for path in
            (sound[3], online[3], gallery[3], pending.OUTPUT, resources, Path(__file__))}))
    decisions = Counter(row['decision'] for row in records)
    assert decisions == {'revision': 4, 'retention': 9}
    base.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        records=records, decisions=decisions, current_ROM_sha256=release['candidate_sha256'],
        current_ARM9_sha256=sha256(arm).hexdigest(), observer_report=str(CONSUMERS),
        observer_report_sha256=base.digest(CONSUMERS), formatting_pending=True, new_credit=0))
    print('13 Online caption contexts and all 13 current masks verified. 12 Gallery caption owners confirmed.')


if __name__ == '__main__':
    main()
