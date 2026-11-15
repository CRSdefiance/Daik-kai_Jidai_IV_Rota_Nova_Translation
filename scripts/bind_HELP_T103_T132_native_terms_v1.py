"""Source-bind Deck role, room and skill labels; no new individual command activations claimed."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Shared_HELP_T103_T132_clean_20261104')
RELEASE = Path('work/analysis/Town_HELP23_release_verified_20261104/registered_release_verification.json')
STARTUP = RELEASE.with_name('own_registered_startup_verification.json')
SLOTS = [
    (0x148304,'命中力','Aim'),(0x14830C,'説得力','Social'),(0x148314,'謀略術','Tactics'),
    (0x14831C,'観察力','Observe'),(0x148324,'統率力','Command'),(0x148334,'剣闘術','Swords'),
    (0x14833C,'生命力','Health'),(0x148344,'操船術','Sailing'),(0x14834C,'測量術','Survey'),(0x148354,'会計術','Finance'),
    (0x12FF50,'個室','Cabin'),(0x12FF58,'舵輪','Helm'),(0x12FF68,'測量','Survey'),(0x12FF70,'甲板','Deck'),
    (0x12FF80,'材木室','Lumber'),(0x12FF88,'参謀室','Tactics'),(0x12FF90,'診察室','Sickbay'),
    (0x12FF98,'調理室','Galley'),(0x12FFA0,'主計室','Purser'),(0x12FFA8,'マスト','Mast'),
    (0x12FFB0,'漕手室','Rowers'),(0x12FFB8,'礼拝室','Chapel'),(0x12FFC8,'飼育室','Nursery'),
    (0x12FFD0,'娯楽室','Lounge'),(0x12FFD8,'副官室','Mate'),(0x12FFE0,'艦長室','Captain'),
    (0x12FFE8,'見張台','Lookout'),(0x12FFF0,'積荷倉庫','Cargo'),(0x12FFFC,'海兵詰所','Quarters'),
    (0x130008,'武装砲台','Battery'),(0x130014,'物資倉庫','Supplies'),
    (0x144684,'甲板画面','Deck View'),(0x14469C,'甲板画面','Deck View'),
    (0x137974,'航路図','Map'),(0x11B5A4,'人事','Crew'),
]
ROLES = [
    ('艦長','Captain'),('副官','First Mate'),('参謀','Strategist'),('主計長','Purser'),
    ('測量士','Surveyor'),('操帆手','Sail Handler'),('操舵手','Helmsman'),('見張り','Lookout'),
    ('斬込隊長','Boarding Leader'),('砲撃手','Gunner'),('宣教師','Missionary'),('船医','Surgeon'),
    ('料理長','Chief Cook'),('船大工','Shipwright'),('飼育員','Animal Keeper'),('甲板要員','Deckhand'),
]

if __name__ == '__main__':
    out = ROOT/'native_roles_rooms_andskills_v1.json'
    assert not out.exists()
    release, startup = map(load,[RELEASE,STARTUP])
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    path = Path(release['candidate'])
    assert sha(path.read_bytes()) == release['candidate_sha256']
    image = NdsImage.open(path)
    arm = image.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    capture_path = Path(startup['capture_report'])
    report = load(capture_path)
    assert report['ROM_sha256'] == release['candidate_sha256']
    snapshot = report['read_only_RAM_snapshot']
    ram = Path(snapshot['path']).read_bytes()
    assert sha(ram) == snapshot['sha256'] and len(ram) == 4194304
    assert arm[0x86314:0x86334] == clean[0x86314:0x86334] == ram[0x86314:0x86334]
    source_table, current_table = [struct.unpack_from('<I',v,0x86334)[0] for v in [clean,arm]]
    roles = []
    for i,(jp,en) in enumerate(ROLES):
        source_pointer = struct.unpack_from('<I',clean,source_table-0x2000000+i*4)[0]
        current_pointer = struct.unpack_from('<I',ram,current_table-0x2000000+i*4)[0]
        source = clean[source_pointer-0x2000000:].split(b'\0',1)[0]
        current = ram[current_pointer-0x2000000:].split(b'\0',1)[0]
        assert source == jp.encode('cp932') and current.rstrip() == en.encode('ascii')
        roles.append(dict(index=i,Japanese=jp,English=en,source_pointer=source_pointer,current_pointer=current_pointer,
            source_hex=source.hex(),current_hex=current.hex(),native_trailing_phase_spaces_preserved_not_part_of_logical_label=True))
    slots = []
    for at,jp,en in SLOTS:
        a,b = [v[at:].split(b'\0',1)[0] for v in [clean,arm]]
        assert a == jp.encode('cp932') and b == en.encode('ascii')
        slots.append(dict(file_path='/__arm9__.bin',offset=at,Japanese=jp,English=en,source_hex=a.hex(),current_hex=b.hex()))
    save(out,dict(current_verified_release=str(RELEASE),current_verified_release_sha256=sha(RELEASE.read_bytes()),
        own_startup=str(STARTUP),own_startup_sha256=sha(STARTUP.read_bytes()),own_capture=str(capture_path),own_capture_sha256=sha(capture_path.read_bytes()),
        own_RAM_snapshot=snapshot,current_ROM=str(path),current_ROM_sha256=release['candidate_sha256'],current_ARM9_sha256=sha(arm),source_ARM9_sha256=sha(clean),
        native_role_table_pointer_field=0x86334,source_role_table=source_table,current_role_table=current_table,native_roles=roles,stored_room_skill_andcommand_labels=slots,
        source_clean_current_static_labels_exact=True,own_current_RAM_andunchanged_role_selector_bound=True,
        concrete_mismatches=dict(生命力='Health, not older Help Vigor',説得力='Social, not older Help Speech',謀略術='Tactics, not older Help Guile'),
        room_synonyms_require_contextual_decisions_not_global_replacement=True,
        HELP103_X_HELP104_Y_HELP106_auto_assignment_controls_still_pending=True,
        individual_Deck_room_skill_UI_visits_not_claimed=True,new_gameplay=False,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('16 native roles and35 exact room/skill/command labels bound. Real Health/Social/Tactics mismatches found; controls and revised prose/display remain.')
