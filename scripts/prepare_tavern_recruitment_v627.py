"""Prepare all seven source-reviewed recruitment voices and native previews."""

import argparse
import copy
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile
from PIL import Image

from dk4tool.dialogue.qa import audit_native_common_entry
from dk4tool.patch.tavern_recruitment import CMP, MANUSCRIPT, TABLE, transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_tavern_queued_native_v626 import queued_wrap
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_recruitment_v627')
LINES = [
    (897, 'Who wants to sail with the Admiral?'),
    (898, "Who'll join the Admiral's crew?"),
    (899, "Step forward if you'd like to sail with the Admiral!"),
    (900, "Doesn't anyone here want to sail with the Admiral?"),
    (901, "Who'll sail with the Admiral?"),
    (902, "Want to join the Admiral's crew? Step forward!"),
    (903, "Anyone for the Admiral's crew?")]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--register-reviewed-previews', action='store_true')
    args = parser.parse_args()
    ROOT.mkdir(exist_ok=True)
    clean = NdsImage.open('work/clean.nds')
    source = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'), clean=True)
    parent = NdsImage.open('out/all_routes_combined_v626_candidate.nds')
    code = MainCodeFile(parent.read_file('/__arm9__.bin'), 0x02000000)
    at = CMP - code.sections[4].ramAddress
    code.sections[4].data[at:at + 4] = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm('cmp r3,#384', CMP)[0])
    research = bytes(code.save())
    records, qa = [], []
    for number, english in LINES:
        native_text = english.replace('I', 'Ｉ').replace('F', 'Ｆ').encode('cp932')
        audit = audit_native_common_entry(b' ' * len(native_text), native_text.decode('cp932') + '{PAD}')
        assert not [e for e in audit['issues'] if e['severity'] in ('warning', 'error')]
        formatted = queued_wrap(research, native_text, 0x02053DB8, TABLE)
        events = []
        pixels = raster(research, formatted, 0x01FFCE40 - 0x02000000,
                        size=(228, 80), glyph_events=events, instruction_limit=500000)
        visible = [e for e in events if e['code'] not in (32, 10)]
        decoded = native_text.decode('cp932')
        assert [e['code'] for e in visible] == [int.from_bytes(c.encode('cp932'), 'big') for c in decoded if not c.isspace()]
        offset = 0
        for word in decoded.split():
            group = visible[offset:offset + len(word)]
            assert len(group) == len(word) and len({e['y'] for e in group}) == 1
            offset += len(word)
        Image.frombytes('L', (228, 80), bytes(0 if p else 255 for p in pixels)).save(ROOT / f'voice_{number}_native.png')
        records.append({
            'id': f'COMMON_MESSAGE_{number}', 'message_id': number,
            'source_hex': source[number].text.hex(), 'japanese': source[number].text.decode('cp932'),
            'previous_japanese': source[number - 1].text.decode('cp932'),
            'next_japanese': source[number + 1].text.decode('cp932'), 'english': english + '{PAD}',
            'speaker': f'Recruiting officer alternative voice {number - 897}',
            'context': 'One independent original Tavern recruitment call from eight-slot table02118360. The source selector chooses one whole line, not successive parts of a sentence.',
            'source_meaning': "Calls for volunteers who want to sail aboard the Admiral's ship." + (' Asks them to step forward.' if number in (899, 902) else ''),
            'localization_note': 'Fresh clean-source English keeps the complete recruiting call and Admiral, with natural polite, casual, rough or older wording. No manual line breaks or fragment shortening. Source-owned cache padding funds complete prose; the encoder owns reserved capital I/F spelling. Native glyph order and whole-word previews pass; CP932-I renderer-model shape coverage remains a separately recorded limit.',
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': args.register_reviewed_previews}})
        qa.append({'message_id': number, 'native_entry_audit': audit,
                   'native_formatted': formatted.decode('cp932'),
                   'all_native_glyph_order_and_complete_words_verified': True})
    save(MANUSCRIPT, {'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
                      'target_locale': 'en-US', 'encoder': 'dialogue-fixed-v1',
                      'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
                      'status': 'reviewed-native-previews' if args.register_reviewed_previews else 'native-previews-pending-review',
                      'records': records})
    save(ROOT / 'source_and_native_preview_proof.json', qa)
    if args.register_reviewed_previews:
        common, arm, proof = transform(parent.read_file('/COMMON/MESFILE.DK4'), parent.read_file('/__arm9__.bin'))
        (ROOT / 'target_arm9.bin').write_bytes(arm)
        (ROOT / 'target_common.bin').write_bytes(common)
        save('translations/tavern_recruitment_v1.json', {'format': 'dk4-tavern-recruitment-v1', 'proof': proof})
        registry = read('translations/release_stack.json')
        profile = copy.deepcopy(registry['profiles']['all-routes-unified-v626'])
        profile.update({'tavern_recruitment': 'translations/tavern_recruitment_v1.json',
                        'description': 'Complete V626 plus seven faithful independent recruitment calls and their original queued voice-table wrapping.',
                        'note': 'Experimental; native cache block sizes/NUL identities and all inherited layers preserved. Actual recruitment and ordinary screens require cold-boot verification.'})
        registry['profiles']['all-routes-unified-v627'] = profile
        save('translations/release_stack.json', registry)
        print('Registered V627; ARM9', proof['target_arm9_sha256'])
    else:
        print('Prepared seven native source/word previews; formatting gates remain pending review.')


if __name__ == '__main__':
    main()
