"""Record complete conversational reviews and prepare the remaining SC0 comparisons."""
from pathlib import Path
import inspect
import re
from struct import unpack_from

from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_rafael4347_registered_v1 import CANDIDATE, LEDGER, NEXT, PACKAGE, REGISTRY, RELEASE, ROOT
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.checkpoint_rafael_B301_B320_contextual_v1 import read_decisions as read_previous
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.seal_rafael_B321_B342_clean_v1 import BLOCKS, SEALED
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import write_rafael_B281_B300_contextual_v1 as previous


INPUTS = (
    SEALED / 'sealed_drafts.json', ROOT / 'current_v1/current_effective.json',
    ROOT / 'objects_v1/current_objects.json', ROOT / 'names_and_terms_v1.json', ROOT / 'roles.json',
)
DECISIONS = Path('translations/rafael_B321_B331_contextual_decisions_v1.txt')
OUT = ROOT / 'B321_B331_contextual_review_v1.json'
LABELS = ROOT / 'scoped_name_decisions_v1.json'
TERMS = ROOT / 'scoped_catalogue_terms_v1.json'
REVIEWED = {321, 322, 323, 326, 328, 330, 331}
NAME_RETENTIONS = {
    0: 'Use approved Rafael Castor in both name consumers. Keep the source runtime substitution where he is addressed.',
    2: 'Lil Argot is the established speaker who recognizes the book before Charles responds.',
    5: 'Keep Claudio Manaus in both consumers. His challenges and aside in the cliff and warrior scenes need no added rank.',
    8: 'Keep Arcadius Eudoxios in dialogue and the source middle name Eirene in the full catalogue.',
    18: 'Keep Charles Rochefort in dialogue and the source middle name Jean in the full catalogue. The crew addresses him as Charles.',
    94: 'Barkeep fits the tavernkeeper who helps himself to a taste. Japan is location metadata.',
    102: 'Patron fits the customer who joins the barkeep in tasting the wine.',
    147: 'Guildmaster identifies the contact who introduces Rafael to the villager without inventing a title for that visitor.',
    151: 'Keep Sailor in dialogue and Retainer for the broader catalogue class. A startup fallback does not establish the actual event roster.',
    161: 'Villager fits the resident who asks about Portugal and the sextant without assigning him a rank.',
    179: 'Villager fits the source label in both the warrior trial and the account of the monk. The training role is expressed through dialogue.',
    201: 'Retain the established Mihwa spelling used for this actor in the linked Julian and crown exchanges.',
    203: 'Keep Sakura in both consumers, consistent with her earlier map exchange and these three visits.',
    204: 'Keep Verisa in both consumers. Her reading and pirate warning establish her activity without changing her nameplate into a job label.',
    205: 'Keep Silvia in both consumers. The map rumor supplies no separate title.',
    206: 'Keep Isabel in both consumers. The story she heard about the monk adds no title or relationship.',
}


def catalogue(runtime):
    ctx = RegisteredRuntime(runtime['release_proof'], runtime['startup_proof'], captain=0)
    assert ctx.receipt() == runtime
    clean_path = Path('work/clean.nds')
    assert digest(clean_path) == ctx.release['clean_input_sha256']
    clean = NdsImage.open(clean_path).read_file('/__arm9__.bin')
    specs = (
        ('commodity', 54, 1438112, 'サラサ', 'Chintz'),
        ('item', 13, 1172296, '錬金術の書', 'Alchemy Book'),
        ('item', 43, 1173016, 'トラロックのナイフ', 'Tlaloc Knife'),
        ('item', 125, 1174984, '六分儀', 'Sextant'),
        ('item', 145, 1175464, '高麗青磁の香炉', 'Goryeo Incense Burner'),
        ('item', 172, 1176112, '古代都市遺跡への地図', 'Ancient City Map'),
    )
    base = 0x02000000
    terms = []
    for kind, ident, field, japanese, english in specs:
        source_pointer, = unpack_from('<I', clean, field)
        source_offset = source_pointer - base
        source = clean[source_offset:clean.index(0, source_offset)]
        pointer, = unpack_from('<I', ctx.arm, field)
        section, = [part for part in ctx.sections if part.ramAddress <= pointer < part.ramAddress + len(part.data)]
        offset = pointer - section.ramAddress
        data = bytes(section.data)
        text = data[offset:data.index(0, offset)]
        assert source.decode('cp932') == japanese and text.decode('cp932') == english
        if pointer == 0x02387BAC:
            assert ctx.raw[pointer-base:pointer-base+len(text)+1] == text + b'\0'
        terms.append(dict(kind=kind, index=ident, file_path='/__arm9__.bin', pointer_field_offset=field,
                          clean=dict(pointer=source_pointer, offset=source_offset, hex=source.hex(), text=japanese),
                          current=dict(pointer=pointer, section_address=section.ramAddress,
                                       section_offset=offset, hex=text.hex(), text=english)))
    return dict(terms=terms, runtime=runtime, clean_ROM_sha256=digest(clean_path), new_credit=0)


record_code = previous.record_source.split('    if ident in PUNCTUATION:', 1)[0] + '''    wide_letters = re.findall(r'[Ａ-Ｚａ-ｚ]', previous)
    if wide_letters:
        assert not retained
        row['current_fullwidth_latin_corrected'] = wide_letters
    return row
'''
name_code = checked_text(previous.name_source, {'RAFAEL281_300_NAME_': 'RAFAEL321_342_NAME_'})
namespace = {**previous.env, **globals(), 'NAME_REVISIONS': {}, 'FE': {}}
exec(compile(record_code + '\n' + name_code, __file__ + '::exact-current-and-source-context', 'exec'), namespace)
decision_source = inspect.getsource(read_previous)
exec(compile(decision_source, __file__ + '::same-explicit-decision-reader', 'exec'), globals())


def main():
    assert not any(path.exists() for path in (OUT, LABELS, TERMS))
    draft, current, objects, identity, role_report = map(load, INPUTS)
    runtime = current['runtime']
    assert all(report['runtime'] == runtime for report in (objects, identity, role_report))
    assert current['current_ROM_sha256'] == runtime['candidate_sha256'] == load(RELEASE)['candidate_sha256']
    assert [group['block'] for group in current['groups']] == draft['complete_blocks'] == BLOCKS
    assert all(digest(path) == checksum for path, checksum in draft['evidence'].items())
    ordinary = [row for group in current['groups'] for row in group['records']]
    styles, choices = objects['style_records'], objects['choice_records']
    assert (len(ordinary), len(styles), len(choices), objects['native_style_getter_cases']) == (242, 298, 16, 384)
    bound = {row['id']: row for row in ordinary + styles + choices}
    assert len(bound) == 556 and bound.keys() == {row['id'] for row in draft['records']}
    selected = [row for row in draft['records'] if row['block'] in REVIEWED]
    decisions = read_decisions([DECISIONS])
    assert decisions.keys() == {row['id'] for row in selected} and len(selected) == 65
    roles = {row['source_selector']: row for row in role_report['native_roles']['rows']}
    names = {row['actor_ID']: namespace['name_review'](row) for row in identity['name_bindings']}
    assert names.keys() == NAME_RETENTIONS.keys()
    rows = [namespace['review_record'](row, bound[row['id']], decisions[row['id']], names, roles, {}) for row in selected]
    assert all(all(row['review'][gate] == (gate != 'formatting') for gate in row['review']) for row in rows)
    assert {row['id'] for row in rows if row.get('current_fullwidth_latin_corrected')} == {
        'DK4_MES_B321_R0006', 'DK4_MES_B328_R0006',
    }
    for row in rows:
        if row['block'] == 323:
            row['context'] = row['context'].replace('Two patrons help themselves', 'The barkeep and a patron help themselves')
            row['source_meaning'] = row['source_meaning'].replace('first patron', 'barkeep').replace('second patron', 'patron')
    terms = catalogue(runtime)
    save(TERMS, terms)
    evidence = {str(path): digest(path) for path in (*INPUTS, DECISIONS, RELEASE, TERMS, Path(__file__))}
    save(LABELS, dict(records=list(names.values()), runtime=runtime, new_credit=0, evidence=evidence,
                      scoped_names_only=True, formatting_and_visual_review_pending=True))
    revisions = sum(row['decision'] == 'revision' for row in rows)
    retained = len(rows) - revisions
    save(OUT, dict(format='dk4-partial-contextual-editorial-review-v1', translation_policy='natural-dialogue-v2',
                   target_locale='en-US', runtime=runtime, records=rows, complete_blocks=sorted(REVIEWED),
                   records_count=len(rows), revisions=revisions, retentions=retained,
                   current_bindings_count=len(bound), remaining_current_comparisons=491, new_credit=0,
                   all_four_prose_gates_pass=True, formatting_pending=True,
                   evidence={**evidence, str(LABELS): digest(LABELS)}))
    release, ledger, package = map(load, (RELEASE, LEDGER, PACKAGE))
    assert ledger[NEXT]['independently_drafted_records'] == 42 and ledger[NEXT]['new_credit'] == 0
    summary = (f'All 556 clean-source drafts for Rafael B321–B342 are sealed and bound to Rafael4347. '
               f'Seven complete conversations have contextual decisions, with {revisions} revisions and {retained} retentions. '
               'The other 491 comparisons and fresh display checks remain. Integrated coverage is 16,192.')
    doc = f"""# Rafael B321–B342 source and comparison checkpoint

{summary}

The clean-first seal preserves all 42 earlier Sakura drafts and adds 514 drafts across the expedition, fortune-telling, warrior training, village and alchemy exchanges. It covers 242 ordinary records, 298 alternate voices and 16 captions. The current binder verified all 384 native style slots. The separate label-free control remains outside the dialogue count. {link('Sealed clean drafts', INPUTS[0])}. {link('Current speech', INPUTS[1])}. {link('Current alternate voices and captions', INPUTS[2])}.

The first 65 contextual decisions cover Sakura’s three visits, Mihwa’s gate hint, Silvia’s map rumor and Verisa’s two visits. The barkeep and a patron take the wine. Three full-width I characters in two records have proposed ASCII replacements. The catalog confirms Chintz, Alchemy Book, Tlaloc Knife, Sextant, Goryeo Incense Burner and Ancient City Map. Sixteen scoped name decisions are recorded, including Barkeep, Patron and the two distinct Villager actors. Role checks use the registered startup and do not establish the actual event roster. {link('Exact contextual decisions', OUT)}. {link('Catalogue terms', TERMS)}. {link('Scoped names', LABELS)}.

Compare the remaining complete exchanges, starting with B324 and B325, then complete display, representative gameplay and registration checks. No new completion credit was added.
"""
    checkpoint(
        mutation=ROOT/'B321_B331_contextual_checkpoint_v1', batch_key=NEXT,
        batch_updates=dict(new_credit=0, independently_drafted_records=556, independent_draft_blocks=BLOCKS,
                           remaining_clean_meanings_anddrafts=0, current_bindings_count=556, contextual_records=65,
                           remaining_current_comparisons=491, contextual_blocks=sorted(REVIEWED),
                           contextual_review=str(OUT), contextual_review_sha256=digest(OUT),
                           proposed_revisions=revisions, justified_retentions=retained,
                           exact_style_alias_checks=384, scoped_name_decisions=len(names)),
        summary=summary, document='docs/editorial_Rafael_B321_B342_contextual_20261106.md',
        document_text=doc, completed=16192, protected={
            str(REGISTRY): release['registry_sha256'], release['canonical_base']: release['canonical_sha256'],
            str(CANDIDATE): release['candidate_sha256'], release['patch']: release['patch_sha256'],
            package['zip']: package['zip_sha256'],
        },
    )
    print(f'Checked 65 exact contextual decisions ({revisions} revisions, {retained} retentions). All 556 drafts are sealed and bound.')


if __name__ == '__main__':
    main()
