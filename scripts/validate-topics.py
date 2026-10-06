#!/usr/bin/env python3
"""Validate mappings and ready-to-publish content without publishing draft material."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'platform'))
from topiclib import ROOT, discover, validate

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--topics-dir', type=Path, default=ROOT / 'topics')
    parser.add_argument('--topic')
    parser.add_argument('--require-published', action='store_true', help='Require completed content and published status')
    args = parser.parse_args()
    bad = False
    try:
        records = [r for r in discover(args.topics_dir) if not args.topic or r[0]['id'] == args.topic]
        if not records: raise ValueError('No matching topic found')
        for manifest, content, path in records:
            errors, missing = validate(manifest, content, path, published_override=args.require_published)
            if args.require_published and manifest['status'] != 'published': errors.append('Topic status is not published')
            print(manifest['id'] + ': ' + ('FAIL' if errors else 'valid ' + manifest['status']) + ', ' + str(len(missing)) + ' pending items')
            for error in errors: print('  ERROR: ' + error)
            bad |= bool(errors)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('Validation failed: ' + str(exc), file=sys.stderr); bad = True
    return 1 if bad else 0

if __name__ == '__main__': sys.exit(main())
