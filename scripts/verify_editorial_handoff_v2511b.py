"""Preserve incomplete audit;make next-packet path explicit across scoped namespaces."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_editorial_handoff_v2511.py')
if __name__=='__main__':
 source=OLD.read_text();a='next_corrected_direct_escape_packet=str(PACKET),next_packet_sha256=sha(PACKET.read_bytes()),';b="next_corrected_direct_escape_packet='work/analysis/escape_source_handoff_v2510/next13_direct_escape_source_packet.json',next_packet_sha256=sha(Path('work/analysis/escape_source_handoff_v2510/next13_direct_escape_source_packet.json').read_bytes()),";assert source.count(a)==1;source=source.replace(a,b).replace('editorial_handoff_verification_v2511','editorial_handoff_verification_v2511b').replace('V2511-audit-of-V2510','V2511b-audit-of-V2510')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/editorial_handoff_verification_v2511b/successor_binding.json',dict(failed_audit=str(OLD),failed_audit_sha256=sha(OLD.read_bytes()),failed_audit_stopped_before_saving_verification_or_changing_ledger=True,missing_scoped_name_replaced_with_exact_packet_path=True,effective_source_sha256=sha(source.encode()),full_goal_complete=False))
