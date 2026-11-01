// Sitenin derlenmiş dosyalarını üretir (npm run build):
//  - assets/site.css : index.html'de kullanılan Tailwind sınıfları (tarayıcıda Tailwind çalıştırmaya gerek kalmaz)
//  - assets/icons.js : yalnızca sitede kullanılan Lucide ikonları (tüm ikon kütüphanesi yerine birkaç KB)
// index.html'e yeni bir Tailwind sınıfı ya da data-lucide ikonu eklenince yeniden çalıştırın (GitHub Actions bunu otomatik yapar).
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { createHash } from 'node:crypto';
import { icons } from 'lucide';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const html = readFileSync(join(root, 'index.html'), 'utf8');
mkdirSync(join(root, 'assets'), { recursive: true });

const pascal = s => s.replace(/(^|-)([a-z0-9])/g, (_, __, c) => c.toUpperCase());
const names = [...new Set([...html.matchAll(/data-lucide="([a-z0-9-]+)"/g)].map(m => m[1]))].sort();
const out = {};
for (const n of names) {
  const node = icons[pascal(n)];
  if (!node) throw new Error('Lucide ikonu bulunamadı: ' + n);
  const children = Array.isArray(node[2]) ? node[2] : node;
  out[n] = children.map(([tag, attrs]) => '<' + tag + Object.entries(attrs).filter(([k]) => k !== 'key').map(([k, v]) => ' ' + k + '="' + v + '"').join('') + '/>').join('');
}
const js = `/* Otomatik üretildi: tools/build-assets.mjs — elle düzenlemeyin. Lucide v0.469.0 (ISC lisansı), yalnızca sitede kullanılan ${names.length} ikon. */
(function () {
  var I = ${JSON.stringify(out)};
  function createIcons() {
    var els = document.querySelectorAll('i[data-lucide]');
    for (var i = 0; i < els.length; i++) {
      var el = els[i], n = el.getAttribute('data-lucide'), body = I[n];
      if (!body) continue;
      var cls = el.getAttribute('class') || '';
      var tmp = document.createElement('span');
      tmp.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" data-lucide="' + n + '" class="lucide lucide-' + n + (cls ? ' ' + cls : '') + '">' + body + '</svg>';
      el.parentNode.replaceChild(tmp.firstChild, el);
    }
  }
  window.lucide = { createIcons: createIcons };
  if (document.readyState !== 'loading') createIcons(); else document.addEventListener('DOMContentLoaded', createIcons);
})();
`;
writeFileSync(join(root, 'assets', 'icons.js'), js);
console.log('assets/icons.js: ' + names.length + ' ikon, ' + js.length + ' bayt');

const bin = join(root, 'node_modules', 'tailwindcss', 'lib', 'cli.js');
execFileSync(process.execPath, [bin, '-c', join(root, 'tailwind.config.cjs'), '-i', join(root, 'tools', 'tailwind.css'), '-o', join(root, 'assets', 'site.css'), '--minify'], { stdio: 'inherit', cwd: root });
console.log('assets/site.css: ' + readFileSync(join(root, 'assets', 'site.css')).length + ' bayt');

// tarayıcı önbelleği: dosya içeriği değişince index.html'deki ?v= damgası da değişir
const stamp = f => createHash('sha1').update(readFileSync(join(root, 'assets', f))).digest('hex').slice(0, 8);
const page = readFileSync(join(root, 'index.html'), 'utf8');
const next = page.replace(/assets\/(site\.css|icons\.js)\?v=[\w]*/g, (_, f) => 'assets/' + f + '?v=' + stamp(f));
if (next !== page) { writeFileSync(join(root, 'index.html'), next); console.log('index.html sürüm damgaları güncellendi'); }
