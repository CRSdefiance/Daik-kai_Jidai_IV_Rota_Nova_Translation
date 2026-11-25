"""One fixed native message, complete inherited stack and exact clean patch."""

import copy
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.late_story_editorial import apply_release
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/cliff_editorial_v829')
ROM = Path('out/all_routes_combined_v829_candidate.nds')


def main():
    old,new = [NdsImage.open(p) for p in ('out/all_routes_combined_v820_candidate.nds',ROM)]
    a,b = [{p:v for _,p,v in r.iter_files()} | dict(r.iter_components()) for r in (old,new)]
    assert set(a) == set(b) and {p for p in a if a[p] != b[p]} == {'/data/SC2.DK4'}
    ob,nb = [IlnkContainer.parse(x['/data/SC2.DK4']).blocks for x in (a,b)]
    assert len(ob) == len(nb) and [i for i,(x,y) in enumerate(zip(ob,nb,strict=True)) if x != y] == [294]
    parts = ob[294].split(b'\0')
    at = sum(len(x)+1 for x in parts[:73])
    assert len(parts[73]) == 48 and nb[294][at] == ob[294][at] == 0x94
    assert len(ob[294]) == len(nb[294])
    assert all(at < i < at+48 for i,(x,y) in enumerate(zip(ob[294],nb[294],strict=True)) if x != y)
    manifest = read(ROM.with_suffix('.manifest.json'))
    prior = read('out/all_routes_combined_v820_candidate.manifest.json')
    assert manifest['batches'][:-1] == prior['batches'] and len(manifest['batches']) == 471
    assert Path(manifest['batches'][-1]) == Path('translations/lil_cliff_editorial_v1.json')
    assert all(manifest['checks'].values())
    registry = read('translations/release_stack.json')
    before = read(ROOT/'release_stack_before_v829.json')
    assert registry['accepted_layers'] == before['accepted_layers'] and len(registry['accepted_layers']) == 114
    assert registry['canonical_baseline'] == before['canonical_baseline']
    assert all(registry['profiles'][k] == v for k,v in before['profiles'].items())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    cfg_path = 'translations/lil_cliff_editorial_release_v1.json'
    cfg = read(cfg_path)
    replay = NdsImage.open('out/all_routes_combined_v820_candidate.nds')
    baseline = NdsImage.open(registry['canonical_baseline']['path'])
    replay_report = apply_release(replay,baseline,cfg_path)
    assert replay.read_file('/data/SC2.DK4') == b['/data/SC2.DK4']
    negatives = []
    for case in ('source','record','target'):
        bad = copy.deepcopy(cfg)
        if case == 'source':
            bad['source_file_sha256']['/data/SC2.DK4'] = '0'*64
        elif case == 'record':
            bad['batches'][0]['current_record_hex']['DK4_MES_B294_R0073'] = '95'+parts[73][1:].hex()
        else:
            bad['target_file_sha256']['/data/SC2.DK4'] = '0'*64
        path = ROOT/f'{case}_negative_config_TEST_ONLY.json'
        save(path,bad)
        image = NdsImage.open('out/all_routes_combined_v820_candidate.nds')
        try:
            apply_release(image,baseline,path)
        except ValueError as error:
            assert image.read_file('/data/SC2.DK4') == a['/data/SC2.DK4']
            negatives.append(dict(case=case,rejected=str(error),no_partial_image_mutation=True))
        else:
            raise AssertionError('Bad late editorial configuration was accepted')
    clean = Path('work/clean.nds')
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch = ROM.with_suffix('.xdelta')
    reconstruction = ROOT/'V829_clean_patch_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(clean,ROM,patch)
    apply_xdelta(clean,patch,reconstruction)
    assert reconstruction.read_bytes() == ROM.read_bytes()
    proof = dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),
        only_SC2_B294_R73_body_bytes_change_from_V820=True,
        fixed48_byte_allocation_original94_actor_header_all_other_commands_and_bytes_exact=True,
        ARM9_sha256=sha(b['/__arm9__.bin']),COMMON_sha256=sha(b['/COMMON/MESFILE.DK4']),
        all471_batches114_accepted_layers_and_older_profiles_preserved=True,manifest_checks_all_pass=True,
        exact_late_stage_replay=replay_report,negative_guards=negatives,
        patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_source_sha256=sha(clean.read_bytes()),
        clean_patch_reconstruction_byte_exact=True,
        original_early_stage_guard_failure_log='work/analysis/cliff_editorial_v829/build.log',
        actual_scene_and_startup_verification_separate=True,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(ROOT/'registered_binary_and_patch_verification.json',proof)
    save(ROM.with_suffix('.verification.json'),proof)
    print('PASS:only fixed48-byte SC2 message body changes;471/114 stack,three negative guards and clean reconstruction pass.',flush=True)
    print('V829 SHA256',proof['candidate_sha256'],flush=True)


if __name__ == '__main__':
    main()
