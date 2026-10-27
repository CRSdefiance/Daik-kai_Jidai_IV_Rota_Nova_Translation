"""Use exact source edits for nested callbacks instead of outer bytecode constants."""
from pathlib import Path


def main():
    source = Path('scripts/probe_duel_thumb_equivalence_v1122.py').read_text(encoding='utf-8')
    target = Path('scripts/probe_duel_thumb_equivalence_v1122b.py')
    assert not target.exists()
    source = source.replace('from types import FunctionType', 'import inspect')
    source = source.replace("duel_thumb_equivalence_v1122')", "duel_thumb_equivalence_v1122b')")
    begin = source.index('    constants = list(')
    end = source.index('    return function, observations', begin)
    source = source[:begin] + '''    text=inspect.getsource(original.execute)
    changes={'BASE + 0xDAC4':str(font_return),
             'sp + 0x47C':f'sp + {0x46C if proposed else 0x47C}',
             'sp + 0x4A4':f'sp + {0x494 if proposed else 0x4A4}',
             'controller, side, 60,':f'controller, side, {delay},'}
    for before,after in changes.items():
        assert text.count(before)==1,before
        text=text.replace(before,after)
    namespace={**original.execute.__globals__,'get_machine':machine,
               'selected_scope':lambda lr,parent,table:lr==font_return and
               parent==BASE+0xD4BC and table in original.TABLES}
    exec(compile(text,'explicit_source_scoped_duel_caller_probe','exec'),namespace)
    function=namespace['execute']
''' + source[end:]
    target.write_text(source, encoding='utf-8')
    print('Created explicit nested-callback source successor;rejected bytecode attempt preserved.')


if __name__ == '__main__':
    main()
