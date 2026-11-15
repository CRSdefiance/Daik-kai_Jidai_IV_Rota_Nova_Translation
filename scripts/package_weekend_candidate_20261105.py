"""Package the exact registered cumulative candidate and freshly verify its clean-input patch."""
from pathlib import Path
import contextlib,io,json,shutil,sys,zipfile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.verify_release_baseline import main as baseline_check,files

ROOT=Path('out/Translation_DS_Weekend_Test_2026-11-05')
AUDIT=Path('work/analysis/Weekend_testing_package_v1_20261105')
ZIP=Path(str(ROOT)+'.zip')
RELEASE=Path('work/analysis/Rafael867_extended_release_verified_v3_20261105/registered_release_verification.json')
REGISTRY=Path('translations/release_stack.json')

if __name__=='__main__':
    assert not ROOT.exists() and not AUDIT.exists() and not ZIP.exists()
    release=load(RELEASE);manifest_path=Path(release['manifest']);manifest=load(manifest_path)
    candidate=Path(release['candidate']);patch=Path(release['patch']);base=Path(release['canonical_base']);clean=Path('work/clean.nds')
    original={p:sha(p.read_bytes()) for p in [RELEASE,REGISTRY,manifest_path,candidate,patch,base,clean,Path('dk4tool/rom/nds.py')]}
    assert original[candidate]==release['candidate_sha256']=='3bf3239736982e6398eda1f837f4c249b93e541128985013fbde02466bcbaa9c'
    assert original[manifest_path]==release['manifest_sha256'] and original[patch]==release['patch_sha256']
    assert original[REGISTRY]==release['registry_sha256']==manifest['release_stack_sha256']
    assert original[base]==release['canonical_sha256']==manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert original[clean]==release['clean_input_sha256']=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert manifest['candidate_sha256']==release['candidate_sha256'] and manifest['profile']==release['profile']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending'] and release['experimental_not_promoted']
    registry=load(REGISTRY);profile=registry['profiles'][release['profile']]
    assert profile['status']=='experimental' and len(registry['accepted_layers'])==release['accepted_layers']==114
    assert len(manifest['batches'])==681 and len(manifest['checks'])==release['passing_release_checks']==26
    assert all(v is True for v in manifest['checks'].values()) and release['all_eight_registered_final_stages_preserved']
    normalize=lambda p:str(Path(p)).replace('\\','/')
    applied={normalize(p) for p in manifest['batches']}
    for accepted in registry['accepted_layers']:
        assert accepted['status']=='accepted'
        assert accepted.get('baked_into_baseline') or normalize(accepted['batch']) in applied
    stage_keys=['ascii_glyph_right_bounds','owned_name_glyph','owned_name_fields','owned_name_fields_next',
        'owned_name_fields_grouped','owned_static_text','owned_reviewed_text_data','owned_Fernan_name_field']
    assert all(normalize(profile[k]) in applied for k in stage_keys)
    startup_path=Path(release['own_registered_startup']);startup=load(startup_path)
    assert sha(startup_path.read_bytes())==release['own_registered_startup_sha256']
    assert startup['candidate_sha256']==release['candidate_sha256'] and startup['cold_boot'] and not startup['savestate']
    assert startup['frames']==4001 and startup['actual_captain_getter']==startup['actual_route_word']==0
    assert not startup['callback_errors'] and startup['ordinary_title_NewGame_Rafael_Castor_andopening_observed']
    capture=Path(startup['capture_report']);assert sha(capture.read_bytes())==startup['capture_report_sha256']
    AUDIT.mkdir(parents=True);ROOT.mkdir(parents=True)
    for path in [candidate,manifest_path,patch,RELEASE,startup_path]:
        dest=ROOT/path.name;shutil.copy2(path,dest);assert sha(dest.read_bytes())==sha(path.read_bytes())
    rom=ROOT/candidate.name;delta=ROOT/patch.name
    rebuilt=AUDIT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
    apply_xdelta(clean,delta,rebuilt)
    assert rebuilt.read_bytes()==rom.read_bytes()==candidate.read_bytes()
    baseline_files,candidate_files=map(lambda p:files(NdsImage.open(p)),[base,rom])
    changed=sorted(p for p in baseline_files.keys()|candidate_files.keys() if baseline_files.get(p)!=candidate_files.get(p))
    assert changed==sorted(manifest['changed_paths']) and len(changed)==53
    assert {f'/data/SC{i}.DK4' for i in range(4)}<=set(changed)
    argv=sys.argv[:];log=io.StringIO()
    try:
        sys.argv=['verify_release_baseline.py',str(base),str(rom),*[v for p in changed for v in ['--allow-path',p]]]
        with contextlib.redirect_stdout(log):baseline_check()
    finally:sys.argv=argv
    (AUDIT/'baseline_verifier.txt').write_text(log.getvalue(),encoding='utf-8')
    contents=dict(status='experimental weekend testing candidate; not promoted',profile=release['profile'],
        candidate=candidate.name,candidate_sha256=release['candidate_sha256'],canonical_base=str(base),canonical_base_sha256=release['canonical_sha256'],
        clean_input_sha256=release['clean_input_sha256'],patch=patch.name,patch_sha256=release['patch_sha256'],
        registry_sha256=release['registry_sha256'],accepted_layers=registry['accepted_layers'],registered_manifest_entries=manifest['batches'],
        original_final_stage_configs={k:profile[k] for k in stage_keys},changed_internal_files=changed,
        existing_registered_checks=manifest['checks'],existing_own_startup=dict(frames=4001,cold_boot=True,savestate=False,
            observed='title, New Game, Rafael selection and opening',report=startup_path.name,
            scope='Existing exact-ROM automated headless evidence; no new complete playthrough or hardware verification.'),
        fresh_package_checks=dict(all_delivered_files_exact_to_registered_originals=True,all114_accepted_layers_preserved=True,
            all_eight_final_stages_present=True,all_four_route_archives_present=True,baseline_and_menu_anchor_verifier=True,
            actual_changed_files_exactly_the53_manifest_paths=True,delivered_patch_reconstructs_clean_input_byte_exact=True),
        integrated_editorial_records=12712,unfinished_B141_B160_557_record_batch_included=False,
        ROM_rebuild_or_main_promotion=False,source_ROM_not_distributed=True)
    save(ROOT/'build_contents.json',contents)
    readme=f'''# Translation DS — weekend test candidate, November 5, 2026

Load `{candidate.name}` on your usual emulator or device. This is the current **combined work-in-progress candidate**, including all four route archives, shared text, UI/graphics work and the registered runtime/name corrections. It includes12,712 integrated editorial reviews. It remains experimental; the main build is unchanged.

The newly reviewed557-record Rafael B141–B160 batch is **not included yet**. It still needs final display, stored-script and representative-scene checks. Those scenes currently use the earlier translations. The two full-catalogue de corrections, unfinished artwork and remaining editorial scope are also still open.

## Useful weekend checks

1. Cold-boot and start Rafael's story. Check the opening conversations and tutorials, including Julio's normal-font F in “First, you're the captain, Rafael.”
2. Try the early ship, trading, crew and sailing instructions. Check that every page starts and ends with complete characters and that A advances/returns normally.
3. Visit shops, the Guild, taverns and town conversations. Look for natural dialogue, awkward early wraps, inconsistent names, missing letters and unexpected blank pages.
4. Continue normal play on any route you want to test. For a finding, note this build, route, town/scene, the exact line and what happened. A screenshot is useful for a display issue; no guide-photo collection is needed.

## Included files and verification

The adjacent manifest is the original registered build manifest:681 entries,114 accepted layers, all eight final runtime/name/text stages and26 passing release checks. It lists all applied accepted/experimental batches and53 changed internal files. `build_contents.json` provides the complete lists. The immutable canonical base is `{base.name}`, SHA-256`{release['canonical_sha256']}`. Profile:`{release['profile']}`.

Fresh packaging checks verify the ROM and original manifest hashes, unchanged main/registry/core, all four route archives, English menu anchors, the exact declared internal-file changes and clean-input reconstruction from the included patch. Existing exact-ROM cold-boot evidence covers4001 frames through title, New Game, Rafael selection and opening. This is targeted automated emulator evidence, not a full playthrough or new device verification.

ROM SHA-256:
`{release['candidate_sha256']}`

The included `{patch.name}` reconstructs this exact ROM from your clean Japanese input with SHA-256`{release['clean_input_sha256']}`. With xdelta3 installed:

```text
xdelta3 -d -s clean.nds {patch.name} rebuilt_candidate.nds
```

The rebuilt file must have the ROM hash above. The clean ROM is not included. `SHA256SUMS.txt` covers every delivered file other than itself. The original ROMs, translations and evidence remain preserved.
'''
    (ROOT/'README.md').write_text(readme,encoding='utf-8')
    hashes={p.name:sha(p.read_bytes()) for p in sorted(ROOT.iterdir()) if p.is_file()}
    (ROOT/'SHA256SUMS.txt').write_text(''.join(f'{digest}  {name}\n' for name,digest in hashes.items()),encoding='utf-8')
    with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=3) as archive:
        for path in sorted(ROOT.iterdir()):archive.write(path,arcname=ROOT.name+'/'+path.name)
    with zipfile.ZipFile(ZIP) as archive:assert archive.testzip() is None
    for path,digest in original.items():assert sha(path.read_bytes())==digest,path
    save(AUDIT/'package_verification.json',dict(package=str(ROOT),zip=str(ZIP),zip_sha256=sha(ZIP.read_bytes()),
        files=hashes,ROM_sha256=release['candidate_sha256'],clean_input_reconstruction=str(rebuilt),
        reconstructed_sha256=sha(rebuilt.read_bytes()),fresh_checks=contents['fresh_package_checks'],
        ZIP_CRCs_pass=True,protected_originals={str(p):v for p,v in original.items()},all_originals_unchanged=True,
        no_registry_ROM_main_ortranslation_edits=True,experimental_not_promoted=True,new_credit=0,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    Path(str(ZIP)+'.sha256').write_text(sha(ZIP.read_bytes())+'  '+ZIP.name+'\n',encoding='utf-8')
    print('READY',ZIP,'ROM',rom,'SHA256',release['candidate_sha256'],'ZIP bytes',ZIP.stat().st_size)
