"""Prepare source-preserving release and boot successors for the mood batch."""
import ast,re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/mood_comments_v981')

def change(text,old,new):
    assert old in text,old
    return text.replace(old,new)

def main():
    items=[]
    def load(source,target):
        s,t=Path(source),Path(target);assert not t.exists()
        raw=s.read_bytes();return s,t,raw,raw.decode('utf-8')
    s,t,raw,text=load('scripts/prepare_illness_critical_release_v975.py','scripts/prepare_mood_comments_release_v981.py')
    text=re.sub(r'v(975|969)\b',lambda m:'v'+{'975':'981','969':'975'}[m[1]],text)
    text=text.replace('illness_critical','mood_comments').replace('physical_wounds','illness_critical')
    text=change(text,'mood_comments_editorial as owned','mood_comments_editorial_v981b as owned')
    start=text.index('    extra=[');end=text.index('    dependencies=',start)
    extra=['dk4tool/patch/mood_comments_editorial_v981b.py','dk4tool/patch/illness_critical_editorial.py',
        'translations/illness_critical_editorial_release_v1.json','translations/illness_critical_editorial_manuscript_v2.json',
        'scripts/mood_comments_layout_v979.py','scripts/mood_comments_layout_v980.py',
        'scripts/prepare_mood_comments_context_v977.py','scripts/prepare_mood_comments_prose_v978.py',
        'scripts/probe_mood_comments_fonts_v979.py','scripts/probe_mood_comments_fonts_v980.py',
        'scripts/prepare_mood_comments_native_v980.py','scripts/prepare_mood_repack_successor_v981b.py',
        'scripts/audit_mood_comments_native_v981b.py','translations/mood_comments_editorial_manuscript_v1.json',
        'work/analysis/mood_comments_v977/source_context_packet.json',
        'work/analysis/mood_comments_v978/source_context_and_nonverbal_review.json',
        'work/analysis/mood_comments_v979/native_font_proof.json',
        'work/analysis/mood_comments_v980/native_font_proof.json',
        'work/analysis/mood_comments_v980/visual_review.json',
        'work/analysis/mood_comments_v981/repack_successor_provenance_v981b.json']
    text=text[:start]+'    extra='+repr(extra)+'+[str(audit),str(copies)]\n'+text[end:]
    text=text.replace('V969','V975').replace('V975 registered','V981 registered').replace('plus26','plus39')
    text=text.replace('illness/near-death alternatives','mood/panic alternatives').replace('illness/near-death comments1807-1832 for native conditions5/4','mood/panic comments1833-1871 for native moods0/4/5')
    text=text.replace('150 original condition4/5 selectors,100 prior-status controls,52 complete native fonts','225 original mood selectors,75 physical-priority and72 normal-mood controls,78 complete native font cases')
    text=text.replace('26 illness/near-death messages','39 mood/panic messages')
    items.append((s,t,raw,text))
    s,t,raw,text=load('scripts/verify_illness_critical_release_v975.py','scripts/verify_mood_comments_release_v981.py')
    text=re.sub(r'v(975|969)\b',lambda m:'v'+{'975':'981','969':'975'}[m[1]],text)
    text=text.replace('illness_critical','mood_comments').replace('physical_wounds','illness_critical')
    text=change(text,'mood_comments_editorial as owned','mood_comments_editorial_v981b as owned')
    text=change(text,'len(changed_IDs)==22','len(changed_IDs)==25')
    text=text.replace('only26 selected','only39 selected').replace('all3642_other','all3629_other').replace('V975_exact_patch','V981_exact_patch')
    text=text.replace('relative_to_V969','relative_to_V975').replace('V975: full','V981: full').replace('illness-critical','mood/panic')
    items.append((s,t,raw,text))
    for name in ('run','verify'):
        s,t,raw,text=load(f'scripts/{name}_illness_critical_startup_v975.py',f'scripts/{name}_mood_comments_startup_v981.py')
        text=text.replace('illness_critical_v975','mood_comments_v981').replace('all_routes_combined_v975','all_routes_combined_v981')
        if name=='verify':text=text.replace('physical_wounds_v969','illness_critical_v975').replace('V969','V975')
        items.append((s,t,raw,text))
    s,t,raw,text=load('scripts/check_illness_critical_title_v976.py','scripts/check_mood_comments_title_v982.py')
    text=change(text,"choices=('975',)","choices=('981',)")
    text=change(text,"('969',CAP/'physical_wounds_v970_title_969'),('975',CAP/'illness_critical_v976_title_975')","('975',CAP/'illness_critical_v976_title_975'),('981',CAP/'mood_comments_v982_title_981')")
    text=change(text,"reports['969'][0][1100].tobytes()==reports['975'][0][1100].tobytes()","reports['975'][0][1100].tobytes()==reports['981'][0][1100].tobytes()")
    text=change(text,"assert args.run=='975'","assert args.run=='981'")
    text=text.replace('V969','V975').replace('all_routes_combined_v975_candidate','all_routes_combined_v981_candidate')
    text=text.replace("folder=CAP/'illness_critical_v976_title_975'","folder=CAP/'mood_comments_v982_title_981'")
    text=text.replace("ROOT=Path('work/analysis/illness_critical_v976')","ROOT=Path('work/analysis/mood_comments_v982')").replace('title_975_run_plan','title_981_run_plan')
    items.append((s,t,raw,text))
    for _,t,_,text in items:ast.parse(text,filename=str(t))
    builder=Path('scripts/build_integrated_release.py');before=builder.read_bytes();anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('mood_comments_editorial')" not in before
    lo=before.index(b"    illness_critical_editorial = profile_config.get('illness_critical_editorial')");hi=before.index(anchor)
    block=before[lo:hi].replace(b'illness_critical',b'mood_comments').replace(b'ILLNESS_CRITICAL',b'MOOD_COMMENTS')
    block=block.replace(b'from dk4tool.patch.mood_comments_editorial import',b'from dk4tool.patch.mood_comments_editorial_v981b import')
    after=before[:hi]+block+before[hi:];assert after.replace(block,b'',1)==before;compile(after,str(builder),'exec')
    assert not (ROOT/'builder_before.py').exists()
    (ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    provenance=[]
    for s,t,raw,text in items:
        with t.open('x',encoding='utf-8') as f:f.write(text)
        assert s.read_bytes()==raw
        provenance.append({'source':str(s),'source_sha256':sha(raw),'source_after_sha256':sha(s.read_bytes()),'successor':str(t),'successor_sha256':sha(t.read_bytes()),'source_unchanged':True})
    assert builder.read_bytes()==before;builder.write_bytes(after)
    save(ROOT/'registered_tools_provenance.json',{'files':provenance,'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'builder_prior_bytes_restored_by_removing_exact_optional_block':after.replace(block,b'',1)==before,
        'all_replacements_and_syntax_preflighted_before_output':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Five release/boot successors and one optional mood stage prepared; historical tools exact.')

if __name__=='__main__':main()
