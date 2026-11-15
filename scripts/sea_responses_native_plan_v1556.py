"""Repack five revised sea-inspection paragraphs and preserve three retained copies."""
import inspect
from pathlib import Path
from scripts import ship_loss_surrender_native_plan_v1444 as previous
from scripts import sea_responses_runtime_v1555 as runtime
from dk4tool.patch.declaration_responses_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/sea_responses_payload_v1556')
MANUSCRIPT = Path('translations/sea_responses_editorial_manuscript_v1.json')
IDS = tuple(range(2209, 2217))
PROFILE = 'sea-inspection-role7-postmacro-v1'
SOURCE_COMMON = '8388243e0da249d0b54379e90106b56dfdbb075adc0c4837c9bec1329ec1cc9e'
SOURCE_ARM = runtime.SOURCE


def compiled(row):
    text = row['english']
    if row['message_id'] not in IDS or not text or not text.isascii() or text != ' '.join(text.split()):
        raise ValueError('One natural unwrapped paragraph without alignment is required')
    if any(ord(c) < 32 or ord(c) > 126 or c in '%{}' for c in text):
        raise ValueError('No source arguments,authored controls or layout markup are permitted')
    if row['native_argument_count'] != 0 or row['source_native_macros']:
        raise ValueError('These original reactions have no runtime argument or speech macro')
    if len(text.encode('ascii')) >= 160:
        raise ValueError('Longer paragraphs need a separately reviewed native contract')
    return text.encode('ascii')


def plan(common, arm, doc):
    source = inspect.getsource(previous.plan)
    for old, new in [
        ('assert changed==[n for n in IDS if n!=2100]', "assert changed==[r['message_id'] for r in doc['records'] if r['editorial_decision']=='revise'] and len(changed)==5"),
        ('=={22}', '=={23}'), ('r.block==22', 'r.block==23'), ('source.blocks[22]', 'source.blocks[23]'),
        ('rebuilt[22]', 'rebuilt[23]'), ('DIRECTORY_OFFSET+22*4', 'DIRECTORY_OFFSET+23*4'), ('if b!=22', 'if b!=23'),
        ('all3645_unselected_or_retained_texts_and_native_copy_spans_preserved', 'all3663_unselected_or_retained_texts_and_native_copy_spans_preserved'),
        ('only_COMMON22_native_metadata_and_existing188_172_selector_spans_changed', 'only_COMMON23_native_metadata_and_existing188_selector_span_changed'),
        ('old_new_block22_bytes', 'old_new_block23_bytes')]:
        assert old in source, old
        source = source.replace(old, new)
    env = {**previous.__dict__, 'SOURCE_COMMON': SOURCE_COMMON, 'SOURCE_ARM': SOURCE_ARM, 'IDS': IDS, 'PROFILE': PROFILE,
           'runtime': runtime, 'current_entries': current_entries, 'compiled': compiled}
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
        'producer_sha256': sha(Path(__file__).read_bytes()), 'no_ROM_registry_or_completion_change': True, 'full_goal_complete': False})
    print('Sea inspection8 payload:5 revisions3 retentions;3663 other/retained copies,40 blocks,186/188 selector,172 gate and123040 staged preserved.')
