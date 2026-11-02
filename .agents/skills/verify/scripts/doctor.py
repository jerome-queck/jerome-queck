#!/usr/bin/env python3
"""Read-only source/target readiness, or a local plan that performs no network IO."""
import argparse
import json
import subprocess
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--url', default='https://github.com/jerome-queck')
parser.add_argument('--plan', action='store_true')
args = parser.parse_args()
url = urlparse(args.url)
if url.scheme != 'https' or url.hostname != 'github.com':
    parser.error('Only public HTTPS github.com pages are supported')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
status = subprocess.check_output(['git', 'status', '--porcelain'], text=True)
result = {'source_head': head, 'worktree_status': status, 'target': args.url}
if args.plan:
    result['plan'] = [
        'Install pinned Playwright into a chosen external runtime directory if absent.',
        'Open a fresh anonymous owned browser, GET GitHub target and authored destinations.',
        'Click chapter links and disclosures; capture four viewport/theme variants.',
        'Write evidence only to a new external output directory; close owned browser.',
        'Collector is separate, opt-in, needs gh authentication and writes chosen output.',
        'No git writes, publication, workflows, launch services, or profile changes.',
    ]
else:
    request = urllib.request.Request(args.url, headers={'User-Agent': 'profile-verification'})
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read().decode()
        result.update(status=response.status, final_url=response.url,
                      readme_present='markdown-body' in body)
    if not result['readme_present']:
        raise SystemExit('GitHub responded without a rendered README; do not drive')
result['feature_maps'] = sorted(p.name for p in (Path(__file__).parent.parent / 'features').glob('*.md'))
print(json.dumps(result, indent=2))
