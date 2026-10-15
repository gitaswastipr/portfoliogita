#!/usr/bin/env python3
"""Refresh public Feeling Rules article previews. Python 3; no dependencies.
Uses the paginated public archive with a public RSS fallback.
RSS coverage may be limited to recent posts; previously saved previews are retained.
The public archive endpoint is unofficial and may change. A failed refresh
leaves the last successful HTML and metadata untouched.
"""
import argparse
import datetime as dt
import html
import email.utils
import shutil
import xml.etree.ElementTree as ET
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request

BASE = 'https://feelingrules.substack.com'
START = '<!-- FEELING_RULES_POSTS_START -->'
END = '<!-- FEELING_RULES_POSTS_END -->'
FEATURED_URL = BASE + '/p/what-love-owes-the-person-who-makes'
FEATURED_EXCERPT = ('In 1938, Aoyama Chizuko arrives in Taiwan as a successful Japanese novelist, '
    'pushing back against the pressure to marry and turning down an offer to write propaganda '
    'for Japan’s expansion southward. Her humor, appetite, and stubborn streak make freedom feel alive.')

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'FeelingRulesPortfolio/1.0'})
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read()

def fetch_archive():
    posts, seen = [], set()
    offset = 0
    while True:
        data = json.loads(get(f'{BASE}/api/v1/archive?sort=new&offset={offset}&limit=50'))
        if not isinstance(data, list):
            raise ValueError('Unexpected archive response; existing previews were preserved.')
        if not data:
            break
        fresh = 0
        for p in data:
            url = p.get('canonical_url')
            if not isinstance(url, str) or not url.startswith(BASE + '/p/'):
                raise ValueError('Unexpected article URL; existing previews were preserved.')
            if url not in seen:
                fresh += 1
                seen.add(url)
                posts.append(p)
        if not fresh:
            raise ValueError('Archive pagination repeated; refusing an incomplete refresh.')
        offset += len(data)
    if not posts:
        raise ValueError('Empty archive; existing previews were preserved.')
    return sorted(posts, key=lambda p: p.get('post_date', ''), reverse=True)

def fetch_rss():
    xml = ET.fromstring(get(BASE + '/feed'))
    posts = []
    for item in xml.findall('./channel/item'):
        url = item.findtext('link') or ''
        if not url.startswith(BASE + '/p/'):
            continue
        enclosure = item.find('enclosure')
        date = email.utils.parsedate_to_datetime(item.findtext('pubDate')).isoformat()
        subtitle = html.unescape(item.findtext('description') or '')
        # RSS descriptions can contain markup. Plain text keeps previews safe.
        subtitle = re.sub(r'<[^>]*>', '', subtitle).strip()
        posts.append({
            'canonical_url': url, 'title': item.findtext('title') or 'Untitled',
            'subtitle': subtitle, 'post_date': date,
            'slug': url.rsplit('/', 1)[-1],
            'cover_image': enclosure.get('url') if enclosure is not None else None,
        })
    if not posts:
        raise ValueError('Public RSS feed returned no articles; saved previews retained.')
    return posts

def fetch_all():
    try:
        return fetch_archive()
    except Exception as archive_error:
        print(f'Archive unavailable ({archive_error}). Trying the public RSS feed.')
    posts = fetch_rss()
    print('Using recent RSS posts; previously saved previews are retained. '
          'Older articles never imported may need a manual archive backfill.')
    return posts

def load_cached(root):
    source_root = Path(__file__).resolve().parents[1]
    for path in [root / 'feeling-rules-posts.json', source_root / 'feeling-rules-posts.json']:
        if path.exists():
            data = json.loads(path.read_text(encoding='utf-8'))
            if not isinstance(data, list):
                raise ValueError('Unexpected saved article list')
            return data
    return []

def repair_images(root, saved):
    """Recover supplied images uploaded at the repo root, even offline."""
    source_root = Path(__file__).resolve().parents[1]
    for post in saved:
        relative = post.get('image', '')
        if not relative or not relative.startswith('assets/feeling-rules/'):
            continue
        target = (root / relative).resolve()
        if not target.is_relative_to(root):
            raise ValueError('Unsafe image path')
        if target.exists():
            continue
        candidates = [source_root / relative, source_root / Path(relative).name,
                      root / Path(relative).name]
        for source in candidates:
            if source.is_file():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
                print(f'Restored article image: {relative}')
                break

def normalize(p, root):
    url = p['canonical_url']
    date = dt.datetime.fromisoformat(p['post_date'].replace('Z', '+00:00'))
    slug = p.get('slug') or url.rsplit('/', 1)[-1]
    if not re.fullmatch(r'[a-zA-Z0-9-]+', slug):
        raise ValueError('Invalid post slug')
    image = p.get('cover_image')
    local_image = ''
    if image:
        parsed = urllib.parse.urlparse(image)
        if parsed.scheme != 'https' or parsed.hostname not in ('substackcdn.com', 'substack-post-media.s3.amazonaws.com'):
            raise ValueError('Unexpected image host')
        local_image = f'assets/feeling-rules/{slug}.jpg'
        path = root / local_image
        if not path.exists():
            try:
                content = get(image)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            except Exception as error:
                print(f'Cover unavailable for {slug}: {error}')
                local_image = ''
    return {
        'url': url, 'title': p['title'], 'subtitle': html.unescape(p.get('subtitle') or ''),
        'date': date.date().isoformat(), 'date_label': date.strftime('%d %B %Y').lstrip('0'),
        'image': local_image,
        'excerpt': FEATURED_EXCERPT if url == FEATURED_URL else '',
    }

def render(p, i):
    e = lambda value: html.escape(value, quote=True)
    image = ''
    if p['image']:
        image = f'<div class="fr-post-image"><img src="{e(p["image"])}" alt="" width="1200" height="800" loading="lazy"></div>'
    label = 'Featured essay' if p['url'] == FEATURED_URL else 'Feeling Rules'
    excerpt = f'<p class="fr-excerpt">{e(p["excerpt"])}</p>' if p['excerpt'] else ''
    credit = '<p class="fr-credit">Photo by <a href="https://www.pexels.com/photo/iced-coffee-and-tea-cup-on-wooden-table-33409494/" target="_blank" rel="noopener noreferrer">Nguyễn Tiến Thịnh</a></p>' if p['url'] == FEATURED_URL and p['image'] else ''
    title_id = f'fr-post-{i}'
    return f'''<article class="fr-post" aria-labelledby="{title_id}">
          {image}
          <div class="fr-post-body">
            <p class="fr-post-meta">{label} <span aria-hidden="true">·</span> <time datetime="{p['date']}">{e(p['date_label'])}</time></p>
            <h3 id="{title_id}"><a href="{e(p['url'])}" target="_blank" rel="noopener noreferrer">{e(p['title'])}</a></h3>
            <p class="fr-subtitle">{e(p['subtitle'])}</p>
            {excerpt}
            {credit}
            <a class="fr-read" href="{e(p['url'])}" target="_blank" rel="noopener noreferrer" aria-label="{e('Continue reading ' + p['title'] + ' on Substack (opens in a new tab)')}">Continue reading <span aria-hidden="true">↗</span></a>
          </div>
        </article>'''

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    path = root / 'index.html'
    saved = load_cached(root)
    repair_images(root, saved)
    source = path.read_text(encoding='utf-8')
    if source.count(START) != 1 or source.count(END) != 1:
        raise ValueError('Expected one article region. Existing HTML was preserved.')
    incoming = [normalize(p, root) for p in fetch_all()]
    merged = {p['url']: p for p in saved}
    for post in incoming:
        old = merged.get(post['url'], {})
        if not post.get('image') and old.get('image') and (root / old['image']).exists():
            post['image'] = old['image']
        merged[post['url']] = post
    posts = sorted(merged.values(), key=lambda p: p.get('date', ''), reverse=True)
    region = '\n        ' + '\n        '.join(render(p, i) for i, p in enumerate(posts)) + '\n        '
    before, rest = source.split(START)
    _, after = rest.split(END)
    changed = before + START + region + END + after
    temp = path.with_suffix('.html.tmp')
    temp.write_text(changed, encoding='utf-8')
    temp.replace(path)
    (root / 'feeling-rules-posts.json').write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Updated {len(posts)} public article preview(s). Existing portfolio sections preserved.')

if __name__ == '__main__':
    main()
