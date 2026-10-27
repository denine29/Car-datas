---
name: vehicle-price-research
description: 车型官网价格调研与采集。当用户要求"查某品牌某市场官网的价格/MSRP/价格表/价目/Excel/是否停售/车型清单"，或发来某品牌官网链接（如 xxx.es / xxx.gr / xxx.co.nz）时使用。覆盖多市场官方 MSRP 采集、价格口径核对、反爬站点绕过、统一格式 XLSX（8 列含燃油分类）交付。数据源必须为官方。
---

# 车型官网价格调研

为「某品牌 × 某市场」官网抓取全部在售车型**官方建议零售价（MSRP）**，交付统一格式 **XLSX（8 列，含燃油分类）**。

## 何时使用

- 用户发来汽车品牌官网 URL（`xxx.es` / `xxx.gr` / `xxx.co.nz` / `xxx.com.ph` …），默认意图 = 采该站在售车型官方价。
- 用户提到：查 MSRP / 价格表 / 价目 / 是否停售 / 生成 Excel / 核对车型清单。
- 用户说"下一个""继续"并给了新品牌链接 → 延续同一套规则。

---

## 一、输出格式（最高优先级，必须逐字遵守）

> 📂 **拿不准格式长什么样，先打开 `examples/`**：里面是 7 份**真实交付过**的成品（403 条的大表、17 条的车系级、多年款并列、印度 lakh 千分位、五动力混排都有），`examples/README.md` 说明了每份「要你看什么」，末尾还列了 6 条反面教材。

**只交付 XLSX，固定 8 列（2026-09-30 起生效；CSV 已取消）：**

```
品牌 | 官网车型名称 | 官网型号名称 | 年款 | 官网MSRP | 是否停销 | 数据日期 | 燃油分类
```

| 列 | 写法 |
|---|---|
| **品牌** | 品牌名（Dacia / DS Automobiles / Nissan …） |
| **官网车型名称** | 车系名（SANDERO / DUSTER / DS 3 / N°4） |
| **官网型号名称** | 官方完整版本名，**发动机/动力必须并入此列**，用官网原始写法 |
| **年款** | 官网标 MY/millesime 就原样写（MY2025）；没标一律写「官网无年款」，**严禁推断** |
| **官网MSRP** | 数字按**该市场货币的原生千分位写法**格式化为文本（不是浮点数）；单元格设为**文本格式**<br>· 欧元区（€）：**点号千分位**（`28.220,00`）<br>· 美元（$）/ 泰铢（฿）/ 英镑（£）：**逗号千分位**（`102,700` / `1,229,000`） |
| **是否停销** | 在售=`否`；已停售/下架=`是` |
| **数据日期** | 抓取当天，YYYYMMDD |
| **燃油分类** | 取「海外燃料分类」**英文原名**（见下表）；无法判定写「未标注」 |

**发动机并入型号名称的正确写法（用户明确要求，踩过坑）：**

```
✔ Dacia|DUSTER|DUSTER expression tribrid 150 4*4|MY2024|28.220,00|否|20260917|HEV
✘ Dacia|DUSTER|DUSTER expression|MY2024|28.220,00|否|20260917|HEV|三擎混动 150 4x4   ← 错误：单独占列 + 中文翻译 + 4x4 写法

✔ INEOS|Grenadier Station Wagon|Grenadier BMW 3.0L Turbo-Benziner, Reihensechszylinder|MY2027|72.640,00|否|20261026|Gasoline
✘ INEOS|Grenadier Station Wagon|Grenadier 3.0L Turbo-Benziner|MY2027|72.640,00|否|20261026|Gasoline   ← 错误：删掉了 BMW 前缀和 , Reihensechszylinder 后缀
```

要点：
- 用**官网原始动力写法**（`4*4` 不写成 `4x4`；`eco-G 120 auto` 保留大写 G）
- **禁止缩写/改写**：品牌前缀、技术后缀、标点一个都不能删。`BMW 3.0L Turbo-Benziner, Reihensechszylinder` ≠ `3.0L Turbo-Benziner`。**长度不是删词的理由**，觉得太长就照原样留着。
- **多字段版本名**：官网把「版本」和「动力」拆成两个字段时（如配置器 `Version:` + `Motor`），按 `{版本} {动力}` **原文照搬、一个空格连接**，不裁剪、不翻译、不调序。
- **动力名权威源**：以官网**配置器里选择动力的那个字段**为准（Ineos = 第 01 步 `Motor` 单选组）；价目 PDF 只供价格，PDF 的表头/行文不作为动力名依据，两者冲突用配置器。
- 不额外增加"发动机/动力"中文列
- 拼接顺序：`{版本名} {动力}`

### 燃油分类对照表（该列取「海外燃料分类」英文原名）

| 海外燃料分类 | 中文名 | 官网常规分类 |
|---|---|---|
| Gasoline | 汽油 | 汽油 |
| Diesel | 柴油 | 柴油 |
| MHEV | 轻混 | hybrid |
| FCV | 燃料电池 | 燃料电池 |
| LPG | 液化石油气 | 液化石油气 |
| BEV | 纯电 | 纯电 |
| Dual Fuel | 双燃料 | hybrid |
| PHEV | 插电式混合动力 | hybrid |
| HEV | 非插电式混合动力 | hybrid |
| REEV | 增成型电动 | hybrid |

> 输出**英文原名**：汽油车 `Gasoline`、纯电 `BEV`、非插电混动 `HEV`、插电混动 `PHEV`。
> 官网写不清时先按「官网常规分类」归大类再落英文名。

**交付物**：XLSX（MSRP 单元格**文本格式**，冻结首行，加自动筛选）。
**命名**：`<品牌>_<市场>_官网价_YYYYMMDD.xlsx`，写入**当前环境的工作区目录**（本机为 `/workspace`；其他沙箱可能是 `/data`、`~/output` 等 —— **以你实际可写且用户能取到文件的目录为准**，不要因为找不到 `/workspace` 就中断）。

### 年款依据副表（每个工作簿必带，2026-10-27 起）

工作簿固定 **2 个 sheet**：`官网价`（8 列，格式不变）+ `年款依据`。副表用于回答「年款是怎么得出来的」。

| 列 | 写法 |
|---|---|
| 品牌 | 与主表一致 |
| 官网车型名称 | 与主表一致 |
| 年款 | `MY2027` / `2026` / `官网无年款`（与主表逐字一致） |
| 覆盖型号数 | **工具自动统计**主表同组行数；全部相加必须 = 主表行数 |
| 年款依据（判定过程） | 一句话说明从哪个字段/文件看出来（如 `c2gMillesime → millesime_2025`、配置器 `MODEL YEAR 2026`、PDF 抬头 `MJ27`、API 无 MY 字段） |
| 官网原文（逐字） | **粘贴原文**，保留大小写/标点/引号，不改写（如 `2026 Lucid Air Pure`、`<meta name="modelYear" content="">`） |
| 来源位置 | URL + 具体位置（车型下拉项 / PDF 页码或抬头 / JSON 路径） |

要点：
- **按 `品牌 + 车型 + 年款` 分组**，一行一组，不逐型号重复。
- 采集时就把依据记下来（与价格同批抓），写成 `year_basis.json`；**不要事后回忆**，更不许拿自己写的 `sites.md` 当证据（自证循环）。
- `官网无年款` 也必须有依据：写明查过哪些位置无 MY，并**明确排除版权年**（`© MINI 2026`）、价格生效日期、以及只是产品/版本代号的 `millesime`（Alpine A110 的 `millesime_2015` 即是，不是年款）。
- 生成：`node write_xlsx.js rows.json <前缀> --date YYYYMMDD --money euro --year-basis year_basis.json`（脚本见 `scripts/write_xlsx.js`，首次用先 `npm i exceljs`）。主表有分组未被依据覆盖时工具会输出 `[WARN]`，必须补齐后再交付。

---

## 二、价格口径（2A 规则）

- 采**不带折扣的官方建议零售价（MSRP）**，含税，**不含选装**。
- **促销价 / 折扣价 / 政府补贴价一律不采**（西班牙 `totalAmount`、希腊 `με προωθητική ενέργεια` 等）；只在说明里备注原价。
- 仅"颜色/轮毂等配置差异"导致的多价，取最低。
- `cash price`（现金价）一般不采；**只有官网唯一报价是现金价时才采**并备注。
- 每条数据必须可回溯到来源 URL。

### ⚠️ 关键坑：目录价 vs 促销价（Stellantis 系）

DS/Citroën/Peugeot 在线商店的 GraphQL `prices.cash` 同时返回两个价：

```
catalogAmount: 35500.01   ← 官方目录价（MSRP，未折扣）✔ 采这个
totalAmount:   33752.96   ← 促销后价 ✘ 不采
discountAmount: 1747.05   ← 折扣额
```

**一律取 `catalogAmount`（= `baseCatalogAmount`）。**

---

## 三、查价优先级（冲突裁决）

1. **配置器**（配置器基础配置 / 其背后的官方价格 API）
2. 车型型号页 From 卡
3. **官方价格表**（prijslijst / price list / 车型页 Download specs·Brochure·Download price → 常为含全版本的 PDF）
4. 官网新闻稿定价
5. 第三方（必须注明"非官网"，且优先不用）

> **优先级说明（2026-10-26 调整）**：配置器是实时报价，排第一；From 卡次之。前两级只给车系起价或配置器为纯壳时，**用官方价格表补全变体级价格**并备注来源 —— 价格表仍是最全的兜底源，不要因为排第三就跳过。
>
> **冲突裁决：配置器 vs 价格表不一致时，以配置器为准**（配置器是实时报价，价格表可能旧版/口径不同）。配置器未收录的版本才用价格表价并备注来源。

**价格数字格式统一**：按市场货币原生写法 —— 欧元区用点千分位 `28.220,00`；美元/泰铢/英镑用逗号千分位 `102,700`。
工具函数：
```python
def eurofmt(p):
    s = f'{float(p):.2f}'
    ip, dp = s.split('.')
    return f'{int(ip):,}'.replace(',', '.') + ',' + dp
# 28220.0 -> '28.220,00'
```

---

## 四、执行流程

1. **探测站点**：可达性、车型导航、价格入口、下载按钮/价格表 PDF。先 `curl` 试，403 就上 Playwright。
2. **定位价格源**：先抓配置器网络请求定位价格 API；配置器不可用或只到车系起价时，看车型页 From 卡；再用官方 PDF/价格表补全变体与缺价版本。
3. **采集**：逐版本采集，记录来源 URL 与口径。
4. **交叉验证**：至少用两个来源核对（如配置器 API vs 页面显示价），冲突时按第三节裁决。
5. **生成 XLSX（8 列，含燃油分类）** 到**工作区目录**（不存在 `/workspace` 就用实际可写目录，如 `/data`）。
6. **交付说明**：数据表 + 口径 / 缺价车型 / 边界说明。

**采集失败时怎么办**（踩过：SEAT BE 全站封锁、Hyundai BE 价格 API 被 SNI 封锁）：
- **不要直接说"采不到"就收工** —— 先分级：是「零数据」还是「部分数据」。
- 若主站可通、只是完整价格拿不到（如 Hyundai BE），**把已得的官方可采数据（车系起价 `Vanaf`）出一份表交付**，并明确标注粒度与缺口，再给出后续选项。
- 优先按 `references/sites.md` 的「止损判定」快速定性，**不要在一棵树上反复调 UI 超过 3 轮**。
- 失败原因要写进 `references/sites.md`，供下次直接复用。

**年款怎么来**（用户问过，务必搞清楚）：
- 配置器 API 里常有 `millesime` / `modelYear` / `MY` 字段 → 确认是**年款**就采；若只是产品/版本代号（Alpine A110 的 `millesime_2015`）不采。
- 官网页面标的 MY/MY25 → 采。
- **页面上的年份若是"版权年"或"交付日期"→ 不是年款**，写「官网无年款」。
  （踩坑：DS 页面 2025 是版权年、2026 是交付期，都不是年款。）
- **⚠ 多年款并售时（北美常见）：必须逐年标注，且「各年款车型清单可能不同」**
  —— 不要用同一年款覆盖全部车型，也不要假设某车型有所有年款。
  例（Cadillac US）：IQ/IQL/XT5/CT4/CT5 只到 MY2026，XT4 只有 MY2025，
  而 ESCALADE 系有 MY2027+MY2026。**逐年把车型列全**，缺的不要编。

---

## 五、反爬与解析（按症状查表）

> **排查顺序**：A 判断能不能采 → B 找数据源 → C 校价格口径 → D 解解析 → E 确认是否该止损。
> 完整坑位与实测字段见 `references/sites.md`（顶部有按市场分组的**站点速查索引**）。

### A. 站点打不开 → 先判封锁级别

| 症状 | 判断与做法 |
|---|---|
| **`/robots.txt` 都 403** | 整站 IP 级封锁。换 UA / 浏览器 / IPv6 / 其他市场域都是徒劳 → **立即止损**（SEAT BE） |
| **Akamai 403**（`errors.edgesuite.net`、固定字节错误页） | 先分两种：① **真浏览器能通** → 只拦无指纹（`xvfb-run` + `headless=False` + 去 `navigator.webdriver`）（Volvo TH）；② **有头仍 403** → 出口 IP 黑名单，无解（Tesla TH）。佐证：同域其他子域是否 200 |
| **Cloudflare Error 1009** | **国家级封锁**，页面会写明 `banned the country ... (CN)` → 无解（Tata TH） |
| **TLS 握手立即 RST**（`openssl s_client` → `read 0 bytes`；浏览器 `net::ERR_CONNECTION_CLOSED`） | **SNI 级封锁**（TCP 通、TLS 被断）→ 该 API 无解，退回主站粗粒度数据。配置器在 `#/trims`/`#/error` 间乱跳也是这个原因，别反复调 UI |
| **curl 000 但 TLS 握手成功**（`HTTP/2` 已建流，随后 `INTERNAL_ERROR (err 2)`） | Akamai **HTTP/2 层拒 bot**；`--http1.1` 也是 000，别试 → 直接有头浏览器（MINI IN） |
| **`getent hosts` 只有 IPv6、curl 静默 000** | 该站 v6 不通 → 先 `getent ahostsv4` + `curl -4`；v4 仍时通时断（Akamai 多边缘）就直接 Playwright（BMW IN） |
| **Cloudflare 托管挑战 / `Just a moment`** | 有解但碰运气：stealth context + **`wait_until='commit'`**（`networkidle` 会被挑战页打断）+ 等 15–25s + 仍失败就 `reload()`，通常第 2 轮通过（VinFast IN）。脚本要带重试 |
| **按 IP / 出口国家跳站**（curl 302 → 他国站） | **先别止损**：curl 被国家跳转 ≠ 整站封锁，真实浏览器常能正常打开（Polestar DE：curl 任意路径 302 到 `.cn`，浏览器 `/de/` 全可采）。先用真浏览器复核同一路径；浏览器仍跳 → 才需海外出口或请用户截图 |

### B. 站能开，但不知道价格在哪

| 症状 | 做法 |
|---|---|
| **官网有独立价格总表页**（`/prices/`、`pricelist`、`prijslijst`） | 配置器拿不到变体级时**优先找它** —— 通常一张表全系全配置，SSR 直读（Force Motors）。⚠ 车系名 = 表内**单列行**，别向前找 heading（会串 `Disclaimer:`） |
| **车型页有 `Download specs` / `Brochure` / `Price List` 按钮** | 下载 PDF，常含全部版本 + MSRP（Ford UK `/cars/<model>/pricelist`、Škoda BE） |
| **北美官网 Build & Price 配置器** | **优先用配置器 API，而不是页面 "From" 价** —— 给「trim × 驱动 × 含目的地运费」，更细更权威。抓 `/p/v1/trim` 响应的 `data.trimList`。⚠ 含运费，与页面 MSRP 口径不同，交付须写明（Cadillac US） |
| **价格纯 JS 渲染** | Playwright 渲染；同时**查 SEO/JSON 数据区**（`modelCards`、`formattedValue`、`STANDARD MODELS`）—— 往往比 DOM 好抓 |
| **Next.js / CRA，HTML 里价格零散** | 挖 `/api/`：`grep -ohE '"/api/[a-zA-Z0-9_/-]{3,60}"' <chunk>` → 逐个 curl（常无鉴权）。⚠ 先看分层：后端只回起价 = 官网不公开变体价，别硬挖（Honda IN） |
| **AEM + feature-app 微前端**（`id="XXX"` 锚点 + `CmsFeatureAppLoader` + 永远 "Loading"） | 变体价在**懒加载 BFF**：滚动触发 + **拦截 `*.feature-app.io/bff/*` 响应**。⚠ BFF 需平台注入 token，**手拼 URL 必失败**（VW IN 的 MOFA） |
| **API 域被 WAF 拦 curl**（`.safeline` 拦截页 / curl 000 但浏览器能通） | **改用「浏览器内 fetch」**：Playwright 打开同站主页建指纹，再在页面上下文 `pg.evaluate` 里 `fetch()` 那个 API。WAF 拦的是非浏览器特征，不是 URL（Toyota IN 拿到 89 条全变体价） |
| **页面被掐死但页面能开** | 「站点难进」≠「数据难拿」：**抓一次 XHR 清单，把 API 拎出来直连**（Mercedes IN：页面 403，`vmos-api` 直接 200） |
| **配置器点击失败**（`Element is outside of the viewport`） | 放弃 DOM，直接调 API |
| **配置器 API 要 token，手带反而 404** | token 有租户/路径校验 → **拦截页面自身的响应体**，别抄 token（Jeep IN） |
| **超大厂只给车系起价，但用户要变体级** | 别停在 models/summary：去**配置器后端**（Mercedes `owcc-backend/.../entry?proposedStep=MOTORIZATION&typeClass=<系列>`）。⚠ 不加 `proposedStep` 只回营销预置卡且会重复；参数大小写敏感 |
| **配置器页只有 20–30 KB 纯壳、等 10 秒无价格 XHR** | 官网公开粒度就只到车系起价，**车系级就是正确交付**（Hyundai UK） |
| **未知路径返回首页 HTML**（SPA fallback） | 别把 `/models` `/shop` 的 200 当有效页 —— **比字节数**，与首页同长即 fallback（Lotus US） |

### C. 找到价了，先确认口径对不对

| 症状 | 判断 |
|---|---|
| **同页同时有 `catalogAmount` 与 `totalAmount`** | 取 **`catalogAmount`**（未折扣目录价）；`totalAmount` 是促销价（Stellantis 全系） |
| **总览页写 `from £X`，但官方 PDF 更高** | 页面是 **Promotional Price**（文案含 `Promotional`/`Grant`/`Offer` 即促销）→ 采 PDF。校验法：找**无促销车型**（页面价 == PDF 价）先验口径（Ford UK） |
| **同一品牌「配置器价」≠「车型页价」** | 多半是**配置器数据滞后**（未随调价同步）→ 3 个吻合、1 个差 1.5 Lakh 即锁定，滞后车型改以车型页为准（Jeep Wrangler） |
| **同一套配置器 API，不同国家字段含义不同** | Škoda：比利时 `modelPrice == priceOriginal`（纯车价）；**英国 `modelPrice` 是 OTR 价**（含 delivery + 首注册 + VED）。判别：拿官网 `From* £X` 去对，哪个字段等于 X 用哪个 |
| **官网把「原价」和「税制优惠后价」分开展示** | KGM `시작가격 ...부터(세제혜택 후)` 是**扣购置税优惠**的价；API/PDF 的 `차량공급금액` 才是原价 → 取原价 |
| **PDF 价目表列很多，不知取哪列** | Stellantis 英国 13 列 → 取 **「On The Road MRRP」**；**不取**「Electric Car Grant Deducted」（已扣 £1,500 补贴）。OTR Costs 按动力固定（汽油 1,570 / 混动 1,520 / 插混 1,230 / 纯电 1,125），可反推校验 |
| **车系表里大量「同配置但价格略高」** | 多为**车身颜色/内饰加价**（`[Pearl]`、`[Dual Tone]`、`+20,000`）→ 按关键词剔除，但**保留真实配置差异**（`[7S]`/`[8S]` 座位数、`[LE]` 特别版） |
| **印度价格格式对不上** | 两种：lakh 逗号 `15,70,522` / **空格分组** `₹ 18 19 000` → 正则 `₹\s*([0-9\s]{5,20})`。⚠ `₹39,999` 常是 **EMI 月供**，不是车价 |

### D. 价在里面，但取不出来

| 症状 | 做法 |
|---|---|
| **车型页只有一个起价，JSON 里有 N 个价** | 价是**变体级**：JSON 按序收价格 + **页面轮播标签**收变体名 → 顺序 zip。⚠ **先抽 3–4 个点击交叉验证顺序**再批量（Jeep IN） |
| **轮播/标签只渲染当前项** | DOM 永远只拿到 1 个 → 点一个读一个，或走 JSON。⚠ `locator.click(force=True)`；**去掉 `scroll_into_view_if_needed()`（常超时）**；JS `el.click()` 对 React 无效 |
| **配置器是云渲染 3D**（`Immersive Configurator`、`gorillastreaming`、WebRTC） | 永远渲染不出 → 反查后端 API（找 `pathSegments`/`BASE_URL`/`VITE_*_API_URL`）。⚠ 若 API 只有 `config` 无金额，说明价格在规则引擎里动态算，大概率拿不到（Lotus US） |
| **HTML 全是 `&quot;` 转义 + `"key":[0,value]` 二元组** | Qwik/Nuxt 序列化状态，**不能 `json.loads`** → `html.unescape` 后用「对象块」正则切卡片，再逐字段 `'"key":\[0,"([^"]*)"\]'`（Porsche IN） |
| **`£`/`₹` 遍地都是，分不清哪个是车型价** | 传统车企把全量 grade 内联进配置器页 → **必须以 `gradeName` 做锚点**：`"price":"(\d{4,7})"[^{}]{0,400}?"gradeName":"([^"]{1,40})"`，否则会把 `Fitted price: £1,800`（选装）一起抓进来（Honda UK：50+ 个 £，真 grade 只有 4 个） |
| **PDF 直链 curl 000，但浏览器能拿** | 浏览器内 `fetch` + base64 回传（代码见下）。⚠ **别用文件名判版本**：`..._october-2025.pdf` 的实际内容可能是 2026-08 版 → 读 `pdfinfo Title` |
| **`pdftotext` 只出页码，正文为空** | **图片版 PDF**（`pdfimages -list` 有大量 JPEG）→ `pdftoppm -r 200 -png` → **数每页 `£` 个数定位价格页**（配件表那页最多，别混）→ `tesseract --psm 6` → 用封面 `from £X` 交叉校验 |
| **同一厂商各车型价目表列数完全不同** | 找「恒为最后一个」的列：**On The Road 价恒为该行最后一个「带千分位逗号」的金额**（后面的 BIK `133.18`、CAP Code `57195`、CO2、VED 都不带逗号）。一条规则覆盖 10 份不同版式（Ford UK 129 条） |
| **PDF 里分组标题（trim 名）单独占一行** | 顺序扫描 + **继承状态**（`SWB`/`LWB` 改车身、`Zetec - 8 Seats` 改 trim、价格行归当前组）。⚠ 后半常混入**技术数据表**与特殊版延伸配置，必须**限定只扫主表区间**（Ford Tourneo Custom：52 页里主表只有 line 380-566） |
| **InDesign 在线文档 `inner_text`/`textContent` 取不到字** | 文字是**矢量 path**（`<text>` 节点数 0）→ 截图 + OCR。⚠ 先裁顶部 20% 找 `PRICE LIST` 定位页，别整本 OCR（Peugeot UK） |
| **OCR 表格列坐标因车型而异，硬编码必错** | 用**算术关系定位列**：`Basic + VAT = Total`、`Total + OTRcost = OnTheRoad`，滑窗找同时满足的连续 5 个金额；失败行裁横带放大 2× + `--psm 7`；仍失败取**行内最大金额** |
| **OCR 认不出 trim 标签**（`STYLE`/`GT` 常错位） | 用「**动力重复即新组**」切组；trim 名从 store 的 `configurationOptions.trims` 拿、按价格升序对应（PDF 恒按价格升序）。⚠ 组数必须 == trim 数 |
| **价格前带 `£` 导致正则全漏** | 正则写 `[£$]?\s?(\d{1,3}(?:,\d{3})+\.\d{2})` 并**取 group(1)**；`fullmatch` 直接匹配带符号串会失败 |

### E. 官网确实没有价 → 止损判定

| 情形 | 铁证（任一成立即止损） |
|---|---|
| **品牌已退出该市场** | 导航全是售后 + sitemap 无车型页 + 车型词全文 0 命中（Chevrolet TH、Ford IN）。⚠ 别把「配件调价页」当新车价页 |
| **超豪华品牌策略性不标价** | ① 车型页 `₹/£/$` 0 命中 ② 配置器 CTA 是 `Enquire to buy` ③ 配置器后端 `priceVersion: null`（Bentley IN、Maserati TH、McLaren、IM Motors） |
| **同一代码不同市场策略不同** | 做**对照实验**：`/en-GB` 有价而 `/en-US` 无价 → 是该市场经销商模式，不是工具问题（Lotus US），可放心判定「官网不标价」 |
| **配置器只是纯壳** | 见 B 组：体积 < 30 KB、无价格 XHR、车型页只有一个 `from £X` → **车系级就是终局** |

> **30 秒止损判定**（详见 `references/sites.md` 的「止损判定」段）：
> ① `curl <站>/robots.txt` → 403 即整站封锁；② 多市场域全 403 → 全球无解；③ `openssl s_client` 看 TLS 是否被 RST。

**突破 Akamai PDF 403 的关键代码**（在 Playwright 页面内同源 fetch）：
```python
res = pg.evaluate("""async (u)=>{
  try{
    const r = await fetch(u,{credentials:'include'});
    const b = await r.arrayBuffer();
    const bytes = new Uint8Array(b);
    let s=''; for(let i=0;i<bytes.length;i++) s+=String.fromCharCode(bytes[i]);
    return {ok:r.ok, status:r.status, len:bytes.length, b64:btoa(s)};
  }catch(e){return {err:String(e)}}
}""", url)
# Python 侧：base64.b64decode(res['b64']) 落盘
```

**Playwright 启动模板**：
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    br = p.chromium.launch(args=['--no-sandbox','--disable-dev-shm-usage'])
    ctx = br.new_context(locale='es-ES',   # 按市场改
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        viewport={'width':1440,'height':1000})
    pg = ctx.new_page()
```

---

## 六、交付前自检清单

**格式**
- [ ] **8 列**，无多余列（尤其**不能**把发动机单独占一列）
- [ ] 发动机/动力已并入「官网型号名称」，用官网原始写法（`4*4` 不写 `4x4`）
- [ ] **型号名逐字比对**：把每个去重后的「官网型号名称」拿去和抓取原文（配置器 `Version` + `Motor` 的快照）做**子串命中**，全部命中才算过；拼接式按 `{版本} {动力}` 两段分别命中。**不许拿自己写的 `sites.md` 笔记当证据**（自证循环）。
- [ ] 动力名取自**配置器里“选择动力”的那个字段**原文；价目 PDF 的表头/行文只供价格，不作为动力名依据
- [ ] 燃油分类填的是**英文原名**；`Hybrid` 文案下若无插电 → HEV，48V 轻混 → **MHEV**（别一律写 HEV）
- [ ] 千分位按市场原生写法（欧元点号 / 美元英镑逗号），MSRP 单元格**文本格式**
- [ ] 冻结首行、加自动筛选
- [ ] 工作簿含**「年款依据」副表**，覆盖型号数合计 = 主表行数（生成时无 `[WARN]`）
- [ ] 每条依据都有**逐字原文 + 来源位置**；`官网无年款` 写明查证范围并排除版权年/生效日期

**数据**
- [ ] 取的是**未折扣 MSRP**（Stellantis 取 `catalogAmount`；Ford 取 PDF 的 OTR，不取 `/cars` 促销价）
- [ ] 年款：官网没标就写「官网无年款」，**未推断**；多年款并售时逐年标注
- [ ] **有官网报价**的停售/下架车型入表并标「是」；已停产且官网无价的老车型**不入表**，在交付说明里列名说明
- [ ] 每条可回溯到来源 URL 或 PDF 版本（`pdfinfo Title`）

**交付**
- [ ] XLSX 写入**工作区目录**（`/workspace` 或环境实际可写目录），命名 `<品牌>_<市场>_官网价_YYYYMMDD.xlsx`
- [ ] 交付说明写清：**价格口径**（OTR / Ex-showroom / 含税）、**粒度**（车系级 or 变体级）、未纳入车型及原因
- [ ] 中间文件已清理（只留最终 XLSX）

---

## 参考文件（本 skill 自包含，不依赖外部路径）

- `references/sites.md` — 各站点坑位速记表（品牌 × 市场）+ 止损判定法
- `references/workflow.md` — 详细工作流与可复制提示词模板（给不支持 skill 的 agent 用）
- `scripts/triage.py` — **站点可达性分诊**（30 秒判断整站封锁 / SNI 级封锁 / 可直连）
- `scripts/fetch_pdf.py` — Akamai PDF 破封脚本
- `scripts/write_xlsx.js` — **唯一生成器**：8 列 + `年款依据` 副表，`--money euro|comma|lakh`（需 `npm i exceljs`）
- `scripts/format_output.py` — **旧版**：只出单 sheet、只支持欧元格式，已被 `write_xlsx.js` 取代，不要用于交付
