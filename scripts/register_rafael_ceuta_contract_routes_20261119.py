"""Register the Ceuta trading-rights and sea-route lessons after the ordinary replay."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import check_rafael_ceuta_contract_routes_20261119 as game
from scripts import register_rafael_voyage_ceuta_20261119 as parent
from scripts import review_rafael_ceuta_contract_routes_20261119 as staged
from scripts.source_locked_derivation_v5118 import checked_text

base,native,workflow = parent.base,parent.native,parent.workflow
stage = SimpleNamespace(ROOT=staged.STAGED,ROM=staged.ROM,PROOF=staged.PROOF,review=staged,ARM=native.ARM)
PROFILE = 'all-routes-rafael-ceuta-contract-routes-v1-20261119'
ROOT = Path('out/rafael_ceuta_contract_routes_registered_20261119_v1')
ROM = ROOT/'Translation_DS_Rafael_Ceuta_Contract_Routes_20261119_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261119_rafael_ceuta_contract_routes_candidate')
VERIFY,PATCH = PACKAGE/'verification',PACKAGE/'translation.xdelta'
REVIEW,RELEASE = VERIFY/'registered_review.json',VERIFY/'registered_release_verification.json'
DOC = Path('docs/editorial_rafael_ceuta_contract_routes_20261119.md')
STARTUP,QA = game.STARTUP,stage.ROOT/'registered_qa.xml'
verified = SimpleNamespace(PROOF=game.OFFLINE,LIVE=game.PROOF)
CHECKPOINT = 'Rafael’s ordinary Ceuta arrival verified both revised tutorials and the shared docking, Market, Square and Port dialogue.'
ROW_NOTES = {
    'DK4_MES_B45_R0018': 'The opening invitation and the Lisbon conditional have complete clause boundaries.',
    'DK4_MES_B45_R0061': 'The whole reply fits on one line.',
    'DK4_MES_B139_R0005': 'The check-in, explanation and offer each have their own full line.',
    'DK4_MES_B139_R0023': 'The first line reserves the company name width. Lisbon and Ceuta stay together on the second.',
    'DK4_MES_B139_R0027': 'The neighboring towns, the company and the resulting sea route have distinct rows.',
    'DK4_MES_B139_R0039': 'The destination instruction and the crew’s role each fit a full line.',
    'DK4_MES_B139_R0064': 'Julio’s complete observation fits one line.',
    'DK4_MES_B139_R0071': 'Keep the resigned pause, purchase instruction and reassurance readable as three beats.',
    'DK4_MES_B139_R0074': 'The complete equipment reminder fits on one line.',
    'DK4_MES_B139_R0082': 'The inventory instruction stays together before the direct order to head to Lisbon.',
}

verification = checked_text(getsource(parent.verify), {
    "len(layouts['exact_retentions']) == 35": "len(layouts['retentions']) == 19",
    "len(live['panels']) == 44": "len(live['panels']) == 29",
    "assert live['wind_choice_native_result'] == [2,1] and live['unvisited_confident_branch_records'] == ['DK4_MES_B127_R0044']":
        "assert live['shared_and_menu_return_frames_equal'] and live['unvisited'] == ['DK4_MES_B139_R0102']",
    "viewed == {s['path']:s['sha256'] for s in live['sheets']}":
        "viewed == {s['path']:s['sha256'] for s in live['sheets']+layouts['sheets']}",
    '{SC0:[42,127]}': '{SC0:[45,139]}',
    'if x != y] == [42,127]': 'if x != y] == [45,139]',
    'parent.parent.parent.stage.PENDING': 'parent.parent.parent.parent.stage.PENDING',
    "retained = {r['id']:r for r in layouts['exact_retentions']}": "retained = set(layouts['retentions'])",
    "dict(prose=11, wrap=1, retention=35)": "dict(prose=13, retention=19)",
    "live['seen_native_choice_labels']": "[live['menu']]",
    "assert ident in live['unvisited_confident_branch_records'] and ident in retained":
        "assert ident in live['unvisited'] and ident in retained",
    "row['focused_offline_reuse'] = retained[ident]": "row['offline_unchanged_command'] = command",
})

publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index('    DOC.write_text'):publish.index('    prefix =')]
program = checked_text(publish, {
    'len(manifest["batches"]) == 926 and len(manifest["checks"]) == 261':
        'len(manifest["batches"]) == 927 and len(manifest["checks"]) == 262',
    'verified_tavern_lesson_predecessor': 'verified_voyage_ceuta_predecessor',
    'previously_localized_records=47': 'previously_localized_records=32',
    'prose_revisions=11, spacing_revisions=0, wrap_only_revisions=1, justified_retentions=35':
        'prose_revisions=13, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=19',
    'text_display_revisions=12': 'text_display_revisions=13',
    'ordinary_Rafael_voyage_and_Ceuta_wind_choice=True': 'ordinary_Rafael_Ceuta_docking_trade_and_sea_routes=True',
    'rafael_voyage_ceuta': 'rafael_ceuta_contract_routes',
    'Preserve the Rafael Voyage and Ceuta ROM or reconstruction': 'Preserve the Rafael Ceuta Contract and Routes ROM or reconstruction',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael Ceuta trade and sea-route test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised Ceuta trading and sea-route tutorials and earlier candidate fixes.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Rafael's Ceuta trade and sea-route lessons

The two complete exchanges received 32 source-bound decisions. Thirteen revisions clarify the conditional Lisbon sale, the 20 percent market-share notice, and Julio’s instructions for Deck View, Auto Move and the sextant. Both choice captions and 17 other records remain exact with individual reasons. The market-share notice fits on three lines with the usual company name and the tested maximum-width substitutions. [Exact review ledger](../{REVIEW.as_posix()})

The two emulator runs used the same ordinary inputs from Lisbon to Ceuta. The final ROM exercised all 12 trading panels and 17 sea-route panels, including the Yes response, the original company and Rafael substitutions, and the normal Port return. The alternate closing line retains its checked bytes. The six held town dialogue and Trade samples, the choice screen and Port return matched between builds. Eight distinct shared messages were requested, all outside the open 276. [Ordinary replay](../{VERIFY.as_posix()}/native_and_ordinary_gameplay.json)

The clean-input patch reconstructs the candidate exactly. Six startup holds, 24 protected name getters and 49 focused tests passed. Two optional historical fixtures skipped. The ledger remains at 27,700 credited reviews and 276 open shared keys. Hardware testing remains open. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env|globals()
exec(compile(verification,__file__+'::verify','exec'),env)
exec(compile(program,__file__+'::register','exec'),env)


if __name__=='__main__':
    env['main']()
