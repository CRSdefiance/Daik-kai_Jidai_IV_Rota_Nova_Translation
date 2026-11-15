"""Join complete clean-first speech/menu/style drafts,retaining every source field andunpassed gate."""
import argparse
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ['packet','choices','styles','out']:
        parser.add_argument('--'+key,type=Path,required=True)
    parser.add_argument('--drafts',type=Path,nargs='+',required=True)
    args = parser.parse_args(); assert not args.out.exists()
    packet, choices, styles = map(load,[args.packet,args.choices,args.styles])
    assert choices['source_packet_sha256'] == styles['source_packet_sha256'] == sha(args.packet.read_bytes())
    ordinary = [r for g in packet['groups'] for r in g['records']]
    source = ordinary+styles['records']+choices['records']
    expected = {r['id']:r for r in source}; assert len(expected) == len(source)
    byid = {}
    for path in args.drafts:
        partial = load(path)
        assert partial['clean_packet_sha256'] == sha(args.packet.read_bytes())
        assert partial['independent_drafts_precede_current_English_extraction_in_this_intake']
        assert partial['no_blanket_historical_unexposure_orfinal_approval_claim']
        for row in partial['records']:
            key = row['id']; assert key not in byid and key in expected
            assert all(row[k] == v for k,v in expected[key].items()), key
            assert row['current_English_comparison_pending'] and row['earlier_English_unconsulted']
            assert row['no_blanket_historical_English_exposure_claim'] and not any(row['review'].values())
            assert row['source_meaning'].strip() and row['source_exchange_context'].strip()
            draft = row['independent_English_draft']
            assert draft.isascii() and draft == draft.strip() and not any(s in draft for s in ['\n','\r','\t','{LB','{ALIGN','{PAD}'])
            for macro,count in row.get('source_macros',{}).items():
                assert draft.count(macro) == count, (key,macro,count)
            value = deepcopy(row)
            value.update(english=draft,context=row['source_exchange_context'],current_ROM_English_unconsulted=True)
            if value.get('kind') == 'actor-style-alternative':
                value.update(kind='progressive',native_object_kind='4100-style-alternative')
            elif 'kind' not in value:
                value['kind'] = 'system-FE' if value['source_selector'] == 254 else 'progressive'
            byid[key] = value
    assert set(byid) == set(expected)
    records = [byid[r['id']] for r in source]
    args.out.mkdir(parents=True)
    sealed = args.out/'all_source_meanings_andindependent_drafts.json'
    save(sealed,dict(format='dk4-complete-source-first-whole-exchange-drafts-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        file_path=packet['file_path'],clean_source_packet=str(args.packet),clean_source_packet_sha256=sha(args.packet.read_bytes()),
        clean_choice_objects=str(args.choices),clean_choice_objects_sha256=sha(args.choices.read_bytes()),
        clean_style_objects=str(args.styles),clean_style_objects_sha256=sha(args.styles.read_bytes()),
        records=records,source_objects=len(records),ordinary_speech_drafts=len(ordinary),physical_style_drafts=len(styles['records']),
        source_caption_drafts=len(choices['records']),remaining_source_speech_style_orcaption_drafts=0,
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        current_SC0_English_not_consulted_in_this_intake=True,no_blanket_prior_English_exposure_claim=True,
        all_current_comparisons_andname_term_control_display_gates_pending=True,no_review_gate_automatically_approved=True,
        new_credit=0,guide_photos=False,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [args.packet,args.choices,args.styles,*args.drafts,Path(__file__)]}))
    save(args.out/'meanings_view.json',dict(records=[byid[r['id']] for r in ordinary],meanings=len(ordinary),
        source_packet=str(args.packet),source_packet_sha256=sha(args.packet.read_bytes()),
        all_drafts_sealed=str(sealed),all_drafts_sha256=sha(sealed.read_bytes()),
        no_blanket_prior_English_exposure_claim=True,no_source_orEnglish_wording_changed=True,new_credit=0))
    print(dict(ordinary=len(ordinary),styles=len(styles['records']),captions=len(choices['records']),sealed_total=len(records),remaining_drafts=0,new_credit=0))


if __name__ == '__main__':
    main()
