import { readFileSync, existsSync } from 'node:fs';
const data = JSON.parse(readFileSync('data/edizioni.json','utf8'));
let errors=0;
for (const e of data) {
  if (!e.year || !e.edition) { console.error('missing year/edition', e.id); errors++; }
  for (const f of e.files) {
    if (!existsSync(f.url)) { console.error('missing file', f.url); errors++; }
  }
  if (!e.description) { console.warn('no description', e.year); }
}
console.log(`Checked ${data.length} editions, ${data.reduce((a,e)=>a+e.files.length,0)} files. Errors: ${errors}`);
process.exit(errors?1:0);
