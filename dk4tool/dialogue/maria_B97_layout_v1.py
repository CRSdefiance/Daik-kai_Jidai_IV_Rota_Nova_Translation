"""Maria B97 source-bound logical prose planner;preserve complete words and byte guards.

The historical balanced planner prioritizes row count for fixed padded records.
This opt-in reorders only its cost for this exact relocated batch: weak endings,
tiny final fragments,row count,an intact fitting first sentence,andthen slack. Native metrics,source commands,
four-row limits,macro widths,guard bytes andpair-phase encoding are unchanged.
Strong terminal punctuation permits a complete sentence toend in anobject pronoun.
The exact B183 successor recognizes complete locative over there as a valid boundary. There remains weak elsewhere. No global helper orprevious profile is modified.
"""
import inspect
from pathlib import Path
from types import FunctionType
from dk4tool.dialogue import layout,encoder,qa
from dk4tool.patch.grand_race_menu_release import sha

DEPENDENCIES={
    'dk4tool/dialogue/layout.py':'52a6990d720e944007c3107952be2fd546938404c0c23c89dcf9b0e092d47503',
    'dk4tool/dialogue/encoder.py':'27ea23f5366badc172838ceee98592785d94b3f3b24aadcf0a3af571dfe915da',
    'dk4tool/dialogue/qa.py':'22ff46b7f865f8ba9ce386a88253502cc2d9add06140372354450bbb32c68a5c'}
for path,digest in DEPENDENCIES.items():
    if sha(Path(path).read_bytes())!=digest:raise ValueError('Scoped relocated planner dependency changed:'+path)

STRONG_ENDINGS=frozenset({'a','an','as','at','for','from','in','of','the','to','with','and','or','but','so','that','which','than','because','if','like','by','into','not','i','you','he','she','it','its','we','they','my','your','our','his','her','their','is','are','was','were','be','been','being','can','could','will','would','shall','should','may','might','must','have','has','had',"don't","doesn't","didn't","can't","couldn't","won't","wouldn't","shouldn't","isn't","aren't","wasn't","weren't","i'll","you'll","we'll","they'll","i'm","you're","we're","they're","it's","that's","there's","i've","you've","we've","they've","it'll"})
BASE_WEAK=frozenset({'a','an','as','at','for','from','in','of','the','to','with'})
PROTECTED_BOUNDARIES=frozenset({('sao','jorge'),('great','powers'),('whole','world'),('slave','traders'),('stone','tablet'),('of','conquest'),('put','us'),('out','of'),('of','business'),('all','over'),('over','again'),('equal','terms'),('take','a'),('a','chance'),('make','a'),('a','move'),('what','it'),('it','takes'),('give','up'),('up','on'),('at','least'),('to','blame'),('think','about'),('in','our'),('our','hands')})

def _word(value):
    return value.strip(".,!?;:\"'()[]").casefold()

def _split_pair(labels,index):
    return index+1<len(labels) and (_word(labels[index]),_word(labels[index+1])) in PROTECTED_BOUNDARIES

def _noun_will_at(labels,index):
    # Exact complete first clause: will is a noun, not a stranded auxiliary.
    return (index >= 3 and labels[index].endswith(',')
        and tuple(_word(v) for v in labels[index-3:index+1]) == ('where',"there's",'a','will'))

def _terminal_label(value):
    return value.rstrip("\"')]}").endswith(('.', '!', '?', ';', ':'))

def _complete_locative_at(labels,index):
    # In this exchange over there completes the preceding noun phrase.
    # It is not the existential there of a stranded there is.
    return index>=1 and tuple(_word(v) for v in labels[index-1:index+1])==('over','there')

source=inspect.getsource(layout._balanced_wrap)
old='    weak = {"a", "an", "as", "at", "for", "from", "in", "of", "the", "to", "with"}'
new='    weak = STRONG_ENDINGS'
if source.count(old)!=1:raise ValueError('Scoped planner weak-boundary source differs')
source=source.replace(old,new)
old='''                tail_cost[0] + 1,
                tail_cost[1] + int(not final and end_word in weak),
                tail_cost[2] + int(orphan),'''
new='''                tail_cost[0] + int(not final and ((end_word in weak and not _noun_will_at(labels,end) and not _complete_locative_at(labels,end) and (end_word in BASE_WEAK or not _terminal_label(labels[end]))) or _split_pair(labels,end))),
                tail_cost[1] + int(orphan),
                tail_cost[2] + 1,'''
if source.count(old)!=1:raise ValueError('Scoped planner priority source differs')
source=source.replace(old,new)
old='            orphan = final and start > 0 and len(" ".join(labels[start:end + 1])) <= 8'
new='            orphan = final and start > 0 and (end == start or len(" ".join(labels[start:end + 1])) <= 8)'
if source.count(old)!=1:raise ValueError('Scoped planner final-fragment source differs')
source=source.replace(old,new)
# A complete first sentence that fits the unchanged guarded row wins over
# filling two partial sentence fragments. Row count,weak boundaries and orphans
# retain their higher priorities;all words and native guards remain unchanged.
needle='    count = len(words)'
replacement='''    count = len(words)
    first_sentence_end = next((i for i,v in enumerate(labels) if _terminal_label(v)), None)
    first_sentence_fits = False
    if first_sentence_end is not None and first_sentence_end + 1 < count:
        first_width = sum(widths[:first_sentence_end+1]) + sum(profile.glyph_width(c) for gap in spaces[1:first_sentence_end+1] for c in gap)
        first_reserve = cell if profile.pair_phase_safe_breaks else 0
        first_sentence_fits = first_width + first_reserve <= profile.window_width_px'''
if source.count(needle)!=1:raise ValueError('Scoped first-sentence source differs')
source=source.replace(needle,replacement)
needle='return (0, 0, 0, 0), ()'
if source.count(needle)!=1:raise ValueError('Scoped cost base differs')
source=source.replace(needle,'return (0, 0, 0, 0, 0), ()')
needle='tail_cost[3] + (0 if final else slack * slack),'
replacement='tail_cost[3] + int(first_sentence_fits and start == 0 and end < first_sentence_end),\n                tail_cost[4] + (0 if final else slack * slack),'
if source.count(needle)!=1:raise ValueError('Scoped slack cost differs')
source=source.replace(needle,replacement)

namespace={**layout.__dict__,'STRONG_ENDINGS':STRONG_ENDINGS,'BASE_WEAK':BASE_WEAK,'_terminal_label':_terminal_label,'_split_pair':_split_pair,'_noun_will_at':_noun_will_at,'_complete_locative_at':_complete_locative_at}
exec(compile(source,__file__,'exec'),namespace)
EFFECTIVE_PLANNER_SHA256=sha(source.encode('utf-8'))

def _clone(fn,updates):
    copy=FunctionType(fn.__code__,{**fn.__globals__,**updates},fn.__name__,fn.__defaults__,fn.__closure__)
    copy.__kwdefaults__=fn.__kwdefaults__
    return copy

_wrap=_clone(layout.wrap_tokens,{'_balanced_wrap':namespace['_balanced_wrap']})
_format=_clone(layout.format_markup,{'wrap_tokens':_wrap})
_encode=_clone(encoder.encode_relocatable_dialogue,{'format_markup':_format})

def encode_relocatable_dialogue(source_raw,target_markup,profile):
    expected={'maria-B97-progressive-runtime-bound-v1':(frozenset({3,10,180}),4),'maria-B97-progressive-two-page-runtime-bound-v1':(frozenset({3,10,180}),8),'maria-B97-FE-runtime-bound-v1':(frozenset({254}),4)}
    if (profile.name not in expected or profile.leading_speaker_bytes!=expected[profile.name][0]
        or profile.window_width_px!=216 or profile.max_lines!=expected[profile.name][1] or profile.default_ascii_width!=6 or profile.line_height_px!=16
        or not profile.guard_linebreaks or not profile.pair_phase_safe_breaks or not profile.balanced_wrapping
        or any(profile.macro_ascii_lengths.get(k)!=n for k,n in [('FI',5),('FA',2),('FO',7)])):
        raise ValueError('Relocated planner requires the exact source-bound Maria B97 profile')
    if profile.name=='maria-B97-progressive-two-page-runtime-bound-v1' and sha(source_raw)!='7101280dd916152927a4b57fd35924affa25d3c56b92bc838b0a4f6ce10ec1e0':
        raise ValueError('Two-page encoding requires exact clean B97R72 source')
    # Bind every source prefix to this exact consumer before the shared
    # encoder interprets executable presentation controls.
    if not source_raw or source_raw[0] not in profile.leading_speaker_bytes:
        raise ValueError('Source presentation prefix does not belong to this scoped consumer')
    expected_tag='{SPEAKER:'+format(source_raw[0],'02X')+'}'
    if not target_markup.startswith(expected_tag):
        raise ValueError('Complete source presentation selector is required before prose')
    if any(tag in target_markup for tag in ['{LB','{ALIGN','{PAD']):
        raise ValueError('This source-reviewed batch authors only logical paragraphs;manual layout is forbidden')
    return _encode(source_raw,target_markup,profile)

_audit=_clone(qa.audit_relocatable_dialogue_record,{'encode_relocatable_dialogue':encode_relocatable_dialogue})

def audit_relocatable_dialogue_record(source_raw,target_markup,profile):
    report=_audit(source_raw,target_markup,profile)
    lines=report['visible_lines']
    display=[line.split('>',1)[1] if line.startswith('<SPEAKER') and '>' in line else line for line in lines]
    for index,line in enumerate(display[:-1],start=1):
        words=line.strip().split()
        if not words:continue
        value=words[-1];end=value.strip(".,!?;:\"'").casefold()
        if end in STRONG_ENDINGS and end not in qa.WEAK_LINE_ENDINGS and not _terminal_label(value) and not _noun_will_at(words,len(words)-1) and not _complete_locative_at(words,len(words)-1):
            report['issues'].append(dict(severity='warning',code='weak-line-ending',message=f'line {index} ends with weak wrap word {value!r}'))
        following=display[index].strip().split()
        if following and (_word(value),_word(following[0])) in PROTECTED_BOUNDARIES:
            report['issues'].append(dict(severity='warning',code='split-protected-phrase',message=f'line {index} splits the phrase {value} {following[0]}'))
    if len(display)>1 and len(display[-1].strip().split())==1 and not _terminal_label(display[-2].rstrip()):
        report['issues'].append(dict(severity='warning',code='single-word-final-fragment',message='Final row isolates one word from the preceding unfinished clause'))
    return report
