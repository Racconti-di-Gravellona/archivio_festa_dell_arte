#!/usr/bin/env node
/**
 * Genera varianti responsive WebP per l'archivio:
 *  - medium/<basename>.webp  → max 1200px lato lungo (gallerie)
 *  - thumb/<basename>.webp   → max 600px lato lungo (caroselli)
 *
 * Due modalità:
 *   node scripts/build-responsive.mjs
 *       modalità JSON (restyle): legge data/edizioni.json, aggiunge `medium`
 *       a ogni file immagine e rigenera i thumb delle edizioni.
 *
 *   node scripts/build-responsive.mjs --html <path/index.html>
 *       modalità HTML (sito di produzione): sostituisce le immagini della
 *       galleria con medium/... e rigenera i thumb del carosello.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';

const MEDIUM_MAX = 1200;
const THUMB_MAX = 600;
const Q_MEDIUM = 80;
const Q_THUMB = 78;

const isImage = (u) => /\.(jpe?g|png|webp)$/i.test(u);
const base = (u) => path.basename(u).replace(/\.[^.]+$/, '');

function dims(file) {
  const out = execFileSync('sips', ['-g', 'pixelWidth', '-g', 'pixelHeight', file], { encoding: 'utf8' });
  const w = Number(out.match(/pixelWidth:\s*(\d+)/)[1]);
  const h = Number(out.match(/pixelHeight:\s*(\d+)/)[1]);
  return [w, h];
}

function targetDims(w, h, max) {
  const scale = Math.min(1, max / Math.max(w, h));
  return [Math.round(w * scale), Math.round(h * scale)];
}

function encodeWebp(src, dst, max, q) {
  const [w, h] = dims(src);
  const [nw, nh] = targetDims(w, h, max);
  mkdirSync(path.dirname(dst), { recursive: true });
  const argv = ['-quiet', '-q', String(q), '-m', '4'];
  if (nw !== w || nh !== h) argv.push('-resize', String(nw), String(nh));
  argv.push(src, '-o', dst);
  execFileSync('cwebp', argv);
  return [nw, nh];
}

const htmlMode = process.argv[2] === '--html';

if (!htmlMode) {
  // ---------- modalità JSON (restyle) ----------
  const data = JSON.parse(readFileSync('data/edizioni.json', 'utf8'));
  const mediums = new Map();
  let thumbs = 0;

  for (const e of data) {
    for (const f of e.files) {
      if (!isImage(f.url)) continue;
      const dst = `medium/${base(f.url)}.webp`;
      if (!mediums.has(f.url)) {
        encodeWebp(f.url, dst, MEDIUM_MAX, Q_MEDIUM);
        mediums.set(f.url, dst);
      }
      f.medium = dst;
    }
    if (e.primaryPoster && isImage(e.primaryPoster)) {
      const thumb = `thumb/${base(e.primaryPoster)}.webp`;
      encodeWebp(e.primaryPoster, thumb, THUMB_MAX, Q_THUMB);
      e.thumb = thumb;
      thumbs++;
    }
  }

  writeFileSync('data/edizioni.json', JSON.stringify(data, null, 2) + '\n');
  console.log(`OK JSON: ${mediums.size} medium, ${thumbs} thumb generati`);
} else {
  // ---------- modalità HTML (produzione) ----------
  const file = process.argv[3];
  if (!file) {
    console.error('Uso: node scripts/build-responsive.mjs --html <index.html>');
    process.exit(1);
  }
  let html = readFileSync(file, 'utf8');

  // 1) thumb del carosello: rigenera dal poster collegato (max 600px)
  const thumbDone = new Set();
  const figureRe = /<a\b[^>]*\bhref='(volantini\/[^']+)'[^>]*><img\b[^>]*\bsrc='(thumb\/[^']+\.webp)'/g;
  let m;
  while ((m = figureRe.exec(html)) !== null) {
    const [, src, thumb] = m;
    if (thumbDone.has(thumb) || !isImage(src)) continue;
    encodeWebp(src, thumb, THUMB_MAX, Q_THUMB);
    thumbDone.add(thumb);
  }

  // 2) immagini della galleria: medium + width/height aggiornati
  const mediumDone = new Map();
  html = html.replace(/<img\b[^>]*>/g, (tag) => {
    const mSrc = tag.match(/\bsrc='(volantini\/[^']+\.(?:jpe?g|png|webp))'/i);
    if (!mSrc) return tag;
    const src = mSrc[1];
    let dst = mediumDone.get(src);
    let nw, nh;
    if (!dst) {
      dst = `medium/${base(src)}.webp`;
      [nw, nh] = encodeWebp(src, dst, MEDIUM_MAX, Q_MEDIUM);
      mediumDone.set(src, { dst, nw, nh });
    } else {
      ({ dst, nw, nh } = mediumDone.get(src));
    }
    let out = tag.replace(mSrc[0], `src='${dst}'`);
    if (/\bwidth='\d+'/.test(out)) out = out.replace(/\bwidth='\d+'/, `width='${nw}'`);
    if (/\bheight='\d+'/.test(out)) out = out.replace(/\bheight='\d+'/, `height='${nh}'`);
    return out;
  });

  writeFileSync(file, html);
  console.log(`OK HTML: ${mediumDone.size} medium, ${thumbDone.size} thumb generati`);
}
