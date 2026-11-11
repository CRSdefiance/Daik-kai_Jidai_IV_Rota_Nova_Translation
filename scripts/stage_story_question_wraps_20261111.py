"""Review the ten detected question breaks against their complete original exchanges."""

from collections import defaultdict
from inspect import getsource
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageDraw

from scripts import register_historical_story_wraps_20261111 as parent
from scripts import scan_current_progressive_wrap_leads_20261111 as triage
from scripts import stage_historical_story_wraps_20261111 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, IlnkContainer = prior.base, prior.sha, prior.IlnkContainer
CLEAN, ARM = prior.CLEAN, prior.ARM
ROOT = Path('work/story_question_wraps_20261111_v2')
REVIEW = triage.OUTPUT.with_name('story_question_wraps_context_v2.json')
PREVIOUS = triage.OUTPUT.with_name('story_question_wraps_context_v1.json')
PROOF = ROOT/'stored_and_native.json'

# Preferences describe phrases that should stay intact. The previous formatter picks the breaks.
DECISIONS = {
    (0,103,53): ('Rafael', 'Rafael says western New World is too broad and asks Samwell for a more specific location for the vest.',
        'The brisk question fits Rafael’s practical follow-up after Samwell gives him only a region. Keep the full question together.',
        None, ("Can't you narrow it down?",)),
    (0,152,57): ('Rafael', 'Rafael asks Duarte Pereira whether the two Portuguese companies can compete fairly.',
        'Keep his restrained appeal to shared nationality and fair competition. Pereira’s contemptuous reply immediately undercuts it.',
        None, ("can't we compete fairly?",)),
    (0,255,23): ('Margrete', 'Margrete asks whether imagining the river carrying gold dust sounds romantic.',
        'The short invitation to picture the scene follows a sailor’s hearsay. The full rhetorical question preserves her wistful voice.',
        None, ("Doesn't it sound romantic?",)),
    (0,296,52): ('Claudio', 'Claudio asks why the people who are to gather for the ritual have not already found the thing hidden in the ruins.',
        '“Yet” gives the same time reference in Claudio’s brisk skeptical reply and lets the question read as one unit.',
        "Then why haven't they found it yet?", ("why haven't they", 'found it yet?')),
    (1,148,37): ('Charles', 'Charles proposes soaking the Ancient Kingdom Coin in the Lotion Jar.',
        'His tentative lead-in and “Could we” preserve the cautious proposal, keeping the coin action and established item name together before Hodram raises the risk.',
        'I was thinking... Could we soak it in the Lotion Jar?', ('Could we', 'soak it', 'the Lotion Jar')),
    (2,26,83): ('Lil', 'Lil asks whether the apparent stranger is new in town and reports a rumor about James Clifford, a terrifying pirate who can silence crying children.',
        'The quick question and escalating exaggeration lead into the monster story and Clifford’s reveal. The revised American English keeps the entire tag, the pirate identity and the rumor’s exaggeration.',
        "Your first time here, right? They say James Clifford's a pirate so fearsome even crying children go quiet at his name.",
        ('Your first time here, right?', "They say James Clifford's", 'a pirate', 'so fearsome', 'crying children', 'go quiet at his name')),
    (2,26,497): ('James Clifford', 'Clifford proposes that he and Lil join forces after admitting that the opposing commander is formidable.',
        'Keep his abrupt turn from concern to an invitation. The separate question gives Lil room to react with surprise.',
        None, ("Why don't you join forces with me?",)),
    (2,146,5): ('Lil', 'Lil asks whether Camille has returned when she cannot find him.',
        'Keep the two quick questions and Camille’s approved name. The sailor’s answer confirms the two are separated.',
        None, ("Hasn't he come back?",)),
    (2,243,22): ('Margrete', 'Margrete finds the imagined gold-bearing river romantic and asks Lil to agree.',
        'The wistful fragment and rhetorical question follow the sailor’s story. Preserve both, keeping the full question together.',
        None, ("Doesn't it sound romantic?",)),
    (3,216,21): ('Margrete', 'Margrete asks Maria whether just imagining the river carrying gold dust is romantic.',
        'The invitation to imagine it and the full rhetorical question preserve the soft end of her account.',
        None, ("Doesn't it sound romantic?",)),
}


def bind_groups(ctx, clean, queue):
    selected=defaultdict(list)
    for row in queue['records']:
        if any(f['kind']=='possible_split_question_tag' for f in row['findings']):
            selected[row['file_path'],row['block']].append(row)
    inventory,_,_=prior.scoped_inventory()
    groups={}
    for (path,block), leads in selected.items():
        source,current=[IlnkContainer.parse(im.read_file(path)).blocks[block] for im in (clean,ctx.image)]
        assert {r['block_sha256'] for r in leads}=={sha(current)}
        (original,clean_rows),(commands,current_rows)=[prior.raw_speeches(arm,blob,inventory)
            for arm,blob in ((clean.read_file(ARM),source),(ctx.arm,current))]
        assert [r['word'] for r in original]==[r['word'] for r in commands]
        assert [r['complete_preamble_hex'] for r in clean_rows]==[r['complete_preamble_hex'] for r in current_rows]
        matches=[]
        for lead in leads:
            index=next(i for i,row in enumerate(current_rows) if row['offset']==lead['offset'])
            ja,at=clean_rows[index],current_rows[index]
            assert at['raw_hex'][2:]==lead['stored_body_hex'] and at['selector']==lead['source_selector']
            ident=f"DK4_MES_B{block}_R{ja['record_index']:04d}"
            matches.append(dict(id=ident,source_reference=ja,current_reference=at))
        groups[path,block]=source,current,commands,clean_rows,current_rows,matches
    assert len(groups)==9
    return groups


def retained_hodram_version(ctx,clean):
    path,block='/data/SC1.DK4',244
    inventory,_,_=prior.scoped_inventory()
    a,b=[IlnkContainer.parse(im.read_file(path)).blocks[block] for im in (clean,ctx.image)]
    _,source=prior.raw_speeches(clean.read_file(ARM),a,inventory)
    _,current=prior.raw_speeches(ctx.arm,b,inventory)
    assert len(source)==len(current)==5 and source[-1]['selector']==current[-1]['selector']==188
    value=bytes.fromhex(current[-1]['raw_hex'])[1:].decode('ascii')
    assert value=="Doesn't it sound romantic, just\n picturing it? "
    return dict(file_path=path,block=block,source_block_sha256=sha(a),current_block_sha256=sha(b),
        source_reference=source[-1],current_reference=current[-1],current_English=value,
        source_Japanese=bytes.fromhex(source[-1]['raw_hex'])[1:].decode('cp932'),decision='retention',
        rationale='The question already keeps the auxiliary and subject together. The continuation reads as a reflective afterthought.')


def native_validation(ctx, records):
    render=FunctionType(prior.native_validation.__code__,vars(prior)|dict(PREVIOUS=PREVIOUS))
    return render(ctx,records)


def plan_record(row):
    if row['source_selector'] != 0:
        return PLANNER(row)
    # The original 00 is part of the six-byte preamble. Format the printable
    # body through the same encoder, then restore that native selector.
    assert row['source_hex'].startswith('00') and row['current_hex'].startswith('00')
    assert row['source_reference']['complete_preamble_hex']=='0040ffff0000'
    assert row['current_reference']['complete_preamble_hex']=='0040ffff0000'
    virtual=row | dict(source_selector=2,source_hex='02'+row['source_hex'][2:],
        english=row['english'].replace('{SPEAKER:00}','{SPEAKER:02}',1))
    result=PLANNER(virtual)
    assert result['encoded_hex'].startswith('02')
    return result | dict(source_hex=row['source_hex'],English=row['english'],encoded_hex='00'+result['encoded_hex'][2:],
        formatted_markup=result['formatted_markup'].replace('{SPEAKER:02}','{SPEAKER:00}',1),original_00_selector_preserved=True)


PLANNER=prior.bind_planner()


def main():
    assert not ROOT.exists() and not REVIEW.exists()
    release=base.load(parent.RELEASE)
    ctx=prior.RegisteredRuntime(parent.RELEASE,release['own_registered_startup'],captain=3)
    queue=base.load(triage.OUTPUT)
    assert queue['candidate_sha256']==release['candidate_sha256'] and base.digest(CLEAN)==release['clean_input_sha256']
    clean=base.NdsImage.open(CLEAN)
    groups=bind_groups(ctx,clean,queue)
    compiler=checked_text(getsource(prior.compile_records), {"b'\\0' not in target,": "b'\\0' not in target[1:],"})
    env=vars(prior)|dict(DECISIONS=DECISIONS)
    exec(compile(compiler,__file__+'::native-selector-separated-from-body','exec'),env)
    contexts,records=env['compile_records'](groups,plan_record)
    assert len(records)==10
    for row in records:
        row['question_type']='tag' if row['id']=='DK4_MES_B26_R0083' else 'interrogative with negative auxiliary'
        print(row['file_path'],row['id'],row['automatic_layout']['lines'],row['trailing_blank_bytes'],flush=True)
    pictures=native_validation(ctx,records)
    retained=retained_hodram_version(ctx,clean)
    ROOT.mkdir()
    paths={}
    for name,raw in prior.transform(ctx.image,records):
        path=ROOT/Path(name).name; path.write_bytes(raw)
        paths[name]=dict(path=path.as_posix(),sha256=sha(raw),source_sha256=sha(ctx.image.read_file(name)))
    sheets=[]; colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
    for start in range(0,len(pictures),8):
        subset=pictures[start:start+8]
        sheet=Image.new('RGB',(888,(len(subset)//2)*154),'#263238'); draw=ImageDraw.Draw(sheet)
        for index,(title,pixels) in enumerate(subset):
            x,y=index%2*444,index//2*154
            draw.text((x+4,y+2),title,fill='white')
            plane=Image.new('RGB',(216,64)); plane.putdata([colors[v] for v in pixels])
            sheet.paste(plane.resize((432,128),Image.Resampling.NEAREST),(x+4,y+21))
        path=ROOT/f'before_after_{len(sheets)+1}.png'; sheet.save(path)
        sheets.append(dict(path=path.as_posix(),sha256=base.digest(path)))
    base.save(REVIEW,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],candidate_sha256=release['candidate_sha256'],
        records=records,retained_unflagged_parallel_record=retained,complete_exchange_references=contexts,
        zero_new_credit=True,full_goal_complete=False))
    base.save(PROOF,dict(candidate_sha256=release['candidate_sha256'],review_sha256=base.digest(REVIEW),archives=paths,sheets=sheets,
        blocks=[list(key) for key in groups],unchanged_terminators_offsets_block_extents_and_unowned_bytes=True,
        archive_inverses_exact=True,checked_complete_native_pages=20,checked_original_processor_alignments=80,
        exact_previous_proof_source=PREVIOUS.as_posix(),exact_previous_proof_sha256=base.digest(PREVIOUS)))


if __name__=='__main__':
    main()
