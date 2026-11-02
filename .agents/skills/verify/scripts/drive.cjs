#!/usr/bin/env node
/* Anonymous browser evidence for the actual GitHub README, never a local rendering. */
const fs = require('node:fs');
const path = require('node:path');
const {execFileSync} = require('node:child_process');
const {chromium} = require('playwright');
const {createHash} = require('node:crypto');

function options(args) {
  const result = {mode: 'read-only', channel: 'chrome'};
  for (let i = 0; i < args.length; i += 2) {
    if (!args[i].startsWith('--') || args[i + 1] === undefined) throw Error('Expected --name value pairs');
    const key = args[i].slice(2);
    if (!['url', 'output', 'mode', 'channel', 'require-outlines'].includes(key)) throw Error('Unknown option ' + key);
    result[key] = args[i + 1];
  }
  if (result.mode !== 'read-only') throw Error('Only --mode read-only is supported');
  if (!result.url || !result.output || !path.isAbsolute(result.output)) throw Error('--url and absolute --output required');
  const url = new URL(result.url);
  if (url.protocol !== 'https:' || url.hostname !== 'github.com') throw Error('Target must be an actual HTTPS github.com page');
  if (fs.existsSync(result.output)) throw Error('Output must be a new directory; evidence is never overwritten');
  const root = execFileSync('git', ['rev-parse', '--show-toplevel'], {encoding: 'utf8'}).trim();
  const parent = fs.realpathSync(path.dirname(result.output));
  if (parent === root || parent.startsWith(root + path.sep)) throw Error('Evidence belongs outside the checkout');
  return result;
}

function anchorSettled(y, expectedTop, uncovered) {
  return y >= 0 && y <= Math.max(160, expectedTop + 8) && uncovered;
}

async function inspect(article) {
  return article.evaluate(async element => {
    const images = await Promise.all([...element.querySelectorAll('img')].map(async img => {
      let error = null;
      try { await img.decode(); } catch (e) { error = e.message; }
      const bounds = img.getBoundingClientRect();
      const picture = img.closest('picture');
      const sources = picture ? [...picture.querySelectorAll('source')].map(source => ({media: source.media, srcset: new URL(source.srcset, document.baseURI).href, matches: matchMedia(source.media).matches})) : [];
      return {alt: img.alt, src: img.src, currentSrc: img.currentSrc, width: bounds.width, height: bounds.height, naturalWidth: img.naturalWidth, naturalHeight: img.naturalHeight, error, sources};
    }));
    const rect = element.getBoundingClientRect();
    return {
      url: location.href, title: document.title, heading: [...element.querySelectorAll('h1,h2,h3')].map(e => ({level: e.tagName, text: e.textContent.trim(), id: e.id, anchor: e.querySelector('a')?.href})),
      images, links: [...element.querySelectorAll('a[href]')].map(e => ({text: e.textContent.trim(), href: e.href, image: !!e.querySelector('img')})),
      details: [...element.querySelectorAll('details')].map(e => ({summary: e.querySelector('summary')?.textContent.trim(), open: e.open})),
      viewport: {width: innerWidth, height: innerHeight}, documentWidth: document.documentElement.scrollWidth,
      article: {x: rect.x, y: rect.y, width: rect.width, height: rect.height, scrollWidth: element.scrollWidth, clientWidth: element.clientWidth},
      theme: {mode: document.documentElement.getAttribute('data-color-mode'), light: document.documentElement.getAttribute('data-light-theme'), dark: document.documentElement.getAttribute('data-dark-theme'), background: getComputedStyle(document.body).backgroundColor, preferredDark: matchMedia('(prefers-color-scheme: dark)').matches},
      text: element.innerText
    };
  });
}

async function paint(page) {
  // A full-page screenshot can capture unpainted offscreen images unless scrolled first.
  await page.evaluate(async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight) { scrollTo(0, y); await new Promise(requestAnimationFrame); } scrollTo(0, 0); });
}

async function run(config) {
  fs.mkdirSync(config.output);
  const write = (name, value) => fs.writeFileSync(path.join(config.output, name), JSON.stringify(value, null, 2) + '\n');
  const report = {url: config.url, started: new Date().toISOString(), sourceHead: execFileSync('git', ['rev-parse', 'HEAD'], {encoding: 'utf8'}).trim(), harnessSHA256: createHash('sha256').update(fs.readFileSync(__filename)).digest('hex'), sourceStatus: execFileSync('git', ['status', '--porcelain'], {encoding: 'utf8'}), playwright: require('playwright/package.json').version, mode: config.mode, failures: [], variants: [], navigation: [], assets: []};
  const browser = await chromium.launch({headless: true, ...(config.channel === 'chromium' ? {} : {channel: config.channel})});
  report.browser = browser.version();
  let counter = 0;
  const fail = (kind, message) => report.failures.push({kind, message});
  try {
    for (const [size, viewport] of [['desktop', {width: 1440, height: 1100}], ['mobile', {width: 390, height: 844}]]) {
      for (const scheme of ['light', 'dark']) {
        const name = `${size}-${scheme}`;
        const context = await browser.newContext({viewport, colorScheme: scheme});
        // A fresh anonymous context owns its cookies and browser state. No credentials loaded.
        const page = await context.newPage();
        const traffic = [];
        page.on('response', response => { if (response.status() >= 400) traffic.push({url: response.url(), status: response.status(), type: response.request().resourceType()}); });
        page.on('requestfailed', request => traffic.push({url: request.url(), error: request.failure()?.errorText, type: request.resourceType()}));
        try {
          const response = await page.goto(config.url, {waitUntil: 'domcontentloaded'});
          if (!response || response.status() !== 200) { fail('github-page', `${name}: target status ${response?.status()}`); continue; }
          const article = page.locator('article.markdown-body');
          await article.waitFor({state: 'visible', timeout: 20000});
          await page.locator('article.markdown-body img').first().waitFor({state: 'visible'});
          const capture = async label => {
            const state = await inspect(article);
            write(`${name}-${label}.json`, state);
            await paint(page);
            await page.screenshot({path: path.join(config.output, `${name}-${label}.png`), fullPage: true});
            return state;
          };
          const before = await capture('before');
          if (new URL(config.url).pathname.replace(/\/$/, '') === '/jerome-queck') {
            const avatar = page.locator('img.avatar-user[alt*="full-sized avatar"]');
            const avatarState = await avatar.evaluate(async img => { await img.decode(); const r = img.getBoundingClientRect(); return {alt: img.alt, currentSrc: img.currentSrc, naturalWidth: img.naturalWidth, naturalHeight: img.naturalHeight, width: r.width, height: r.height}; });
            write(`${name}-avatar.json`, avatarState);
            await avatar.screenshot({path: path.join(config.output, `${name}-avatar.png`)});
            if (!avatarState.naturalWidth || !avatarState.width) fail('avatar', `${name}: avatar failed to decode or render`);
          }
          for (const chapter of ['mathematics', 'software', 'public-work']) {
            const chapterLink = article.locator(`a:is([href="#${chapter}"], [href="#user-content-${chapter}"]):has(img)`);
            if (await chapterLink.count() !== 1) { fail('chapter', `${name}: missing unique ${chapter} image link`); continue; }
            await chapterLink.click();
            await page.evaluate(() => document.fonts.ready);
            await page.waitForFunction(id => { const e = document.getElementById(id) || document.getElementById('user-content-' + id); return e && e.getBoundingClientRect().y >= 0 && e.getBoundingClientRect().y <= Math.max(160, (parseFloat(getComputedStyle(e).scrollMarginTop) || 0) + 8); }, chapter, {timeout: 3000}).catch(() => {});
            await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
            const state = await inspect(article);
            const target = page.locator(`#user-content-${chapter}, #${chapter}`).first();
            const rect = await target.boundingBox();
            const expectedTop = await target.evaluate(e => parseFloat(getComputedStyle(e).scrollMarginTop) || 0);
            const headingUncovered = await target.evaluate(e => { const heading = e.parentElement.querySelector('h1,h2,h3') || e; const r = heading.getBoundingClientRect(); const top = document.elementFromPoint(r.x + Math.min(20, r.width / 2), r.y + r.height / 2); return top && (heading.contains(top) || top.contains(heading)); });
            const action = {action: 'click chapter', chapter, url: page.url(), target: rect, expectedTop, headingUncovered};
            write(`${name}-chapter-${chapter}.json`, {...state, action});
            await page.screenshot({path: path.join(config.output, `${name}-chapter-${chapter}.png`)});
            if (!new URL(page.url()).hash.endsWith(chapter) || !rect || !anchorSettled(rect.y, expectedTop, headingUncovered)) fail('chapter', `${name}: ${chapter} did not reach an uncovered heading near the top`);
          }
          const details = article.locator('details');
          for (let i = 0; i < await details.count(); i++) {
            const summary = details.nth(i).locator('summary').first();
            await summary.click();
            if (!(await details.nth(i).getAttribute('open') !== null)) fail('details', `${name}: summary ${i} did not open`);
            write(`${name}-details-${i}.json`, await inspect(article));
            await page.screenshot({path: path.join(config.output, `${name}-details-${i}.png`)});
          }
          const after = await capture('expanded');
          for (const img of after.images) {
            if (img.error || !img.naturalWidth || !img.width || !img.height) fail('asset', `${name}: undecoded or empty image ${img.currentSrc}`);
            if (!img.alt && !/chapter-/.test(img.src)) fail('accessibility', `${name}: nondecorative image lacks alternative text ${img.src}`);
            const selected = img.sources.find(s => s.matches);
            const expected = selected?.srcset || img.src;
            // GitHub Camo rewrites sources; compare URL-decoded path suffix, not proxy host.
            const expectedFile = new URL(expected).pathname.split('/').pop();
            if (!decodeURIComponent(img.currentSrc).includes(expectedFile)) fail('responsive-source', `${name}: expected ${expectedFile}; got ${img.currentSrc}`);
          }
          if (after.documentWidth > viewport.width + 1 || after.article.scrollWidth > after.article.clientWidth + 1) fail('overflow', `${name}: horizontal overflow`);
          if (!after.heading.some(h => h.level === 'H1') || ['Mathematics', 'Software', 'Public work'].some(text => !after.heading.some(h => h.level === 'H2' && h.text === text))) fail('accessibility', `${name}: native chapter headings missing`);
          if (after.details.length < 3) fail('details', `${name}: expected mathematics, repository, and definitions disclosures`);
          const rgb = after.theme.background.match(/\d+/g)?.slice(0, 3).map(Number);
          if (!rgb || (scheme === 'dark') !== (rgb.reduce((a, b) => a + b, 0) < 384)) fail('theme', `${name}: actual page background does not follow ${scheme}`);
          report.variants.push({name, before: `${name}-before.json`, expanded: `${name}-expanded.json`, traffic});
          traffic.filter(t => t.type === 'image').forEach(t => fail('asset-network', `${name}: ${JSON.stringify(t)}`));
          if (counter++ === 0) {
            // Check each authored source and each publication target via a real anonymous GET navigation.
            const sourceLinks = after.links.filter(link => /^https:\/\/github.com\/(Jerome-Group|jerome-queck)\/[^/#?]+\/?$/i.test(link.href));
            const publication = after.links.filter(link => /\/tree\/profile-data/.test(link.href));
            if (new Set(sourceLinks.map(link => link.href)).size < 9) fail('sources', 'Fewer than nine selected repository source links');
            const upstream = after.links.filter(link => /^https:\/\/github.com\/[^/]+\/[^/]+\/pull\/\d+/.test(link.href));
            const workflow = after.links.filter(link => /\/actions\/workflows\/profile.yml/.test(link.href));
            const targets = [...new Set([...sourceLinks, ...publication, ...workflow, ...upstream].map(link => link.href))];
            for (const [i, target] of targets.entries()) {
              const opened = await context.newPage();
              await opened.goto(config.url, {waitUntil: 'domcontentloaded'});
              const sourceArticle = opened.locator('article.markdown-body');
              for (const summary of await sourceArticle.locator('details > summary').all()) await summary.click();
              const anchor = sourceArticle.locator(`a[href="${target}"]`).first();
              const [response] = await Promise.all([
                opened.waitForNavigation({waitUntil: 'domcontentloaded'}),
                anchor.click()
              ]);
              const navigation = {target, url: opened.url(), title: await opened.title(), status: response?.status() ?? null};
              report.navigation.push(navigation);
              await opened.screenshot({path: path.join(config.output, `destination-${i}.png`)});
              write(`destination-${i}.json`, {...navigation, text: (await opened.locator('body').innerText()).slice(0, 40000)});
              if (target.endsWith('/tree/profile-data')) {
                const snapshotLink = opened.locator('article.markdown-body a[href$="/snapshot.json"]').first();
                if (await snapshotLink.count()) {
                  const snapshotURL = new URL(await snapshotLink.getAttribute('href'), opened.url()).href.replace('/blob/', '/raw/');
                  const published = await context.request.get(snapshotURL);
                  if (published.ok()) { write('published-snapshot.json', await published.json()); write('published-snapshot-source.json', {observedLink: await snapshotLink.getAttribute('href'), requested: snapshotURL, final: published.url(), status: published.status()}); }
                  else fail('publication', `Snapshot response ${published.status()}`);
                } else fail('publication', 'Published text does not link snapshot.json');
              }
              if (/Page not found|404/.test(navigation.title)) fail('github-destination', target + ': ' + navigation.title);
              await opened.close();
            }
            for (const url of [...new Set(after.images.map(img => img.currentSrc).filter(src => /\.svg(?:\?|$)/.test(src)))]) {
              const assetResponse = await context.request.get(url);
              const body = await assetResponse.text();
              const asset = {url, status: assetResponse.status(), paths: (body.match(/<path\b/g) || []).length, textNodes: (body.match(/<text\b/g) || []).length, bytes: Buffer.byteLength(body)};
              report.assets.push(asset);
              if (!assetResponse.ok() || !body.includes('<svg')) fail('asset-body', url);
              if (config['require-outlines'] === 'yes' && /(?:nav-|enter-|exit|chapter-)/.test(url) && (!asset.paths || asset.textNodes)) fail('svg-outlines', url);
              fs.writeFileSync(path.join(config.output, `asset-${report.assets.length}.svg`), body);
            }
          }
        } catch (error) { fail('drive', `${name}: ${error.stack}`); }
        finally { await context.close(); }
      }
    }
  } finally {
    await browser.close();
    report.finished = new Date().toISOString();
    report.cleanup = 'Owned browser and anonymous contexts closed; evidence retained.';
    write('report.json', report);
  }
  console.log(JSON.stringify({output: config.output, variants: report.variants.length, navigation: report.navigation.length, failures: report.failures}, null, 2));
  return report.failures.length ? 1 : 0;
}
if (require.main === module) {
  try { run(options(process.argv.slice(2))).then(code => { process.exitCode = code; }).catch(error => { console.error(error); process.exitCode = 1; }); }
  catch (error) { console.error(error.message); process.exitCode = 1; }
}
module.exports = {options, anchorSettled};
