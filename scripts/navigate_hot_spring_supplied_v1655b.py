"""Correct a navigator-only Python local binding;1655 sent no emulator inputs."""
from pathlib import Path

if __name__ == '__main__':
    source = Path('scripts/navigate_hot_spring_supplied_v1655.py').read_text(encoding='utf-8')
    assert source.count('            import struct\n') == 1
    source = source.replace('            import struct\n', '')
    source = source.replace('bounded_navigator_v1655.jsonl', 'bounded_navigator_v1655b.jsonl')
    exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
