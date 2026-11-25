"""Bind exact scoped geography/stat terms and reconcile the registered Sao Jorge name."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.arm9_profiles import WORLD_CITY_ENTRIES
from scripts.audit_story_glyph_consistency import load,save
from scripts.bind_hodram_B191_B210_identities import cstring
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_hodram_B251_B280_contextual_v1 import ROOT,CURRENT,OUT as PRIOR_PROSE

TERMS=ROOT/'scoped_terms_v1.json'
PROSE=Path('translations/hodram_B251_B280_contextual_review_v2.json')
CITY=Path('work/analysis/maria_B97_terms_v5006/bound_Maria_Xien_Bandit_Li_Clan_Sao_Jorge_Proof_and_tablet_context.json')

def main():
    assert not TERMS.exists() and not PROSE.exists()
    current,prose,prior=map(load,(CURRENT,PRIOR_PROSE,CITY));runtime=current['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=1);assert ctx.receipt()==runtime
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');source=prior['source_current_city_item_and_HELP_versions'][0]['city']
    prior_city=prior['source_current_city_item_and_HELP_versions'][1]['city'];at=source['pointer_field']
    assert prior['approved_city']=='Sao Jorge' and source['pointer']==prior_city['pointer']
    assert struct.unpack_from('<I',clean,at)[0]==struct.unpack_from('<I',ctx.arm,at)[0]==source['pointer']
    where=source['pointer']-0x02000000
    raw=clean[where:clean.index(0,where)];assert raw.decode('cp932')==source['text']=='サン＝ジョルジェ'
    city=cstring(ctx.raw,source['pointer']);assert city==b'Sao Jorge'
    aliases=[];cities={'London','Stockholm','Hangzhou','Basra','Calicut','Athens','Syracuse'}
    for entry in WORLD_CITY_ENTRIES:
        if entry.suggested_english not in cities:continue
        assert clean[entry.offset:entry.offset+entry.source_length]==entry.expected_bytes
        span=ctx.arm[entry.offset:entry.offset+entry.slot_size];english=entry.suggested_english.encode('ascii')
        assert span==english+bytes(entry.slot_size-len(english))
        aliases.append(dict(profile_ID=entry.row_id,offset=entry.offset,source_Japanese=entry.japanese,source_hex=entry.expected_bytes.hex(),
            current_span_hex=span.hex(),current_term=entry.suggested_english,
            inline_span_not_a_new_termination_ownership_or_UI_consumer_claim=True))
    assert len(aliases)==10
    reference=Path('guide/research/player-terminology-reference.json');stats=[r for r in load(reference) if (r['japanese'],r['english']) in [('運勢','Luck'),('魅力','Charm')]]
    assert len(stats)==2
    revised=deepcopy(prose);changed=[]
    for row in revised['records']:
        if row['id'] not in {'DK4_MES_B267_R0041','DK4_MES_B269_R0006'}:continue
        old=deepcopy(row);assert 'San Jorge' in row['english']
        row.update(english=row['english'].replace('San Jorge','Sao Jorge'),logical_English=row['english'].replace('San Jorge','Sao Jorge'),
            decision='revision',retention_reason=None,finding='Use the registered Sao Jorge city name, qualified by its exact clean/current pointer and public string; preserve all other meaning.',
            localization_note='Align the city spelling with the registered source-bound Sao Jorge term, without changing the city data or any dialogue facts.')
        changed.append(dict(id=row['id'],prior_decision=old['decision'],prior_English=old['english'],revised_English=row['english'],
            source_reference=row['source_reference'],current_reference=row['current_reference']))
    assert len(changed)==2
    a={r['id']:r for r in prose['records']};assert all(r==a[r['id']] for r in revised['records'] if r['id'] not in {v['id'] for v in changed})
    revised.update(counts={'retention':87,'revision':129},scoped_term_reconciliation=str(TERMS),prior_contextual_manuscript=str(PRIOR_PROSE),
        prior_contextual_manuscript_sha256=digest(PRIOR_PROSE),only_two_city_spellings_andone_prior_retention_reclassified=True)
    terms=dict(runtime=runtime,equipment_terms=[],inline_city_aliases=aliases,
        Sao_Jorge=dict(pointer_field=at,source_pointer=source['pointer'],source_Japanese=raw.decode('cp932'),source_hex=raw.hex(),current_hex=city.hex(),current_term=city.decode(),
            approved_reference=str(CITY),approved_reference_sha256=digest(CITY),
            separate_legacy_untranslated_alias_not_changed_andremains_in_later_reaudit=prior['separate_untranslated_Sao_Jorge_alias_still_open']),
        permanent_attributes=stats,geographic_andliterary_forms={'イギリス人':'English','オランダ人':'Dutch','イタリア':'Italy','ポルトガル人':'Portuguese','スペイン':'Spain',
            'カリブ海':'Caribbean','地中海':'Mediterranean','インド':'India','サハラ':'Sahara','紫禁城':'Forbidden City'},
        source_unnamed_figureheads_voices_buildings_andtreasures_not_expanded_to_item_titles=True,
        curse_question_not_a_stat_or_diagnosis=True,no_new_native_city_UI_orolder_record_technical_credit=True,
        source_terms_are_localization_not_external_historical_verification=True,no_current_orclean_ROM_mutation=True,
        prose_reconciliation=changed,new_credit=0,
        evidence={str(p):digest(p) for p in [CURRENT,PRIOR_PROSE,CITY,reference,Path('dk4tool/script/arm9_profiles.py'),Path(__file__)]})
    save(TERMS,terms);revised['scoped_term_reconciliation_sha256']=digest(TERMS);save(PROSE,revised)
    print('Sao Jorge, ten city spans and Luck/Charm bound; 129 revisions/87 retentions. Other 214 decisions exact.')

if __name__=='__main__':main()
