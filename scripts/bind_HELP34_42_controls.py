"""Bind Inn cancel intent andSquare Trends label using exact captured code/source data,not another full replay."""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_T21_T43_clean_20261104')
if __name__=='__main__':
    proof_path=ROOT/'Inn34_Square42_control_bindings_v1.json';assert not proof_path.exists()
    old=ROOT/'whole_article_comparisons_v2.json';doc=load(old)
    current=NdsImage.open(doc['current_ROM']);arm=current.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    inn_path=Path('work/analysis/inn_history_v804/departure_gameplay_verification.json');inn=load(inn_path)
    report_path=Path(inn['report']);report=load(report_path);assert sha(report_path.read_bytes())==inn['report_sha256']
    assert inn['B_interrupt_at_original_night_boundary_verified'] and inn['A_yes_leaves_early']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    snapshot=next(r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots'] if r['frame']==6600)
    raw=Path(snapshot['path']).read_bytes();assert len(raw)==4194304 and sha(raw)==snapshot['sha256'] and snapshot['read_only_export']
    assert dict(start=6701,duration=80,buttons=['B']) in report['scripted_input_schedule']
    windows=[]
    # Source-owned Inn flow,dialogue parent callbacks andinput helper spans fromcontext_inn_v801/probe_inn_layout_v802.
    for lo,hi,role in [(0x5C450,0x5D4EC,'Inn flow'),(0x53DB8,0x54058,'Inn dialogue parent callbacks'),(0xB2CD8,0xB2D58,'input helper'),(0x7E988,0x7E9A0,'voice helper')]:
        assert arm[lo:hi]==raw[lo:hi],hex(lo)
        windows.append(dict(ARM9_offset=lo,bytes=hi-lo,RAM_address=0x02000000+lo,sha256=sha(arm[lo:hi]),role=role,captured_bytes_exact=True))
    square_report_path=Path('work/emulation_v193/square_cells_v484/capture_report.json');square=load(square_report_path)
    frame=next(r for r in square['frames_captured'] if r['frame']==3900);assert sha(Path(frame['path']).read_bytes())==frame['PNG_sha256']
    at=0x143E98;pointer=0x143F78
    source=clean[at:].split(b'\0',1)[0];target=arm[at:].split(b'\0',1)[0]
    assert source.decode('cp932')=='流行情報' and target==b'Trends'
    assert struct.unpack_from('<I',arm,pointer)[0]==struct.unpack_from('<I',clean,pointer)[0]==0x02143E98
    save(proof_path,dict(current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],current_ARM9_sha256=sha(arm),
        Inn=dict(clean_source_cross_is_not_assumed_to_mean_physical_X=True,
            localized_equivalent='To interrupt a stay of several nights, press B.',
            historical_actual_proof=str(inn_path),historical_actual_proof_sha256=sha(inn_path.read_bytes()),
            report=str(report_path),report_sha256=sha(report_path.read_bytes()),captured_snapshot=snapshot,exact_current_control_code_windows=windows,
            original30_night_request_interrupted_after_two_nights=True,physical_X_not_tested_andnot_claimed_broken=True,
            historical_ROM_file_missing_but_original_hashed_captured_RAM_available=True,
            source_cross_action_intent_preserved_via_verified_B_interrupt=True,
            no_current_gameplay_font_orwhole_ARM9_identity_claim=True),
        Square=dict(clean_label=source.decode('cp932'),clean_label_hex=source.hex(),current_label='Trends',current_label_hex=target.hex(),
            ARM9_offset=at,pointer_offset=pointer,pointer_value=0x02143E98,exact_source_current_pointer_bound=True,
            historical_capture=frame,historical_capture_report=str(square_report_path),historical_capture_report_sha256=sha(square_report_path.read_bytes()),
            capture_directly_viewed=True,scope='Observed historical Square shop-sign UI says Trends. Current exact native label andsource pointer bind the wording;this isnot a new current-widget pixel proof.'),
        actual_new_gameplay=False,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [old,inn_path,report_path,square_report_path,Path('scripts/context_inn_v801.py'),Path('scripts/probe_inn_layout_v802.py'),Path('scripts/verify_inn_departure_v804.py')]}))
    for row in doc['records']:
        if row['topic_id']==34:
            row['english']="Stay at the inn for 1 gold coin per night. Each night reduces your sailors' [[157|Fatigue]] by about 10 and restores your officers' condition and HP. [!] A [[118|Strategist]] may gather information about other factions while you stay. [!] To interrupt a stay of several nights, press B."
            row['finding']+=' Binding resolved:the historical actual B interrupt andoriginal hashed captured code windows match the current Inn logic. Localize the source cross/cancel intent withthe verified B action. Do not claim physicalX fails. Officers preserves the current group term distinct fromordinary sailors,without limiting recovery toNavigation duty.'
        elif row['topic_id']==42:
            row['english']="Gather information in the square, where retail shops display their signs. Under 'Trends', select a shop's sign to learn about goods that are [[25|in fashion]]. See [[43|Distribute Goods]]."
            row['finding']+=' Binding resolved:clean native流行情報 andcurrentTrends share ARM9 field143E98 andpointer143F78. The observed historical Square sign UI confirms the label/function. Do not invent an extra select-Trends-then-enter-a-new-menu step.'
        else:continue
        row['review']['localization']=True;row['native_term_orcontrol_binding_pending']=False
        row['control_binding']=str(proof_path);row['control_binding_sha256']=sha(proof_path.read_bytes())
    doc['first_four_gates_passed']=23;doc['pending_localization_binding_topic_IDs']=[]
    doc['previous_comparison']=str(old);doc['previous_comparison_sha256']=sha(old.read_bytes());doc['control_binding']=str(proof_path)
    doc['control_binding_sha256']=sha(proof_path.read_bytes());doc['evidence'][str(proof_path)]=sha(proof_path.read_bytes())
    doc['evidence'][str(Path(__file__))]=sha(Path(__file__).read_bytes())
    save(ROOT/'whole_article_comparisons_v3.json',doc)
    print('Inn B intent andSquare Trends label bound without new gameplay:all23 four-gate comparisons now pass;18 revisions/5 retentions. Fresh display/allocation checks remain.')
