"""Record actual escape failure and superseding native proofs without completion credit."""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import current_entries
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/escape_binding_erratum_v1187')
DOC=Path('docs/escape_direct_v1187_checkpoint.md')


def main():
    assert not ROOT.exists() and not DOC.exists()
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_escape_v1179_1166_compassAttack8')
    report=read(cap/'capture_report.json')
    assert report['frames']==6922 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    rom=NdsImage.open('out/all_routes_combined_v1166_candidate.nds');arm=rom.read_file('/__arm9__.bin')
    entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    pointer=struct.unpack_from('<I',arm,0x54450)[0];holds=[]
    for frame in (6912,6922):
        ram=cap/f'frame_{frame:06d}_arm9_ram.bin';image=cap/f'frame_{frame:06d}_navigation.png'
        raw=ram.read_bytes();text=raw[pointer-0x02000000:pointer-0x02000000+256].split(b'\0')[0]
        assert text==entries[1973].text and b'\n' not in text
        holds.append({'frame':frame,'RAM':str(ram),'RAM_sha256':sha(raw),'image':str(image),'image_sha256':sha(image.read_bytes()),
            'original_formatted_buffer':pointer,'text_hex':text.hex(),'actual_word_Everyone_visibly_split_Ever_yone':True})
    proofs=[Path(p) for p in ('work/analysis/escape_direct_frame_v1182/original_direct_frame_contract.json',
        'work/analysis/escape_direct_runtime_v1184c/native_runtime_verification.json',
        'work/analysis/escape_direct_fonts_v1185/native_direct_escape_fonts.json',
        'work/analysis/escape_direct_source_v1186c/original_direct_pipeline.json')]
    assert len(read(proofs[2])['cases'])==1417 and len(read(proofs[3])['all13_direct_pipeline_cases'])==13
    ROOT.mkdir(parents=True)
    save(ROOT/'actual_failure_and_native_successor.json',{'actual_failed_candidate':'out/all_routes_combined_v1166_candidate.nds',
        'candidate_sha256':report['ROM_sha256'],'actual_message_ID':1973,'failed_actual_holds':holds,
        'incorrect_historical_contract':[0x02053DB8,0x27C,0x0211],
        'proven_original_direct_contract':[0x02053F40,0x274,0x0211],
        'wrong_historical_CPU_frame_cannot_approve_actual_escape_formatting':True,
        'static_duel20_completion_not_affected':True,'all13_escape_entries_remain_incomplete':True,
        'superseding_proofs':{str(p):sha(p.read_bytes()) for p in proofs},
        'corrected_direct_native_fonts_review_sheet_visually_inspected':True,
        'new_ROM_build_and_original_defeat_replay_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    text='''# Direct escape formatting: V1187 erratum and native correction

Original V1166 gameplay after the isolated low-positive-HP, unarmored test
duel selects COMMON1973. Captures6912/6922 show “Everyone” split across the
physical edge as “Ever” / “yone”. The original formatted buffer at0228E5A8
still contains the unwrapped paragraph. These two real holds contradict the
earlier escape-format approval based on a manually assumed queued frame.

The original53F0C ->54058 prologue proves parent02053F40, voice-table field
+274 and high word0211. The previous53DB8/+27C membership was wrong for
this consumer. The successor removes those two erroneous queued memberships
and adds only direct tables02117500/02117620. All33 English paragraphs,
Japanese glosses, substitutions and compiled COMMON bytes remain unchanged.

The172-byte gate and212-byte public bank remain within their original owned
allocations. A failed regression caught the live PC-relative status suffix
constant in the old gate tail. Its exact pointer is retained in the unused
end of the44-byte status-tail allocation; both the load and its literal are
source locked. Incoming branch/absolute/PC-relative accesses are audited.
The failed1184 probe and successors are retained; it was never a ROM release.

Corrected native evidence:122324 exact dispatch/register/stack cases,
3668 modal outputs plus238 wrong-parent and5 boundary controls,140 complete
status-memory contracts,1417 escape-name/full-native-font cases, and13
original direct source-call pipelines with416 unchanged voice selections.
The native-font sheet was visually reviewed for complete words, first/last
letters, margins and bounds. File I/O and portrait UI construction remain
explicit CPU-test boundaries. Actual combined-ROM gameplay is still required.

The20 static duel entries remain complete on their existing independent
evidence. All13 escape entries remain incomplete. Counts stay1216 complete
(904 revised,312 retained),1267 source/prose reviewed,51 reviewed COMMON
entries incomplete. Separate graphics work, all18 plaques, the remaining
shared/routes/raw-source inventory and the older-record re-audit remain open.
The full editorial goal remains active; no canonical promotion is authorized.

Proof: `work/analysis/escape_binding_erratum_v1187/actual_failure_and_native_successor.json`.
'''
    DOC.write_text(text,encoding='utf8')
    for path,title in [('docs/known_issues.md','V1187: original direct escape caller'),('docs/translation_progress.md','V1187: escape formatting evidence correction')]:
        with Path(path).open('a',encoding='utf8') as stream:stream.write('\n\n## '+title+'\n\n'+text.split('\n\n',1)[1])
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1216,904,312,1267)
    assert set((*range(1951,1957),*range(1973,1980)))<=set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    ledger['escape_direct_binding_erratum_v1187']={'proof':str(ROOT/'actual_failure_and_native_successor.json'),
        'documentation':str(DOC),'historical_escape_native_format_approval_superseded':True,
        'corrected_native_format_proofs_pass_actual_combined_ROM_replay_pending':True,
        'new_completed_entries':0,'full_goal_complete':False}
    ledger['duel_prose_v1103']['formatting_status']='static20-complete;escape13-historical-parent-approval-superseded;corrected-direct-native-proofs-pass;combined-original-defeat-replay-pending'
    ledger['latest_checkpoint']='V1187 records actual COMMON1973 word splitting in V1166 and corrects the source-proven direct caller.122324 scope,3668 modal,140 status,1417 font and13 original source-call cases pass; combined V1189 build and actual replay pending. No new completion credit:1216 complete/1267 prose-reviewed;51 reviewed COMMON entries and whole remaining inventory open.'
    save(ledger_path,ledger)
    print('Actual failure and corrected native evidence recorded;13 escape entries remain incomplete.',flush=True)


if __name__=='__main__':main()
