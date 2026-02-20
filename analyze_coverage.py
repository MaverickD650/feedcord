import xml.etree.ElementTree as ET
from collections import defaultdict

p = 'FeedCord.Tests/TestResults/af321f5f-3e2b-4030-88a3-cf42a889deeb/coverage.opencover.xml'
root = ET.parse(p).getroot()

file_map = {f.attrib['uid']: f.attrib.get('fullPath','') for f in root.findall('.//File')}
stats = defaultdict(lambda:[0,0])
uncovered = defaultdict(list)

for sp in root.findall('.//SequencePoint'):
    fid = sp.attrib.get('fileid')
    if not fid:
        continue
    full = file_map.get(fid,'')
    if '/FeedCord/src/' not in full:
        continue
    vc = int(sp.attrib.get('vc','0'))
    stats[fid][1] += 1
    if vc > 0:
        stats[fid][0] += 1
    else:
        sl = sp.attrib.get('sl')
        if sl:
            try:
                uncovered[fid].append(int(sl))
            except:
                pass

rows = []
for fid, (cov, total) in stats.items():
    full = file_map.get(fid,'')
    pct = (100.0*cov/total) if total else 100.0
    rows.append((pct, cov, total, full, fid))

rows.sort(key=lambda t: (t[0], t[3]))

print("LOWEST 10 FILES BY COVERAGE:")
for pct, cov, total, full, fid in rows[:10]:
    name = full.split('src/')[-1] if 'src/' in full else full
    print(f"{pct:5.1f}%  {cov:3}/{total:3}  {name}")

print("\n\nPOSTBUILDER COVERAGE:")
for pct, cov, total, full, fid in rows:
    if 'PostBuilder.cs' in full:
        print(f"{pct:.1f}% ({cov}/{total})")
        lines = sorted(uncovered.get(fid,[]))[:15]
        if lines:
            print(f"Uncovered lines: {lines}")
        break

print("\n\nTOP 5 BY COVERAGE:")
for pct, cov, total, full, fid in rows[-5:]:
    name = full.split('src/')[-1] if 'src/' in full else full
    print(f"{pct:5.1f}%  {cov:3}/{total:3}  {name}")
