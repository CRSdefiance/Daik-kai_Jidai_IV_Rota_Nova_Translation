"""Full-font successor for refined prose,with exact zero-ink guard accounting."""
from pathlib import Path
from scripts import probe_declaration_fonts_v1537 as previous

if __name__ == '__main__':
    source = Path(previous.__file__).read_text(encoding='utf-8')
    for old, new in [
        ('work/analysis/declaration_responses_fonts_v1537', 'work/analysis/declaration_responses_fonts_v1537c'),
        ('work/analysis/declaration_responses_payload_v1535/native_payload_plan.json', 'work/analysis/declaration_responses_payload_v1535b/native_payload_plan.json'),
        ('translations/declaration_responses_editorial_manuscript_v1.json', 'translations/declaration_responses_editorial_manuscript_v2.json'),
        ("    reps = {r['message_ID']", "    assert not any(raster(arm, b' ', 0x01FFCE40 - 0x02000000, size=(228, 64), instruction_limit=2000000))\n    reps = {r['message_ID']"),
        ('        for index, line in enumerate(lines):', '        blank_guards = []\n        for index, line in enumerate(lines):'),
        ("            assert [e['code'] for e in actual] == list(line.encode('ascii'))", """            guards = []
            while actual and actual[0]['code'] == 32 and actual[0]['x'] == 6:
                guards.append(actual.pop(0))
            assert len(guards) <= 1 and (not guards or index > 0)
            blank_guards.append({'row': index, 'zero_ink_guard_events': guards})
            assert [e['code'] for e in actual] == list(line.encode('ascii'))"""),
        ("'full228x64_native_and_independent_font_exact': True,", "'full228x64_native_and_independent_font_exact': True, 'native_zero_ink_continuation_guards': blank_guards,"),
    ]:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
