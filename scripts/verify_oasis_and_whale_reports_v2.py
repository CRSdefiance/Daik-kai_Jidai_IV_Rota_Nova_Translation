"""Verify the sailing return before the next native port-sighting report."""

from inspect import getsource
from pathlib import Path

from scripts import verify_oasis_and_whale_reports_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text


def verify_gameplay():
    source = checked_text(getsource(prior.verify_gameplay), {
        "            assert not visible_paper(frames[end]['path'])":
            "            return_frame = 12000\n"
            "            old_frames = {row['frame']: row for row in old_report['frames_captured']\n"
            "                          if row['path'].endswith('_navigation.png')}\n"
            "            assert not visible_paper(frames[return_frame]['path'])\n"
            "            assert text(snapshot(end), owner + 0x2030) == b\"Admiral, we've spotted a port!\"\n"
            "            for boundary in (return_frame, end):\n"
            "                assert city.captured(frames[boundary]).tobytes() == city.captured(old_frames[boundary]).tobytes()",
        'original_return=frames[end])': 'original_return=frames[return_frame], next_port_report=frames[end])',
        'inputs = [], {}, [PROOF, VISUAL, BOOT, QA, Path(__file__)]':
            'inputs = [], {}, [PROOF, VISUAL, BOOT, QA, Path(__file__), Path(prior.__file__)]',
    })
    environment = vars(prior) | {'__file__': __file__, 'prior': prior, 'Path': Path}
    exec(compile(source, __file__ + '::sailing-return', 'exec'), environment)
    environment['verify_gameplay']()


if __name__ == '__main__':
    verify_gameplay()
