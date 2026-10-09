#!/usr/bin/env python3
"""Create an honest draft; never overwrite another topic or edit application code."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'platform'))
from topiclib import ROOT, skeleton, write_json

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--id', required=True)
    parser.add_argument('--en', required=True)
    parser.add_argument('--zh', required=True)
    parser.add_argument('--region-en', default='')
    parser.add_argument('--region-zh', default='')
    parser.add_argument('--topics-dir', type=Path, default=ROOT / 'library')
    args = parser.parse_args()
    try:
        manifest, content = skeleton(args.id, args.en, args.zh, args.region_en, args.region_zh)
        destination = args.topics_dir / args.id
        destination.mkdir(parents=True, exist_ok=False)
        (destination / 'figures').mkdir()
        write_json(destination / 'topic.json', manifest)
        write_json(destination / 'content.json', content)
        (destination / 'figures/.gitkeep').write_text('')
        # Every chapter owns its 3D part (standards/library/steps.md ST-7).
        (destination / '3d').mkdir()
        (destination / '3d/README.md').write_text('# 3D\n\nThis chapter\'s 3D part (ST-7). Model mappings start in ../topic.json `viewer`.\n本章的三维部分（ST-7）；模型映射先写在 ../topic.json 的 viewer 中。\n', encoding='utf-8')
        print('Created draft: ' + str(destination))
        print('Fill content.json and model mappings, then validate and build. No course is published yet.')
    except (ValueError, OSError) as exc:
        parser.exit(1, str(exc) + '\n')

if __name__ == '__main__': main()
