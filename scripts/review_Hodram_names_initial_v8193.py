"""Record five source-based name retentions andan explicit unresolved Gerhard surname-order lead."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B137_B45_B46_name_review_v8193')
NATIVE=Path('work/analysis/Hodram_B137_B45_B46_names_v8192/six_static_speakers12_getters_clean_fields24_synthetic_macro_alignments.json')
GLOSS=Path('work/analysis/Hodram_B137_B45_B46_clean_gloss_v8183/28_first_clean_glosses_six_identities_explicit_prerequisite_graph_before_current_English.json')
PRIOR=Path('translations/lil_B222_speaker_name_review_v3.json')
OUT=Path('translations/hodram_B137_B45_B46_speaker_name_review_v1.json')
REASONS={
1:'Retain approved Hodram andJoakim andthe established Bergstrom family component forホドラム/ヨアキム/ベルグストロン. The actual own-current NewGame shows the same three editable fields;original progressive getter omits the middle name while full getter keeps Joakim. The three source exchanges identify the same fleet leader;neitherkun norcourteous address creates a new rank,kinship orname.',
2:'Retain Lil Argot forリル/アーゴット. The original Argot Company invitation andthe preceding territorial/business rivalry identify the same competitive speaker;retain the established company/person spelling consistently. Source姐さん in the invitation is familiar address forthe woman concerned,not an older sister relationship ornew noble/military title.',
9:'Retain approved Camille andthe Overijssel family component forカミル/オーフェルアイセル. Preserve sourceマリヌス asMarinus in the full getter;its absence fromthe progressive nameplate follows the original consumer. The complete apology andreunion context adds no new rank,romance,kinship orhidden identity;kun is localized through the address/tone rather than an invented title.',
18:'Retain Charles Rochefort forシャルル/ロシュフォール andJean forthe source middle fieldジャン. The standard French given/family forms andmiddle-field ordering fit the clean identity without adding an aristocratic title,occupation orhistorical counterpart. Progressive andfull getters retain the original difference;the blunt initial challenge andlater silences remain the same speaker.',
113:'Retain Port Worker as the functional role label for出港所の兄貴 in the complete Amsterdam invitation. A familiar older-brother-style address is not actual siblinghood. Cleanヨーロッパ is source metadata;both original current getters suppress it,so do not turn Europe into a surname orappend invented age/biography. The wider seven-consumer PortWorker review lead remainsopen.',
}
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists();native,gloss,prior=map(read,[NATIVE,GLOSS,PRIOR])
    assert native['source_gloss_sha256']==sha(GLOSS.read_bytes()) and native['current_English_Hodram_B137_B45_B46_bodies_still_unread']
    assert len(native['complete_clean_andcurrent_name_fields'])==6 and len(gloss['records'])==28
    ledger=read('translations/editorial_review_current_v1.json');assert ledger['records_editorially_completed']==7171
    clean=NdsImage.open('work/clean.nds');historical=[]
    for family in ledger['completed_editorial_families']:
        for row in family['records']:
            if 'アーデルンカッツ' not in (row.get('source_Japanese') or ''):continue
            file=row.get('file_path',family.get('file_path'));block=IlnkContainer.parse(clean.read_file(file)).blocks[row['block']]
            ref=row['source_reference'];raw=bytes.fromhex(row['source_hex']);assert block[ref['offset']:ref['offset']+len(raw)]==raw
            historical.append(dict(file_path=file,id=row['id'],block=row['block'],source_reference=ref,source_hex=raw.hex(),source_Japanese=row['source_Japanese'],
                completed_family=family['id'],no_new_dialogue_credit=True))
    assert len(historical)==5
    earlier=next(r for r in prior['records'] if r['actor_ID']==16);assert earlier['english']=='Gerhard Ardelknatts'
    rows=[]
    for record in native['complete_clean_andcurrent_name_fields']:
        actor=record['actor_ID'];getters=record['original_getters'];progressive=next(g for g in getters if g['consumer']=='progressive-nameplate')
        row=dict(actor_ID=actor,name=progressive['text'],source_clean_fields=record['clean_fields'],current_fields=record['current_fields'],original_getters=getters,
            source_speech_references=[dict(id=r['id'],block=r['block'],source_reference=r['source_reference'],source_Japanese=r['source_Japanese']) for r in gloss['records'] if r['source_selector']==actor],
            actual_new_scene_headers_not_yet_observed=True,native_full_glyph_planes_bounds_andactual_headers_pending=True,new_name_or_dialogue_credit=0)
        if actor==16:
            row.update(decision='pending-surname-review',given_name_retention='Gerhard faithfully representsゲルハルト andis used consistently in the complete source exchange.',
                current_surname='Ardelknatts',source_surname='アーデルンカッツ',possible_minimal_order_correction='Ardelnkatts',
                finding='The clean sequenceルンカ corresponds to an n-before-k sequence;current Ardelknatts has k-before-n. The established fictional spelling was previously retained,butthat approval alone doesnot resolve this fresh orthographic concern. No definitive original Latin spelling hasbeen established;the minimal alternative is a proposal,not a shipped orcanonically verified name.',
                required_followup='Review exact registered/current surname consumers andtheir complete clean contexts,then choose a correction orjustify retention before final name-localization approval. Preserve earlier translations/approvals anddo not invent a German historical identity ornewrank. No unavailable external source is imposed as a mandatory gate.',
                previous_review=str(PRIOR),previous_review_sha256=sha(PRIOR.read_bytes()),previous_retention_reason=earlier['fresh_retained_wording_justification'],
                review=dict(source=True,context=True,localization=False,naturalness=False,formatting=False))
        else:row.update(decision='retention',retention_reason=REASONS[actor],review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
        rows.append(row)
    ROOT.mkdir(parents=True)
    save(ROOT/'five_clean_surname_mentions_selfintro_andprior_name_decision.json',dict(records=historical,previous_name_review=deepcopy(earlier),
        original_clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),only_source_name_evidence_no_new_body_English_consulted=True,new_credit=0,full_goal_complete=False))
    save(OUT,dict(format='dk4-source-speaker-name-initial-review-v1',records=rows,
        source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),native_name_proof=str(NATIVE),native_name_proof_sha256=sha(NATIVE.read_bytes()),
        five_individual_localization_retentions_one_surname_concern_not_auto_approved=True,
        external_primary_reference_notes=[
            dict(url='https://www.gamecity.ne.jp/products/products/ee/new/dai4/dai4_02.htm',finding='Official Japanese protagonist introduction names Gerhard in Japanese;this was not decisive original Latin surname evidence. No extra biography orrank is imported into the DS dialogue.'),
            dict(url='https://www.gamecity.ne.jp/manual/dk4HeN38/jp/3500.html',finding='Official Japanese manual labels the speaker by Japanese given name;no decisive Latin surname proof established here.'),
            dict(url='https://www.gamecity.ne.jp/products/products/ee/new/dai4/dai4_04.htm',finding='Legacy companion-page text was returned with a decoding problem;not used as reliable Latin surname evidence.')],
        no_community_romanization_oroutside_biography_overrides_clean_Japanese=True,
        source_only_body_phase_no_current_Hodram_B137_B45_B46_dialogue_English_consulted=True,
        full207_names_roles_aliases_catalogue_customnames_andwider_PortWorker_consumers_still_open=True,
        no_name_asset_ROM_registry_orcompletion_credit_change=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,NATIVE,PRIOR,Path(__file__)]}))
    print('Initial six-name review:five source-context retentions;Gerhard surname ordering unresolved andnot auto-approved.All name formatting pending;no asset/credit change.')
