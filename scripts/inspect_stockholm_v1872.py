"""Bounded source/evidence inspection for the resumed editorial review."""
import json
from pathlib import Path

def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

if __name__ == '__main__':
    import sys
    mode=sys.argv[1] if len(sys.argv)>1 else 'prose'
    if mode=='ledger':
        d=read('translations/editorial_review_current_v1.json')
        for k in ('records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','records_with_source_and_prose_pass','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file','reviewed_but_incomplete_route_record_IDs','active_source_prose_drafts','next_route_scene_editorial_packet','contextual_review','contextual_pass'):
            print(k,json.dumps(d.get(k),ensure_ascii=False)[:6500])
        print('UNITS',[(u['id'],u.get('status')) for u in d['coverage_units'][-5:]])
        print('WATCH',[(k,list(v) if isinstance(v,dict) else v) for k,v in d['formatting_watchlist'].items() if 'Stockholm' in k or 'stockholm' in k])
        print('ALL KEYS',list(d))
        raise SystemExit
    if mode=='prose':
        for r in read('translations/lil_Stockholm_encounter_editorial_manuscript_v2.json')['records']:
            print(json.dumps({k:r[k] for k in ('id','speaker','source_Japanese','english','editorial_decision','localization_note')},ensure_ascii=False))
        raise SystemExit
    if mode=='evidence':
        for p in ['work/analysis/lil_Stockholm_revised_audit_v1867c/revised_Stockholm36_branch_and_three_fixture_audit.json','work/analysis/lil_Stockholm_font_approval_v1859b/visual_and_scoped_profile_review.json']:
            d=read(p);print(p)
            for k,v in d.items():
                if k in ('revised_speech_observations','original_command_pairs'):continue
                print(k,json.dumps(v,ensure_ascii=False)[:3500])
        raise SystemExit
    paths = [
        'translations/lil_Stockholm_encounter_editorial_manuscript_v2.json',
        'work/analysis/lil_Stockholm_source_v1848b/all51_clean_current_native_source_context.json',
        'work/analysis/lil_Stockholm_relocation_v1861/nested_source_relocation_research.json',
        'work/analysis/lil_Stockholm_reference_census_v1866/all102_commands24_relative_sites_and_shipped_entry_census.json',
        'work/analysis/lil_Stockholm_revised_audit_v1867c/revised_Stockholm36_branch_and_three_fixture_audit.json',
    ]
    for p in paths:
        d=read(p)
        print('\nFILE',p,'KEYS',list(d))
        for k,v in d.items():
            if isinstance(v,list):
                print(k,'COUNT',len(v),'FIRST',str(v[:1])[:2200])
            elif isinstance(v,dict):
                print(k,'DICT KEYS',list(v))
            else: print(k,str(v)[:500])
    d=read(paths[0])
    for r in d['records']:
        print('REVIEW',json.dumps({k:v for k,v in r.items() if k in ('id','source_meaning','english','speaker','context','localization_note','source_text','current_text','decision','retention_reason')},ensure_ascii=False))
    s=read('translations/release_stack.json')
    print('REGISTRY',list(s),'ACCEPTED',len(s['accepted_layers']))
    p=s['profiles']['all-routes-unified-v1841']
    print('PROFILE KEYS',list(p),'PROMOTED',s['latest_promoted_build'])
    lines=Path('docs/known_issues.md').read_text(encoding='utf-8').splitlines()
    print('KNOWN ISSUES TAIL','\n'.join(lines[-110:]))
