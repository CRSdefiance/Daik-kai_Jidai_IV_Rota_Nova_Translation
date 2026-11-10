"""Explicit checkpoint continuation of the original owned_names stage."""
from scripts.registered_canonical_checkpoint_resume_v1 import run_driver


def main():
    run_driver('owned_names', __file__)


if __name__ == '__main__':
    main()
