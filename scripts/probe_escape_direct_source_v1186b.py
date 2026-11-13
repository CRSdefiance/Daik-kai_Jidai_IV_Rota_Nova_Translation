"""Use the unchanged COMMON's exact registered source parser without weakening it."""
import inspect
from pathlib import Path
from scripts import probe_escape_direct_source_v1186 as previous


def main():
    source=inspect.getsource(previous.main)
    old='entries=current_entries(common,arm);raw=RAW.read_bytes()'
    new="entries=current_entries(common,rom.read_file('/__arm9__.bin'));raw=RAW.read_bytes()"
    assert source.count(old)==1
    source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/escape_direct_source_v1186b')}
    exec(compile(source,__file__,'exec'),env);env['main']()


if __name__=='__main__':main()
