"""Archive successor: ordinary startup reports have no pause-snapshot field."""
import inspect
from pathlib import Path
from scripts import archive_powder_fire_release_v1324 as previous

if __name__=='__main__':
    source = inspect.getsource(previous.main)
    old = "report['read_only_pause_RAM_snapshots']"
    assert source.count(old)==1
    source = source.replace(old,"report.get('read_only_pause_RAM_snapshots',[])")
    env = {**previous.__dict__,'__file__':__file__,
        'ROOT':Path('work/analysis/powder_fire_archive_v1324b'),
        'DEST':Path('E:/Rota Nova translations/Editorial review/V1324b Powder fire completed release')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
