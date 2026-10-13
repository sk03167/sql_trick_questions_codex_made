/* Parse and render every owned Mermaid diagram in an isolated browser. */
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..');
const runtime = process.env.DIAGRAM_RUNTIME_DIR || __dirname;
const playwright = require(require.resolve('playwright', { paths: [runtime] }));
const mermaidModule = require.resolve('mermaid', { paths: [runtime] });
const mermaidScript = path.join(path.dirname(mermaidModule), 'mermaid.min.js');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'diagram_manifest.json')));
const samples = new Set(['01-platform-map-1','03-integration-runtimes-1','05-datasets-and-paths-1','11-watermarks-1','13-rest-copy-1','18-triggers-windows-events-1','26-azure-devops-ci-1','30-worked-lab-1','01-on-prem-migration-1','12-release-maintenance-1']);
const rendered = path.join(root, 'rendered');
fs.mkdirSync(rendered, { recursive: true });
(async () => {
  const launch = { headless: true };
  if (process.env.DESIGN_CHROMIUM_PATH) launch.executablePath = process.env.DESIGN_CHROMIUM_PATH;
  const browser = await playwright.chromium.launch(launch);
  const report = [], errors = [];
  let next = 0;
  try {
    const workers = Array.from({ length: 4 }, async (_, worker) => {
      const page = await browser.newPage({ viewport: { width: 1600, height: 1600 }, deviceScaleFactor: 1 });
      await page.setContent('<!doctype html><html><head><style>body{margin:0;padding:12px;background:white;}svg{display:block;}*{box-sizing:border-box;}</style></head><body></body></html>');
      await page.addScriptTag({ path: mermaidScript });
      await page.evaluate(() => mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: 'base', fontFamily: 'Arial',
        themeVariables: { fontFamily: 'Arial', fontSize: '16px', primaryColor: '#eff6ff', primaryTextColor: '#0f172a', primaryBorderColor: '#475569', lineColor: '#475569', secondaryColor: '#f8fafc', tertiaryColor: '#ffffff' },
        flowchart: { htmlLabels: true, useMaxWidth: false, curve: 'linear' }, sequence: { useMaxWidth: false, wrap: true, actorMargin: 45 } }));
      while (next < manifest.length) {
        const index = next++, diagram = manifest[index];
        try {
          const result = await page.evaluate(async ({ diagram, index }) => {
            await mermaid.parse(diagram.source);
            const { svg } = await mermaid.render(`design_${index}`, diagram.source);
            document.body.innerHTML = svg;
            await document.fonts.ready;
            const element = document.querySelector('svg');
            const view = element.viewBox.baseVal;
            const nodes = [...element.querySelectorAll('g.node')].map(n => {
              const b = n.getBoundingClientRect();
              const shape = n.querySelector('rect, polygon, circle, ellipse, path');
              const text = n.querySelector('.label');
              const sb = shape?.getBoundingClientRect(), tb = text?.getBoundingClientRect();
              return { x: b.x, y: b.y, w: b.width, h: b.height, label: n.textContent.trim(),
                clipped: !!(sb && tb && (tb.left < sb.left-1 || tb.right > sb.right+1 || tb.top < sb.top-1 || tb.bottom > sb.bottom+1)) };
            });
            let overlaps = 0;
            for (let i = 0; i < nodes.length; i++) for (let j = i+1; j < nodes.length; j++) {
              const a=nodes[i],b=nodes[j];
              if (Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>1 && Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>1) overlaps++;
            }
            return { svg, width: view.width, height: view.height, nodes: nodes.length,
              overlappingNodePairs: overlaps, clippedLabels: nodes.filter(n=>n.clipped).map(n=>n.label), textElements: element.querySelectorAll('text,foreignObject').length };
          }, { diagram, index });
          if (!result.width || !result.height || !result.textElements) throw new Error('Empty render');
          if (result.overlappingNodePairs || result.clippedLabels.length) throw new Error(`Layout defect: ${JSON.stringify({overlaps:result.overlappingNodePairs,clipped:result.clippedLabels})}`);
          if (samples.has(diagram.id)) {
            fs.writeFileSync(path.join(rendered, `${diagram.id}.svg`), result.svg);
            await page.locator('svg').screenshot({ path: path.join(rendered, `${diagram.id}.png`) });
          }
          delete result.svg;
          report.push({ id: diagram.id, sourceSha256: crypto.createHash('sha256').update(diagram.source).digest('hex'), ...result, status: 'passed' });
        } catch (error) { errors.push({ id: diagram.id, message: error.message }); }
        if ((index+1)%50===0) process.stdout.write(`Rendered ${index+1}/${manifest.length}\n`);
      }
      await page.close();
    });
    await Promise.all(workers);
  } finally { await browser.close(); }
  report.sort((a,b)=>a.id.localeCompare(b.id));
  const output={researchDate:'2026-10-13', mermaidVersion: JSON.parse(fs.readFileSync(path.resolve(path.dirname(mermaidModule), '..', 'package.json'))).version,
    checked:report.length, errors, checks:['Mermaid parse','SVG render','Nonempty geometry and labels','No overlapping flowchart node bounds','No labels outside flowchart node shapes'], diagrams:report};
  fs.writeFileSync(path.join(root, 'diagram_validation.json'),JSON.stringify(output,null,2)+'\n');
  if (errors.length) { process.stderr.write(JSON.stringify(errors,null,2)+'\n'); process.exitCode=1; }
  else process.stdout.write(`PASS: parsed and rendered ${report.length} diagrams; ${samples.size} static examples exported.\n`);
})().catch(error=>{process.stderr.write(error.stack+'\n');process.exitCode=1;});
