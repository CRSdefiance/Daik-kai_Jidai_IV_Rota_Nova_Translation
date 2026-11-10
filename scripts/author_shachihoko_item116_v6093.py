"""Author coordinated cultural title/description from the already read clean context."""
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_item116_prose_v6093')
DOC=Path('translations/shachihoko_item116_editorial_manuscript_v1.json')
BIND=Path('work/analysis/shachihoko_description_consumers_v6092/current218_live_description_getters_two_item_callers_and_exact_owned_representations.json')
DESC=Path('work/analysis/shachihoko_description_v6085/clean_description_neighbor_context_current_COMMON_and_staged_copy_lead.json')
NAME=Path('work/analysis/shachihoko_item_name_research_v6079/provisional_item116_manuscript.json')
ENGLISH='A shachihoko figurehead posed with its tail raised as if to threaten foes. Legend says even fearsome storms avoid a fleet carrying it.'
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();binding,description,names=map(read,[BIND,DESC,NAME]);title=deepcopy(names['records'][0])
    assert names['source_context_sha256']==sha(Path(names['source_context']).read_bytes())
    title['context']='The four complete castle exchanges identify the upturned ornament as シャチホコ;the independent item title is 鯱の像. The shared title appears in catalog/list,story card and generated acquisition consumers. Its Figurehead category remains separate. Guard and daimyo speech and Jam\'s boast/letter have their own distinct voices.'
    title['localization_note']='Use Shachihoko for the culturally identified ornament,matching the four castle variants and actual sprite. The English cultural noun names the ornament itself,so a redundant statue suffix is unnecessary. Do not replace Jam\'s intentionally mistaken ship-use account with architectural narration. Preserve the source description\'s independent シャチ wording as evidence rather than claiming it literally says シャチホコ. No nickname,rank,relationship,material,castle name or guaranteed effect is invented.'
    title['review']=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
    row=dict(id='COMMON_ITEM_116_CULTURAL_DESCRIPTION',item_ID=116,message_id=2931,source_Japanese=description['source_description']['text'],source_hex=description['source_description']['text_hex'],
        source_reference=description['source_description'],current_reference=description['current_description'],current_text_hex=description['current_description']['text_hex'],
        current_English=description['current_description']['text'],english=ENGLISH,speaker='Item description narrator',
        source_meaning=description['clean_first_gloss'],context='Read with the seven clean neighboring descriptions and all four complete castle exchanges. This is the shared item description,not Jam\'s unreliable letter. Preserve the threatening raised-tail pose and reported storm legend;do not turn a legend into a promised gameplay result.',
        localization_note='Use the coordinated cultural object name while retaining the complete threatening pose and the explicit as-if qualification. Legend says preserves 言い伝え;even fearsome storms preserves the emphasis;fleet carrying it preserves the subject and conditional equipment context. The prose does not add roof/fire-protection lore or a historical castle. This is a complete natural English item description,authored before allocation/layout choices.',
        editorial_decision='revise',translation_policy='natural-dialogue-v2',target_locale='en-US',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
        native_argument_count=0,source_native_macros=[],manual_line_breaks=[],new_duplicate_editorial_credit=0)
    assert all('\n' not in r['english'] and '{' not in r['english'] and not r['english'].startswith(' ') and '  ' not in r['english'] for r in [title,row])
    parent=NdsImage.open(binding['candidate']);canonical=Path('out/raphael_natural_v2_accepted_base.nds');clean=Path('work/clean.nds')
    ROOT.mkdir(parents=True);save(DOC,dict(format='dk4-coordinated-cultural-item-editorial-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        current_ROM=binding['candidate'],current_ROM_sha256=binding['candidate_sha256'],current_ARM9_sha256=binding['ARM9_sha256'],current_COMMON_sha256=binding['COMMON_sha256'],
        source_ROM=str(clean),source_ROM_sha256=sha(clean.read_bytes()),canonical_baseline=str(canonical),canonical_baseline_sha256=sha(canonical.read_bytes()),
        records=[title,row],source_context=names['source_context'],source_context_sha256=names['source_context_sha256'],
        description_bindings=str(BIND),description_bindings_sha256=sha(BIND.read_bytes()),source_description=str(DESC),source_description_sha256=sha(DESC.read_bytes()),
        all_English_words_authored_before_storage_choice=True,source_context_localization_naturalness_reviewed=True,native_formatting_and_combined_release_pending=True,
        both_active_COMMON_and_compiled_item_description_must_agree=True,no_global_Orca_or_nickname_substitution=True,
        all207_names_all_storylines_and_full_editorial_goal_preserved=True,new_review_credit=0,full_goal_complete=False))
    save(ROOT/'source_first_prose_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),description_characters=len(ENGLISH),description_words=len(ENGLISH.split()),
        four_per_record_gates_true_formatting_pending=True,no_ROM_registry_or_ledger_mutation=True,
        evidence={str(p):sha(p.read_bytes()) for p in [BIND,DESC,NAME,Path(__file__)]},full_goal_complete=False))
    print(dict(description=ENGLISH,characters=len(ENGLISH),source_first=True,formatting_and_combined_release_pending=True))
