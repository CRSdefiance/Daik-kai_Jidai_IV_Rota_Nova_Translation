"""Seal individual source meanings without granting localization ordisplay approval."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

def seal(packet_path,output,meanings,contexts,producer):
    packet_path,output,producer=map(Path,[packet_path,output,producer])
    assert not output.exists() and set(meanings)==set(contexts)
    packet=load(packet_path);rows=[];counts={}
    assert packet['clean_only_no_prior_English_ornew_editorial_credit']
    for group in packet['groups']:
        number=group['block']
        if number not in meanings:continue
        parsed=[line.split('|',1) for line in meanings[number].strip().splitlines()]
        by_index={int(k):v for k,v in parsed}
        assert len(by_index)==len(parsed)==len(group['records'])
        assert set(by_index)=={r['source_reference']['record_index'] for r in group['records']}
        for original in group['records']:
            assert original['source_decode_error'] is None and original['earlier_English_unconsulted']
            row=deepcopy(original)
            row.update(source_meaning=by_index[row['source_reference']['record_index']],whole_exchange_context=contexts[number],
                source_read_with_all_previous_andfollowing_speeches_in_block=True,
                clean_name_event_membership_current_comparison_drafts_andall_five_gates_pending=True)
            rows.append(row)
        counts[number]=len(group['records'])
    assert set(counts)==set(meanings) and len({r['id'] for r in rows})==len(rows)
    save(output,dict(source_packet=str(packet_path),source_packet_sha256=sha(packet_path.read_bytes()),records=rows,
        complete_exchanges=list(counts),counts_by_block=counts,
        all_source_meanings_read_as_complete_exchanges_before_existing_English=True,
        all_five_editorial_gates_still_pending=True,source_gloss_not_final_English=True,
        new_credit=0,guide_photos=False,producer_sha256=sha(producer.read_bytes()),helper_sha256=sha(Path(__file__).read_bytes())))
    print(f'{len(rows)} source-only meanings/{len(counts)} complete exchanges sealed;older English unconsulted,no completion credit.',flush=True)
