#!/usr/bin/env node
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {options, anchorSettled, pixelDifference} = require('./drive.cjs');
const parent = fs.mkdtempSync(path.join(os.tmpdir(), 'profile-guard-test-'));
const output = path.join(parent, 'evidence');
const valid = ['--url', 'https://github.com/jerome-queck', '--output', output];
test('read-only plan rejects writes before creating any evidence', () => {
  assert.throws(() => options([...valid, '--mode', 'publish']), /read-only/);
  assert.throws(() => options([...valid, '--upload', 'yes']), /Unknown option/);
  assert.equal(fs.existsSync(output), false);
});
test('only actual public HTTPS GitHub pages are accepted', () => {
  for (const url of ['file:///tmp/profile.html', 'http://github.com/jerome-queck', 'https://github.com.example.com/profile']) {
    assert.throws(() => options(['--url', url, '--output', output]), /actual HTTPS github.com/);
  }
});
test('evidence cannot overwrite a previous run or contaminate the checkout', () => {
  assert.throws(() => options(['--url', valid[1], '--output', parent]), /never overwritten/);
  assert.throws(() => options(['--url', valid[1], '--output', path.join(process.cwd(), 'forbidden-evidence')]), /outside the checkout/);
  assert.equal(fs.existsSync(path.join(process.cwd(), 'forbidden-evidence')), false);
});
test('valid options leave evidence creation to the actual run', () => {
  assert.equal(options(valid).output, output);
  assert.equal(fs.existsSync(output), false);
  fs.rmdirSync(parent);
});

test('a visible heading cannot falsely prove chapter navigation', () => {
  // Observed live-profile defect: the hash changes while heading stays at y813.
  assert.equal(anchorSettled(813, 64, true), false);
  assert.equal(anchorSettled(64, 64, true), true);
  assert.equal(anchorSettled(64, 64, false), false);
});


test('motion compares decoded pixels rather than PNG metadata or elapsed time', () => {
  const {PNG} = require('pngjs');
  const a = new PNG({width: 2, height: 1}); a.data.fill(255);
  const still = PNG.sync.write(a);
  assert.equal(pixelDifference(still, PNG.sync.write(a, {deflateLevel: 1})).changedPixels, 0);
  a.data[0] = 0;
  assert.equal(pixelDifference(still, PNG.sync.write(a)).changedPixels, 1);
  assert.throws(() => pixelDifference(still, PNG.sync.write(new PNG({width: 1, height: 1}))), /geometry/);
});

test('file selection preserves different SVG views as separate evidence', () => {
  const {assetFile, sameAssetFile, selectedSource} = require('./drive.cjs');
  const roof = 'https://example.test/full-wide-ambient.svg#roof';
  const cellar = 'https://example.test/full-wide-ambient.svg#cellar';
  assert.equal(sameAssetFile(roof, cellar), true);
  assert.notEqual(roof, cellar);
  assert.equal(assetFile(cellar), 'https://example.test/full-wide-ambient.svg');
  assert.equal(sameAssetFile(roof, 'https://example.test/full-mobile-still.svg#roof'), false);
  assert.equal(selectedSource({src: cellar, sources: [{matches: false, srcset: roof}, {matches: true, srcset: cellar}]}), cellar);
});

test('continuous canvas rejects vertical gaps, partial rows and split source buttons', () => {
  const {canvasRows} = require('./drive.cjs');
  const canvas = {x: 10, width: 400};
  const images = [{x: 10, y: 0, width: 400, height: 100}, {x: 10, y: 100, width: 300, height: 80}, {x: 310, y: 100, width: 100, height: 80}];
  assert.equal(canvasRows(images, canvas).errors.length, 0);
  assert.ok(canvasRows(images.map(image => ({...image, y: image.y ? image.y + 8 : 0})), canvas).errors.some(error => /vertical gap/.test(error)));
  assert.ok(canvasRows(images.map((image, i) => ({...image, x: i === 2 ? image.x + 5 : image.x})), canvas).errors.some(error => /tiles do not meet/.test(error)));
  assert.ok(canvasRows([{x: 10, y: 0, width: 390, height: 100}], canvas).errors.some(error => /width/.test(error)));
});

test('SVG fragments remain discoverable when fetching selected media assets', () => {
  const {assetFile} = require('./drive.cjs');
  const sources = ['https://example.test/title-wide-ambient.svg#algebra', 'https://example.test/title-wide-ambient.svg#calculus', 'https://example.test/world.svg'];
  assert.equal(sources.filter(src => /\.svg(?:#|\?|$)/.test(src)).length, 3);
  assert.equal(new Set(sources.map(assetFile)).size, 2);
});

test('a matching master file cannot prove the selected crop exists or differs', () => {
  const {viewErrors, sameAssetFile} = require('./drive.cjs');
  const views = [{id: 'roof', viewBox: '0 0 900 220'}, {id: 'cellar', viewBox: '0 220 900 220'}];
  assert.equal(sameAssetFile('https://example.test/full.svg#roof', 'https://example.test/full.svg#cellar'), true);
  assert.deepEqual(viewErrors(views, ['roof', 'cellar']), []);
  assert.ok(viewErrors(views, ['missing']).some(error => /missing SVG view/.test(error)));
  assert.ok(viewErrors(views.map(view => ({...view, viewBox: views[0].viewBox})), ['roof', 'cellar']).some(error => /duplicate/.test(error)));
});

test('meeting title/source tiles still require the authored 75/25 split', () => {
  const {canvasRows} = require('./drive.cjs');
  const canvas = {x: 0, width: 400};
  assert.ok(canvasRows([{x: 0, y: 0, width: 200, height: 80}, {x: 200, y: 0, width: 200, height: 80}], canvas).errors.some(error => /75\/25/.test(error)));
});
