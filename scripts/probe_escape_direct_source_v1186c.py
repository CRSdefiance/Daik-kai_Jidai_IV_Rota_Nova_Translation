"""Accept a naturally single-line notice while preserving exact reference output."""
import inspect
from pathlib import Path
from scripts import probe_escape_direct_source_v1186 as previous


def main():
    source=inspect.getsource(previous.main)
    replacements={
        'entries=current_entries(common,arm);raw=RAW.read_bytes()':"entries=current_entries(common,rom.read_file('/__arm9__.bin'));raw=RAW.read_bytes()",
        "assert b'\\n' in bytes.fromhex(seen['formatted_hex'])":"if len(candidates[0]['lines'])>1: assert b'\\n' in bytes.fromhex(seen['formatted_hex'])",
    }
    for old,new in replacements.items():
        assert source.count(old)==1;source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/escape_direct_source_v1186c')}
    exec(compile(source,__file__,'exec'),env);env['main']()


if __name__=='__main__':main()
