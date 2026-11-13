"""Run independent native/actual production readers over existing captures;no emulator producer replay."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B49_native_evidence_v1 import check_native_models
from dk4tool.patch.hodram_B49_actual_evidence_v1 import check_actual
from scripts.validate_Hodram_B49_native_v8433 import PROOFS as native_paths,require
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_independent_actual_v8434')
PROOFS={**native_paths,
 'fixtures':'work/analysis/Hodram_B49_fixtures_v8406/two_whole_scripts.json',
 'tail_fixtures':'work/analysis/Hodram_B49_tail_v8415/bounded_tail_fixtures.json',
 'actual':'work/analysis/Hodram_B49_actual_v8409/B49/paired_actual_dialogue_headers_flow_returns.json',
 'tail_actual':'work/analysis/Hodram_B49_tail_actual_v8417/bounded_tail_actual.json',
}

if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/hodram_B49_editorial_manuscript_v4.json');data={k:read(p) for k,p in PROOFS.items()}
    parent=NdsImage.open(doc['current_ROM']);clean=NdsImage.open('work/clean.nds');mapping=read('work/analysis/Hodram_B49_relocation_v8398/reconstruction.json')
    rebuilt=dict(target_archive=Path(mapping['target_archive']).read_bytes());assert sha(rebuilt['target_archive'])==mapping['target_archive_sha256']
    native=check_native_models(data,doc['records'],parent,read,require)
    actual=check_actual(data,doc['records'],parent,clean,rebuilt,native,read,require)
    ROOT.mkdir(parents=True);save(ROOT/'independent_actual.json',dict(manuscript='translations/hodram_B49_editorial_manuscript_v4.json',manuscript_sha256=sha(Path('translations/hodram_B49_editorial_manuscript_v4.json').read_bytes()),native_summary=native['summary'],actual_summary=actual['summary'],no_emulator_orproducer_replay=True,menu_owned_backing_FE_typed_VRAM_comparison_controls_atomic_andregistered_release_pending=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('dk4tool/patch/hodram_B49_actual_evidence_v1.py'),Path('dk4tool/patch/hodram_B49_native_evidence_v1.py'),*map(Path,PROOFS.values())]}))
    print('Independent B49 actual:all4whole/boundedfixtureROMs reconstruct/invert;6capturedgroups/34pageoccurrences/200completebody-name holds/14unique speeches/bothmenuvalues/normalreturns independently pass.No emulator replay orcredit.')
