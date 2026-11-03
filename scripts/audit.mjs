import { readFileSync, statSync, existsSync, writeFileSync } from 'node:fs';
const data = JSON.parse(readFileSync('data/edizioni.json','utf8'));
const lines = [];
lines.push('# Audit archivio — Festa dell\'Arte');
lines.push('');
lines.push(`Edizioni: ${data.length} (${data[0].year}–${data[data.length-1].year})`);
lines.push('');
lines.push('| Anno | Ed. | File | Transcr. | Ext links | Peso totale |');
lines.push('|---|---|---|---|---|---|');
let totalBytes=0;
for (const e of data) {
  let bytes=0, missing=0;
  for (const f of e.files) {
    if (existsSync(f.url)) { bytes += statSync(f.url).size; } else { missing++; }
  }
  totalBytes += bytes;
  lines.push(`| ${e.year} | ${e.edition}ª | ${e.files.length}${missing?` (${missing} manc.)`:''} | ${e.transcription?'sì':'—'} | ${e.externalLinks.length} | ${(bytes/1024/1024).toFixed(1)} MB |`);
}
lines.push('');
lines.push(`Peso totale file referenziati: ${(totalBytes/1024/1024).toFixed(1)} MB`);
lines.push('');
// missing years 1995-2026
const ys = new Set(data.map(e=>+e.year));
const gaps = [];
for (let y=1995; y<=2026; y++) if (!ys.has(y)) gaps.push(y);
lines.push(`Anni senza edizione: ${gaps.join(', ') || 'nessuno'}`);
lines.push('');
// alt text coverage
const files = data.flatMap(e=>e.files);
const withAlt = files.filter(f=>f.alt && f.alt !== f.url.split('/').pop()).length;
lines.push(`File totali: ${files.length}; con alt descrittivo (≠nome file): ${withAlt}`);
writeFileSync('docs/audit.md', lines.join('\n')+'\n');
console.log(lines.join('\n'));
