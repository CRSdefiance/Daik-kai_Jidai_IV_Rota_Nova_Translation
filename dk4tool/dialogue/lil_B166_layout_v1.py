"""Source-bound relocated prose planner;preserve reviewed words and byte guards.

The historical balanced planner prioritizes row count for fixed padded records.
This opt-in reorders only its cost for this exact relocated batch: weak endings,
tiny final fragments,row count,andthen slack. Native metrics,source commands,
four-row limits,macro widths,guard bytes andpair-phase encoding are unchanged.
Strong terminal punctuation permits a complete sentence toend in anobject pronoun.
No global helper orprevious profile is modified.
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

STRONG_ENDINGS=frozenset({
    'am','both',
    'without','there','over','neither','once','on','having','another','even','just','maybe','ever','under',"let's",'who','after','a','an','as','at','for','from','in','of','the','to','with','do','does','did','no','this','these','those','then','why','where','what','when','how',
    'and','or','but','so','that','which','than','because','if','like','by','into','not',
    'i','you','he','she','it','its','we','they','my','your','our','his','her','their',
    'is','are','was','were','be','been','being','can','could','will','would','shall','should','may','might','must','have','has','had',
    "don't","doesn't","didn't","can't","couldn't","won't","wouldn't","shouldn't","isn't","aren't","wasn't","weren't",
    "would've","i'll","you'll","he'll","she'll","we'll","they'll","i'm","you're","we're","they're","it's","that's","there's","i've","you've","we've","they've","i'd","you'd","he'd","she'd","we'd","they'd"})

BASE_WEAK=frozenset({'a','an','as','at','for','from','in','of','the','to','with'})
PROTECTED_BOUNDARIES=frozenset({('nothing','but'),('now','sales'),('make','up'),('get','my'),('my','best'),('best','meal'),('both','do'),('brought','this'),('good','customer'),('taken','over'),('one','problem'),('problem','after'),('after','another'),('run','out'),('fawned','over'),('lost','my'),('my','dignity'),('with','dignity'),('opened','my'),('my','eyes'),('end','up'),("what's","your"),('give','you'),('one','for'),('money','makes'),('bar','snacks'),('below','average'),('big','tip'),('five','times'),('poetry','notes'),('my','money'),('other','girls'),('under','my'),('my','control'),('world','go'),('go','round'),('raise', 'hell'),('pretty', 'well'),('enemy', 'fleet'),('fleet', 'movements'),('one', 'unit'),('lot', 'of'),('final', 'round'),('guiding','staff'),('snow-silk','robe'),('old','maid'),('sharp','tongue'),('cargo', 'hold'),('stone', 'tablet'),('source', 'of'),('of', 'hope'),('gold', 'coins'),("grandson's", 'life'),('nice','work'),('of', 'conquest'),('map', 'keys'),('holy', 'spirit'),('santiago', 'cathedral'),('ancient', 'megalithic'),('civilization', 'research'),('research', 'society'),('new', 'star'),('dead', 'end'),('left', 'hand'),('right', 'hand'),('first', 'mate'),('lucky','charm'),('tomato', 'seedling'),('miracle', 'bullet'),('bullet', 'charm'),('peacock', 'mail'),('ninja', 'garb'),('jaguar', "god's"),("god's", 'vest'),('minerva', 'shield'),("hestia's", 'pot'),('aristarchus', 'telescope'),('cape', 'of'),('of', 'good'),('good', 'hope'),('give', 'back'),('come', 'back'),('get', 'your'),('your', 'hopes'),('hopes', 'up'),('covert', 'operations'),('back', 'to'),('to', 'work'),('silla','gold'),('gold','crown'),('janus','pasar'),('charles','jean'),('jean','rochefort'),('dr','charles'),('yukihisa','genjo'),('genjo','shiraki'),('luo','yuli'),('gunpowder','promptly'),('national','academy'),('of','science'),('settle','down'),('come','along'),('no','time'),('time','like'),('like','the'),('give','up'),('get','married'),('scares','me'),('more','than'),('pretty','good'),('good','pair'),('mivor','genz'),('all','kinds'),('owe','it'),('set','sail'),('coming','from'),('sense','of'),('get','along'),('sweep','her'),('as','long'),('long','as'),('believe','in'),('up','with'),('boxed','in'),('pull','it'),('it','off'),('let','me'),('lets','you'),('meet','you'),('tiny','holland'),('part','of'),('make','me'),('me','sick'),('all','over'),('english','crown'),('spanish','imperial'),('imperial','navy'),('tang','bamboo'),('bamboo','craft'),('bamboo','assembly'),('assembly','plan'),('thank','you'),('next','to'),('pulling','out'),('crush','you'),('more','use'),('silk','road'),('proofs','of'),('social','standing'),('back','home'),('lots','of'),('work','hard'),('scary','dad'),('sounds','like'),('looks','like'),('see','you'),('worry','about'),('how','to'),('want','to'),('pretty','words'),("governor's",'office'),('source','item'),('source','items'),('trade','goods'),('market','share'),('pirate','king'),('ottoman','empire'),('out','of'),('one','step'),('step','ahead'),('thanks','to'),('kind','of'),('antony','kuhn'),('kuhn','company'),('pereira','company'),('southeast','asia'),('mr','kuhn'),('let','go'),('come','in'),('something','else'),('say','something'),('mysterious','woman'),('east','asia'),('sun-crest','sheath'),('ceremonial','knife'),('spice','islands'),('new','world'),('new',"world's"),('hand','them'),('them','over'),('marinus','kuhn'),('james','clifford'),('maria','huamei'),('huamei','li'),('proof','of'),('proofs','of'),('of','supremacy'),('qin','palace'),('palace','lamp')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('evergreen','lotus'),('lotus','leaf'),('kushan','platter'),('indian',"ocean's"),('coastal','dikes'),('pump','out'),('polder','project'),('living','expenses'),('farming','village'),('every','day'),('one','day'),('make','people'),('people','happy')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('nice','timing'),('good','land'),('poor','too'),('call','it'),('make','lives'),('lives','better'),('all','this'),('many','countries'),('grand','house')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('million','gold'),('900,000','gold'),('save','up'),('work','hard'),('wish','you'),('you','well'),('went','all'),('all','over'),('different','people'),('a','tenth'),('polder','soon')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('still',"don't"),('gotta','work'),('working','hard'),("trading's",'my'),('my','specialty'),('only','raised')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('patterned','cloth'),('brass','lamp'),('mediterranean','proof'),('300,000','gold'),('research','funds'),('extra','armor'),('hidden','writing'),('long','shot'),('since','then'),('as','soon'),('soon','as'),('all','right')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('come','on')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('ancient','kingdom'),('kingdom','coin'),('lotion','jar'),('al','ferid'),('ferid','shin'),('guard','you'),('carry','your'),('your','bags'),('run','errands'),('your','wages'),('more','obedient'),('something','special'),('fighting','skills'),('limited','vocabulary'),('have','you'),('with','us')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('closer','look'),('really','is'),('want','a'),('put','my'),('my','life'),('life','on'),('new','guard'),('either','cool'),('such','a'),('us','al')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('get','a'),("man's",'either')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('cool','or')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('small','fry'),('rude','queen'),('no','queen'),('butt','out'),('run','along'),('someone','like'),('like','you'),('of','line'),('camille','overijssel'),('angelo','puccini'),('cute','boys'),('too','nice'),('your','own'),('own','good'),('eye','for'),('for','people'),('a','read'),('read','on'),('on','him'),('little','lady'),('trade','routes'),('contract','fees'),('big','powers'),('big','return'),('tidy','fortune'),('room','to'),('to','grow'),('time','to'),('to','waste'),('putting','you'),('you','to')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('get','called'),('seem','so'),('so','bad'),('nice','for'),('for','your'),('working','with'),('with','you'),('around','the'),('the','ship'),('look','promising'),('plenty','of'),('small','investment'),('back','and'),('and','forth'),('bring','in'),('bigger','holds'),('at','once'),('hard','to'),('to','get'),('make','a'),('a','fortune'),('sail','for'),('for','africa')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES - frozenset({('working','with'),('with','you'),('look','promising'),('room','to')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('this','is'),('one','of'),('cargo','space')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('ian','dukov'),('give','it'),('it','a'),('a','rest'),('give','me'),('leave','a'),('let','you'),('you','go'),('right','up'),('close','to'),('saving','my'),('my','life'),('on','my'),('my','own'),('take','me'),('me','aboard'),('come','with'),('turn-on','')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({("why's",'he')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('mamma','mia'),('beauty','sleep'),('ship','thief'),('early','this'),('this','morning'),('all','by'),('by','himself'),('pretty','bad'),('mixing','it')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({("you're","not")})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('where',"there's"),("there's",'a'),('strawberry','jam'),('jam','jack'),('jack','ludwyan'),('live','large'),('life','is'),('is','short'),('kindhearted','jam'),('picked','her'),('her','up'),('lying','around'),('looking','lonely'),('all','right'),('the','head'),('get','back'),('a','will'),('a','way'),("it's",'all'),('all','good'),('hoping','for'),('what','a'),('out','to'),('to','sea'),('all','weird')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({("how'd",'you'),('going','to'),('to','do'),('come','travel'),('me','introduce')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('cesare','tony'),('contract','towns'),('end','of'),('one','percent'),('five','cargo'),('cargo','holds'),('supply','holds'),('marine','barracks'),('gun','batteries'),('sail','handlers'),('regional','fleets'),('large','ships'),('medium','ships'),('small','ships'),('one','large'),('two','medium'),('picking','a'),('a','fight'),('prepare','for'),('for','departure'),('many','thanks')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('the','earth'),('you','cannot'),('more','sailors'),('for','now'),('no','new')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('julio','erneco'),('good','drink'),('decent','drink'),('good','long'),('long','life'),('young','people'),('some','manners'),('formerly','active'),('active','navigator'),('not','again'),('show','me'),('to','the'),('the','ship'),('give','in'),('calm','down')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('still','an'),('an','active'),('coming','aboard'),('aboard','your'),('your','ship'),('take','him'),('him','aboard')})

PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('manuel','almeida'),('sail','placement'),('extra','sails'),('basic','sail'),('sail','type'),('cannon','type'),('carried','away'),('take','offense'),('first','thing'),('shrug','it'),('it','off'),('still','at'),('at','sea'),('good','care'),('high','speech'),('first',"mate's"),("mate's",'office'),('private','cabin'),('recreation','room'),('lumber','room'),('livestock','room')})

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

source=inspect.getsource(layout._balanced_wrap)
old='    weak = {"a", "an", "as", "at", "for", "from", "in", "of", "the", "to", "with"}'
new='    weak = STRONG_ENDINGS'
if source.count(old)!=1:raise ValueError('Scoped planner weak-boundary source differs')
source=source.replace(old,new)
old='''                tail_cost[0] + 1,
                tail_cost[1] + int(not final and end_word in weak),
                tail_cost[2] + int(orphan),'''
new='''                tail_cost[0] + int(not final and ((end_word in weak and not _noun_will_at(labels,end) and (end_word in BASE_WEAK or not _terminal_label(labels[end]))) or _split_pair(labels,end))),
                tail_cost[1] + int(orphan),
                tail_cost[2] + 1,'''
if source.count(old)!=1:raise ValueError('Scoped planner priority source differs')
source=source.replace(old,new)
old='            orphan = final and start > 0 and len(" ".join(labels[start:end + 1])) <= 8'
new='            orphan = final and start > 0 and (end == start or len(" ".join(labels[start:end + 1])) <= 8)'
if source.count(old)!=1:raise ValueError('Scoped planner final-fragment source differs')
source=source.replace(old,new)
namespace={**layout.__dict__,'STRONG_ENDINGS':STRONG_ENDINGS,'BASE_WEAK':BASE_WEAK,'_terminal_label':_terminal_label,'_split_pair':_split_pair,'_noun_will_at':_noun_will_at}
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
    expected={'lil-B166-progressive-runtime-bound-v1':frozenset({2,9,20,23})}
    if (profile.name not in expected or profile.leading_speaker_bytes!=expected[profile.name]
        or profile.window_width_px!=216 or profile.max_lines!=4 or profile.default_ascii_width!=6 or profile.line_height_px!=16
        or not profile.guard_linebreaks or not profile.pair_phase_safe_breaks or not profile.balanced_wrapping
        or any(profile.macro_ascii_lengths.get(k)!=n for k,n in [('FI',3),('FA',5),('FO',9)])):
        raise ValueError('Relocated planner requires the exact source-bound B166 profile')
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
        if end in STRONG_ENDINGS and end not in qa.WEAK_LINE_ENDINGS and not _terminal_label(value) and not _noun_will_at(words,len(words)-1):
            report['issues'].append(dict(severity='warning',code='weak-line-ending',message=f'line {index} ends with weak wrap word {value!r}'))
        following=display[index].strip().split()
        if following and (_word(value),_word(following[0])) in PROTECTED_BOUNDARIES:
            report['issues'].append(dict(severity='warning',code='split-protected-phrase',message=f'line {index} splits the phrase {value} {following[0]}'))
    if len(display)>1 and len(display[-1].strip().split())==1 and not _terminal_label(display[-2].rstrip()):
        report['issues'].append(dict(severity='warning',code='single-word-final-fragment',message='Final row isolates one word from the preceding unfinished clause'))
    return report
