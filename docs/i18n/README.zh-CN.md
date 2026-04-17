<p align="center">
  <img src="https://raw.githubusercontent.com/juyterman1000/entroly/main/docs/assets/logo.png" width="180" alt="Entroly">
</p>

<h1 align="center">Entroly Daemon</h1>

<h3 align="center">你的AI是盲的。30秒修复——然后看它自我进化。</h3>

<p align="center">
  <i>Claude、Cursor、Copilot、Codex 和 MiniMax 只能看到你代码库的5%。Entroly 为它们提供 <b>200万token的大脑，成本降低90%</b>——一个<b>持续自我进化的守护进程，压缩你的上下文并自主学习新技能，唯一的执念：节省更多token，提升每一个回答的质量</b>。首个学习过程被证明是token负增长的AI运行时。</i>
</p>

---

## 实际效果

| | 没有 Entroly | **使用 Entroly** |
|---|---|---|
| AI能看到的文件 | 5–10个 | **整个代码库** |
| 每次请求的token数 | ~186,000 | **9,300 – 55,000** |
| 每1K请求成本 | ~$560 | **$28 – $168** |
| 有效上下文窗口 | 200K | **~2M（通过可变分辨率压缩）** |
| 长期学习成本 | 持续增长（token） | **$0 — 可证明的token负增长** |
| 设置时间 | 数小时的提示词调优 | **30秒** |

关键文件完整传输。支持文件以签名形式传输。其余作为引用。你的AI获得全局视野，而你几乎不需要为此付费。

---

## 安装

```bash
npm install entroly-wasm && npx entroly-wasm
# 或者
pip install entroly && entroly go
```

就是这样。它会自动检测你的IDE，接入Claude/Cursor/Copilot/Codex/MiniMax，并开始压缩。

---

## 为什么变得更智能是零成本——三大支柱

**1. Token经济** — `ValueTracker` 测量终身节省 `S(t)`。进化预算被严格限制：`C_spent(t) ≤ τ · S(t)（τ = 5%）`

**2. 结构归纳（$0）** — 在触及任何token之前，确定性合成器读取你代码的AST、依赖边和熵梯度，并生成可工作的工具。无需LLM、无需嵌入、无需云端。

**3. 梦境循环** — 当空闲超过60秒时，系统生成合成查询，扰动评分权重，并针对基准进行自我博弈。严格的改进被保留；退化被丢弃。

---

<p align="center">
  <a href="https://github.com/juyterman1000/entroly">⬅ 返回主README</a>
</p>
