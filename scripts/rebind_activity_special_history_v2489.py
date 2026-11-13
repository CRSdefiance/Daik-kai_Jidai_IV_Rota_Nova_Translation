"""Bind nine preserved V987 scenes to current17 exact payloads and distinct displays."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_activity_special_gameplay_v989.py')
if __name__=='__main__':
 source=OLD.read_text();changes={
 'from dk4tool.patch import activity_special_editorial_v987b as owned':'from dk4tool.patch import refit_contextual_spritsail_v1 as owned\nfrom dk4tool.patch.activity_special_editorial_v987b import current_entries as old_entries\nfrom scripts.mood_comments_flags_v982 import format_instruction',
 "ROOT=Path('work/analysis/activity_special_v988')":"ROOT=Path('work/analysis/activity_special_history_v2489')\nOLDROOT=Path('work/analysis/activity_special_v988')",
 "ROM=Path('out/all_routes_combined_v987_candidate.nds')":"ROM=Path('out/all_routes_combined_v2284_candidate.nds')",
 "read('translations/activity_special_editorial_manuscript_v2.json')":"read('translations/activity_special_contextual_editorial_manuscript_v1.json')",
 "entries=owned.current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)":"entries=owned.current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)\n    historical_path=OLDROOT/'actual_gameplay_verification.json';historical=read(historical_path);oldpath=Path(historical['candidate']);old_digest=sha(oldpath.read_bytes());assert old_digest==historical['candidate_sha256'];oldrom=NdsImage.open(oldpath);oldarm=oldrom.read_file('/__arm9__.bin');spans=((0x11000,0x20000),(0x3F0F8,0x3F100),(0x53914,0x55300),(0x7E000,0x7FA00),(0x81F54,0x82E0C));assert all(arm[a:b]==oldarm[a:b]for a,b in spans);assert format_instruction(arm)==format_instruction(oldarm)==format_instruction(NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))==bytes.fromhex('0000d6e5');assert rom.read_file('/GRP/KANJI.FNT')==oldrom.read_file('/GRP/KANJI.FNT');prior=old_entries(oldrom.read_file('/COMMON/MESFILE.DK4'),oldarm);assert all(entries[n].text==prior[n].text==compiled(r)for n,r in rows.items());assert not ROOT.exists();ROOT.mkdir(parents=True)",
 'load(folder,digest,terminal)':'load(folder,old_digest,terminal)',
 'assign(arm,data[frame],request)':'assign(oldarm,data[frame],request)',
 "assign(arm,data[16100],{'case':label,'late_case_only':True})":"assign(oldarm,data[16100],{'case':label,'late_case_only':True})",
 "save(ROOT/'actual_gameplay_verification.json',{'candidate'":"save(ROOT/'historical_activity_special_current_binding.json',{'ARM9_sha256':sha(arm),'COMMON_sha256':sha(rom.read_file('/COMMON/MESFILE.DK4')),'historical_proof':str(historical_path),'historical_proof_sha256':sha(historical_path.read_bytes()),'executed_code_spans_current_old_exact':[dict(start=a,end=b,sha256=sha(arm[a:b]))for a,b in spans],'all17_current_compiled_and_historical_payloads_equal':True,'historical_holds':holds,'historical_IDs':sorted({h['message_id']for h in holds}),'scoped_historical_battle_returns_freshly_rechecked':returns,'thirty_six_negative_controls_current_reexecution_on_offline_clones':controls,'no_new_current_battle_emulator_runs_or_family_visits':True,'historical_fixture_replay_uses_original_source_bound_V987_ARM9_no_hash_guard_bypass':True,'current_native_fonts_and_original_code_are_checked_separately':True,'review_sheets':[dict(path=str(path),sha256=sha(path.read_bytes())),dict(path=str(back_path),sha256=sha(back_path.read_bytes()))],'candidate'",
 '18 complete native/actual RGB holds,nine returns and36 offline corruption controls pass;visual review pending.':'18 historical V987 holds freshly bind to current payloads;9 returns and36 negative controls pass. Zero new emulator runs;visual review pending.',
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/activity_special_history_v2489/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),frozen_verifier_fixtures_and_donors_unchanged=True,full_goal_complete=False))
