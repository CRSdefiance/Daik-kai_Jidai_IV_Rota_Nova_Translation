"""Prepare an uncredited clean-only checkpoint without repeating sealed release checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
NEXT='Continue B203 from complete clean inventory6006 and whole-exchange gloss6007 before reading older English. Bind source selectors2/76/170 and the separate FE notice to exact clean/current names,roles,voices and display consumers without borrowing B202 actors or aliases. Retrospectively review awkward anonymous labels against the Japanese and actual scene;preserve all207 names/roles/aliases in scope. Preserve the cordyceps/Chinese medicinal context as character dialogue,the unspecified offered reference work,hesitation about an expensive-looking gift,teasing about companion interest and1000-to100 spoken negotiation without inventing kinship,rank,profession,provenance,guaranteed efficacy or payment semantics. Bind actual source scene,item14 assumptions must not be inherited,picture/widget/native item identity,entry,all31 commands,nine nonspeech leaves,one FE/FI charm+1 and four-byte end810 in816 stored/814 logical bytes/two tailzeros. There is no explicit spoken book title. Preserve clean references,then compare old English as evidence and complete natural-dialogue-v2/native/reference/representative/release gates. Keep22 glosses uncredited until necessary gates pass and registered integration is verified. Reuse sealed B202/V5998 checks absent a concrete new risk. Keep every storyline,earlier translations,shared town/shop/random/Help/prose,premature wraps and207 names open. Preserve all artifacts and earlier leads including following B43 source-item/Local Product,Samwell and Alexandria. Graphics/all18 plaques and later older-record technical re-audit remain separate/open.'
DETAILS='V6008 records a fresh clean-only B203 inventory and whole-exchange gloss:22 objects,21 progressive speeches plus one FE/FI charm+1 notice,31 commands,selectors76x6/2x8/170x7/254x1,zero FA/FO,choices or typed styles. Source816 stored/814 logical bytes has two alignment zeros and a complete four-byte end at810. Nine nonspeech leaves remain exact and uninterpreted beyond inventory:one4820,one4735,one6003,one632E,fourA000 and the end.4C reacts to an insect with apparent grass growing on it;AA identifies cordyceps and describes its Chinese medicinal use. AA then offers a reference work about medicinal materials.02 hesitates over its apparent value;AA says it is no longer needed,then teases4C interest.4C admits wanting to read the book.02 proposes paying1000 gold;AA accepts100 instead. No explicit book title is spoken. Preserve uncertain discovery,older colloquial/teasing voices,unfinished objection,embarrassed admission,generosity and exact amounts. Names/roles/voices,actual source scene,item/widget identity,payment/effects,current references,old-English comparison and all target gates remain pending. These22 clean glosses add no source-prose/completion credit,no ROM and no new emulator run. Registered cumulative experimental V5998 and its exact clean-input patch remain verified with590 batches/114 accepted/18 release checks. B20219 reviews were integrated once:six revisions/13 justified retentions. Coverage stays6327 completed/6330 source-prose/3959 integrated revisions/2368 justified retentions/SC24442/SC396/routes4728/4728,zero credited route drafts pending. Main V4701 remains promoted. All earlier root/nested history,ROMs,translations,failed producers and unresolved scope are preserved. Full editorial and207-entry name/role/alias review remain active.'
if __name__=='__main__':
    source=Path('scripts/checkpoint_lil_B202_clean_v5957.py').read_text(encoding='utf-8')
    oldnext=next(line for line in source.splitlines() if line.startswith('NEXT='))
    olddetails=next(line for line in source.splitlines() if line.startswith('DETAILS='))
    changes={
      oldnext:'NEXT='+repr(NEXT),olddetails:'DETAILS='+repr(DETAILS),
      'Record19 uncredited':'Record22 uncredited',
      'lil_B202_clean_checkpoint_v5957':'lil_B203_clean_checkpoint_v6008',
      'editorial_handoff_verification_v5958':'editorial_handoff_verification_v6009',
      'editorial_handoff_verification_v5953':'editorial_handoff_verification_v6004',
      'lil_B202_clean_inventory_v5955/all_clean_B202_speeches':'lil_B203_clean_inventory_v6006/all_clean_B203_speeches',
      'lil_B202_clean_context_v5956/all19_clean_unsolicited_book_handoff_pursuit_and_self_interested_request_glosses':'lil_B203_clean_context_v6007/all22_clean_cordyceps_book_offer_and1000_to100_negotiation_glosses',
      'Lil_B202_clean_source_v5957':'Lil_B203_clean_source_v6008',
      'unfinished_editorial_scope_v5957':'unfinished_editorial_scope_v6008',
      'lil_B201_release_v5948':'lil_B202_release_v5999',
      'all_routes_unified_v5947':'all_routes_unified_v5998',
      "len(manifest['batches'])==589":"len(manifest['batches'])==590",
      "len(gloss['records'])==19":"len(gloss['records'])==22",
      "old['unfinished_editorial_scope_v5952']":"old['unfinished_editorial_scope_v6003']",
      'historical_B202_clean_pending_before_v5957':'historical_B203_clean_pending_before_v6008',
      'next_Lil_B202_clean_review_pending':'next_Lil_B203_clean_review_pending',
      'Lil_B202_clean_only_uncredited_v5957':'Lil_B203_clean_only_uncredited_v6008',
      'source_speech_objects=19,source_commands=26':'source_speech_objects=22,source_commands=31',
      'B202_clean_only_uncredited_speeches=19':'B203_clean_only_uncredited_speech_and_notice_objects=22',
      'source_speech_objects=19,new_source_prose_reviews=0':'source_speech_objects=22,new_source_prose_reviews=0',
      '## V5957: B202 clean-only whole-exchange gloss;V5947 stays verified':'## V6008: B203 clean-only whole-exchange gloss;V5998 stays verified',
      '# Current editorial handoff - V5957':'# Current editorial handoff - V6008',
      '19 clean-only B202 glosses':'22 clean-only B203 glosses',
      "new['records_editorially_completed']==6308 and new['records_with_source_and_prose_pass']==6311":"new['records_editorially_completed']==6327 and new['records_with_source_and_prose_pass']==6330",
      "'next_B202_clean_source_glosses':19,'B202_target_reviews_uncredited':True,'prior_English_B202_speech_unread':True":"'next_B203_clean_source_glosses':22,'B203_target_reviews_uncredited':True,'prior_English_B203_speech_unread':True",
      'Verified V5957 clean-only checkpoint:V5947/6308 completed unchanged,B20219 glosses':'Verified V6008 clean-only checkpoint:V5998/6327 completed unchanged,B20322 glosses',
    }
    proof=derive('scripts/checkpoint_lil_B202_clean_v5957.py','scripts/checkpoint_lil_B203_clean_v6008.py',changes)
    root=Path('work/analysis/lil_B203_checkpoint_preparation_v6008');root.mkdir(parents=True);save(root/'derivation.json',proof)
