"""Read complete B53 Japanese before earlier English; qualify apparent wanted status."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B53_clean_gloss_v8712')
SOURCE=Path('work/analysis/Hodram_B53_clean_v8711/complete_clean_SC1_B53_EV1_andcoverage_before_current_English.json')

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);assert not packet['inventory_failures'] and packet['source_only_no_current_English_exposed_orused']
    group=deepcopy(packet['groups'][0]);assert group['block']==53 and len(group['commands'])==9 and len(group['records'])==1 and group['uncredited_source_positions']==1
    row=group['records'][0]
    assert row['id']=='DK4_MES_B53_R0007' and row['source_selector']==113 and row['source_decode_error'] is None
    assert row['source_Japanese']=='あんた、とうとうオスマン帝国から\n手配されちまったようだぜ\nせいぜい気をつけなよ'
    assert [(e['event_ID'],e['script_block'],e['must_be_completed'],e['must_not_be_completed']) for e in group['source_event_records']]==[(53,53,[31],[74])]
    assert not any(c['word'] in [0x2100,0x100,0x200,0x300,0x400,0x8000,0x8100] for c in group['commands'])
    row.update(first_clean_source_gloss='The colloquial speaker says it appears the addressee has finally ended up wanted or being sought by the Ottoman Empire, then advises the addressee to be especially careful.',
        source_context_note='Read all three Japanese lines as one warning, not three disconnected statements. あんた/だぜ/気をつけなよ give an informal, gruff conversational voice. とうとう signals the culmination of an undesirable development, while されちまった conveys that it has happened to the addressee. ようだ retains apparent or reported status rather than omniscient certainty. 手配 here means being sought/wanted, not arranging a purchase or travel. せいぜい気をつけなよ is practical caution. Do not invent an alleged crime, court process, warrant, monetary bounty, named pursuer, precise danger, rank, nationality of the addressee, location or guaranteed outcome. Bind the approved Ottoman Empire term and actor113 role separately before final localization.',
        whole_clean_exchange_read_before_current_English=True,
        current_English_dialogue_still_unconsulted=True,
        source_meaning_only_not_editorial_orformatting_approval=True,
        no_completion_or_source_prose_counter_credit_added=True)
    context='B53 contains one complete three-line spoken warning and no source menu or explicit relative/query sites. Source selector71 and its complete preamble are retained, but native dispatch, role/voice consumers, opaque command effects and end handling still require source-qualified review. Event53 requires31 and excludes74; outer eligibility, scheduling, original location and natural activation remain unexecuted. This is not established as a continuation of B52: its required event differs and numeric adjacency does not prove chronology. Do not import Hayreddin, opposition choices, a battle result or any other detail from B52 into this utterance.'
    ROOT.mkdir(parents=True)
    save(ROOT/'one_first_clean_gloss_apparent_Ottoman_wanted_status_before_current_English.json',dict(
        source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),source_ROM=packet['source_ROM'],source_ROM_sha256=packet['source_ROM_sha256'],
        groups=[group],whole_exchange_context=context,
        all_clean_speech_read_before_earlier_English=True,current_English_body_still_unconsulted=True,
        apparent_status_culmination_gruff_warning_andpractical_caution_preserved=True,
        no_bounty_crime_rank_relationship_orlocation_invented=True,
        source_controls_native_dispatch_names_glossary_formatting_actual_andintegration_pending=True,
        B52_registered_build_patch_startup_andcredit_remain_separate=True,
        no_new_ROM_emulator_run_orcounter_credit=True,new_credit=0,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('B53 clean-first:one complete warning glossed;apparent wanted status/undesirable culmination/gruff caution preserved. No crime/bounty/rank/chronology invented. Earlier English unread;zero credit.')
