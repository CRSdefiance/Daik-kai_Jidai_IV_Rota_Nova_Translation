"""Exact successor plan for seven refined paragraphs and unchanged runtime scope."""
import inspect
from pathlib import Path
from scripts import retreat_transfer_native_plan_v1511 as previous
from scripts import retreat_transfer_runtime_v1509b as runtime
from scripts.retreat_transfer_native_plan_v1511 import IDS, PROFILE, SOURCE_COMMON, SOURCE_ARM, compiled
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/retreat_transfer_payload_v1514')
MANUSCRIPT = Path('translations/retreat_transfer_editorial_manuscript_v2.json')


def plan(common, arm, doc):
    source = inspect.getsource(previous.plan)
    for old, new in [('len(changed)==3', 'len(changed)==7'),
                     ('all3665_unselected_or_retained_texts_and_native_copy_spans_preserved',
                      'all3661_unselected_or_retained_texts_and_native_copy_spans_preserved')]:
        assert source.count(old) == 1
        source = source.replace(old, new)
    env = {**previous.__dict__, 'runtime': runtime}
    exec(compile(source, __file__, 'exec'), env)
    return env['plan'](common, arm, doc)


if __name__ == '__main__':
    assert not ROOT.exists()
    doc = read(MANUSCRIPT)
    rom = NdsImage.open(doc['current_ROM'])
    c, a, proof = plan(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), doc)
    ROOT.mkdir(parents=True)
    cp, ap = ROOT / 'COMMON_RESEARCH_ONLY.DK4', ROOT / 'ARM9_PAYLOAD_RESEARCH_ONLY.bin'
    cp.write_bytes(c)
    ap.write_bytes(a)
    save(ROOT / 'native_payload_plan.json', {**proof, 'target_COMMON': str(cp), 'target_ARM9': str(ap),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'no_ROM_registry_or_completion_change': True,
        'full_goal_complete': False})
    print('Retreat7 refined payload: 3661 other texts/copies, 40 blocks, 186/188 selector and 172-byte gate preserved.')
