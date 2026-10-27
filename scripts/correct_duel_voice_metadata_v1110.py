"""Include original minus-one voice fallbacks and complete macro-path provenance."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

SOURCE=Path('translations/duel_editorial_manuscript_v1.json')
TARGET=Path('translations/duel_editorial_manuscript_v2.json')
ROOT=Path('work/analysis/duel_metadata_v1110')


def main():
    assert not TARGET.exists() and not ROOT.exists()
    doc=read(SOURCE);context=read(doc['native_context_proof']);supplement=read(doc['source_context_supplement'])
    by_table={r['address']:r['voice_IDs'] for r in context['tables']}
    by_table[supplement['original_alternate_table']]=supplement['voice_IDs']
    changes=[]
    for row in doc['records']:
        ids=by_table[row['source_table']];fallback=next(n for n in ids if n!=-1)
        voices=[i for i,n in enumerate(ids) if (fallback if n==-1 else n)==row['message_id']]
        old=row['source_voice_classes_including_native_fallback']
        if voices!=old:changes.append({'message_ID':row['message_id'],'old_voice_classes':old,'correct_voice_classes':voices})
        row['source_voice_classes_including_native_fallback']=voices
        row['source_null_actor_fallback_selects_this_message']=row['message_id']==fallback
        assert not row['review']['formatting']
    assert [r['message_ID'] for r in changes]==[1939,1945,1951,1973]
    macro=Path('work/analysis/duel_consumer_v1107/duel_text_consumer_source_path.json')
    doc.update(supersedes_manuscript=str(SOURCE),supersedes_manuscript_sha256=sha(SOURCE.read_bytes()),
        native_consumer_path_proof=str(macro),native_consumer_path_proof_sha256=sha(macro.read_bytes()),
        source_metadata_correction='Voice classes now include the original -1 table fallbacks;DuelDA28 calls53914 beforeD5404. Prose unchanged;native geometry remains pending.')
    assert [(r['message_id'],r['english'],r['source_meaning']) for r in doc['records']]==[(r['message_id'],r['english'],r['source_meaning']) for r in read(SOURCE)['records']]
    ROOT.mkdir(parents=True);save(TARGET,doc)
    proof=ROOT/'voice_fallback_metadata_correction.json'
    save(proof,{'previous_manuscript':str(SOURCE),'previous_manuscript_sha256':sha(SOURCE.read_bytes()),
        'current_manuscript':str(TARGET),'current_manuscript_sha256':sha(TARGET.read_bytes()),'corrected_metadata':changes,
        'all33_English_source_meanings_and_review_decisions_exact':True,'all1040_original_voice_selections_and4_null_controls_already_source_bound':True,
        'native_geometry_fonts_release_and_actual_still_pending':True,'no_new_source_prose_or_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1267
    paths=ledger['active_source_prose_drafts']['manuscripts'];assert paths.count(str(SOURCE))==1
    paths[paths.index(str(SOURCE))]=str(TARGET)
    ledger['duel_prose_v1103'].update(manuscript=str(TARGET),voice_fallback_metadata_correction=str(proof),
        native_consumer_path_supplement=str(macro))
    save(ledger_path,ledger)
    print('Four voice-family fallbacks corrected;33 English/source glosses unchanged. Complete duel macro path bound;formatting gates remain pending.')


if __name__=='__main__':main()
