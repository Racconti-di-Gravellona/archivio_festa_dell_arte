import { readFileSync, writeFileSync } from 'node:fs';

const html = readFileSync('index.html', 'utf8');

// Split into edition sections: each starts with <h2 id="edYYYY"> ... until next <h2
const re = /<h2 id="(ed(\d{4}))">(.*?)<\/h2>(.*?)(?=<h2 id=|$)/gs;
const editions = [];
for (const m of html.matchAll(re)) {
  const id = m[1];
  const year = m[2];
  const heading = m[3];
  const body = m[4];
  // edition number from heading "YYYY — Edizione N"
  const numMatch = heading.match(/Edizione\s+(\d+)/);
  const edition = numMatch ? parseInt(numMatch[1], 10) : null;

  // description
  const descMatch = body.match(/<p class='desc'>(.*?)<\/p>/s);
  const description = descMatch ? descMatch[1].replace(/<[^>]+>/g, '').trim() : '';

  // files in .gal
  const galMatch = body.match(/<div class='gal'>(.*?)<\/div>/s);
  const gal = galMatch ? galMatch[1] : '';
  const fileRe = /<figure>.*?<a href='([^']+)'.*?(?:<figcaption>(.*?)<\/figcaption>)?.*?<\/figure>/gs;
  const files = [];
  for (const f of gal.matchAll(/<figure>(.*?)<\/figure>/gs)) {
    const inner = f[1];
    const href = (inner.match(/<a href='([^']+)'/) || [])[1];
    const caption = (inner.match(/<figcaption>(.*?)<\/figcaption>/s) || [])[1];
    const imgAlt = (inner.match(/alt='([^']*)'/) || [])[1];
    const cap = caption ? caption.replace(/<[^>]+>/g,'').trim() : null;
    if (href) files.push({ url: href, caption: cap, alt: `${year} — ${cap || (href.split('/').pop())}` });
  }

  // transcription (pre inside details)
  const preMatch = body.match(/<pre>(.*?)<\/pre>/s);
  const transcription = preMatch ? preMatch[1].replace(/&#x27;/g, "'").replace(/&#39;/g, "'").trim() : null;

  // dati list
  const datiMatch = body.match(/<ul class='dati'>(.*?)<\/ul>/s);
  const dati = [];
  if (datiMatch) {
    for (const li of datiMatch[1].matchAll(/<li><b>(.*?)<\/b>:\s*(.*?)<\/li>/gs)) {
      dati.push({ key: li[1].trim(), value: li[2].replace(/<[^>]+>/g,'').trim() });
    }
  }

  // external links (in desc)
  const extLinks = [];
  for (const a of description.matchAll(/<a href='([^']+)'[^>]*>(.*?)<\/a>/g)) {
    // already stripped; re-extract from raw desc
  }
  const rawDesc = descMatch ? descMatch[1] : '';
  for (const a of rawDesc.matchAll(/<a href='([^']+)'[^>]*>(.*?)<\/a>/g)) {
    extLinks.push({ url: a[1], label: a[2].replace(/<[^>]+>/g,'').trim() });
  }

  // thumb path
  const thumb = files.length ? 'thumb/' + files[0].url.split('/').pop().replace(/\.(jpg|jpeg|png)$/i, '.webp') : null;

  editions.push({
    id,
    year,
    edition,
    decade: year >= 2020 ? '2020s' : year >= 2010 ? '2010s' : year >= 2000 ? '2000s' : '1990s',
    title: dati.find(d => /tema o titolo/i.test(d.key))?.value || null,
    description,
    date: dati.find(d => /date dell.evento/i.test(d.key))?.value || null,
    location: dati.find(d => /^luogo/i.test(d.key))?.value || null,
    primaryPoster: files[0]?.url || null,
    thumb: thumb && (thumb) || null,
    files,
    transcription,
    dati,
    externalLinks: extLinks,
  });
}

// only real editions (edYYYY)
const real = editions.filter(e => /^ed\d{4}$/.test(e.id));
writeFileSync('data/edizioni.json', JSON.stringify(real, null, 2) + '\n');
console.log('editions:', real.length);
console.log('years:', real.map(e=>e.year).join(', '));
