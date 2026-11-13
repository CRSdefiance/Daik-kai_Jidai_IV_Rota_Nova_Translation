"""Apply the existing portrait formatter to the complete Tavern message family."""

import json
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries

HOOK = 0x01FFCF54
TEXT = "Hmm... %s, right? Here's to our new friendship!"


def transform(common, arm, manuscript):
    validate_natural_dialogue_batch(manuscript)
    assert len(manuscript['records']) == 1
    row = manuscript['records'][0]
    assert row['message_id'] == 827 and row['english'].removesuffix('{PAD}') == TEXT
    entries = common_message_entries(common, arm, clean=False)
    toast = entries[827]
    assert toast.text == b'Right...%s, right? A toast to our new friendship!'
    data = IlnkContainer.parse(common)
    block = bytearray(data.blocks[toast.block])
    # Keep the original NUL boundary and every native offset/copy extent.
    block[toast.block_offset:toast.block_offset+len(toast.text)] = TEXT.encode('ascii').ljust(len(toast.text),b' ')
    data.blocks[toast.block] = bytes(block)
    target_common = data.to_bytes()
    code = MainCodeFile(arm,0x02000000)
    before = [bytes(s.data) for s in code.sections]
    section = code.sections[4]
    assert section.ramAddress == 0x01FFC000 and len(section.data) == 4096
    ks = Ks(KS_ARCH_ARM,KS_MODE_ARM)
    old = bytes(ks.asm('cmp r3,#1',HOOK)[0])
    new = bytes(ks.asm('cmp r3,#53',HOOK)[0])
    at = HOOK-section.ramAddress
    assert before[4][at:at+4] == old
    # r3 is message_id-820 at this point. Caller filtering, repair801,
    # the original expander, guarded wrapper and unrelated dispatch stay intact.
    section.data[at:at+4] = new
    # The shared selector already distinguishes the portrait caller from
    # equipment/modal callers. Reserve both guard/pair phases in every portrait
    # paragraph: 35 content cells on continuation rows.
    width_at = 0xB54
    old_width = bytes(ks.asm('ldr ip,[sp,#0x390]; sub ip,ip,#0xe00',0x01FFCB54)[0])
    new_width = bytes(ks.asm('mov r7,#35; bx lr',0x01FFCB54)[0])
    assert before[4][width_at:width_at+8] == old_width
    section.data[width_at:width_at+8] = new_width
    # These callers pass ordinary paragraphs. Legacy LF/guard spaces are
    # whitespace, not part of the following word. Reuse the same 284-byte
    # owned helper extent, original scratch bound and four-row limit.
    helper_at,helper_size = 0xA00,284
    helper = bytes(ks.asm(Path(__file__).with_name('tavern_paragraph_helper.asm').read_text(encoding='utf-8'),0x01FFCA00)[0])
    assert len(helper) <= helper_size
    helper += bytes(ks.asm('nop',0)[0])*((helper_size-len(helper))//4)
    assert len(helper) == helper_size
    section.data[helper_at:helper_at+helper_size] = helper
    target_arm = bytes(code.save())
    after_code = MainCodeFile(target_arm,0x02000000)
    assert all(bytes(after_code.sections[i].data) == before[i] for i in range(4))
    restored = bytearray(after_code.sections[4].data)
    restored[at:at+4] = old
    restored[width_at:width_at+8] = old_width
    restored[helper_at:helper_at+helper_size] = before[4][helper_at:helper_at+helper_size]
    assert bytes(restored) == before[4]
    after = common_message_entries(target_common,target_arm,clean=False)
    assert len(common) == len(target_common)
    for a,b in zip(entries,after):
        assert (a.block,a.block_offset,a.copy_end) == (b.block,b.block_offset,b.copy_end)
        assert b.text == (TEXT.encode().ljust(len(a.text),b' ') if a.message_id == 827 else a.text)
    return target_common,target_arm,{
        'changed_records': ['COMMON_MESSAGE_827','COMMON_TAVERN_FAMILY_PORTRAIT_WORD_WRAP'],
        'portrait_parent_return': 0x02054014,'tavern_message_family': [820,873],
        'owned_helper_bytes': helper_size,'dispatch_and_width_bytes': 12,'code_or_pool_growth': 0,
        'ordinary_paragraph_whitespace_normalized_before_wrapping': True,
        'all_portrait_continuations_reserve_pair_phase_with_35_cell_budget': True,
        'equipment_and_other_caller_continuation_budgets_preserved': True,
        'native_directory_offsets_copy_extents_and_all_other_text_preserved': True,
        'original_macro_expander_and_guarded_wrapper_preserved': True,
        'status': 'experimental','full_graphics_goal_complete': False,
    }


def apply_release(common,arm,path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-tavern-family-wrap-v1'
    assert sha(common) == config['source_common_sha256'] and sha(arm) == config['source_arm9_sha256']
    manuscript_path = Path(config['manuscript'])
    assert sha(manuscript_path.read_bytes()) == config['manuscript_sha256']
    assert sha(Path(__file__).with_name('tavern_paragraph_helper.asm').read_bytes()) == config['helper_asm_sha256']
    manuscript = json.loads(manuscript_path.read_text(encoding='utf-8'))
    result_common,result_arm,report = transform(common,arm,manuscript)
    assert sha(result_common) == config['target_common_sha256'] and sha(result_arm) == config['target_arm9_sha256']
    return result_common,result_arm,report
