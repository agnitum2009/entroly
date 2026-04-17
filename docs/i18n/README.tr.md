<p align="center">
  <img src="https://raw.githubusercontent.com/juyterman1000/entroly/main/docs/assets/logo.png" width="180" alt="Entroly">
</p>

<h1 align="center">Entroly Daemon</h1>

<h3 align="center">Yapay zekanız kör. 30 saniyede düzeltin — sonra kendi kendine öğrenmesini izleyin.</h3>

<p align="center">
  <i>Claude, Cursor, Copilot, Codex ve MiniMax kod tabanınızın yalnızca %5'ini görüyor. Entroly onlara <b>%90 daha az maliyetle 2M token'lık bir beyin</b> sağlar — <b>sürekli kendi kendini geliştiren, bağlamınızı sıkıştıran ve tek bir takıntıyla yeni beceriler öğrenen bir daemon: daha fazla token'ınızı kurtarmak ve her cevabı keskinleştirmek</b>. Öğrenmenin kanıtlanabilir şekilde token-negatif olduğu ilk AI çalışma zamanı.</i>
</p>

---

## Gerçekte ne elde ediyorsunuz

| | Entroly Olmadan | **Entroly ile** |
|---|---|---|
| AI'nın gördüğü dosyalar | 5–10 | **Tüm repo** |
| İstek başına token | ~186,000 | **9,300 – 55,000** |
| 1K istek başına maliyet | ~$560 | **$28 – $168** |
| Etkin bağlam penceresi | 200K | **~2M (değişken çözünürlüklü sıkıştırma)** |
| Zaman içinde öğrenme maliyeti | Artıyor (token) | **$0 — kanıtlanabilir token-negatif** |
| Kurulum | Saatlerce prompt hack | **30 saniye** |

---

## Kurulum

```bash
npm install entroly-wasm && npx entroly-wasm
# veya
pip install entroly && entroly go
```

Hepsi bu. IDE'nizi otomatik algılar, Claude/Cursor/Copilot/Codex/MiniMax'a bağlanır ve sıkıştırmaya başlar.

---

## Neden daha akıllı olmak $0 — 3 Sütun

**1. Token Ekonomisi** — `ValueTracker` ömür boyu tasarruf `S(t)`'yi ölçer. Evrim bütçesi kesinlikle sınırlıdır: `C_spent(t) ≤ τ · S(t) (τ = %5)`

**2. Yapısal Tümevarım ($0)** — Herhangi bir token'a dokunulmadan önce, deterministik sentezleyici kodunuzun AST'sini, bağımlılık kenarlarını ve entropi gradyanını okur. LLM yok. Gömme yok. Bulut yok.

**3. Rüya Döngüsü** — 60 saniyeden fazla boşta kaldığında, sistem sentetik sorgular üretir, puanlama ağırlıklarını perturbe eder ve kıyaslamalara karşı kendi kendine oynar.

---

<p align="center">
  <a href="https://github.com/juyterman1000/entroly">⬅ Ana README'ye dön</a>
</p>
