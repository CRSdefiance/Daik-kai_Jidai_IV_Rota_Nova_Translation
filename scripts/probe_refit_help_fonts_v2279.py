"""Successor controlled native font probe, all31 help paragraphs including revisions."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/refit_help_fonts_v2279');OLD=Path('scripts/verify_refit_editorial_v830.py')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);source=OLD.read_text()
 changes={
 'from scripts.prepare_refit_editorial_v830 import MANUSCRIPT, ROM, ROOT':"MANUSCRIPT=Path('translations/refit_contextual_editorial_manuscript_v1.json');ROM=Path('out/all_routes_combined_v2171_candidate.nds');ROOT=Path('work/analysis/refit_help_fonts_v2279')",
 "    target = NdsImage.open(ROM).read_file('/__arm9__.bin')":"    target = Path('work/analysis/refit_spritsail_payload_v2278/ARM9_RESEARCH_ONLY.bin').read_bytes()\n    manuscript['records']=[r for r in manuscript['records']if r['consumer']=='refit-help27-pair-safe-v1']\n    assert len(manuscript['records'])==31",
 "        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),":"        'source_candidate': str(ROM), 'source_candidate_sha256': sha(ROM.read_bytes()),\n        'research_ARM9_sha256': sha(target), 'research_only_no_ROM_created': True,"
 }
 for old,new in changes.items():assert source.count(old)==1,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save(ROOT/'successor_probe_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),source_capture_is_historical_controlled_help_globals=True,current_research_code_installed_over_historical_globals=True,native_allocator_intercept_supplies9072bytes=True,not_new_gameplay_or_GPU=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
