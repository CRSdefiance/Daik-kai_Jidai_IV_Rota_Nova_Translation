"""Keep complete live pixel/order/host guards and bind the current concrete risks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

previous=Path('scripts/audit_maria337_gameplay_v1.py').read_text(encoding='utf-8')
start=previous.index('            for n,nextn in [(325,328)')
stop=previous.index("        else:assert dict(start=4140",start)
old=previous[start:stop]
new='''            for ident,nextid in [('DK4_MES_B141_R0043','DK4_MES_B141_R0054'),
                    ('DK4_MES_B146_R0056','DK4_MES_B148_R0008'),('DK4_MES_B148_R0008','DK4_MES_B148_R0012')]:
                pair=[c for c in calls if c['id']==ident]
                assert len(pair)==1 and pair[0]['page']==1
                following=next(c for c in calls if c['frame']>pair[0]['frame'])
                assert following['id']==nextid
                pushes=[c for c in controls if pair[0]['frame']<c['start']<following['frame'] and c['buttons']==['A']]
                assert len(pushes)==1 and pushes[0]['duration']==16
                tutorial.append(dict(id=ident,one_complete_page=pair[0],following=following,ordinary_A=pushes[0]))
            FEids={r['id'] for r in fixture['selected_records'] if r['selector']==254};assert len(FEids)==11
            guards={'DK4_MES_B139_R0199','DK4_MES_B139_R0202','DK4_MES_B145_R0051',
                'DK4_MES_B145_R0057','DK4_MES_B145_R0077','DK4_MES_B150_R0036'}
            assert guards<=FEids
            for ident in sorted(FEids):
                call=next(c for c in calls if c['id']==ident)
                following=next((c for c in calls if c['frame']>call['frame']),None)
                # The final wheat forecast returns into the original host cleanup.
                if ident=='DK4_MES_B151_R0050':
                    assert following is None
                    assert transitions['source_complete_hosts_reach_resupply_departure_andfinal_sailing']
                else:assert following is not None
                FEchecks.append(dict(id=ident,call=call,following=following,scoped_guard_repair=ident in guards,
                    original_host_return_instead_of_next_selected_speech=following is None))
            for ident,nextid in [('DK4_MES_B139_R0202','DK4_MES_B139_R0205'),
                    ('DK4_MES_B145_R0057','DK4_MES_B145_R0060'),('DK4_MES_B145_R0077','DK4_MES_B145_R0081'),
                    ('DK4_MES_B145_R0097','DK4_MES_B145_R0100')]:
                left=next(c for c in calls if c['id']==ident)
                following=next(c for c in calls if c['frame']>left['frame'])
                assert following['id']==nextid
'''
source=checked_text(previous,{
    'scripts.meaning_maria337_clean_v1':'scripts.meaning_maria335_B137_B151_v1',
    "ROOT/'reconstruction_v1/reconstruction.json'":"ROOT/'reconstruction_v2/reconstruction.json'",
    '[(0,22241,46,50,88),(1,10961,3,3,6)]':'[(0,20801,44,44,66),(1,10721,2,2,4)]',
    '==(136,356,2)':'==(138,1274,2)',old:new,
    '==(335,48,52,2)':'==(333,44,44,2)',
    'totals==[106,94,6] and len(tutorial)==4 and len(FEchecks)==6 and len(sheets)==14':
        'totals==[92,70,6] and len(tutorial)==3 and len(FEchecks)==11 and len(sheets)==13',
    "{'DK4_MES_B127_R0029','DK4_MES_B128_R0080','DK4_MES_B130_R0271','DK4_MES_B135_R0294','DK4_MES_B136_R0211'}":
        "{'DK4_MES_B137_R0046','DK4_MES_B138_R0109','DK4_MES_B139_R0134','DK4_MES_B140_R0116','DK4_MES_B148_R0012','DK4_MES_B151_R0031'}",
    'distinct_native_body_candidates=48,distinct_source_body_objects=48,distinct_body_pages=52':
        'distinct_native_body_candidates=44,distinct_source_body_objects=44,distinct_body_pages=44',
    'complete_body_planes=106,complete_header_planes=94':'complete_body_planes=92,complete_header_planes=70',
    'offline_only_source_body_objects=287':'offline_only_source_body_objects=289',
    'all_four_two_page_tutorial_A_andfollowing_returns_observed=True,all_six_FE_panels_andnamed_returns_observed=True':
        'all_three_reclaimed_one_page_paragraph_A_andfollowing_returns_observed=True,all_eleven_FE_panels_andreturns_observed=True,all_six_scoped_FE_guard_repairs_observed=True',
    'both_mixed_font_Latin_I_repairs_observed=True,Carlo_Cesare_Fernando_name_introductions_observed=True':
        'Julio_mixed_font_I_andIndeed_repairs_observed=True,all_eight_tutorial_room_terms_andbread_forecast_prose_observed=True',
    'all52_selected_pages_two_captions_andboth_host_transitions_directly_viewed=True':
        'all44_selected_pages_two_captions_andboth_host_transitions_directly_viewed=True',
    'PASS actual QA:48 source bodies/52 viewed pages,both captions/options,four tutorial page turns,six FE panels,both sailing returns.':
        'PASS actual QA:44 source bodies/pages,both caption options,three reclaimed paragraphs,11 FE panels andboth sailing returns.',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-live-complete-pixel-header-controller-and-host-guards-current-risks','exec'),globals())
