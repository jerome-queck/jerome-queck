#!/usr/bin/env node
const fs = require('node:fs');
const path = require('node:path');
const {execFileSync} = require('node:child_process');
const {chromium} = require('playwright');
const {PNG} = require('pngjs');
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

function assetFile(url) {
  const parsed = new URL(url);
  parsed.hash = '';
  return parsed.href;
}

function selectedSource(image) {
  return image.sources.find(source => source.matches)?.srcset || image.src;
}

function sameAssetFile(actual, expected) {
  return assetFile(actual) === assetFile(expected);
}

function canvasRows(images, article, tolerance = 1) {
  const rows = [];
  for (const image of images) {
    let row = rows.find(item => Math.abs(item.y - image.y) <= tolerance);
    if (!row) { row = {y: image.y, images: []}; rows.push(row); }
    row.images.push(image);
  }
  rows.sort((a, b) => a.y - b.y);
  const errors = [];
  rows.forEach((row, index) => {
    row.images.sort((a, b) => a.x - b.x);
    row.bottom = Math.max(...row.images.map(image => image.y + image.height));
    const first = row.images[0], last = row.images.at(-1);
    if (row.images.length === 2 && (Math.abs(first.width - article.width * .75) > tolerance || Math.abs(last.width - article.width * .25) > tolerance)) errors.push(`row ${index} title/source ratio is not 75/25`);
    if (Math.abs(first.x - article.x) > tolerance || Math.abs(last.x + last.width - article.x - article.width) > tolerance) errors.push(`row ${index} does not fill canvas width`);
    for (let i = 1; i < row.images.length; i++) {
      const left = row.images[i - 1], right = row.images[i];
      if (Math.abs(right.x - left.x - left.width) > tolerance || Math.abs(right.height - left.height) > tolerance) errors.push(`row ${index} tiles do not meet`);
    }
    if (index && Math.abs(row.y - rows[index - 1].bottom) > tolerance) errors.push(`row ${index} vertical gap or overlap`);
  });
  return {rows, errors};
}

function viewErrors(views, references) {
  const errors = references.filter(reference => !views.some(view => view.id === reference)).map(reference => `missing SVG view ${reference}`);
  if (new Set(views.map(view => view.viewBox)).size !== views.length) errors.push('duplicate SVG view boxes');
  return errors;
}

function analyzeSvg(source) {
  const doc = new DOMParser().parseFromString(source, 'image/svg+xml');
  const data = doc.getElementById('world-data');
  const styles = [...doc.querySelectorAll('style')].map(e => e.textContent).join('\n');
  const selectors = [...styles.matchAll(/([^{}]+)\{([^{}]*animation\s*:[^{}]+)\}/g)].map(match => match[1].trim()).filter(selector => !selector.startsWith('@'));
  const invalidSelectors = [];
  const animated = [...new Set(selectors.flatMap(selector => { try { return [...doc.querySelectorAll(selector)]; } catch { invalidSelectors.push(selector); return []; } }))];
  return {
    snapshot: doc.documentElement.getAttribute('data-snapshot'), dataBoundary: !!data, dataMarkup: data?.outerHTML, styles, selectors, invalidSelectors,
    unsupportedAnimation: doc.querySelectorAll('animate,animateMotion,animateTransform,set,script,[style*="animation"]').length,
    animatedElements: animated.map(e => ({tag: e.tagName, id: e.id, class: e.getAttribute('class')})),
    decorativeOnly: animated.every(e => e.tagName === 'circle' && !e.querySelector('text,path')),
    dataAffected: data ? animated.some(e => e === data || e.contains(data) || data.contains(e)) : false,
    views: [...doc.querySelectorAll('view')].map(e => ({id: e.id, viewBox: e.getAttribute('viewBox')}))
  };
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
      const hit = img.closest('a')?.getBoundingClientRect();
      const sources = picture ? [...picture.querySelectorAll('source')].map(source => ({media: source.media, srcset: new URL(source.srcset, document.baseURI).href, matches: matchMedia(source.media).matches})) : [];
      return {hitArea: hit ? {x: bounds.x, y: bounds.y, width: bounds.width, height: bounds.height} : null, anchorBox: hit ? {x: hit.x, y: hit.y, width: hit.width, height: hit.height} : null, alt: img.alt, src: img.src, srcAttribute: img.getAttribute('src'), currentSrc: img.currentSrc, href: img.closest('a')?.href, canvas: img.closest('p') === element.querySelector('picture')?.closest('p'), x: bounds.x, y: bounds.y, width: bounds.width, height: bounds.height, naturalWidth: img.naturalWidth, naturalHeight: img.naturalHeight, error, sources};
    }));
    const rect = element.getBoundingClientRect();
    const canvas = element.querySelector('picture')?.closest('p')?.getBoundingClientRect();
    return {
      url: location.href, title: document.title, heading: [...element.querySelectorAll('h1,h2,h3')].map(e => ({level: e.tagName, text: e.textContent.trim(), id: e.id, anchor: e.querySelector('a')?.href})),
      canvas: canvas ? {x: canvas.x, y: canvas.y, width: canvas.width, height: canvas.height} : null, images, links: [...element.querySelectorAll('a[href]')].map(e => ({text: e.textContent.trim(), href: e.href, image: !!e.querySelector('img'), alt: e.querySelector('img')?.alt})),
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

function pixelDifference(first, second) {
  const a = PNG.sync.read(first), b = PNG.sync.read(second);
  if (a.width !== b.width || a.height !== b.height) throw Error('Motion frame geometry changed');
  let changed = 0;
  for (let i = 0; i < a.data.length; i += 4) {
    if (a.data.subarray(i, i + 4).some((value, j) => value !== b.data[i + j])) changed++;
  }
  return {changedPixels: changed, totalPixels: a.width * a.height};
}

async function captureMotion(page, image, output, name) {
  await image.scrollIntoViewIfNeeded();
  await image.evaluate(async element => { for (const img of element.matches('img') ? [element] : element.querySelectorAll('img')) await img.decode(); });
  const frames = [], timestamps = [];
  for (let i = 0; i < 3; i++) {
    if (i) await page.waitForTimeout(i === 1 ? 2300 : 2700);
    timestamps.push(new Date().toISOString());
    frames.push(await image.screenshot({path: path.join(output, `${name}-frame-${i}.png`), animations: 'allow'}));
  }
  const selectedImage = await image.evaluate(img => ({alt: img.alt, currentSrc: img.currentSrc, width: img.getBoundingClientRect().width, height: img.getBoundingClientRect().height}));
  return {image: selectedImage, timestamps, media: await page.evaluate(() => matchMedia('(prefers-reduced-motion: reduce)').matches), comparisons: frames.slice(1).map(frame => pixelDifference(frames[0], frame))};
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
        const context = await browser.newContext({viewport, colorScheme: scheme, reducedMotion: 'no-preference'});
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
          const sectionLinks = await article.locator('a[href^="#"]:not(.anchor)').evaluateAll(links => [...new Set(links.map(a => a.getAttribute('href')).filter(href => href !== '#'))]);
          for (const href of sectionLinks) {
            const section = href.replace(/^#(?:user-content-)?/, '');
            const sectionLink = article.locator(`a:is([href="#${section}"], [href="#user-content-${section}"]):not(.anchor)`);
            if (await sectionLink.count() !== 1) { fail('section', `${name}: missing unique ${section} link`); continue; }
            await sectionLink.click();
            await page.evaluate(() => document.fonts.ready);
            await page.waitForFunction(id => { const e = document.getElementById(id) || document.getElementById('user-content-' + id); return e && e.getBoundingClientRect().y >= 0 && e.getBoundingClientRect().y <= Math.max(160, (parseFloat(getComputedStyle(e).scrollMarginTop) || 0) + 8); }, section, {timeout: 3000}).catch(() => {});
            await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
            const state = await inspect(article);
            const target = page.locator(`#user-content-${section}, #${section}`).first();
            const rect = await target.boundingBox();
            const expectedTop = await target.evaluate(e => parseFloat(getComputedStyle(e).scrollMarginTop) || 0);
            const headingUncovered = await target.evaluate(e => { const heading = e.parentElement.querySelector('h1,h2,h3') || e; const r = heading.getBoundingClientRect(); const top = document.elementFromPoint(r.x + Math.min(20, r.width / 2), r.y + r.height / 2); return top && (heading.contains(top) || top.contains(heading)); });
            const action = {action: 'click section', section, url: page.url(), target: rect, expectedTop, headingUncovered};
            write(`${name}-section-${section}.json`, {...state, action});
            await page.screenshot({path: path.join(config.output, `${name}-section-${section}.png`)});
            if (!new URL(page.url()).hash.endsWith(section) || !rect || !anchorSettled(rect.y, expectedTop, headingUncovered)) fail('section', `${name}: ${section} did not reach an uncovered heading near the top`);
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
            if (!img.alt) fail('accessibility', `${name}: nondecorative image lacks alternative text ${img.src}`);
            const expected = selectedSource(img);
            if (!sameAssetFile(img.currentSrc, expected)) fail('responsive-source', `${name}: expected file ${expected}; got ${img.currentSrc}`);
          }
          if (after.documentWidth > viewport.width + 1 || after.article.scrollWidth > after.article.clientWidth + 1) fail('overflow', `${name}: horizontal overflow`);
          if (!after.heading.length || after.heading.some(h => !h.text)) fail('accessibility', `${name}: native text-edition headings missing or empty`);
          if (!after.details.length || after.details.some(d => !d.summary)) fail('details', `${name}: text-edition disclosure missing or unnamed`);
          const rgb = after.theme.background.match(/\d+/g)?.slice(0, 3).map(Number);
          if (!rgb || (scheme === 'dark') !== (rgb.reduce((a, b) => a + b, 0) < 384)) fail('theme', `${name}: actual page background does not follow ${scheme}`);
          const canvasImages = after.images.filter(image => image.canvas);
          const geometry = canvasRows(canvasImages, after.canvas);
          write(`${name}-canvas.json`, geometry);
          geometry.errors.forEach(error => fail('canvas-geometry', `${name}: ${error}`));
          if (canvasImages.length !== 16 || geometry.rows.length !== 11 || geometry.rows.filter(row => row.images.length === 2).length !== 5) fail('canvas-contract', `${name}: expected hero, nine projects with five source pairs, data world`);
          if (size === 'mobile') for (const image of canvasImages.filter(image => image.href)) {
            if (!image.hitArea || image.hitArea.height < 44 || image.hitArea.width < 44) fail('mobile-hit-area', `${name}: image link smaller than 44 CSS pixels ${image.alt}`);
          }
          const pictures = article.locator('p:has(picture)').first().locator('picture img');
          const normal = [];
          for (const index of [0, 1]) normal.push(await captureMotion(page, pictures.nth(index), config.output, `${name}-motion-${index}`));
          const staticData = await captureMotion(page, pictures.last(), config.output, `${name}-data`);
          if (staticData.comparisons.some(diff => diff.changedPixels)) fail('data-motion', `${name}: data glyphs or counts changed between frames`);
          if (!normal.some(item => item.comparisons.some(diff => diff.changedPixels > 0))) fail('motion', `${name}: no visible decorative master motion observed`);
          const fragments = [];
          for (let i = 0; i < canvasImages.length - 1; i++) {
            const bitmap = await pictures.nth(i).screenshot({path: path.join(config.output, `${name}-view-${i}.png`), animations: 'allow'});
            fragments.push({source: selectedSource(canvasImages[i]), srcAttribute: canvasImages[i].srcAttribute, currentSrc: canvasImages[i].currentSrc, screenshotSHA256: createHash('sha256').update(bitmap).digest('hex')});
          }
          write(`${name}-fragments.json`, fragments);
          const reducedContext = await browser.newContext({viewport, colorScheme: scheme, reducedMotion: 'reduce'});
          let reducedState, reduced;
          try {
            const reducedPage = await reducedContext.newPage();
            await reducedPage.goto(config.url, {waitUntil: 'domcontentloaded'});
            const reducedArticle = reducedPage.locator('article.markdown-body');
            reducedState = await inspect(reducedArticle);
            write(`${name}-reduced-state.json`, reducedState);
            for (const image of reducedState.images) {
              const expected = selectedSource(image);
              if (!/-still\.svg(?:#|\?|$)/.test(expected) || !sameAssetFile(image.currentSrc, expected)) fail('reduced-source', `${name}: wrong reduced file ${image.currentSrc}; expected ${expected}`);
            }
            const canvas = reducedArticle.locator('p:has(picture)').first();
            await paint(reducedPage);
            reduced = await captureMotion(reducedPage, canvas, config.output, `${name}-reduced-canvas`);
            if (reduced.comparisons.some(diff => diff.changedPixels)) fail('reduced-motion', `${name}: reduced canvas moves`);
          } finally { await reducedContext.close(); }
          write(`${name}-motion.json`, {normal, staticData, reduced});
          report.variants.push({name, before: `${name}-before.json`, expanded: `${name}-expanded.json`, traffic});
          traffic.filter(t => t.type === 'image').forEach(t => fail('asset-network', `${name}: ${JSON.stringify(t)}`));
          const allImages = [...after.images, ...reducedState.images];
          const urls = [...new Set(allImages.map(selectedSource).filter(src => /\.svg(?:#|\?|$)/.test(src)).map(assetFile))];
          for (const url of urls) {
            const assetResponse = await context.request.get(url);
            const body = await assetResponse.text();
            const asset = {url, status: assetResponse.status(), paths: (body.match(/<path\b/g) || []).length, textNodes: (body.match(/<text\b/g) || []).length, bytes: Buffer.byteLength(body)};
            asset.motionSource = await page.evaluate(analyzeSvg, body);
            const motion = asset.motionSource;
            if (motion.dataMarkup) motion.dataSHA256 = createHash('sha256').update(motion.dataMarkup).digest('hex');
            delete motion.dataMarkup;
            const dataWorld = /\/world(?:-mobile)?(?:-still)?\.svg(?:\?|$)/.test(url);
            const still = /-still\.svg(?:\?|$)/.test(url);
            if (motion.invalidSelectors.length || motion.unsupportedAnimation || motion.dataAffected || !motion.decorativeOnly || (still && motion.styles) || (dataWorld && (!motion.dataBoundary || !motion.snapshot || motion.animatedElements.length))) fail('motion-source', `${name}: invalid authored/data/static boundary in ${url}`);
            if (!dataWorld && !still && !motion.animatedElements.length) fail('motion-source', `${name}: ambient master has no decorative animation ${url}`);
            const references = allImages.map(selectedSource).filter(src => assetFile(src) === url).map(src => new URL(src).hash.slice(1)).filter(Boolean);
            for (const error of viewErrors(motion.views, references)) fail('fragment-source', `${name}: ${error} in ${url}`);
            if (dataWorld && report.publishedSnapshot && motion.snapshot !== report.publishedSnapshot.observed_to) fail('snapshot-generation', `${name}: data asset timestamp differs from observed JSON ${url}`);
            if (motion.dataBoundary) {
              const counterpart = report.assets.find(previous => previous.motionSource.dataBoundary && previous.url.replace('-still.svg', '.svg') === url.replace('-still.svg', '.svg'));
              if (counterpart && counterpart.motionSource.dataSHA256 !== motion.dataSHA256) fail('data-boundary', `${name}: normal/still world-data markup differs ${url}`);
            }
            report.assets.push(asset);
            if (!assetResponse.ok() || !body.includes('<svg')) fail('asset-body', url);
            if (config['require-outlines'] === 'yes' && (!asset.paths || asset.textNodes)) fail('svg-outlines', url);
            fs.writeFileSync(path.join(config.output, `asset-${report.assets.length}.svg`), body);
          }
          if (counter++ === 0) {
            const fallback = await context.newPage();
            await fallback.route('**/*', route => route.request().resourceType() === 'image' ? route.abort() : route.continue());
            await fallback.goto(config.url, {waitUntil: 'domcontentloaded'});
            const fallbackArticle = fallback.locator('article.markdown-body');
            for (const summary of await fallbackArticle.locator('details > summary').all()) await summary.click();
            const fallbackState = await inspect(fallbackArticle);
            write('images-blocked.json', fallbackState);
            await fallback.screenshot({path: path.join(config.output, 'images-blocked.png'), fullPage: true});
            for (const project of JSON.parse(fs.readFileSync(path.join(__dirname, '../../../../data/projects.json'), 'utf8'))) {
              if (!fallbackState.text.includes(project.name) || !fallbackState.links.some(link => link.href.toLowerCase().includes(project.repo.toLowerCase()))) fail('images-blocked', `Missing native fallback for ${project.name}`);
            }
            if (!fallbackState.text.includes('Open proposals') || !fallbackState.links.some(link => /public records|definitions/i.test(link.text))) fail('images-blocked', 'Public records and exact-source fallback missing');
            await fallback.close();

            const projects = JSON.parse(fs.readFileSync(path.join(__dirname, '../../../../data/projects.json'), 'utf8'));
            const targets = [];
            for (const project of projects) {
              const title = after.links.find(link => link.image && link.href.replace(/\/$/, '') === project.url.replace(/\/$/, '') && link.alt?.startsWith(project.name + '.'));
              if (!title) fail('projects', `Missing image title destination for ${project.name}`);
              else targets.push({...title, role: 'project-title'});
              if (project.group === 'mathematics') {
                const source = after.links.find(link => link.image && link.href.toLowerCase().replace(/\/$/, '') === `https://github.com/${project.repo}`.toLowerCase() && link.alt === `Repository for ${project.name}`);
                if (!source) fail('sources', `Missing secondary image repository button ${project.name}`);
                else targets.push({...source, role: 'project-source'});
              }
            }
            const mergedIDs = ['189784', '189855', '189960', '189993', '130275', '71474'];
            for (const id of mergedIDs) {
              const upstream = after.links.find(link => new RegExp(`/pull/${id}$`).test(link.href));
              if (!upstream) fail('upstream', `Missing merged contribution #${id}`);
              else targets.push({...upstream, role: 'merged-pr'});
            }
            const publication = after.links.find(link => /public records|definitions/i.test(link.text));
            if (publication) targets.push({...publication, role: 'publication'});
            else fail('publication', 'No rendered records/source link');
            for (const [i, target] of targets.entries()) {
              const opened = await context.newPage();
              try {
                await opened.goto(config.url, {waitUntil: 'domcontentloaded'});
                const sourceArticle = opened.locator('article.markdown-body');
                for (const summary of await sourceArticle.locator('details > summary').all()) await summary.click();
                const anchors = sourceArticle.locator('a[href]');
                const matchingIndex = await anchors.evaluateAll((links, target) => links.findIndex(link => link.href === target.href && (target.image ? link.querySelector('img')?.alt === target.alt : !link.querySelector('img'))), target);
                if (matchingIndex < 0) throw Error('Observed destination anchor disappeared');
                const anchor = anchors.nth(matchingIndex);
                const clickable = target.image ? anchor.locator('img') : anchor;
                const hitArea = await clickable.boundingBox();
                const previousTitle = await opened.title();
                const [response] = await Promise.all([opened.waitForNavigation({waitUntil: 'domcontentloaded'}), clickable.click()]);
                await opened.waitForFunction(previous => document.title && document.title !== previous, previousTitle);
                const readback = response || await context.request.get(opened.url());
                const navigation = {role: target.role, expected: target.href, url: opened.url(), title: await opened.title(), status: readback.status(), statusSource: response ? 'clicked-document-response' : 'GET-destination-readback-after-SPA-click', hitArea};
                const bodyText = (await opened.locator('body').innerText()).slice(0, 60000);
                if (target.role === 'merged-pr' && !/Merged/.test(bodyText)) fail('upstream', `Merged state not observed ${target.href}`);
                if (target.role === 'publication') {
                  const snapshotLink = opened.locator('article.markdown-body a[href$="/snapshot.json"]').first();
                  if (await snapshotLink.count()) {
                    const observedLink = await snapshotLink.getAttribute('href');
                    const snapshotURL = new URL(observedLink, opened.url()).href.replace('/blob/', '/raw/');
                    await snapshotLink.click();
                    await opened.waitForLoadState('domcontentloaded');
                    const published = await context.request.get(snapshotURL);
                    write('published-snapshot-source.json', {observedLink, requested: snapshotURL, final: published.url(), status: published.status()});
                    if (published.ok()) {
                      const snapshot = await published.json();
                      write('published-snapshot.json', snapshot);
                      report.publishedSnapshot = {schema_version: snapshot.schema_version, observed_to: snapshot.observed_to, counts: snapshot.counts};
                      if (snapshot.schema_version !== 4) fail('publication', 'Expected schema-v4 public input');
                      for (const asset of report.assets.filter(asset => asset.motionSource.dataBoundary)) if (asset.motionSource.snapshot !== snapshot.observed_to) fail('snapshot-generation', `Data timestamp differs from observed JSON ${asset.url}`);
                    }
                    else fail('publication', `Snapshot response ${published.status()}`);
                  } else fail('publication', 'Published source does not link snapshot.json');
                }
                if (navigation.status !== 200 || /Page not found|404/.test(navigation.title)) {
                  if (new URL(target.href).hostname !== 'github.com' && [401, 403].includes(navigation.status)) navigation.outcome = 'verified-unreachable: anonymous website access blocked';
                  else fail('destination', target.href + ': ' + navigation.title + ' status ' + navigation.status);
                } else navigation.outcome = 'observed destination response 200';
                report.navigation.push(navigation);
                await opened.screenshot({path: path.join(config.output, `destination-${i}.png`)});
                write(`destination-${i}.json`, {...navigation, text: bodyText});
              } catch (error) { fail('destination', `${target.href}: ${error.message}`); }
              finally { await opened.close(); }
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
module.exports = {options, anchorSettled, pixelDifference, captureMotion, assetFile, sameAssetFile, selectedSource, canvasRows, analyzeSvg, viewErrors};
