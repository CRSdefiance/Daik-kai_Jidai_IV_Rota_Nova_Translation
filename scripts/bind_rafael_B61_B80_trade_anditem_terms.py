"""Bind existing terms to the independently verified current native data, read-only."""
from pathlib import Path
import struct
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_native_given_name_table import string
from scripts.audit_story_glyph_consistency import load, save
from scripts.bind_hodram_B191_B210_identities import cstring
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT = Path('work/analysis/Rafael_B61_B80_clean_20261104')
RELEASE = Path('work/analysis/Rafael_B51_B60_release_verified_20261104/registered_release_verification.json')
EXPECTED_ARM = 'd45932617dfffeac2932a5a8d398d236758a8c1a835081ab9601aea5ed67dac2'
EXPECTED_COMMON = '94cfaf8debed48b1b76af82f850ac26d44c16b8d50704791e3587c49fadf5903'

if __name__ == '__main__':
    output = ROOT/'trade_house_andBamboo_Assembly_Plan_binding_v1.json'
    assert not output.exists()
    ctx = RegisteredRuntime(RELEASE, RELEASE.with_name('own_registered_startup_verification.json'), captain=0)
    assert sha(ctx.arm) == EXPECTED_ARM and sha(ctx.common) == EXPECTED_COMMON
    clean = NdsImage.open('work/clean.nds')
    source_arm = clean.read_file('/__arm9__.bin')
    config_path = Path('translations/shop657_full_width_reflow_release_v1.json')
    config = load(config_path)
    directory = sha(ctx.arm[DIRECTORY_OFFSET:TABLE_OFFSET])
    # This is a read-only use of the existing exact-directory parser, scoped by
    # the independently verified complete current ARM9 and COMMON identities.
    # The historical657 config names an older directory; do not change its guard.
    entry = owned_entries(ctx.common, ctx.arm, directory)[657]
    assert entry.text.hex() == config['target_text_hex']
    assert b' '.join(entry.text.split()) == b"You're a sailor, aren't you? For bulk trade, try the trade house."
    japanese = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), source_arm)[657]
    assert '交易所' in japanese.text.decode('cp932')
    asset_path = Path('translations/all_item_names_arm9_v1.json')
    approved = next(r for r in load(asset_path)['records'] if r['id']=='DK4_ITEM_POINTER_186')
    field = approved['offset']
    original = string(source_arm, struct.unpack_from('<I', source_arm, field)[0])
    pointer = struct.unpack_from('<I', ctx.arm, field)[0]
    current = cstring(ctx.raw, pointer)
    assert original['text'] == '竹細工の組立絵図'
    assert current.decode('cp932') == approved['english'] == 'Bamboo Assembly Plan'
    assert source_arm[field+4:field+24] == ctx.arm[field+4:field+24]
    save(output, dict(runtime=ctx.receipt(), records=[
        dict(id='RAFAEL_TERM_TRADE_HOUSE', Japanese='交易所', English='trade house', decision='retention',
            source_reference=dict(file_path='/COMMON/MESFILE.DK4', message_ID=657, block=japanese.block,
                offset=japanese.block_offset, table_offset=japanese.table_offset, record_index=japanese.record_index),
            source_hex=japanese.text.hex(), current_reference=dict(file_path='/COMMON/MESFILE.DK4', message_ID=657,
                block=entry.block, offset=entry.block_offset, table_offset=entry.table_offset, record_index=entry.record_index),
            current_hex=entry.text.hex(),
            finding='The already-reviewed shared shop recommendation calls the same trading facility trade house. Use that natural established term consistently in the village construction arc.',
            affected_story_blocks=[65,66], no_current_data_change=True),
        dict(id='RAFAEL_TERM_BAMBOO_ASSEMBLY_PLAN', Japanese=original['text'], English=approved['english'],
            decision='retention', item_ID=186, source_reference=dict(file_path='/__arm9__.bin', pointer_field=field,
                pointer=original['pointer'], string_offset=original['offset']), source_hex=original['hex'],
            current_reference=dict(file_path='/__arm9__.bin', pointer_field=field, pointer=pointer), current_hex=current.hex(),
            finding='Plan naturally preserves the source assembly drawing and matches the existing source-correct item label. Use Bamboo Assembly Plan and generic plan during B70/B72 comparison instead of creating a conflicting Diagram title.',
            affected_story_records=['DK4_MES_B70_R0214','DK4_MES_B70_R0218','DK4_MES_B72_R0071'],
            all_nonname_metadata_exact=True, no_current_data_change=True)],
        current_directory_sha256=directory, historical657_directory_sha256=config['directory_sha256'],
        historical657_directory_guard_correctly_rejected_later_image=True,
        existing_parser_unchanged_andindependently_registered_complete_image_locks_used=True,
        exact_existing657_text_retained_through_later_directory_repacking=True,
        term_decisions_require_propagation_to_remaining250_comparisons=True,
        original_source_first_drafts_frozen_as_provenance=True,
        no_new_native_execution_gameplay_page_orcompletion_credit=True, new_credit=0, guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [RELEASE,config_path,asset_path,Path(__file__)]}))
    print('Bound trade house to exact current COMMON657 and Bamboo Assembly Plan to clean/current item186. Retain existing item label; propagate during remaining comparisons. No ROM change.', flush=True)
