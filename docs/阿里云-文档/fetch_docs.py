import requests, re, json

url = 'https://help.aliyun.com/zh/model-studio/model-user-guide/'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
text = r.text

# Try different patterns
patterns = [
    r'window\.__ICE_PAGE_PROPS__\s*=\s*(\{.*?\});',
    r'__ICE_PAGE_PROPS__\s*=\s*(\{.*?\})\s*</script>',
    r'__ICE_PAGE_PROPS__["\']?\s*[:=]\s*(\{.*?\})\s*[;<]',
]

for p in patterns:
    m = re.search(p, text, re.DOTALL)
    if m:
        print(f'Found with pattern: {p[:40]}...')
        try:
            data = json.loads(m.group(1))
            print('Keys:', list(data.keys()))
            break
        except json.JSONDecodeError as e:
            print(f'JSON parse error: {e}')
            # Try to find the end
            raw = m.group(1)
            print(f'Raw length: {len(raw)}')
            print(f'First 200: {raw[:200]}')
            print(f'Last 200: {raw[-200:]}')
    else:
        print(f'Not found: {p[:40]}...')

# Also search for menu/nav data in HTML
nav_match = re.findall(r'href="(/zh/model-studio/[a-z0-9-]+)"[^>]*>([^<]+)<', text)
print(f'\nFound {len(nav_match)} model-studio links:')
for href, title in nav_match[:50]:
    print(f'  {href} -> {title.strip()}')
