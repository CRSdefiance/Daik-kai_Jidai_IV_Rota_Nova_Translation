"""Research coherent native pages and signature wrapping without changing any manuscript word."""
from pathlib import Path
from functools import cache
from dataclasses import replace
from types import FunctionType
from dk4tool.dialogue import encoder,layout
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.codec import parse_markup,tokens_to_markup
from dk4tool.dialogue.model import DialogueToken
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
DOC=Path('translations/lil_B209_editorial_manuscript_v1.json')
ROOT=Path('work/analysis/lil_B209_layout_research_v6462d')
WEAK=set('a an as at for from in of the to with and or but so that than because if by into not i you he she it we they my your our his her their is are was were be been being can could will would shall should may might must have has had do does did this these those then why where what when how said them us me him her'.split())
WEAK.update({"that's","there's","i'll","you've"})
PAIRS={('muramasa','blades'),('fine','swords'),('ruler','of'),('of','japan'),('east','asia'),('yukihisa','genjo'),('genjo','shiraki'),('for','now'),('heard','rumors'),('a','letter'),('look','for'),("isn't",'it'),('typical','yukihisa'),('just','like'),('typical','of'),('maybe',"i'll"),('come','in'),("that's",'yukihisa'),('wipe','them')}
def norm(s):return s.strip('.,!?;:\"\'()').casefold()
def plan(row):
    prefix,body=row['english'].split('}',1);prefix+='}';assert body and body.strip()==body and all(32<=ord(c)<127 for c in body)
    words=body.split();assert ' '.join(words)==body;count=len(words);long=row['id']=='DK4_MES_B209_R0027';maximum=8 if row['id'] in ['DK4_MES_B209_R0027','DK4_MES_B209_R0030'] else 4
    signature=row['id']=='DK4_MES_B209_R0033';footer=words.index('--') if signature else None
    @cache
    def solve(start,r):
        if start==count:return (0,0,0,0),()
        if r>=maximum:return None
        best=None
        for stop in range(start+1,count+1):
            line=' '.join(words[start:stop]);length=len(line);final=stop==count
            # Exact printable ASCII phase rule; unknown source/token shapes never enter this research planner.
            reserve=int(not final and length%2==0)
            # An ordinary guarded LF cancels its leading cell in the current painter.
            # At a native page restart,the retained guard occupies the first cell.
            indent=int(r>0 and r%4==0)
            if length+reserve+indent>36:continue
            if not final and line.endswith('I'):continue
            if footer is not None and (start<footer<stop or start==footer and stop<count):continue
            # A whole core assertion ends at Tokugawa;the appositive ruler of Japan remains together next page.
            if r==3 and not final and row['id'] in ['DK4_MES_B209_R0027','DK4_MES_B209_R0030'] and words[stop-1]!=('Tokugawa,' if long else 'Asia.'):continue
            tail=solve(stop,r+1)
            if tail is None:continue
            cost,breaks=tail;word=norm(words[stop-1]);pair=(word,norm(words[stop])) if not final else None
            terminal=words[stop-1].rstrip('\"\')').endswith(('.', '!', '?', ';', ':'))
            particle_in=(row['id']=='DK4_VOICE_B209_C8_T188' and stop>=2 and words[stop-2:stop]==['come','in'])
            ordinary_report=(row['id']=='DK4_MES_B209_R0027' and pair in [('said','to'),('are','afoot')])
            weak=int(not final and (((word in WEAK and not terminal) and not particle_in and not ordinary_report) or pair in PAIRS))
            tiny=int(final and start>0 and (stop-start==1 or length<=8))
            candidate=((cost[0]+weak,cost[1]+tiny,cost[2]+1,cost[3]+(0 if final else (36-length)**2)),(stop,*breaks))
            if best is None or candidate[0]<best[0]:best=candidate
        return best
    result=solve(0,0)
    if result is None:raise ValueError('No bounded source/prose-preserving plan:'+row['id'])
    lines=[];start=0
    for stop in result[1]:lines.append(' '.join(words[start:stop]));start=stop
    assert ' '.join(lines)==body and len(lines)<=maximum and all(lines)
    markup=prefix+'{LB}'.join(lines)
    profile=replace(get_dialogue_profile('lil-opening-editorial-native-v1'),name='B209-source-bound-layout-RESEARCH-ONLY',max_lines=maximum,leading_speaker_bytes=frozenset([2,11,12,208]))
    # The translator authors one paragraph. Only the formatter supplies these ordinary breaks.
    def formatted(text,p):assert text==row['english'] and p==profile;return markup
    enc=FunctionType(encoder.encode_relocatable_dialogue.__code__,{**encoder.encode_relocatable_dialogue.__globals__,'format_markup':formatted},argdefs=encoder.encode_relocatable_dialogue.__defaults__)
    raw=bytes.fromhex(row['source_hex'])
    if row['kind']!='progressive':raw=bytes([row['source_selector']])+raw
    encoded=enc(raw,row['english'],profile)
    return dict(id=row['id'],source_kind=row['kind'],source_hex=row['source_hex'],English=row['english'],formatted_markup=markup,lines=lines,line_lengths=[len(v) for v in lines],encoded_hex=encoded.encoded.hex(),virtual_typed_selector_removed_when_packed=row['kind']!='progressive',diagnostics=[dict(code=d.code,message=d.message,severity=d.severity) for d in encoded.diagnostics],planning_cost=result[0],max_total_rows=maximum,native_rows_per_page=4,signature_footer_on_separate_automatic_row=signature,all_words_and_punctuation_unchanged=True)
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);results=[];failures=[]
    for row in doc['records']:
        try:results.append(plan(row))
        except (ValueError,AssertionError) as e:failures.append(dict(id=row['id'],error=str(e)))
    ROOT.mkdir(parents=True);save(ROOT/'all20_research_plans_no_word_changes_or_approval.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=results,failures=failures,first_letter_exact_semantic_page_boundary='Tokugawa, / ruler of Japan,',page_boundary_reason='The complete core assertion that these swords are said to be the bane of Tokugawa remains on page1. His entire appositive ruler of Japan begins page2 with the following clause. No title group is split,no new dramatic pause or command is authored,and all182 characters remain. Current actual original button/page behavior still requires proof.',first_letter_wrap_reasons_pending_exact_visual_review=True,exact_report_complement_boundaries_researched=['said/to','are/afoot'],report_boundary_reason='These are normal complete-word wraps between the reporting verb and its to-infinitive complement,and between the copula and afoot. Allowing only these exact source/prose combinations avoids an unnecessary extra short row while preserving the complete clause and all words. No global auxiliary,phrase,glyph,guard,bounds or page exemption.',second_letter_page_boundary='East Asia. / For now,',second_letter_reason='The apparent concealment report completes before the provisional news-passing sentence. Two original four-row native pages are researched without shortening the135-character prose or adding commands.',come_in_particle_boundary_reason='In come in,the final in is a completed phrasal-verb particle;from Yukihisa is the following sender adjunct. Only the exact source-bound style4 introduction receives this grammatical distinction,not a global preposition waiver.',native_phase_reservation_and_two_page_behavior_research_not_release_approved=True,signature_blank_Japanese_row_not_copied_as_authored_spacing=True,no_manual_break_in_editable_prose=True,all_formatting_gates_remain_false=True,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print([(r['id'],r['lines'],r['line_lengths']) for r in results]);print('FAILURES',failures)
    if failures:raise SystemExit(1)
