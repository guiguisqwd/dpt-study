#!/usr/bin/env python3
"""Discover and generate topic pages from data; no per-topic application edits."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'platform'))
from topiclib import ROOT, build

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--topics-dir', type=Path, default=ROOT / 'library')
    parser.add_argument('--output', type=Path, default=ROOT / 'library/shoulder/3d/public')
    args = parser.parse_args()
    try:
        catalog = build(args.topics_dir, args.output)
        print('Built ' + str(len(catalog)) + ' topics to ' + str(args.output))
        for topic in catalog: print('  ' + topic['id'] + ' (' + topic['status'] + ')')
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, str(exc) + '\n')

if __name__ == '__main__': main()
