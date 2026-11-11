"""Find story wrap review leads in the staged four-route archives."""

from collections import Counter
from pathlib import Path
import re

from scripts import replay_historical_story_wraps_20261111 as replay
from scripts import stage_historical_story_wraps_20261111 as stage


base = stage.base
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/current_progressive_wrap_triage_v1.json')
PREFIX = re.compile(rb'\x00\x40\xff\xff\x00')
CONTRACTION = re.compile(r"\b(?:I'm|you're|we're|they're|he's|she's|it's|that's|there's|here's|who's|what's)$", re.I)
TAG = re.compile(r"\b(?:aren't|isn't|wasn't|weren't|don't|doesn't|didn't|haven't|hasn't|won't|wouldn't|can't|couldn't)$", re.I)
PRONOUN_QUESTION = re.compile(r'^(?:you|he|she|it|we|they)\b[^.!?]*\?', re.I)


def scan(path, data):
    blocks = stage.IlnkContainer.parse(data).blocks
    stats = Counter()
    results = []
    for number, block in enumerate(blocks):
        for match in PREFIX.finditer(block):
            offset = match.end()
            if offset >= len(block) or block[offset] >= 207:
                continue
            end = block.find(b'\0',offset+1)
            if end < 0:
                continue
            payload = block[offset+1:end]
            if not payload or any(c!=10 and not 32<=c<127 for c in payload):
                continue
            stats['ascii_body_candidates'] += 1
            rows = [line.strip() for line in payload.decode('ascii').split('\n')]
            if len(rows)<2 or any(not line for line in rows):
                continue
            stats['multiline_body_candidates'] += 1
            reasons = []
            for i,(left,right) in enumerate(zip(rows,rows[1:])):
                if CONTRACTION.search(left):
                    reasons.append(dict(kind='contraction_at_break', after_row=i+1))
                if TAG.search(left) and PRONOUN_QUESTION.search(right):
                    reasons.append(dict(kind='possible_split_question_tag', after_row=i+1))
            first=rows[0]
            if len(first)<=20 and first[-1] not in '.!?:' and not any(t in payload for t in (b'FI',b'FA',b'FO',b'FU')):
                if len(first)+1+len(rows[1].split()[0])<=35:
                    reasons.append(dict(kind='sparse_first_row',after_row=1))
            if reasons:
                results.append(dict(file_path=path,block=number,offset=offset,source_selector=block[offset],
                    block_sha256=stage.sha(block),native_preamble_hex=block[offset-5:offset+1].hex(),
                    stored_body_hex=payload.hex(),rows=rows,findings=reasons))
    return stats,results


def main():
    assert not OUTPUT.exists()
    setup, proof = map(base.load,(replay.SETUP,stage.PROOF))
    assert base.digest(replay.ROM)==setup['candidate_sha256']
    image=base.NdsImage.open(replay.ROM)
    entries, totals = [], {}
    for route in range(4):
        path=f'/data/SC{route}.DK4'
        raw=image.read_file(path)
        assert stage.sha(raw)==proof['archives'][path]['sha256']
        stats,rows=scan(path,raw)
        totals[path]=dict(stats)|dict(flagged_bodies=len(rows),archive_sha256=stage.sha(raw))
        entries.extend(rows)
    by_kind=Counter(reason['kind'] for row in entries for reason in row['findings'])
    base.save(OUTPUT,dict(candidate_sha256=setup['candidate_sha256'],scanned=totals,records=entries,findings_by_kind=dict(by_kind),
        scope='Byte-signature triage of ASCII progressive speech candidates in four story archives. Confirm the typed owner, effective text, original scene and break before judging each lead. This excludes other consumers and makes no exhaustive display claim.',
        new_editorial_credit=0,full_goal_complete=False))
    print(f'{len(entries)} candidate bodies flagged across all four archives: {dict(by_kind)}')


if __name__=='__main__':
    main()
