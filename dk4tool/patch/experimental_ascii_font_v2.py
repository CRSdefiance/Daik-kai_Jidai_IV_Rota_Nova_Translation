"""Install the reviewed 6x11 font without changing native drawing code or metrics."""

import json
from pathlib import Path

from dk4tool.dialogue.font_audit import ASCII_FONT_OFFSET, GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha


def apply_release(arm, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-experimental-ascii-font-v2':
        raise ValueError('Unsupported experimental font format')
    for name, digest in config['dependencies'].items():
        if sha(Path(name).read_bytes()) != digest:
            raise ValueError(f'Font dependency changed: {name}')
    if sha(arm) != config['source_ARM9_sha256']:
        raise ValueError('Font test requires the complete registered V4749 predecessor')
    source = GameAsciiFont.from_arm9(arm).glyphs
    target = Path(config['font_asset']).read_bytes()
    if sha(source) != config['source_font_sha256'] or sha(target) != config['target_font_sha256']:
        raise ValueError('Original or reviewed mockup font hash differs')
    if len(source) != len(target) or len(target) != 95 * 11:
        raise ValueError('Font must retain all 95 native six-column, eleven-row cells')
    if config['offset'] != ASCII_FONT_OFFSET or target[-11:] != source[-11:]:
        raise ValueError('Font location or reserved final glyph differs')
    result = arm[:ASCII_FONT_OFFSET] + target + arm[ASCII_FONT_OFFSET + len(target):]
    if len(result) != len(arm) or sha(result) != config['target_ARM9_sha256']:
        raise ValueError('Final ARM9 differs from the exact font-only successor')
    changed = [code for code in range(33, 128)
               if source[(code - 33) * 11:(code - 32) * 11] != target[(code - 33) * 11:(code - 32) * 11]]
    return result, {
        'status': 'experimental; user gameplay approval pending',
        'predecessor_profile': config['predecessor_profile'],
        'source_ARM9_sha256': sha(arm), 'target_ARM9_sha256': sha(result),
        'source_font_sha256': sha(source), 'target_font_sha256': sha(target),
        'owned_span': [ASCII_FONT_OFFSET, ASCII_FONT_OFFSET + len(target)],
        'changed_records': [f'ASCII_U{code:04X}' for code in changed],
        'changed_glyph_count': len(changed),
        'ordinary_glyphs_raised_pixels': 2,
        'tall_punctuation_raised_at_most_pixels': 1,
        'redrawn_descenders': 'gjpqy', 'completed_symbols': '[](){}$_',
        'native_cell': [6, 11], 'native_advance': 6,
        'native_drawing_code_and_all_bytes_outside_font_identical': True,
        'line_spacing_textbox_origins_and_string_bytes_unchanged': True,
        'font_asset': config['font_asset'], 'font_asset_sha256': sha(target),
    }
