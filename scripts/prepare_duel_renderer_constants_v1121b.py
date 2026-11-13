"""Bind the transcription to the three observed original renderer literals."""
from pathlib import Path


def main():
    source = Path('scripts/duel_renderer_thumb_v1121.py').read_text(encoding='utf-8')
    target = Path('scripts/duel_renderer_thumb_v1121b.py')
    assert not target.exists()
    source = source.replace("duel_renderer_thumb_v1121')", "duel_renderer_thumb_v1121b')")
    for before, after in (
        ('0x022a3cdc', '0x022cf7dc'), ('0x022a3884', '0x022cf784'), ('0x021125b4', '0x023120b4'),
        ('0x022A3CDC', '0x022CF7DC'), ('0x022A3884', '0x022CF784'), ('0x021125B4', '0x023120B4')):
        assert source.count(before) == 1
        source = source.replace(before, after)
    target.write_text(source, encoding='utf-8')
    print('Created source-literal-bound successor;failed guessed-literal predecessor retained.')


if __name__ == '__main__':
    main()
