"""Register the complete inherited stack plus the native-audited planning stage."""

from copy import deepcopy
from pathlib import Path
from dk4tool.patch import planning_finance_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/planning_finance_v863')
MANUSCRIPT=Path('translations/planning_finance_editorial_manuscript_v2.json')
OLD=Path('out/all_routes_combined_v855_candidate.nds')


def main():
    assert not Path(owned.CONFIG).exists()
    registry_path=Path('translations/release_stack.json');registry=read(registry_path)
    assert 'all-routes-unified-v863' not in registry['profiles']
    save(ROOT/'registry_before.json',registry)
    rom=NdsImage.open(OLD);c,a,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),read(MANUSCRIPT))
    assert sha(c)==read('work/analysis/common_single_cache_v861/prospective_repack.json')['target_COMMON_sha256']
    save(ROOT/'repack_plan.json',proof)
    (ROOT/'target_COMMON.bin').write_bytes(c);(ROOT/'target_ARM9.bin').write_bytes(a)
    audit='work/analysis/planning_finance_v863/native_audit/audit.json'
    copies={name:f'work/analysis/common_single_cache_v862/{name}_native.json' for name in ('code_only','target','boundary')}
    dependencies=list(map(Path,('dk4tool/patch/planning_finance_editorial_v2.py','dk4tool/patch/common_single_cache_v861.py',
        'scripts/planning_finance_layout_v860.py','scripts/livestock_prayer_layout_v854.py','scripts/work_comments_layout_v843.py',
        'scripts/probe_planning_finance_fonts_v860.py','scripts/probe_work_fonts_v843.py','scripts/probe_common_single_cache_v862.py',
        'scripts/research_common_single_cache_v861.py','scripts/audit_planning_finance_native_v863.py',
        'work/analysis/common_single_cache_v861/prospective_repack.json','translations/planning_finance_editorial_manuscript_v1.json',
        'work/analysis/planning_finance_v857/source_context_packet.json','work/analysis/planning_finance_v860/native_font_proof.json',
        'work/analysis/planning_finance_v860/visual_review.json',audit,*copies.values())))
    config={'format':'dk4-planning-finance-editorial-v2','source_common_sha256':owned.SOURCE_COMMON,'source_arm9_sha256':owned.SOURCE_ARM,
        'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),'directory_sha256':proof['directory_sha256'],
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'native_cache_proofs':copies,
        'native_consumer_audit':audit,'dependencies':{str(p):sha(p.read_bytes()) for p in dependencies}}
    save(owned.CONFIG,config)
    replay=owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)
    assert replay[:2]==(c,a)
    assert read(registry_path)==read(ROOT/'registry_before.json')
    profile=deepcopy(registry['profiles']['all-routes-unified-v855'])
    profile.update(planning_finance_editorial=owned.CONFIG,status='experimental',
        description='Complete V855 stack plus24 source-reviewed planning19/finance20 comments and single8KiB cache within original allocation.',
        note='Native complete7336 target and7336 code-only copies,214 exact8KiB boundary cases and534 sequence cases pass. All24 glyph previews/216x36 bounds pass. Actual cold boot and revised scenes pending;canonical unchanged.')
    registry['profiles']['all-routes-unified-v863']=profile;save(registry_path,registry)
    print('V863 registered;all earlier profiles unchanged. Actual boot,scenes and exact patch remain.',flush=True)


if __name__=='__main__':main()
