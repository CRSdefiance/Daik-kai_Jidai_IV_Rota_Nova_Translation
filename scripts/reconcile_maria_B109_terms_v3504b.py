"""Bind approved Admiral,Ming,country andspeaker forms to current records."""
from dataclasses import asdict
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.surrender_advice_contextual_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B109_terms_v3504b')
SOURCE=Path('work/analysis/maria_B109_source_v3498/all26_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);image,clean=NdsImage.open(packet['current_ROM']),NdsImage.open('work/clean.nds');ledger=read('translations/editorial_review_current_v1.json');family=next(g for g in ledger['completed_editorial_families'] if g['id']=='Maria-Hangzhou-opening38');jp,en=[IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks[33] for im in [clean,image]];refs=[]
    for r in family['records']:
        if '提督' not in r['source_Japanese'] and '明' not in r['source_Japanese']:continue
        s,c=r['source_reference'],r['current_reference'];raw,value=bytes.fromhex(r['source_hex']),bytes.fromhex(r['current_text_hex']);assert jp[s['offset']:s['offset']+s['bytes']]==raw and en[c['offset']:c['offset']+c['bytes']]==value and en[c['offset']+c['bytes']]==0
        if '提督' in r['source_Japanese']:assert 'Admiral' in r['english']
        refs.append(dict(id=r['id'],source_reference=s,source_hex=raw.hex(),source_Japanese=r['source_Japanese'],current_reference=c,current_hex=value.hex(),approved_English=r['english'],context_reference_only_no_fresh_review_credit=True))
    entries=current_entries(image.read_file('/COMMON/MESFILE.DK4'),image.read_file('/__arm9__.bin'));country=entries[689];assert b'Netherlands' in country.text
    country_family=next(g for g in ledger['completed_editorial_families'] if g['id']=='Square-country-briefings');assert any(r['message_id']==689 and r['decision']=='revised-and-integrated' for r in country_family['records'])
    legacy=read('translations/maria_deep_route_v91.json');old=next(r for r in legacy['records'] if 'Zheng He' in r.get('english','') and r.get('id')=='DK4_MES_B109_R0025');source_r25=next(r for r in packet['records'] if r['source_record_index']==25);assert '鄭和' in source_r25['source_Japanese']
    # The historical wording supplies spelling provenance only;the new gloss owns meaning.
    ROOT.mkdir(parents=True);save(ROOT/'current_approved_Admiral_Ming_Netherlands_and_source_culture.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),current_Maria_B33_reference_records=refs,source_title_tei_toku_has_approved_Admiral_form=True,source_explicit_rank_not_invented=True,source_country_Oranda_approved_English='Netherlands',current_COMMON689_entry={**asdict(country),'text':country.text.decode('ascii')},country689_completed_family=country_family['id'],approved_source_five_country_list=['Portugal','Spain','Netherlands','England','France'],source_Ming_Chinese_dynasty_and_maritime_ban_context_preserved=True,Zheng_He_source_Japanese='鄭和',Zheng_He_legacy_spelling_provenance=dict(manuscript='translations/maria_deep_route_v91.json',id=old['id']),legacy_meaning_and_layout_not_automatically_retained=True,source_janku_is_nautical_junk_ship_not_rubbish=True,source_Ian_help_not_strengthened_to_unproven_life_rescue=True,source_Jam_France_and_forced_departure_no_exile_cause_invented=True,source_policy_criticism_not_rewritten_as_new_treason_orlegal_claim=True,fresh_source_glosses='work/analysis/maria_B109_clean_context_v3503/all26_complete_clean_context_and_fresh_glosses.json',fresh_glosses_precede_this_older_proper_name_reference=True,no_old_record_technical_reaudit_or_new_completion_credit=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Approved Admiral/Ming forms rebound to current B33;Netherlands to current completedCOMMON689. Zheng He/junks,five countries andsource help/exile distinctions retained;no new credit.')
