"""Successor creates the record directory before the frozen queue producer.

The first attempt failed before writing a receipt or appending any command.
"""
from scripts import queue_duel_special_observation_v1229 as previous


if __name__ == '__main__':
    previous.ROOT.mkdir(parents=True, exist_ok=True)
    previous.main()
