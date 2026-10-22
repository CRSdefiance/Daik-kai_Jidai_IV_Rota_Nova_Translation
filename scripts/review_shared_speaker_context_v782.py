"""Correct role1 metadata from source labels and the actual speech fallback."""

import struct
from copy import deepcopy
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch import shared_dialogue_editorial as owned
from dk4tool.patch.crew_role_labels import ORIGINAL, LABELS, JAPANESE
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shared_integration_v782')
V2 = Path('translations/shared_dialogue_editorial_manuscript_v2.json')
V3 = Path('translations/shared_dialogue_editorial_manuscript_v3.json')


def main():
    rom = NdsImage.open('out/all_routes_combined_v782_candidate.nds')
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for a, b in ((0x7B60, 0x7C34), (0x82478, 0x8261C), (0x53CB0, 0x53E4C)):
        assert arm[a:b] == clean[a:b]
    captured = Path('E:/Rota Nova translations/Generated/work/emulation_v193/shared_v782_recruit_live/capture_report.json')
    report = read(captured)
    snapshot = next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame'] == 3200)
    raw = Path(snapshot['path']).read_bytes()
    assert sha(raw) == snapshot['sha256'] and report['ROM_sha256'] == sha(Path(report['ROM']).read_bytes())
    u = machine(arm)
    u.mem_write(0x02000000, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    def ptr(at): return struct.unpack('<I', u.mem_read(at, 4))[0]
    def text(at): return bytes(u.mem_read(at, 256)).split(b'\0')[0]

    jp_at = struct.unpack_from('<I', clean, ORIGINAL-0x02000000+4)[0]
    jp = clean[jp_at-0x02000000:jp_at-0x02000000+32].split(b'\0')[0].decode('cp932')
    assert jp == JAPANESE[1] == '副官'
    role_table = get(0x86314)
    english = text(ptr(role_table+4)).decode('ascii').strip()
    assert english == LABELS[1] == 'First Mate'
    assert get(0x7B60, (1,)) == 6
    controller = get(0xCB1A8)+0x2090
    assigned, selected = get(0x825E4, (controller, 1)), get(0x82478, (controller, 1))
    assert assigned == 208 and selected == 18
    actor = get(0xCB184)+4+selected*32
    name = text(get(ptr(ptr(actor)+8)-0x02000000, (actor,))).decode('cp932')
    assert 'Charles' in name and 'Rochefort' in name
    proof = {'source_ROLE1_Japanese': jp, 'accepted_ROLE1_English': english,
             'original_shared_role_table_provider': 0x02086314, 'actual_English_role_table': role_table,
             'original_role_to_room_getter': 0x02007B60, 'role1_room_type': 6,
             'strict_assignment_getter': 0x020825E4, 'strict_assigned_actor_ID': assigned,
             'speech_provider': 0x02082478, 'selected_speech_actor_ID': selected,
             'selected_actor': actor, 'selected_name': name,
             'unassigned208_uses_original_speech_fallback': True,
             'source_snapshot': snapshot, 'source_capture_report': str(captured),
             'ROM_sha256': report['ROM_sha256'], 'corrected_IDs': list(range(1035, 1049)),
             'meaning_pronouns_and_all_encoded_dialogue_bytes_unchanged': True,
             'frozen_V1_V2_and_production_config_preserved': True,
             'metadata_only_registered_replay_still_required': True,
             'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False}
    save(ROOT/'role1_speaker_context_correction.json', proof)
    doc = deepcopy(read(V2))
    for row in doc['records']:
        if 1035 <= row['message_id'] <= 1048:
            assert row['speaker'] == 'Role1 Barkeep, original selected voice'
            row['speaker'] = 'Original role1 (First Mate) speech provider, with native officer fallback'
            old = "The barkeep recruits for the player;do not mislabel this as an officer speaking about the barkeep's own crew."
            assert row['localization_note'].count(old) == 1
            row['localization_note'] = row['localization_note'].replace(old,
                "The original role1 speech provider selects a crew officer to address the player about the fleet's staffing and offer another recruitment attempt. Preserve the source voice's personal or collective phrasing.")
            row['context'] += ' Source role1 is 副官/First Mate. Original82478 selects a speech fallback when the strict assignment is208;the actual Istanbul sample selects Charles Rochefort(actor18).'
    doc['speaker_context_correction'] = str(ROOT/'role1_speaker_context_correction.json')
    doc['speaker_context_correction_sha256'] = sha((ROOT/'role1_speaker_context_correction.json').read_bytes())
    doc['previous_frozen_manuscript'] = str(V2)
    doc['previous_frozen_manuscript_sha256'] = sha(V2.read_bytes())
    doc['status'] = 'speaker-context-corrected;metadata-only-registered-replay-and-remaining-gameplay-pending'
    validate_natural_dialogue_batch(doc)
    before = read(V2)
    for old, new in zip(before['records'], doc['records'], strict=True):
        assert owned.compile_text(old) == owned.compile_text(new)
        assert {k for k in old if old[k] != new[k]} <= {'speaker', 'context', 'localization_note'}
    save(V3, doc)
    save(ROOT/'speaker_metadata_v3_equivalence.json', {
        'frozen_V2_sha256': sha(V2.read_bytes()), 'V3_sha256': sha(V3.read_bytes()),
        'all50_complete_encoded_paragraphs_identical': True, 'context_IDs_corrected': list(range(1035, 1049)),
        'production_config_unchanged': str('translations/shared_dialogue_editorial_release_v1.json'),
        'registered_metadata_replay_pending': True, 'new_completion_credit': 0})
    print(f'Role1 is {jp}/{english};native fallback selects {name}.14 metadata records corrected;all50 paragraphs encode identically. Registration pending.', flush=True)


if __name__ == '__main__':
    main()
