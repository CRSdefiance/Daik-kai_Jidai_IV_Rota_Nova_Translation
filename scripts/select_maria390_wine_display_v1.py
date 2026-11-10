"""Select the corrected challenge with its exact two surrounding source utterances."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B152_B175_clean_20261109')


def main():
    out=ROOT/'wine_display_selection_v1.json';assert not out.exists()
    reconstruction=ROOT/'reconstruction_v3/reconstruction.json';storedpath=ROOT/'stored_v3/stored_native_verification.json'
    rebuilt,stored=map(load,[reconstruction,storedpath]);native=load(rebuilt['native'])
    assert stored['reconstruction_sha256']==digest(reconstruction) and stored['complete_stored_pages']==373
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    ids=[f'DK4_MES_B152_R{i:04d}' for i in [5,8,12]]
    assert all(i in {r['id'] for r in native['records']} for i in ids)
    fixture=dict(name='Maria390_wine_reply_context',sequence=[dict(speech=i) for i in ids],
        selection_source_utterances=3,selection_expected_pages=3,frames=10721,extra_inputs=[],capture_extra=[],
        purpose='Verify the corrected complete question/answer context in three source utterances: Hey, you are still drinking that stuff? / Got a problem with that? / Not at all. Reuse82 unchanged actual source-body proofs only after exact command/font/runtime dependencies match. Preserve the qualified full Maria host and16-frame A inputs. No original tavern activation orstory outcomes are simulated.')
    save(out,dict(fixtures=[fixture],selected_speech_ids=ids,selected_source_bodies=3,
        original_meanings_andindependent_draft_preserved=True,one_retention_reopened_not_new_source_credit=True,
        natural_activation=False,earned_chronology=False,actual_gameplay_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in [reconstruction,storedpath,ROOT/'wine_reply_contextual_amendment_v1.json',Path(__file__)]}))
    print('Selected3 source utterances around the corrected wine reply;one focused10721-frame host test.')


if __name__=='__main__':main()
