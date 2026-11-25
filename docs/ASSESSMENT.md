# Phase 0 Assessment — Autonomous Crypto Quant Trading Platform

*Prepared 2026-11-25. Status: draft for owner review. Nothing here is a backtest result or a return forecast. No market data has been analyzed yet.*

> **How to read this document.** Each section answers one of the twelve first-assignment questions. Where a fact comes from an outside source, the source is listed in §13. Fee figures marked **[VERIFY]** came from secondary sources. They must be confirmed inside your own exchange account before we rely on them.

---

## 1. Independent feasibility assessment

### Short answer
- **Technically feasible.** A single person can build a reliable, low-frequency, automated spot trading system. It can run on about $15–25/month of infrastructure. The engineering is a solved problem.
- **Financially, the goal as stated is unlikely to be met.** That goal is "meaningful supplemental income" from $5,000. Here is the arithmetic, using illustrative numbers only:

| Assumption (illustrative, not a forecast) | Value |
|---|---|
| Capital | $5,000 |
| Hypothetical return *above* simply holding BTC/ETH (an optimistic edge) | 10%/yr |
| Dollar value of that edge | $500/yr |
| Infrastructure + data + tools | −$200 to −$400/yr |
| Your time (≈1.5 h/week × 52) | ≈78 hours |
| **Implied value of your time** | **≈ $1–4/hour, before tax** |

At $5,000, infrastructure alone (~$300/yr) is a **6% annual hurdle** the strategy must clear before it earns anything. The economics only start to make sense at much larger capital. More capital is only justified after the edge has been proven, and proving it takes a long time (see §8).

### What success realistically looks like
Treat the next 12–18 months as a **research program**, not a business launch. Realistic good outcomes, in order of likelihood:
1. **The most likely result:** the evidence shows no strategy beats a simple, cheap, passive allocation after costs and taxes. You learn this for a few hundred dollars instead of losing thousands. This is a legitimate success, and I will tell you plainly if it happens.
2. **A plausible result:** a slow trend-following / risk-control overlay on BTC and ETH gives *similar* returns to holding them, with *meaningfully smaller drawdowns*. That is valuable as risk management, but it is not an "income" machine.
3. **The least likely result:** a durable, statistically credible edge that justifies scaling capital.

### Things that hurt this project specifically
- **Fees for small US accounts are very high right now.** Secondary sources report Coinbase Advanced's entry tier for US customers at roughly **0.50% maker / 0.90% taker** after a September 2026 fee change. Older guides cite 0.40–0.60% maker and 0.60–1.20% taker. Kraken Pro's July 2026 Tier 1 is reported at **0.40% maker / 0.80% taker**. **[VERIFY all]** A round trip (buy + sell) therefore costs about **0.8%–1.8%**. A strategy that trades fully in and out 20 times a year would pay **16–36% of capital per year in fees.** **This one fact eliminates most "active" strategies for us.**
- **Taxes.** Every sale is a taxable event. Short-term gains are taxed at ordinary income rates. Buy-and-hold defers tax and can qualify for long-term rates. Every strategy will be compared to benchmarks **after estimated tax drag**, not just before.
- **Statistics.** Crypto has only about 10–12 years of usable history, and only a few full bull/bear cycles. With low-frequency strategies, the number of independent observations is small. Distinguishing real skill from luck is genuinely hard (see §8).

### Verdict
**Proceed, with a reframed objective and strict gates.** The primary objective becomes:

> *Determine whether any systematic, low-turnover spot strategy beats BTC/ETH buy-and-hold and a cash benchmark on a **risk-adjusted, after-cost, after-tax** basis, with statistical credibility. Stop and recommend passive investing if it does not.*

---

## 2. Competitive position of an individual AI-assisted crypto trader

| Advantages (real) | Disadvantages (real) |
|---|---|
| **Small size.** $5k can enter and exit BTC/ETH with essentially zero market impact. | **Fees.** Retail tier fees are about 10–50× what professional firms pay. Speed- and arbitrage-based edges are closed to us. |
| **Patience.** No clients, no quarterly reporting, no career risk. You can hold cash for months, or hold a slow strategy through years of underperformance. Institutions often can't. | **Speed.** Professional firms co-locate servers and react in microseconds. Anything that depends on being first is already taken. |
| **Freedom of mandate.** You can trade small, less-crowded edges that are too small for a fund. *In practice, our fees mostly cancel this out.* | **Data.** Professionals buy order-book, on-chain and alternative data that costs thousands of dollars a month. |
| **Cheap engineering.** AI-assisted development lowers the cost of building and testing to near zero. | **Crowding.** Public strategies (moving-average crosses, RSI) have been tested by millions of people. Any edge in them has been arbitraged down. |
| **Discipline.** Automation removes emotional trading, which is a well-documented source of retail underperformance. | **AI is not an edge in itself.** Every competitor has the same models. AI makes *research* cheaper. It does not make *prediction* better. |

**Bottom line.** Our only realistic edges are **patience** and **behavioral discipline**. Those two favor **slow, rules-based, risk-managed strategies**. They give us no advantage in speed, arbitrage or prediction.

---

## 3. Build from scratch vs. established framework

| Criterion | **Freqtrade** | **Hummingbot** | **Custom "thin" Python platform** (recommended) |
|---|---|---|---|
| Designed for | Candle-based directional bots across many pairs | Market making and arbitrage (high frequency) | Exactly our use case: slow, portfolio-level rebalancing |
| Coinbase support | **Not on its supported list** in any source I found. Kraken is supported, but backtest data must be rebuilt from raw trades, which is slow and RAM-heavy. **[VERIFY on freqtrade.io; the site was unreachable from this environment]** | Has a `coinbase_advanced_trade` spot connector. Its listed V2-strategy support is unclear. | Coinbase's official Python SDK, plus `ccxt` as a cross-exchange fallback |
| Validation tooling | Backtesting, plus "hyperopt" (mass parameter optimization). Hyperopt **encourages overfitting**. There's no built-in deflated Sharpe, holdout locking or trial registry. | Limited for directional strategies | We build exactly the validation you specified (§8). Libraries do the maths. |
| Portfolio-level logic | Weak: it thinks in per-pair trades | Weak | Native |
| Learning curve for you | Moderate (config files, strategy classes) | High | Low: plain-English config and a dashboard |
| Maintenance | Monthly releases; you inherit their changes and breaking upgrades | Active, but crypto-HFT focused | Small codebase (a few thousand lines) that we own; the risk is our own bugs |
| Cost | Free (open source) | Free (open source) | Free (open-source libraries) |

**Recommendation: a custom thin platform built on established libraries. No trading framework.**

The reasoning:
1. Our strategies make decisions **once a day or once a week**. Execution is simple: compute a target allocation, then place a few limit orders. A framework's main value is handling complex, high-frequency execution, and we don't need that.
2. The **hard and valuable part** is the validation and risk layer. Neither framework provides it the way you specified.
3. Freqtrade's lack of Coinbase support and its overfitting-prone optimizer conflict with two of your core requirements.
4. We still **don't reinvent anything**. We use `pandas`/`numpy` (data), `ccxt` and Coinbase's SDK (exchange access), `scipy`/`statsmodels` (statistics), SQLAlchemy and PostgreSQL (records), and Streamlit (dashboard).

**Fallback.** If we later move to Kraken and want many pairs and faster strategies, Freqtrade becomes a reasonable choice for *execution only*. Strategies validated in our framework could be ported to it.

**Main risk of this choice:** bugs in our own order-handling code. We mitigate it with four layers: an independent risk gate, a paper-trading phase, reconciliation against the exchange, and automated tests.

---

## 4. Recommended technical architecture

```
                        ┌──────────────── DigitalOcean droplet (Ubuntu, Docker Compose) ────────────────┐
 Coinbase public API ──►│ [1] Data collector ──► PostgreSQL ◄── [6] Reporter (daily/weekly; optional AI)  │
                        │                         ▲   ▲                                                   │
                        │ [2] Strategy engine ────┘   │       [7] Dashboard (Streamlit, private access)    │
                        │     (targets only, no orders)│            │ emergency-stop button                 │
                        │          │                   │            ▼                                       │
                        │          ▼                   │       kill-switch flag (DB + file)                 │
                        │ [3] RISK GATE (independent, hard-coded limits, read-only config, approves/denies) │
                        │          │                                                                        │
                        │          ▼                                                                        │
                        │ [4] Executor ── paper broker (default)  |  live broker (disabled; needs 2 keys)   │
                        │          │                                                                        │
                        │ [5] Reconciler: compares our ledger to exchange balances every cycle + at startup │
                        └──────────┼────────────────────────────────────────────────────────────────────────┘
                                   ▼
                     Coinbase Advanced Trade API (key scope: view + trade only; no transfer/withdraw; IP-allowlisted)

  Off-box: GitHub (code) · encrypted nightly DB backups (DO Spaces / Backblaze) · Healthchecks.io (dead-man alarm)
           · Telegram/Pushover alerts · Tailscale (private network; no public SSH or dashboard ports)
```

**Key design principles (in business terms):**
- **Separation of duties.** Strategies can only *propose* a target portfolio. They cannot place orders. The risk gate is separate code with its own tests. Its limits live in a config file that strategies and AI cannot write to. Think of it as a trader who cannot sign checks and a controller who cannot trade.
- **Two-key live trading.** Live mode needs *both* an environment setting on the server *and* a signed approval record in the database that names the strategy version and capital limit. Paper mode is the default and the fallback.
- **Event-sourced ledger.** Every decision, order, fill, fee and reconciliation is written as an append-only record. That gives you full auditability and tax exports.
- **Fail safe, not fail open.** On stale data, API errors, an unexpected balance or a failed reconciliation, the system **stops opening new positions** and alerts you. It does *not* panic-sell. Panic-selling into a crash is itself a risk.
- **Product allow-list.** Even a stolen API key can only trade the 2–10 approved coins. This blocks the known attack where hackers use a hijacked account to buy an illiquid coin they are dumping.

**Database.** PostgreSQL from the paper-trading phase onward. In the research phase, data is stored as local Parquet files, which is fast and simple. Code goes through SQLAlchemy, so the storage layer is swappable.

**Secrets.** The API key lives in a root-only file on the server, injected as a Docker secret. It is never in Git, never in chat, and never in logs. You will create the key yourself in Coinbase's web UI and paste it directly into the server via a guided command. I never see it.

---

## 5. Phased development roadmap

| Phase | Goal | Exit gate (all required) | Rough duration |
|---|---|---|---|
| **0. Assessment** (this doc) | Agree on objective, architecture and constraints | Your written decisions in `DECISION_LOG.md` | Now |
| **1. Data & benchmarks** | Clean multi-year price history; realistic cost model; benchmark results (BTC, ETH, BTC/ETH mix, cash); trial registry | Data quality report passes; benchmarks reproduce public price history | 1–2 weeks |
| **2. Strategy research** | Test the §7 candidates under the §8 protocol | ≥1 strategy reaches "Approve for paper", **or** we recommend passive investing and stop | 3–6 weeks |
| **3. Paper trading platform** | Cloud deployment, risk gate, paper executor on live prices, dashboard, alerts, reports | 90+ days of continuous running; zero unexplained reconciliation breaks; execution costs within modeled range | 3–4 weeks build + ≥90 days run |
| **4. Live pilot** | $250–500 real capital, same frozen strategy version | ≥90 days; real fills match paper; no risk-control failures; your explicit approval | ≥90 days |
| **5. Scale / extend** | Step capital toward $5k in tranches. Optionally research derivatives (funding-rate carry) under separate approval. | Each step needs evidence **and** your sign-off | Ongoing |

**Earliest real-money date: roughly 5–7 months from now**, and only if every gate passes. **There is a meaningful chance we stop at the end of Phase 2.** That would be the system working as designed.

---

## 6. Estimated costs

### Development
- **Your time:** about 3–6 h/week during Phases 1–3 (decisions, reviewing reports, account setup). Then about 1–2 h/week.
- **AI development time:** covered by your existing Claude plan. No contractor costs are assumed.

### Recurring operating costs (estimates; verify at signup)

| Item | Research (Ph 1–2) | Paper/Live (Ph 3+) | Notes |
|---|---|---|---|
| Cloud server (DigitalOcean Basic droplet) | $0–6 | $12–24 | 2 GB plans reported at ~$12/mo, 4 GB at ~$24/mo **[VERIFY]**. Start at 2 GB. |
| Droplet backups | — | $2–5 | Roughly 20% of the droplet price |
| Off-site backup storage (Backblaze B2 / DO Spaces) | — | $1–5 | |
| Domain name (optional) | — | ~$1 | Not needed if we use Tailscale |
| Tailscale, Healthchecks.io, GitHub, Telegram | $0 | $0 | Free tiers are sufficient |
| Market data | $0 | $0 | Exchange public APIs are free |
| AI API for report narration (optional) | $0 | $2–10 | Only if it proves useful; a capped budget |
| Crypto tax software | — | $50–200/yr | Needed once live trading starts |
| **Total** | **≈ $0–10/mo** | **≈ $18–45/mo** | Within your $25 infrastructure / $100 research targets |

**Trading costs are separate, and they are the largest cost.** Every strategy is charged modeled fees, spread and slippage. These are stress-tested at 2× and 3× the expected level.

---

## 7. Prioritized strategy list

The ranking criteria are published evidence, survival under our fees, fit with spot-only/no-leverage, and low turnover. **No strategy is assumed profitable.**

| # | Strategy | Why it's on the list | Main concern | Priority |
|---|---|---|---|---|
| 0 | **Benchmarks:** BTC buy-and-hold, ETH buy-and-hold, 50/50 BTC/ETH (rebalanced quarterly), cash (T-bill yield), monthly dollar-cost averaging | The bar every strategy must clear | — | **Required** |
| 1 | **Time-series trend following** on BTC/ETH, daily data, weekly decisions. Hold when the multi-horizon trend is positive, otherwise hold cash. | The strongest published evidence. Time-series momentum is documented across asset classes (Moskowitz, Ooi & Pedersen 2012) and specifically in crypto (Liu & Tsyvinski 2021). Low turnover. Its main benefit is avoiding deep bear-market drawdowns. | Whipsaws in sideways markets; few independent trades | **High** |
| 2 | **Volatility targeting / risk scaling**, as an overlay on #1 or on buy-and-hold. Hold less when the market is turbulent. | Well-established risk-management technique; improves risk-adjusted returns in many asset classes | Turnover; needs "no-trade bands" to control fees | **High** |
| 3 | **Market regime detection**, as a *filter* rather than a standalone strategy (trend/volatility state, simple statistical regime models) | Can switch strategies on or off by regime | Very easy to overfit; must add value beyond #1 itself | **Medium** |
| 4 | **Volatility breakout** (e.g., new N-day high, daily data) | A close cousin of trend following, with different entry timing | Likely redundant with #1; we test it as a variant, not a separate bet | **Medium** |
| 5 | **Cross-sectional momentum / rotation** among the top 5–10 liquid coins, monthly | Documented in academic crypto studies | **Survivorship bias:** coins that died vanish from the data. Altcoins are much riskier. Higher fees from more pairs. | **Medium–Low** |
| 6 | **Short-horizon mean reversion** | Common retail strategy | Needs many trades with small gains. At 0.8–1.8% round-trip fees, almost certainly unprofitable for us. | **Low:** one quick test to document the rejection |
| 7 | **Statistical arbitrage (pairs)** | Classic quant strategy | Needs short selling, which is excluded. Long-only versions are weak. | **Deferred** |
| 8 | **Funding-rate arbitrage** (cash-and-carry) | Real, well-understood carry trade | Needs derivatives and a short position, which are excluded. US access exists via Coinbase's US "perpetual-style" futures; the details need verification. | **Deferred to Phase 5**; we can *record* funding data now for later research |
| 9 | **Cross-exchange arbitrage** | Frequently pitched to retail | Price gaps are smaller than our fees; transfers take minutes; professionals dominate; capital is split across venues | **Rejected** (documented) |
| — | **AI/ML price prediction, sentiment or news trading** | Popular | Weak evidence at retail scale, high overfitting risk, API costs | **Not now**; revisit only with specific hypotheses |

---

## 8. Strategy validation methodology

### 8.1 Protocol (performed in this order, with no skipping)
1. **Pre-register.** Before any test, the strategy's rules, parameter ranges and rationale are written to `strategies/<name>/SPEC.md` and committed to Git. This prevents "inventing the story after seeing the result."
2. **Trial registry.** Every backtest run is logged automatically, including the failures. The total count feeds the multiple-testing correction in step 6.
3. **Data split** (proposed; your decision D5):
   - **Development:** start of reliable data through 2022 (includes the 2017–18 and 2021–22 bull/bear cycles)
   - **Validation (walk-forward):** 2023 through mid-2025
   - **Locked holdout:** the most recent ~17 months. Its file is checksummed and **opened once per strategy version**, at the end.
4. **Walk-forward testing.** Parameters are chosen using only past data, then tested on the next unseen window, rolling forward. The system never "sees the future."
5. **Realistic costs.** Taker fees on market orders, maker fees plus fill-uncertainty on limit orders, the measured bid-ask spread, slippage, a one-candle execution delay, and a random failed-order rate. **Stress tests run at 2× and 3× costs.**
6. **Statistical significance.**
   - Bootstrap confidence intervals that preserve the time structure of returns ("block bootstrap")
   - **Deflated Sharpe Ratio** (Bailey & López de Prado 2014), which corrects the Sharpe ratio for the number of trials and for non-normal crypto returns
   - **Probability of Backtest Overfitting** (Bailey et al.), which measures how often the "best" in-sample setting underperforms out of sample
   - A strict significance threshold (t-stat around 3) for any claimed edge, following Harvey, Liu & Zhu (2016)
7. **Robustness.** Results must hold across a *plateau* of nearby parameter values, not one lucky spike. They must also hold for BTC and ETH separately, and in each market regime (bull, bear, sideways, high volatility, low liquidity).
8. **Benchmark comparison.** Each strategy is compared to the benchmarks before costs, after costs, and after estimated taxes.

### 8.2 An honest note on statistical power
The standard error of an annual Sharpe ratio is roughly √((1 + ½·SR²) / years) (Lo 2002). With about 10 years of data, that is **±0.3–0.4**. **That means a backtest cannot reliably tell a good strategy (Sharpe 1.0) from buy-and-hold BTC.** We will therefore lean heavily on *economic logic, robustness and drawdown reduction*, not on headline returns.

The same applies to paper trading. **90 days of paper trading proves the machinery works. It proves almost nothing about whether the strategy has an edge.** Reports will state this explicitly.

### 8.3 Stage-gate screening

| Decision | Requires |
|---|---|
| **Reject** | Negative after-cost excess return vs the appropriate benchmark, **or** collapse under 2× costs, **or** a fragile parameter spike, **or** a holdout failure |
| **Investigate further** | Positive but not significant; or works in only some regimes; or too few trades/exposure to judge |
| **Approve for paper trading** | Survives walk-forward + 2× costs + holdout; parameter plateau; Deflated Sharpe probability ≥ ~0.90 **or** a clear drawdown-reduction benefit with similar returns; economic rationale documented |
| **Candidate for live pilot** | Paper ≥90 days, real-time behavior within the backtest's expected range, execution costs ≤ modeled, zero unresolved operational incidents, **your written approval** |

Thresholds are judged *together* with sample size and exposure. No single number decides alone. Each metric is explained in plain English in the scorecard (built in Phase 1).

---

## 9. Risk assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **No real edge (strategies only fit history)** | **High** | Medium (the money is lost slowly) | §8 protocol, holdout, small pilot, passive fallback |
| **Fee drag erodes returns** | High | High | Low-turnover strategies, limit orders, rebalance bands, 2–3× cost stress |
| **Crypto market crash (−50% to −80% has happened repeatedly)** | Medium per year | High | Exposure caps, trend filter, drawdown circuit breaker, small allocation |
| **Software bug places wrong orders** | Medium | High | Independent risk gate, order-size sanity checks, duplicate-order IDs, paper phase, tests |
| **API key theft** | Low | High | Trade+view scope only, **no withdrawal or transfer permission**, IP allow-list, product allow-list, dedicated Coinbase portfolio/sub-account **[VERIFY availability]** |
| **Exchange failure/insolvency** | Low | Very high | Use a regulated US exchange; keep only the trading allocation there |
| **Stale or bad market data** | Medium | Medium | Freshness checks; cross-check against a second source; halt on anomalies |
| **Outage, partial fills, restart mid-order** | Medium | Medium | Client order IDs (idempotent), reconciliation at startup and every cycle, halt-on-mismatch |
| **Server downtime** | Medium | Low (slow strategies tolerate hours of downtime) | Docker auto-restart, external dead-man alarm, daily backups |
| **Dashboard compromise** | Low | High | Private network only (Tailscale), 2FA, no public ports; emergency stop available but **no trading controls exposed publicly** |
| **Tax complexity / short-term gains** | Certain | Medium | Full ledger with cost basis per lot; tax-software export; CPA consultation before going live |
| **Regulatory changes** | Medium | Medium | Spot-only on a US-regulated exchange; review annually |
| **Owner over-confidence after a good streak** | Medium | High | Pre-agreed capital-scaling rules; conservative reports; every change needs a new version and revalidation |

### Proposed initial hard limits (live pilot; final values decided in Phase 3)

| Control | Proposed value |
|---|---|
| Maximum single position | 60% of strategy capital (BTC or ETH) |
| Maximum total crypto exposure | 100% of allocated capital, no leverage (enforced by spot-only) |
| Daily loss halt | −8% of portfolio (crypto moves 5–10% in a day fairly often; tighter limits would trigger constantly) |
| Cumulative drawdown kill-switch | −25% from peak → flatten to cash and require your approval to resume |
| Maximum orders per day | 10 |
| Maximum single order size | 25% of capital; larger moves are split |
| Data freshness | Halt new orders if price data is >5 min old during execution |
| Abnormal volatility | Pause if a 1-hour move is >15% (a possible flash crash or bad data) |
| Reconciliation tolerance | Any balance mismatch >0.5% of the position → halt + alert |
| Live trading | **Off by default**; enabling it needs two separate actions |

---

## 10. Simplest viable first version (MVP)

**"Version 0.1: one strategy, paper only, two coins."**
- **Universe:** BTC-USD and ETH-USD on Coinbase.
- **Strategy:** one pre-registered trend-following rule with volatility scaling, evaluated once per day. It trades only when the target changes meaningfully.
- **Paper broker:** simulated fills at live Coinbase prices, with modeled fees and spread.
- **Risk gate:** the limits above, enforced in code.
- **Records:** append-only ledger in PostgreSQL; CSV exports.
- **Outputs:** a daily Telegram summary, a weekly report, and a simple Streamlit dashboard showing equity, positions, trades, benchmark comparison, health and the emergency stop.
- **Not included in v0.1:** live trading, AI features, extra exchanges, altcoins, derivatives.

It is deliberately boring. If v0.1 can't beat benchmarks after costs, adding complexity is far more likely to add overfitting than profit.

---

## 11. Accounts, software and resources you will need

| When | Item | Purpose | Cost |
|---|---|---|---|
| **Now** | **GitHub account + private repository** | Stores code and documentation; lets future Claude sessions resume | Free |
| Now | **Password manager** (1Password or Bitwarden) and an authenticator app, ideally a hardware security key | Protects every account below | $0–36/yr |
| Now | **Coinbase account** (verified) | Read your actual fee tier from the logged-in fee page | Free |
| Phase 1 | Allow this cloud environment to reach Coinbase's **public** market-data API | Download price history; no keys involved | Free |
| Phase 3 | **DigitalOcean** account | Hosting | ≈$15–30/mo |
| Phase 3 | **Tailscale** account | Private, secure access to the server and dashboard from your phone | Free |
| Phase 3 | **Telegram** (or Pushover) | Alerts and daily summaries | Free / $5 one-time |
| Phase 3 | **Healthchecks.io** | Alerts you if the system goes silent | Free |
| Phase 3 (optional) | Anthropic API key, spending cap ≤ $10/mo | AI-written report narrative | Usage-based |
| Phase 4 | **Coinbase Advanced Trade API key**: view + trade only, IP-restricted. *You create it; never paste it into chat.* | Live trading | Free |
| Phase 4 | Crypto tax software (e.g., Koinly, CoinTracker); one CPA consultation | Tax reporting | $50–200/yr + CPA fee |
| Optional | Kraken account | Second data source and backup exchange | Free |

**Please also tell me which US state you live in.** Exchange and product availability varies by state (New York's BitLicense rules, for example).

---

## 12. Milestone 1 — instructions

### Goal
A clean, verified multi-year price database for BTC and ETH. Also a realistic trading-cost model, benchmark results, and the trial registry. That gives us the measuring stick before any strategy is tested.

### Your tasks (about 1–2 hours total)
1. **Read this document and answer the decisions in `DECISION_LOG.md`** (D1–D6). Replying in chat is fine; I'll record your answers.
2. **Create a private GitHub repository** named `crypto-quant-platform`. Then connect it to Claude Code so this session can push to it. I'll walk you through it when you're ready.
3. **Check your real Coinbase fees.** Log in to Coinbase Advanced, open the fee tier page, and tell me the maker and taker percentages shown for your account. **Do not create API keys yet.**
4. **Approve network access** for this cloud workspace to reach Coinbase's public market-data endpoints. I'll trigger an approval prompt when we start; no account or key is involved.
5. Set up the password manager and two-factor authentication on GitHub and Coinbase if you haven't already.

### My tasks
1. Project structure, a Python environment, and automated tests.
2. Data downloader for daily and hourly BTC-USD/ETH-USD candles from Coinbase public APIs, with full history.
3. Data quality checks (gaps, duplicates, outliers, cross-check against a second source), with a plain-English report.
4. Cost model, parameterized by your actual fee tier.
5. Backtest engine core: no look-ahead, one-bar execution delay, fees, spread and slippage.
6. Benchmark report (buy-and-hold BTC, ETH, 50/50, monthly DCA, cash) covering every metric from your scorecard list, explained in plain English.
7. Trial registry and the locked-holdout mechanism.

### Milestone 1 is complete when
- The data quality report passes, and benchmark returns match independently known BTC/ETH price history.
- Tests pass, including deliberate "look-ahead trap" tests that the engine must catch.
- You have reviewed the benchmark report and confirmed the scorecard layout makes sense to you.

---

## 13. Sources

- Coinbase Advanced fees (help page): https://help.coinbase.com/en/coinbase/trading-and-funding/advanced-trade/advanced-trade-fees
- Coinbase fee change reporting, Sept 2026 (secondary): https://cryptodaily.co.uk/2026/09/coinbase-advanced-fees-usdc-vip-tiers · https://www.securities.io/coinbase-lowers-advanced-trading-fees-with-tiers-starting-at-10-000/ · https://primexbt.com/news/coinbase-cuts-advanced-platform-trading-fees-and-lowers-volume-threshold/
- Account-level fee variance report: https://stocktwits.com/news-articles/markets/cryptocurrency/coinbase-faces-criticism-for-fee-structure-again-nansen-ceo-calls-it-insane/cmUY2VlR49B
- Kraken Pro fee tiers (July 2026): https://blog.kraken.com/product/pro/new-kraken-pro-fee-tiers · https://www.kraken.com/pro/fees
- Freqtrade exchange notes (Kraken data caveats): https://codeclimate.com/github/freqtrade/freqtrade/docs/exchanges.md/source · Freqtrade review (2026): https://gainium.io/review/freqtrade
- Hummingbot Coinbase connector: https://hummingbot.org/exchanges/coinbase/ · Releases: https://hummingbot.org/release-notes/2.16.0/
- Coinbase US perpetual-style futures: https://www-marketing.coinbase.com/learn/futures/us-perpetual-style-futures-101 · https://crypto.news/coinbase-launches-regulated-alternative-to-offshore-crypto-perpetuals/
- DigitalOcean pricing: https://www.digitalocean.com/pricing/droplets · https://betterstack.com/community/guides/web-servers/digitalocean-review/ · https://www.temperstack.com/plans/digitalocean/
- IRS Form 1099-DA instructions: https://www.irs.gov/instructions/i1099da · https://koinly.io/de/blog/form-1099-da/
- Bailey & López de Prado, *The Deflated Sharpe Ratio* (2014): https://papers.ssrn.com/abstract=2460551
- Bailey, Borwein, López de Prado & Zhu, *The Probability of Backtest Overfitting* (2017, J. Computational Finance)
- Moskowitz, Ooi & Pedersen, *Time Series Momentum* (J. Financial Economics, 2012)
- Liu & Tsyvinski, *Risks and Returns of Cryptocurrency* (Review of Financial Studies, 2021)
- Harvey, Liu & Zhu, *…and the Cross-Section of Expected Returns* (Review of Financial Studies, 2016)
- Lo, *The Statistics of Sharpe Ratios* (Financial Analysts Journal, 2002)

*Note: the primary Coinbase, Freqtrade and DigitalOcean pages could not be opened from this environment's network. Figures from them are taken from search-result summaries and are marked [VERIFY].*
