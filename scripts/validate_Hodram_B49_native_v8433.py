"""Validate independent current-code source/stored glyph/name reconstruction without emulator replay."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B49_native_evidence_v1 import check_native_models
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_independent_native_v8433')
PROOFS={
 'source_display':'work/analysis/Hodram_B49_source_display_v8386b/source_display.json',
 'stored':'work/analysis/Hodram_B49_stored_v8399/stored_bodies.json',
 'models':'work/analysis/Hodram_B49_models_v8408/native_models.json',
 'pages':'work/analysis/Hodram_B49_pages_v8395/compiled_native_pages.json',
}

def require(ok,label):
    if not ok:raise ValueError('B49 independent native:'+label)

if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/hodram_B49_editorial_manuscript_v4.json');data={k:read(p) for k,p in PROOFS.items()}
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    result=check_native_models(data,doc['records'],image,read,require);summary=result['summary']
    assert summary['native_body_pages_recomputed']==28 and summary['scoped_style11_nameplanes_recomputed']==2
    assert len(result['bodies']['clean_Japanese'])==len(result['bodies']['revised_English'])==14 and set(result['names'])=={1,2}
    ROOT.mkdir(parents=True);save(ROOT/'independent_native_models.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript='translations/hodram_B49_editorial_manuscript_v4.json',manuscript_sha256=sha(Path('translations/hodram_B49_editorial_manuscript_v4.json').read_bytes()),independent_native_summary=summary,no_producer_oractual_emulator_replay=True,no_ROM_orcompletion_credit_change=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('dk4tool/patch/hodram_B49_native_evidence_v1.py'),Path('dk4tool/patch/hodram_B49_native_guards_v1.py'),*map(Path,PROOFS.values())]}))
    print('Independent B49 native:28 complete source/stored pages,26progressive/twoFE,two original style11names. All full glyphs/ink/bounds/consumption andtrusted adapters pass.No emulator replay orcredit.')
