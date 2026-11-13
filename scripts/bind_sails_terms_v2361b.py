"""Current native role labels and exact HELP83 Half Open terminology binding."""
from pathlib import Path
import struct
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.crew_role_labels import ORIGINAL
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/sails_terms_v2361b')
if __name__=='__main__':
 assert not ROOT.exists();rompath=Path('out/all_routes_combined_v2284_candidate.nds');rom=NdsImage.open(rompath);arm=rom.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');oldpath=Path('work/analysis/sails_boarding_v879/terminology_proof.json');old=read(oldpath);helpbytes=rom.read_file('/COMMON/HELP.DK4');topic=IlnkContainer.from_bytes(helpbytes).blocks[83];assert topic.hex()==old['current_HELP83_hex']and b'Half Open'in topic and b'Full Open'in topic
 context=read('work/analysis/sails_boarding_context_v2361/native_context.json');receipt=context['current_NPC_source_snapshot'];raw=Path(receipt['path']).read_bytes();assert sha(raw)==receipt['sha256'];cpu,get=get_machine(arm,raw);labels=get(0x86314);roles=[]
 for index,japanese,english in((5,'操帆手','Sail Handler'),(8,'斬込隊長','Boarding Leader')):
  ptr=struct.unpack('<I',cpu.mem_read(labels+index*4,4))[0];text=bytes(cpu.mem_read(ptr,64)).split(b'\0',1)[0].decode('cp932').strip();originalptr=struct.unpack_from('<I',clean,ORIGINAL-0x02000000+index*4)[0];source=clean[originalptr-0x02000000:].split(b'\0',1)[0].decode('cp932');assert text==english and source==japanese;roles.append(dict(native_index=index,source_Japanese=source,current_native_English=text))
 files=[Path(old['reviewed_sail_artwork']),Path(old['source_context_document'])];assert sha(files[0].read_bytes())==old['reviewed_sail_artwork_sha256']and sha(files[1].read_bytes())==old['source_context_document_sha256']
 ROOT.mkdir(parents=True);save(ROOT/'current_terms.json',dict(candidate=str(rompath),candidate_sha256=sha(rompath.read_bytes()),ARM9_sha256=sha(arm),native_roles=roles,current_snapshot=receipt,current_HELP83_complete_payload_exact_to_prior_proof=True,current_HELP83_hex=topic.hex(),current_HELP_sha256=sha(helpbytes),Half_Open_and_Full_Open_terms_source_bound=True,source_fore_and_aft_vs_square_scope_inherited_from_verified_terminology_artwork=True,fore_and_aft_not_restricted_to_lateen=True,prior_terms_proof=str(oldpath),prior_terms_proof_sha256=sha(oldpath.read_bytes()),preserved_reference_files={str(p):sha(p.read_bytes())for p in files},graphics_audit_is_separate_and_not_completed=True,no_new_HELP_graphics_or_role_label_credit=True,no_ROM_or_sail_performance_or_assignment_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(current_roles=2,HELP83_exact=True,Half_Open_source_bound=True,graphics_scope_separate=True))
