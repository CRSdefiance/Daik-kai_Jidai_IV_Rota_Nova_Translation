"""Recover one already-credited source position from its exact preserved Japanese/native proof."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

OUT=Path('work/Lil_B294_source_binding_20261109_v1/qualification.json')
IDENT='DK4_MES_B294_R0073'
FAMILY='Lil-SC2-B294-R73-previously-omitted-native-message'

def qualified_location(row):
    proof=load(OUT);raw=proof['source_hex']
    assert row['id']==IDENT and row['file_path']=='/data/SC2.DK4'
    assert row['raw_source']['hex']==raw and row['source_japanese']==proof['source_Japanese']
    assert row['source_control_evidence']==proof['source_control_evidence']
    assert digest(proof['source_control_evidence'])==proof['source_control_evidence_sha256']
    assert all(row['review'].values())
    return 294,proof['source_reference']['offset'],raw

def main():
    assert not OUT.parent.exists()
    ledger_path=Path('translations/editorial_review_current_v1.json');before=ledger_path.read_bytes();ledger=load(ledger_path)
    family=next(f for f in ledger['completed_editorial_families'] if f['id']==FAMILY)
    assert not family['whole_B293_B294_editorial_complete']
    row=next(r for r in family['records'] if r['id']==IDENT)
    source_proof=Path(row['source_control_evidence']);old=load(source_proof);raw=bytes.fromhex(row['raw_source']['hex'])
    assert old['source_record_hex']==raw.hex() and old['source_record_bytes']==len(raw)==48
    assert old['source_control_prefix_hex']==row['raw_source']['presentation_prefix_hex']=='94'
    assert old['whole_actual_SC2_B294_resident_copy_exact'] and old['original_body_reaches_live_wrapped_buffer_after_exact_one_byte_prefix']
    census_path=Path('work/story_source_coverage_20261109_SC2_v1/coverage.json');census=load(census_path)
    native=next(r for r in census['records'] if r['id']==IDENT and r['block']==294)
    assert native['source_hex']==raw.hex() and native['source_Japanese']==row['source_japanese']==raw[1:].decode('cp932')
    clean_path=Path('work/clean.nds');clean=NdsImage.open(clean_path);archive=clean.read_file('/data/SC2.DK4');block=IlnkContainer.parse(archive).blocks[294]
    at=native['source_reference']['offset'];assert at==641 and block[:at].count(b'\0')==73
    assert block[at-5:at+1].hex()=='0040ffff0094' and block[at:at+49]==raw+b'\0'
    assert block.find(raw+b'\0')==at and block.find(raw+b'\0',at+1)<0
    assert all(row['review'].values()) and ledger['records_editorially_completed']==19161
    OUT.parent.mkdir();save(OUT,dict(id=IDENT,file_path='/data/SC2.DK4',family=FAMILY,
        source_reference=native['source_reference'],source_hex=raw.hex(),source_Japanese=native['source_Japanese'],
        source_control_evidence=str(source_proof),source_control_evidence_sha256=digest(source_proof),
        source_ROM=str(clean_path),source_ROM_sha256=digest(clean_path),source_archive_sha256=census['source_archive_sha256'],
        original_census=str(census_path),original_census_sha256=digest(census_path),
        exact_clean_native_command_position_index_prefix_andoriginal_source_record_match=True,
        only_missing_metadata_bound_no_new_editorial_or_native_display_approval=True,
        whole_B293_B294_editorial_complete=False,ledger_unchanged=True,new_credit=0,producer_sha256=digest(__file__)))
    assert ledger_path.read_bytes()==before
    print('Bound already-credited Lil B294R73 to clean offset641/index73 andoriginal94 source proof;zero new credit,no whole-exchange completion claim.')

if __name__=='__main__':main()
