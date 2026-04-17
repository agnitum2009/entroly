<p align="center">
  <img src="https://raw.githubusercontent.com/juyterman1000/entroly/main/docs/assets/logo.png" width="180" alt="Entroly">
</p>

<h1 align="center">Entroly Daemon</h1>

<h3 align="center">당신의 AI는 장님입니다. 30초 만에 고치세요 — 그리고 스스로 진화하는 걸 지켜보세요.</h3>

<p align="center">
  <i>Claude, Cursor, Copilot, Codex, MiniMax는 코드베이스의 5%만 봅니다. Entroly는 <b>90% 적은 비용으로 200만 토큰의 두뇌</b>를 제공합니다 — <b>지속적으로 자기 진화하며, 컨텍스트를 압축하고 새로운 스킬을 자율적으로 학습하는 데몬. 단 하나의 집착: 더 많은 토큰을 절약하고 모든 답변을 날카롭게</b>. 학습이 증명 가능하게 토큰-네거티브인 최초의 AI 런타임.</i>
</p>

---

## 실제 효과

| | Entroly 없이 | **Entroly 사용** |
|---|---|---|
| AI가 보는 파일 | 5–10개 | **전체 저장소** |
| 요청당 토큰 | ~186,000 | **9,300 – 55,000** |
| 1K 요청당 비용 | ~$560 | **$28 – $168** |
| 유효 컨텍스트 윈도우 | 200K | **~2M (가변 해상도 압축)** |
| 시간 경과에 따른 학습 비용 | 증가 (토큰) | **$0 — 증명 가능한 토큰-네거티브** |
| 설정 | 수 시간의 프롬프트 해킹 | **30초** |

---

## 설치

```bash
npm install entroly-wasm && npx entroly-wasm
# 또는
pip install entroly && entroly go
```

그게 전부입니다. IDE를 자동 감지하고 Claude/Cursor/Copilot/Codex/MiniMax에 연결하여 압축을 시작합니다.

---

## 왜 더 똑똑해지는 데 $0인가 — 3가지 기둥

**1. 토큰 이코노미** — `ValueTracker`가 평생 절감액 `S(t)`를 측정. 진화 예산은 엄격하게 제한: `C_spent(t) ≤ τ · S(t) (τ = 5%)`

**2. 구조적 귀납 ($0)** — 토큰을 건드리기 전에 결정론적 합성기가 AST, 의존성 엣지, 엔트로피 기울기를 읽고 작동하는 도구를 생성. LLM 없음. 임베딩 없음. 클라우드 없음.

**3. 드리밍 루프** — 60초 이상 유휴 시, 시스템이 합성 쿼리를 생성하고, 점수 가중치를 교란하며, 벤치마크에 대해 셀프 플레이. 엄격한 개선만 유지; 퇴보는 폐기.

---

<p align="center">
  <a href="https://github.com/juyterman1000/entroly">⬅ 메인 README로 돌아가기</a>
</p>
