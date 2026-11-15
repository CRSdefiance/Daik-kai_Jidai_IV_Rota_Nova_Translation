"""Refine record-specific wrap and page boundaries without changing the manuscript."""
import linecache
from pathlib import Path
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B221_B240_v1 import FORMATTING, PREFERENCES, ROOT, planner, qualify_source
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B221_B240_contextual_v1 import digest

PREFS = ROOT / 'ordinary_visual_preferences_v2.json'
PREFER = {
    '221:27': dict(page_clause='There are efforts', line_phrases=['ruler of Japan', 'reached me of'],
                   reason='Keep the Tokugawa identification intact and start page two with the separate report of efforts.'),
    '221:30': dict(page_clause='I thought', line_phrases=['East Asia'],
                   reason='Finish the location report before the closing thought.'),
    '224:54': dict(page_clause="That's the best!", line_phrases=['Changban Bridge', "Cao Cao's army"],
                   reason='Keep both names together and separate the reader’s reaction from the question.'),
    '224:78': dict(page_clause="He's probably", line_phrases=['tear to your eye,', "doesn't it?"],
                   reason='Keep the question tag with the assessment before the separate ranking.'),
    '225:45': dict(page_clause='He shall bear', line_phrases=['king of the sea', 'the gold seal'],
                   reason='Let the next prediction open the second page of the continuing quotation.'),
    '226:38': dict(line_phrases=['spread their faith.', 'one persecution after another'],
                   reason='Keep the missionary purpose and repeated persecution together.'),
    '230:36': dict(QA_line_ending_retention=dict(exact_line="Admiral? What's that look for?",
                   reason='For is part of a complete question here. The question mark closes the thought before the next question.'),
                   reason='Keep the first question intact and preserve the natural break between Ian’s two questions.'),
    '233:49': dict(page_clause='They looted', line_phrases=["weren't they?", 'looted and killed'],
                   reason='Keep the spoken tag together and start the next page with a complete new sentence.'),
    '233:64': dict(page_clause='He never', line_phrases=['terms for peace'],
                   reason='Keep the list of Saladin’s actions together before the closing assessment.'),
    '234:42': dict(page_clause='I feel as though', line_phrases=['spirit of the East'],
                   reason='Separate the general remark from Gerhard’s personal response.'),
    '235:31': dict(page_clause='He built a vast', line_phrases=['Central to Western Asia'],
                   reason='Keep Timur’s lineage account and the extent of his empire in distinct thoughts.'),
    '235:68': dict(page_clause="It's only natural", line_phrases=['for a long time.'],
                   reason='Complete the explanation of the rivalry before Cesare explains Ian’s interest.'),
    '237:28': dict(line_phrases=['Tours and Poitiers', 'Iberian Peninsula'],
                   reason='Keep the paired battle locations and regional name intact.'),
    '238:40': dict(page_clause='They say he once', line_phrases=['nomadic horsemen', 'Roman Empires'],
                   reason='Keep the Huns’ introduction together and begin the next page with the reported threat.'),
    '238:48': dict(page_clause='No one stays', line_phrases=['stays on top forever.'],
                   reason='Keep Manuel’s conclusion intact at the end of the lesson.'),
    '239:16': dict(page_clause="You've got to have", line_phrases=['the nerve to commit.'],
                   reason='Keep the final instruction intact on its own page if a second page is needed.'),
}


def prepare():
    assert not PREFS.exists()
    prefs = load(PREFERENCES)
    rows = {row['id']: row for row in load(FORMATTING)['records']}
    for key, choice in PREFER.items():
        block, record = map(int, key.split(':'))
        ident = f'DK4_MES_B{block}_R{record:04d}'
        row = rows[ident]
        prefs['records'][ident] = {**choice, 'bindings': {
            field: planner.sha(row[field].encode('utf-8'))
            for field in ('source_hex', 'current_hex', 'english')
        }}
    prefs['previous_preferences_sha256'] = digest(PREFERENCES)
    save(PREFS, prefs)


source = checked_text(planner.source, {
    "['DK4_MES_B142_R0159','DK4_MES_B56_R0077']":
        "['DK4_MES_B230_R0036']",
    "result['lines'][0 if row['id']=='DK4_MES_B56_R0077' else 3]":
        "result['lines'][0]",
})
filename = __file__ + '::same-geometry-with-one-complete-question-line-ending'
linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
env = {**planner.env, '__file__': __file__, 'qualify_source': qualify_source}
exec(compile(source, filename, 'exec'), env)

if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        env['main']()

