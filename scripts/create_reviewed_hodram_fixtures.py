"""Prepare selected complete scenes after original initializers for focused QA."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/create_hodram_representative_fixtures.py').read_text(encoding='utf-8'),{
    "    parser.add_argument('--out', type=Path, required=True)":
    "    for arg in ['reference','native','out']:parser.add_argument('--'+arg,type=Path,required=True)\n    parser.add_argument('--scenes',nargs='+',required=True,help='Complete scene block:frame-count entries')\n    parser.add_argument('--capture-prefix',required=True)",
    "    rebuild_path = Path('work/analysis/Hodram_B61_B70_stored_20261101/reconstruction.json')":
    '    rebuild_path = args.reference',
    "    native_path = Path('work/analysis/Hodram_B61_B70_stored_native_20261101/stored_native_verification.json')":
    '    native_path = args.native',
    "    assert native['research_ROM_sha256'] == rebuilt['research_ROM_sha256']":
    "    assert native['reconstruction_sha256']==rebuilt['story_reconstruction_sha256']\n    assert sha(Path(rebuilt['story_reconstruction']).read_bytes())==rebuilt['story_reconstruction_sha256']",
    '    for number, frames in [(67, 16001), (69, 8001)]:':
    "    requested=[tuple(map(int,value.split(':'))) for value in args.scenes]\n    assert len({n for n,f in requested})==len(requested) and all(4001<=f<=20001 for n,f in requested)\n    for number, frames in requested:",
    "capture_folder=f'work/emulation_v193/Hodram_pending_B{number}_20261101'":
    "capture_folder=f'work/emulation_v193/{args.capture_prefix}_B{number}'",
    "    print('Two full-script initialized scene fixtures prepared; no natural activation or gameplay coverage claimed yet.')":
    "    print(dict(complete_script_fixtures=len(fixtures),actual_coverage_pending=True,natural_activation=False))",
})
exec(compile(source,__file__+'::source-qualified-complete-scenes','exec'),globals())
