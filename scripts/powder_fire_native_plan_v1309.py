"""Six source-reviewed alerts in one native block; no playable ROM is built."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.patch.battle_aftermath_editorial import current_entries
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries, DIRECTORY_OFFSET, TABLE_OFFSET
from scripts import powder_fire_runtime_v1307 as runtime
from scripts.powder_fire_layout_v1304 import IDS, PROFILE, paragraph
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/powder_fire_payload_v1309')
MANUSCRIPT = Path('translations/powder_fire_editorial_manuscript_v1.json')
SOURCE_COMMON = '6fc5d831612c8ecbf4708a90a3624506fc4a3a3f121e973d9f6f39316636e2ce'
SOURCE_ARM = runtime.SOURCE


def compiled(row):
    return b' '+paragraph(row)


def plan(common,arm,doc):
    assert sha(common) == SOURCE_COMMON and sha(arm) == SOURCE_ARM
    assert doc['translation_policy'] == 'natural-dialogue-v2' and doc['target_locale'] == 'en-US'
    assert doc['consumer_layout_profile'] == PROFILE and tuple(r['message_id'] for r in doc['records']) == IDS
    clean,canonical = NdsImage.open('work/clean.nds'),NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(Path('work/clean.nds').read_bytes()) == doc['source_clean_ROM_sha256']
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    jp = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    base = common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    before = current_entries(common,arm)
    source = IlnkContainer.parse(common)
    authored = {}
    for row in doc['records']:
        number = row['message_id']
        assert row['source_hex'] == jp[number].text.hex() and row['canonical_source_hex'] == base[number].text.hex()
        assert row['current_text_hex'] == before[number].text.hex()
        assert all(row['review'][g] for g in ['source','context','localization','naturalness'])
        assert row['unwrapped_paragraph_hex'] == paragraph(row).hex()
        authored[number] = compiled(row)
    assert {before[number].block for number in IDS} == {22}
    target,runtime_plan = runtime.apply(arm)
    target = bytearray(target)
    rebuilt = list(source.blocks)
    numbers = [row.message_id for row in before if row.block == 22]
    assert numbers == list(range(numbers[0],numbers[-1]+1))
    body,fields,metadata = bytearray(),[],[]

    def put(at,value):
        target[at:at+len(value)] = value
        fields.append([at,len(value)])
        metadata.append({'address':0x02000000+at,'source_hex':arm[at:at+len(value)].hex(),'target_hex':value.hex()})

    for number in numbers:
        row = before[number]
        payload = source.blocks[22][row.block_offset:row.copy_end]
        assert 0 < len(payload) < 512 and payload.startswith(row.text+b'\0')
        if number in authored:
            assert not set(payload[len(row.text)+1:])-{0,32}
            payload = authored[number]+b'\0'
        put(TABLE_OFFSET+number*2,struct.pack('<H',len(body)))
        body.extend(payload)
    assert 0 < len(body) <= 8192
    rebuilt[22] = bytes(body)
    put(DIRECTORY_OFFSET+22*4,struct.pack('<HH',numbers[0],len(body)))
    target = bytes(target)
    common_target = IlnkContainer(rebuilt).to_bytes()
    directory = sha(target[DIRECTORY_OFFSET:TABLE_OFFSET])
    after = owned_entries(common_target,target,directory)
    assert len(before) == len(after) == 3668
    assert all(new.text == authored.get(old.message_id,old.text) for old,new in zip(before,after,strict=True))
    assert all(rebuilt[i] == source.blocks[i] for i in range(41) if i != 22)
    for number in numbers:
        if number not in authored:
            old,new = before[number],after[number]
            assert source.blocks[22][old.block_offset:old.copy_end] == rebuilt[22][new.block_offset:new.copy_end]
    patches = runtime_plan['patches']+metadata
    restored = bytearray(target)
    for patch in patches:
        at = patch['address']-0x02000000
        value = bytes.fromhex(patch['source_hex'])
        restored[at:at+len(value)] = value
    assert bytes(restored) == arm
    old,new = [MainCodeFile(value,0x02000000) for value in [arm,target]]
    shape = lambda obj:[(s.ramAddress,len(s.data),s.bssSize) for s in obj.sections]
    assert shape(old) == shape(new) and cache_plan(arm) == cache_plan(target)
    assert all(old.sections[i].data == new.sections[i].data for i in [1,2,3,4])
    assert len(new.sections[3].data)-48 == 123040
    return common_target,target,{'source_COMMON_sha256':sha(common),'source_ARM9_sha256':sha(arm),
        'target_COMMON_sha256':sha(common_target),'target_ARM9_sha256':sha(target),'directory_sha256':directory,
        'changed_records':[f'COMMON_MESSAGE_{number}' for number in IDS],'native_IDs':list(IDS),
        'metadata_fields':fields,'patches':patches,'runtime_plan':runtime_plan,
        'all3662_unselected_texts_and_native_copy_spans_preserved':True,'all40_other_blocks_and_opaque_duel_prefix_exact':True,
        'only_COMMON22_native_metadata_and_existing188_byte_table_changed':True,
        'all_code_gate_fonts_sections_BSS_cache_arena_ITCM_and123040_staged_bytes_exact':True,
        'old_new_block22_bytes':[len(source.blocks[22]),len(body)],'all_ARM9_patches_restore_source_exact':True}


def main():
    assert not ROOT.exists()
    doc = read(MANUSCRIPT)
    rom = NdsImage.open(doc['current_ROM'])
    common,arm = rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin')
    c,a,proof = plan(common,arm,doc)
    ROOT.mkdir(parents=True)
    cp,ap = ROOT/'COMMON_RESEARCH_ONLY.DK4',ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin'
    cp.write_bytes(c)
    ap.write_bytes(a)
    save(ROOT/'native_payload_plan.json',{**proof,'target_COMMON':str(cp),'target_ARM9':str(ap),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_ROM_registry_or_completion_change':True,'full_goal_complete':False})
    print('Six alerts repacked;3662 other texts/copy spans,40 blocks and all123040 staged bytes exact.',flush=True)


if __name__ == '__main__':
    main()
