"""All custom-name lengths1-23 through prospective ceremony consumers."""

import inspect
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import probe_ceremony_layout_v807 as probe
from scripts.refine_ceremony_layout_v807 import MANUSCRIPT
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/ceremony_layout_v807_name_bounds')


def main():
    source=inspect.getsource(probe.main)
    needle="b'ABCDEFGHIJKLMNOPQRSTUVW'"
    assert source.count(needle)==1
    source=source.replace(needle,"*(b'ABCDEFGHIJKLMNOPQRSTUVW'[:length] for length in range(1,24))")
    env={**probe.__dict__,'ROOT':ROOT,'MANUSCRIPT':MANUSCRIPT}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
    report=read(ROOT/'research_report.json')
    report.update(adapter_producer_sha256=sha(Path(__file__).read_bytes()),
        effective_main_sha256=sha(source.encode()),synthetic_name_lengths=list(range(1,24)),
        synthetic_bounds_not_claimed_as_earned_or_user_names=True)
    save(ROOT/'research_report.json',report)
    assert report['layouts']==202
    print('202 exhaustive-length prospective cases saved; findings require review before approval.',flush=True)


if __name__=='__main__':main()
