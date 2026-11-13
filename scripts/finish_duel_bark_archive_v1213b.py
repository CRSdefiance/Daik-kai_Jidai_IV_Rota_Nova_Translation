"""Finish the archive after1213's external-copy CAP-name error; never recount."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V1213 Timed duel reaction completion')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_bark_v1207_1206')
ROOT=Path('work/analysis/duel_bark_completion_v1213')


def main():
    assert ARCHIVE.is_dir() and not (ARCHIVE/'archive_manifest.json').exists()
    ledger_path=Path('translations/editorial_review_current_v1.json');before=ledger_path.read_bytes();ledger=read(ledger_path)
    assert [ledger[k] for k in ('records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','records_with_source_and_prose_pass')]==[1245,925,320,1283]
    final=read('translations/duel_bark_editorial_final_review_v1.json');assert len(final['records'])==16
    assert sum(1957<=n<=1972 for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[]))==16
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==38
    rows=[]
    for dest in sorted(ARCHIVE.rglob('*')):
        if not dest.is_file():continue
        relative=dest.relative_to(ARCHIVE);source=Path.cwd()/relative
        assert source.is_file() and source.read_bytes()==dest.read_bytes(),str(relative)
        rows.append({'source':str(source),'path':str(dest),'sha256':sha(dest.read_bytes())})
    actual=read('work/analysis/duel_bark_terminal_v1211/terminal_gameplay_verification.json')
    external=[Path(r[k]) for r in actual['actual_new_reaction_holds'] for k in ('RAM','capture')]
    external += [CAP/f"frame_{r['frame']:06d}_arm9_ram.bin" for r in actual['actual_preserved_escape_holds']]
    external += [Path(r['capture']) for r in actual['actual_preserved_escape_holds']]
    external += [Path(actual['terminal_report']),CAP/'navigation_command_journal.json']
    for source in dict.fromkeys(external):
        relative=source.absolute().relative_to(Path('E:/Rota Nova translations').absolute());dest=ARCHIVE/'external_E'/relative
        assert not dest.exists();dest.parent.mkdir(parents=True,exist_ok=True);copy2(source,dest)
        assert dest.read_bytes()==source.read_bytes();rows.append({'source':str(source),'path':str(dest),'sha256':sha(dest.read_bytes())})
    receipt=ROOT/'archive_completion_recovery.json';assert not receipt.exists()
    save(receipt,{'completion_script':'scripts/complete_duel_bark_review_v1213.py',
        'terminal_archive_only_error':'NameError: CAP not defined while preparing external reference list; ledger/final-review/docs/pin/checkpoint had already completed.',
        'verified_completed_counts':[1245,925,320,1283],'new_credit_in_recovery':0,'ledger_unchanged':True,
        'all_preexisting_archived_files_exact_before_recovery':True,'external_sources_copied_with_explicit_physical_E_root':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    for source in (Path(__file__),receipt):
        dest=ARCHIVE/source.absolute().relative_to(Path.cwd());assert not dest.exists()
        dest.parent.mkdir(parents=True,exist_ok=True);copy2(source,dest)
        rows.append({'source':str(source),'path':str(dest),'sha256':sha(dest.read_bytes())})
    assert ledger_path.read_bytes()==before
    save(ARCHIVE/'archive_manifest.json',{'files':rows,
        'candidate_physical_E_path':'E:/Rota Nova translations/Generated/out/all_routes_combined_v1206_candidate.nds',
        'candidate_sha256':final['candidate_sha256'],'all_copied_sources_proofs_and_selected_actual_RAM_images_byte_exact':True,
        'new_completed_entries':16,'external_archive_completion_recovery':str(receipt),'full_goal_complete':False})
    print('V1213 archive complete:',len(rows),'exact files;counts1245/1283 unchanged;no duplicate credit.',flush=True)


if __name__=='__main__':main()
