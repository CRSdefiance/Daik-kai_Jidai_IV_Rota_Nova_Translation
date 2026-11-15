"""Explicit checkpoint continuation of the original static_text stage."""
from scripts.registered_canonical_checkpoint_resume_v1 import run_driver


def main():
    run_driver('static_text', __file__)


if __name__ == '__main__':
    main()
