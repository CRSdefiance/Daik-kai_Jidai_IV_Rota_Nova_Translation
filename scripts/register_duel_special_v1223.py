"""Register complete V1206 ancestry plus15 source-reviewed special calls."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import duel_special_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.duel_special_native_plan_v1218 import plan
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_special_release_v1223')
PROFILE = 'all-routes-unified-v1224'


def main():
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    manuscript = Path('translations/duel_special_editorial_manuscript_v2.json')
    doc = read(manuscript)
    rom = NdsImage.open('out/all_routes_combined_v1206_candidate.nds')
    c, a, proof = plan(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), doc)
    registry_path = Path('translations/release_stack.json')
    registry, raw = read(registry_path), registry_path.read_bytes()
    builder = Path('scripts/build_integrated_release.py')
    before = builder.read_bytes()
    assert PROFILE not in registry['profiles'] and b"profile_config.get('duel_special_editorial')" not in before
    anchor = b'    # Lexically valid "% o"'
    assert before.count(anchor) == 1
    lo = before.index(b"    duel_bark_editorial = profile_config.get('duel_bark_editorial')")
    hi = before.index(anchor)
    block = before[lo:hi].replace(b'duel_bark_editorial', b'duel_special_editorial').replace(
        b'DUEL_BARK_NATIVE_SELECTION_METADATA', b'DUEL_SPECIAL_NATIVE_SELECTION_METADATA').replace(
        b'DUEL_BARK_FIVE_TABLE_FRONT_SAME_OWNED108', b'DUEL_SPECIAL_SOURCE_OWNED_HELPER64_AND_FRONT108')
    after = before[:hi]+block+before[hi:]
    assert after.replace(block, b'', 1) == before
    compile(after, str(builder), 'exec')
    files = [str(Path(__file__)), str(manuscript), 'dk4tool/patch/duel_special_editorial.py',
        'scripts/duel_special_native_plan_v1218.py', 'scripts/duel_special_dispatch_v1217.py',
        'scripts/duel_special_layout_v1216.py', 'scripts/prepare_duel_special_prose_v1216.py',
        'scripts/research_duel_special_context_v1215.py', 'scripts/research_duel_special_context_v1215b.py',
        'scripts/research_duel_special_dispatch_v1217.py', 'scripts/verify_duel_special_native_v1219.py',
        'scripts/verify_duel_special_native_v1219b.py', 'scripts/verify_duel_special_copies_v1220.py',
        'scripts/verify_duel_special_escape_v1221.py', 'scripts/approve_duel_special_native_v1222.py',
        'translations/duel_bark_editorial_release_v1.json', 'translations/duel_special_editorial_manuscript_v1.json',
        'work/analysis/duel_special_native_v1218/native_payload_plan.json']
    files += [doc[k] for k in ('native_context_proof', 'native_font_proof', 'native_copy_proof',
                             'escape_regression_proof', 'dispatch_proof', 'visual_review')]
    files += [read(doc['native_font_proof'])['review_sheet']]
    files += [r['path'] for r in read(doc['native_font_proof'])['bound_effective_sources']]
    config = {'format': 'dk4-duel-special-editorial-v1', 'source_common_sha256': owned.SOURCE_COMMON,
        'source_arm9_sha256': owned.SOURCE_ARM, 'target_common_sha256': sha(c), 'target_arm9_sha256': sha(a),
        'directory_sha256': proof['directory_sha256'], 'manuscript': str(manuscript),
        'dependencies': {p: sha(Path(p).read_bytes()) for p in dict.fromkeys(files)}}
    ROOT.mkdir(parents=True)
    save(owned.CONFIG, config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), owned.CONFIG)[:2] == (c, a)
    (ROOT/'target_COMMON.bin').write_bytes(c)
    (ROOT/'target_ARM9.bin').write_bytes(a)
    save(ROOT/'repack_plan.json', proof)
    (ROOT/'registry_before_raw.json').write_bytes(raw)
    save(ROOT/'registry_before.json', registry)
    (ROOT/'builder_before.py').write_bytes(before)
    (ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    assert registry_path.read_bytes() == raw and builder.read_bytes() == before
    builder.write_bytes(after)
    profile = deepcopy(registry['profiles']['all-routes-unified-v1206'])
    profile.update(duel_special_editorial=owned.CONFIG, status='experimental',
        description='Full V1206 stack plus15 source-reviewed original numeric special-move calls, including Julio2146.',
        note='51 full fonts49 caller exclusions;131324 dispatch;7336 copies180 cache sequences;13 escape pipelines. Source-owned64-byte unreachable selector tail and existing108-byte front; no allocation growth. Startup, exact patch and original special gameplay pending;canonical unchanged.')
    registry['profiles'][PROFILE] = profile
    save(registry_path, registry)
    save(ROOT/'registration_provenance.json', {'profile': PROFILE, 'source_profile': 'all-routes-unified-v1206',
        'builder_before_sha256': sha(before), 'builder_after_sha256': sha(after),
        'optional_stage_removal_restores_prior_builder_exact': True,
        'registry_before_sha256': sha(raw), 'registry_after_sha256': sha(registry_path.read_bytes()),
        'all_prior_profiles_accepted_layers_and_batches_preserved': True,
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'build_startup_patch_actual_gameplay_and_completion_pending': True, 'full_goal_complete': False})
    print('V1224 full experimental profile registered;build and original special activation remain pending.', flush=True)


if __name__ == '__main__':
    main()
