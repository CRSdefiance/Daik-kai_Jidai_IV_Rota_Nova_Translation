"""Prepare reference-approved B179 metadata and full-history independent audit."""
from pathlib import Path
import re
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B179_reference_checkpoint_tools_v4745')
assert not ROOT.exists()
counts={'5898':'5912','5885':'5898','5901':'5915','3738':'3740','2147':'2158','4299':'4313','4286':'4299'}
tools=[]
sources=[('scripts/checkpoint_lil_B178_references_v4697.py','scripts/checkpoint_lil_B179_references_v4745.py'),
         ('scripts/verify_editorial_handoff_v4698.py','scripts/verify_editorial_handoff_v4746.py')]
for src,dst in sources:
    source,target=Path(src),Path(dst);assert not target.exists()
    text=source.read_text(encoding='utf-8');changes=[]
    def change(old,new):
        global text
        assert old in text,old
        changes.append(dict(before=old,after=new,count=text.count(old)))
        text=text.replace(old,new)
    pattern=re.compile(r'(?<![0-9])('+('|'.join(counts))+r')(?![0-9])')
    changes.append(dict(counter_contexts=[text[max(0,m.start()-22):m.end()+22] for m in pattern.finditer(text)]))
    text=pattern.sub(lambda m:counts[m.group()],text)
    if 'checkpoint_lil_B178' in src:
        change("FAMILY='Lil-B178-home-baking-three-Ladies-husband-corner-bakery-teaching-ingredients-and-prospective-Amsterdam-wheat13'",
            "FAMILY='Lil-B179-Barkeep-Patron-Sailor-wine-trial-three-gulps-joining-order-and-prospective-Sao-Jorge14'")
    else:
        for old,new in [
            ("{'revise':2,'retain-wording':11}","{'revise':8,'retain-wording':6}"),
            ("scope['remaining_B179_B180_physical_speeches']==25","scope['remaining_B180_physical_speeches']==11"),
            ("block['block']==178","block['block']==179"),('blocks[178]','blocks[179]'),
            ('[(490,452)]','[(508,492)]'),('==(496,456)','==(512,496)'),
            ('==(52,28,24)','==(56,20,36)'),
            ("len(control['all3_source_current_target_nonrelative_nonspeech_leaves'])==3 and len(control['relocated_C200_pairs'])==1",
             "len(control['all2_source_current_target_nonrelative_nonspeech_leaves'])==2 and len(control['relocated_C200_pairs'])==0"),
            ("len(visual['paired_full_screen_views'])==4","len(visual['paired_full_screen_views'])==5"),
            ("for s in visual['paired_full_screen_views'])==16","for s in visual['paired_full_screen_views'])==20"),
            ("len(visual['actual_timing_differences'])==14","len(visual['actual_timing_differences'])==8"),
            ("{'total':14,'speech':12,'control_or_end':2}","{'total':8,'speech':7,'control_or_end':1}"),
            ('source_A0008_C200488_single_end490_actually_executed','source_A0008_single_end508_actually_executed_no_C200'),
            ('[3306586022,3306586022]','[403514907,403514907]'),('[5977,5976]','[6216,6215]'),
            ('13_relocated_dispatches52_stored','14_relocated_dispatches56_stored'),
            ('actual13_panels12_progressive1_impersonal_FE_A000_C200_single_end','actual14_panels13_progressive1_impersonal_FE_A000_single_end_no_C200'),
            ('equal_14_timings','equal_8_timings'),('PRNG3306586022','PRNG403514907'),
            ('and11_retained','and6_retained'),
        ]:change(old,new)
    for old,new in [
        ('checkpoint_lil_B178_references_v4697','checkpoint_lil_B179_references_v4745'),
        ('lil_B178_reference_checkpoint_text_v4697','lil_B179_reference_checkpoint_text_v4745'),
        ('lil_B178_reference_checkpoint_v4697','lil_B179_reference_checkpoint_v4745'),
        ('editorial_handoff_verification_v4698','editorial_handoff_verification_v4746'),
        ('editorial_handoff_verification_v4684','editorial_handoff_verification_v4732'),
        ('lil_B178_reference_approval_v4696','lil_B179_reference_approval_v4744'),
        ('lil_B178_editorial_manuscript_v3','lil_B179_editorial_manuscript_v3'),
        ('lil_B178_editorial_manuscript_v4','lil_B179_editorial_manuscript_v4'),
        ('lil_B178_display_fixture_v4691','lil_B179_display_fixture_v4739'),
        ('lil_B178_research_v4686','lil_B179_research_v4734'),
        ('unfinished_editorial_scope_v4679','unfinished_editorial_scope_v4727'),
        ('unfinished_editorial_scope_v4697','unfinished_editorial_scope_v4745'),
        ('lil_B178_reference_reconciliation_v4697','lil_B179_reference_reconciliation_v4745'),
        ('B178_reference_and_actual_coverage_v4697','B179_reference_and_actual_coverage_v4745'),
        ('all-routes-unified-v4595','all-routes-unified-v4701'),('all-routes-unified-v4655','all-routes-unified-v4701'),
        ('all13','all14'),('==13','==14'),('pending=13','pending=14'),('actual_complete_native_panels=13','actual_complete_native_panels=14'),
        ('(5912,5898,13)','(5912,5898,14)'),('13-Lil','14-Lil'),('/13 pending','/14 pending'),
        ('sealed13-actual','sealed14-actual'),('V4697:13','V4745:14'),('V4697','V4745'),('B178','B179'),
        ('main_V4595','main_V4701'),('main V4595','main V4701'),('thirteen','fourteen'),
    ]:
        if old in text:change(old,new)
    compile(text,str(target),'exec');target.write_text(text,encoding='utf-8',newline='\n')
    tools.append(dict(source=src,source_sha256=sha(source.read_bytes()),target=dst,target_sha256=sha(target.read_bytes()),changes=changes))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,all_source_prose_and_completion_counts_preserved=True,
    fresh_actual14_panels8_timings20_fullscreens_and_PRNG403514907_bound=True,city_alias_lead_and_full_scope_preserved=True,
    main_V4701_unchanged=True,full_goal_complete=False))
print('Prepared B179 reference checkpoint and independent deep audit; no current metadata mutation.')
