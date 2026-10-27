"""Explicit successor payload for the refined war-response manuscript."""
from pathlib import Path
from scripts.declaration_responses_native_plan_v1535 import plan, compiled, IDS, PROFILE, SOURCE_COMMON, SOURCE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/declaration_responses_payload_v1535b')
MANUSCRIPT = Path('translations/declaration_responses_editorial_manuscript_v2.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc = read(MANUSCRIPT)
    rom = NdsImage.open(doc['current_ROM'])
    c, a, proof = plan(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), doc)
    assert proof['runtime_plan']['patches'] == read('work/analysis/declaration_responses_runtime_v1536/runtime_plan.json')['patches']
    ROOT.mkdir(parents=True)
    cp, ap = ROOT / 'COMMON_RESEARCH_ONLY.DK4', ROOT / 'ARM9_PAYLOAD_RESEARCH_ONLY.bin'
    cp.write_bytes(c)
    ap.write_bytes(a)
    save(ROOT / 'native_payload_plan.json', {**proof, 'target_COMMON': str(cp), 'target_ARM9': str(ap),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'no_ROM_registry_or_completion_change': True, 'full_goal_complete': False})
    print('Refined war8 payload passes;runtime patches identical to529442-case proof,all prior spans/allocations preserved.')
