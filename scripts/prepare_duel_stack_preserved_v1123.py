"""Keep original private stack addresses while compacting only executable code."""
from pathlib import Path


def main():
    source = Path('scripts/duel_renderer_thumb_v1121b.py').read_text(encoding='utf-8')
    target = Path('scripts/duel_renderer_thumb_v1123.py')
    assert not target.exists()
    changes = {
        "duel_renderer_thumb_v1121b')": "duel_renderer_thumb_v1123')",
        'push {r4-r7,lr}\nsub sp,#508': 'push {r4-r7,lr}\nsub sp,#16\nsub sp,#508',
        'add sp,#100\npop {r4-r7,pc}': 'add sp,#100\nadd sp,#16\npop {r4-r7,pc}',
        "'proposed_saved_register_bytes': 20,":
            "'proposed_saved_register_bytes': 20, 'proposed_private_padding_bytes':16,",
        "'new_outer_return_font_SP_offset': 0x46C, 'new_voice_table_font_SP_offset': 0x494,":
            "'new_outer_return_font_SP_offset': 0x47C, 'new_voice_table_font_SP_offset': 0x4A4,",
    }
    for before, after in changes.items():
        assert source.count(before) == 1, before
        source = source.replace(before, after)
    target.write_text(source, encoding='utf-8')
    probe = Path('scripts/probe_duel_thumb_equivalence_v1122b.py').read_text(encoding='utf-8')
    output = Path('scripts/probe_duel_thumb_equivalence_v1123.py')
    assert not output.exists()
    changes = {
        'from scripts.duel_renderer_thumb_v1121b import': 'from scripts.duel_renderer_thumb_v1123 import',
        "duel_thumb_equivalence_v1122b')": "duel_thumb_equivalence_v1123')",
        'u.mem_read(context, 0x50)': 'u.mem_read(context, 0x4C)',
        "0x46C if proposed else 0x47C": '0x47C',
        "0x494 if proposed else 0x4A4": '0x4A4',
        "'original_function308_research_transcription196_remaining_tail112': True,":
            "'original_function308_research_transcription200_remaining_tail108': True,\n"
            "        'original_stack_footprint_and_all76_allocated_context_bytes_exact':True,\n"
            "        'earlier80byte_probe_read4bytes_beyond_original_context_allocation':True,",
        "'new_outer_parent_font_SP_offset': 0x46C": "'new_outer_parent_font_SP_offset': 0x47C",
        "'new_saved_voice_table_font_SP_offset': 0x494": "'new_saved_voice_table_font_SP_offset': 0x4A4",
    }
    for before, after in changes.items():
        assert probe.count(before) == 1, before
        probe = probe.replace(before, after)
    output.write_text(probe, encoding='utf-8')
    print('Created original-stack-footprint successor;76 allocated context bytes remain a strict equality gate.')


if __name__ == '__main__':
    main()
