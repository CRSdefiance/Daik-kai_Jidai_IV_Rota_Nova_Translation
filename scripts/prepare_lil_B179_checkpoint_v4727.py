"""Derive the B179 pending-credit producer and deep audit from sealed B178 tools."""
from pathlib import Path
import re
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B179_checkpoint_tools_v4727')
assert not ROOT.exists()
counts={'5885':'5898','5888':'5901','5898':'5912','5901':'5915','4032':'4045','4045':'4059',
        '3738':'3740','2147':'2158','4299':'4313','4286':'4299'}
sources=[('scripts/checkpoint_lil_B178_v4679.py','scripts/checkpoint_lil_B179_v4727.py'),
         ('scripts/verify_editorial_handoff_v4680.py','scripts/verify_editorial_handoff_v4728.py')]
tools=[]
for src,dst in sources:
    source,target=Path(src),Path(dst);assert not target.exists()
    text=source.read_text(encoding='utf-8');changes=[]
    def change(old,new):
        global text
        assert old in text,old
        changes.append(dict(before=old,after=new,count=text.count(old)))
        text=text.replace(old,new)
    # Apply numeric counters simultaneously with digit boundaries. These count values
    # occur in assertions/reporting only; record IDs, addresses and version names differ.
    pattern=re.compile(r'(?<![0-9])('+('|'.join(counts))+r')(?![0-9])')
    changes.append(dict(counter_contexts=[text[max(0,m.start()-24):m.end()+24] for m in pattern.finditer(text)]))
    text=pattern.sub(lambda m:counts[m.group()],text)
    if 'checkpoint_lil_B178' in src:
        change("FAMILY='Lil-B178-home-baking-three-Ladies-husband-corner-bakery-teaching-ingredients-and-prospective-Amsterdam-wheat13'",
               "FAMILY='Lil-B179-Barkeep-Patron-Sailor-wine-trial-three-gulps-joining-order-and-prospective-Sao-Jorge14'")
        change("work/analysis/editorial_handoff_verification_v4674/verified_handoff.json",
               "work/analysis/promotion_v4725b/promotion_receipt.json")
        change("if r['block'] in [179,180]","if r['block']==180")
        change("len(remaining)==2 and sum(r['speeches'] for r in remaining)==25",
               "len(remaining)==1 and sum(r['speeches'] for r in remaining)==11")
        change("# Current editorial handoff - V4673","# Current editorial handoff - V4725")
        change("previous=ledger['unfinished_editorial_scope_v4659'];assert sha(Path(previous['path']).read_bytes())==previous['sha256']\n    inventory=deepcopy(read(previous['path']))",
               "previous=ledger['unfinished_editorial_scope_v4725']\n    inventory=deepcopy(previous)")
        change("row_count_notes=5","row_count_notes=4")
        change("remaining_B179_B180_unreviewed_uncredited","remaining_B180_unreviewed_uncredited")
        change("physical_speeches=25","physical_speeches=11")
        change("remaining_B179_B180_physical_speeches=25","remaining_B180_physical_speeches=11")
        change("'source_effect_and_predicate_contract','source_nameplate_consumer_proof']",
               "'source_effect_and_predicate_contract','source_nameplate_consumer_proof','separate_untranslated_city_alias_lead']")
    else:
        change("oldinventory=read(before['unfinished_editorial_scope_v4659']['path'])",
               "oldinventory=before['unfinished_editorial_scope_v4725']")
        change("scope['remaining_B179_B180_physical_speeches']==25","scope['remaining_B180_physical_speeches']==11")
        change("remaining_B179_B180_unreviewed_uncredited","remaining_B180_unreviewed_uncredited")
        change("main_V4595_and_latest_experimental_V4655_preserved","main_V4701_and_registered_stack_preserved")
    for old,new in [('lil_B178_checkpoint_text_v4679','lil_B179_checkpoint_text_v4727'),
        ('lil_B178_native_approval_v4678','lil_B179_native_approval_v4726'),
        ('lil_B178_editorial_manuscript_v3','lil_B179_editorial_manuscript_v3'),
        ('checkpoint_lil_B178_v4679','checkpoint_lil_B179_v4727'),
        ('lil_B178_checkpoint_v4679','lil_B179_checkpoint_v4727'),
        ('editorial_handoff_verification_v4680','editorial_handoff_verification_v4728'),
        ('lil_B178_scope_reconciliation_v4679','lil_B179_scope_reconciliation_v4727'),
        ('unfinished_editorial_scope_v4679','unfinished_editorial_scope_v4727'),
        ('lil_B178_v4679','lil_B179_v4727'),('B178_fresh_context_review_checkpoint_v4679','B179_fresh_context_review_checkpoint_v4727'),
        ('earlier_B178_uncredited_leads_are_historical_after_V4679','earlier_B179_uncredited_leads_are_historical_after_V4727')]:
        if old in text:change(old,new)
    for old,new in [('all13','all14'),('and11_retention','and6_retention'),('new_source_prose_reviews=13','new_source_prose_reviews=14'),
        ('source_prose_reviews_added=13','source_prose_reviews_added=14'),('proposed_revisions=2','proposed_revisions=8'),
        ('justified_retentions=11','justified_retentions=6'),('retentions=11','retentions=6'),
        ("'proposed_revisions']==2","'proposed_revisions']==8"),("'retentions']==11","'retentions']==6"),
        ("{'revise':2,'retain-wording':11}","{'revise':8,'retain-wording':6}"),
        ("==13","==14"),('records=13','records=14'),('pending-release','pending-release'),
        ('fresh_pending=13','fresh_pending=14'),('pending_native_actual_release=13','pending_native_actual_release=14'),
        ('pending_records=13','pending_records=14'),('count=13','count=14'),('prose_count=13','prose_count=14'),
        ('source_prose=13','source_prose=14'),('(5912,5898,13)','(5912,5898,14)'),
        ('current_original_macro_alignment_calls\']==104','current_original_macro_alignment_calls\']==112'),
        ("==(12,1)","==(13,1)"),('native_alignment_cases=104','native_alignment_cases=112'),
        ('blocks[178]','blocks[179]'),('blocks=[178]','blocks=[179]'),('B178','B179'),
        ('V4679','V4727'),('thirteen','fourteen'),('13 pending','14 pending'),('/13 pending','/14 pending'),
        ('13-Lil','14-Lil'),(':13 ',':14 '),('records=13','records=14'),('pending=13','pending=14')]:
        if old in text and old!=new:change(old,new)
    compile(text,str(target),'exec')
    target.write_text(text,encoding='utf-8',newline='\n')
    tools.append(dict(source=src,source_sha256=sha(source.read_bytes()),target=dst,target_sha256=sha(target.read_bytes()),changes=changes))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,old_ledger_counter_and_all_nested_history_audit_required_before_mutation=True,
    existing_city_alias_lead_and_full_scope_carried=True,main_V4701_unchanged=True,full_goal_complete=False))
print('Prepared B179 pending-credit and independent deep-audit tools; no current metadata mutation.')
