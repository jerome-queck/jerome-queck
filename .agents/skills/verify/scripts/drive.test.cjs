#!/usr/bin/env node
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {options, anchorSettled} = require('./drive.cjs');
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
