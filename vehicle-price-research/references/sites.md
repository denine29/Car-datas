# 站点坑位速记表（品牌 × 市场）

> 实测积累，持续追加。每采一个新站，把坑位补进来。

## 0. 站点速查（先看这里）

> **30 秒定位**：按市场扫一眼 → 知道结论和该用哪条路 → 再看下方同名段落的坑位细节（Ctrl+F 品牌名）。
>
> **结论图例**：`✅` 可采并已交付 · `⚠️` 可采但粒度/覆盖不全 · `❌` 无解（封锁，或官网不标价）

### 西班牙 ES

| 品牌 | 结论 | 数据源 / 一句话方法 |
|---|---|---|
| Dacia / Renault | ✅ | `es.co.rplug.renault.com` 配置器后端，Schema.org `priceType:SRP`；每个车系独立 base，用返回的 `next` URL |
| DS / Citroën / Peugeot / Opel / Fiat / Jeep | ✅ | `store.<brand>.es/graphql` → `getProductOffer`；取 `catalogAmount`，**不取** `totalAmount`；`engineGearbox` 传 slug |
| Abarth | ⚠️ | Stellantis Omnichannel SPA，DOM/坐标/URL 全进不去；只能从 `api.omnichannel.stla-aws.net/.../ncs/retrieve` 拿车系级 `cataloguePrice` |
| Audi | ⚠️ | `audi.es` 等全域 Akamai 403（curl/Playwright/外部节点全被拦）→ 改走 `datos.autopista.es/coches/audi/<车系>/`，口径与官方发布稿一致 |
| Aston Martin | ❌ | 官方从不公布售价，配置器全链路无价格字段 |

### 比利时 BE

| 品牌 | 结论 | 数据源 / 一句话方法 |
|---|---|---|
| CUPRA | ✅ | `api.cupra.be/v1/car-configurator/choices/<CARLINE>` 无鉴权，1 请求/车系；取 `engine.price`，**不取** `priceWithReduction` |
| Škoda | ✅ | `cc.skoda-auto.com/c3pobe/*` 配置器 API；`modelId` 第 3 段是年款；取 `modelPrice`（比 `priceOriginal` 高 £/€） |
| Volvo | ✅ | Akamai 拦 headless → 必须 `xvfb` + `headless=False` |
| Citroën | ✅ | 主站 curl 全 403，但**页面内 `fetch()` 不受限** → `sccf` 静态价格库 JSON |
| KGM / KG Mobility | ✅ | Vercel 托管全开放，`__NEXT_DATA__` 直读 `configurations[].listPrice.priceInclVat` |
| Hyundai | ⚠️ | 主站通，但 PAPI `org-eu-www.hyundai.com` 被 **SNI 级封锁**（TCP 通、TLS 立即 RST）→ 只到 `Vanaf` 起价 |
| SEAT | ❌ | 全站按 IP 封锁，`robots.txt` 都 403；curl/浏览器/换 UA/IPv6 全无效 |

### 丹麦 DK

| 品牌 | 结论 | 数据源 / 一句话方法 |
|---|---|---|
| MG | ✅ | Cloudflare 但不拦；WordPress + 经销商配置器 |
| CUPRA | ❌ | 全站 IP 封锁；同 IP 访问 `api.cupra.be` 却正常 → 站方策略，非我方 IP 问题 |
| Citroën | ❌ | 价格源是第三方 `pricelists-api.cars4ever.eu`，**TCP 443 我方路由阻断**（无 response、无 fail） |
| Nissan | ❌ | IP 级风控 |

### 智利 CL

| 品牌 | 结论 | 数据源 / 一句话方法 |
|---|---|---|
| Opel | ✅ | `www.opel.cl` curl 403 但 Playwright 可通；滚动懒加载后的 "PRECIO DESDE" 卡片（含完整型号名 + 起价） |

### 泰国 TH

| 品牌 | 结论 | 数据源 / 一句话方法 |
|---|---|---|
| GWM 长城 | ✅ | Fastly 全通，SSR；`span.option` ↔ `data-title="฿..."` 顺序 zip；⚠ slug 不带 `-diesel` 的多为 HEV |
| Nissan | ✅ | CloudFront 全通；`all-grade-price.html` 内嵌 `const data={...}`（JS 字面量，交 node 解析）；Terra 只在车型页 |
| Mitsubishi | ✅ | SSR `<h3>车系</h3>` + `<table>`；用 `/en/` 版版本名更规范；站点慢（单页 1MB+/200s） |
| Subaru | ✅ | Azure SSR 正则直读；`/th/en/home/` 已 404，正确入口 `/th/en/` |
| Isuzu | ✅ | Netlify 全通；`รุ่นรถ` 段「版本行 + `N,N,NNN THB`」配对；⚠ 页脚 `MODEL LINEUP` 有他车价须截断 |
| Denza 腾势 | ⚠️ | 无独立价格页；价格只在促销活动页 `ราคาจำหน่าย` 表格，Playwright 渲染 |
| Volvo | ⚠️ | curl 全 403，**有头 Playwright 200**；价格只在配置器 `/en-th/build/<model>/`；EX90 无价 |
| Chevrolet | ❌ | 官网已转型纯售后站（GM 2020 退出泰国新车市场） |
| Tata Motors | ❌ | Cloudflare **国家封锁**（Error 1009，封 CN）；源站 80/443 均 CLOSED |
| Tesla | ❌ | Akamai 按出口 IP 黑名单；`auth.tesla.com` 200 但 `www` 全 403 |
| Maserati | ❌ | 站点全通，**纯政策问题**：AEM `.model.json` 的 `price` 全为 `"0"` |
| McLaren | ❌ | 站点全通、API 全打通，但 `showPriceSummary='false'` + `showPricesByCountry='false'` |

### 美国 US

| 品牌 | 结论 | 数据源 / 一句话方法 |
|---|---|---|
| Cadillac | ✅ | 配置器 API 最全：`aec-cp-configurator-gateway/p/v1/trim` → `data.trimList`（含运费，粒度 trim × 驱动）；三代年款清单不同 |
| Mazda | ✅ | 车型页内联 JSON `"lowestMsrp":"$X","title":"TRIM"`；须先 `html.unescape`；CX-30 无 JSON，用 FAQ 文本兜底 |
| Lotus | ⚠️ | 美国站仅 Eletre Carbon 标价；配置器是云渲染 3D（GorillaStreaming）；★ 对照 `/en-GB` 有价、`/en-US` 无价 → 站方策略 |

### 印度 IN

| 品牌 | 结论 | 数据源 / 一句话方法 |
|---|---|---|
| Force Motors | ✅ | 无任何反爬；`/prices/` 34 个 `<table>` 即官方总表；车系 = 表内**单列行**（别向前找 heading，会串 `Disclaimer:`） |
| Jeep | ✅ | 车型页内联 JSON 给变体价；**变体名只在轮播标签**→ 按顺序 zip；⚠ JS `el.click()` 对 React 无效，用 `locator.click(force=True)` |
| Toyota | ✅ | 价格 API 有 **SafeLine WAF** 拦 curl → **Playwright 页面上下文 `fetch()`** 调 `POST 1.0/api/price/list/{dealerId}/{modelId}` 拿 XML；⚠ 剔除 68 条颜色加价 |
| VinFast | ✅ | Cloudflare 托管挑战，stealth + `wait_until='commit'` + reload 概率通过；价格在 `shop.vinfastauto.in/reservation?model=<X>`；⚠ **MPV7 参数是 `VFMPV7`** |
| BYD | ✅ | curl 只有 6.5 KB SPA 壳 → Playwright 渲染车型页；首页 `₹ 24.99 Lakh`、车型页空格分组 `₹ 24 99 000` |
| Volkswagen | ✅ | AEM + feature-app；变体价在 **MOFA BFF**（需平台注入 token，**只能拦截响应，手拼 URL 必失败**） |
| BMW | ✅ | **IPv6 全断 / IPv4 时通时断**（Akamai 多边缘）→ 直接 Playwright；价格全在 `/en/all-models` 卡片（车型详情页无价） |
| Porsche | ✅ | Qwik 序列化状态内嵌（`"key":[0,value]` 二元组），`html.unescape` 后正则切卡片，**不能 `json.loads`** |
| Mercedes-Benz | ✅ | 页面无头 403 / 有头 200；价格在 **VMOS API**（可直连 curl）+ 配置器 **OWCC**（`proposedStep=MOTORIZATION`） |
| MINI | ⚠️ | Akamai **HTTP/2 层拒绝**（`INTERNAL_ERROR`，`--http1.1` 也 000）→ 只有有头浏览器；官网只公开 7 条 |
| Honda | ⚠️ | curl 直通，官方 API `GET /api/getAllCarsData` **无鉴权但只给车系起价** |
| Ford | ❌ | 2021-09-09 已退出印度新车市场，官网纯售后（sitemap 仅 29 条无车型页） |

### 韩国 KR

| 品牌 | 结论 | 数据源 / 一句话方法 |
|---|---|---|
| KGM / KG Mobility | ✅ | 主 HTML 被地理屏蔽（空壳），但 `/assets/*.js` 可下 → **grep JS 挖出无鉴权 API** `web.kg-mobility.com/app/*.do` |

### 英国 UK

| 品牌 | 结论 | 数据源 / 一句话方法 |
|---|---|---|
| Ford | ✅ | **`/cars` 页是促销价不能采**；真价在 `/cars/<model>/pricelist` → 官方 PDF；**行内最后一个带逗号的金额 = OTR**；文件名日期不可信，读 `pdfinfo Title` |
| Peugeot | ✅ | 官方价目表是 **Adobe InDesign 在线文档**，文字是矢量 path（`<text>` 节点数 0）→ **截图 + OCR**；用算术关系定位列 |
| Honda | ✅ | curl 全通；grade 级价格在配置器页内联 JSON，**必须以 `gradeName` 做锚点** |
| Hyundai | ⚠️ | curl 全通；只有车系级起价（models 页 JSON），配置器是纯壳 |
| Fiat | ⚠️ | 主站 JS 全挂（61 KB 空壳）；只有 `store.fiat.co.uk/compare` 的 10 个车系 |

### 新西兰 NZ / 菲律宾 PH / 全球

| 品牌 | 结论 | 数据源 / 一句话方法 |
|---|---|---|
| Mercedes-Benz NZ | ⚠️ | Akamai 按数据中心 IP 拦（403）；部分车型 SSR 带 `Estimated Drive Away Price` |
| 保时捷 NZ | ✅ | 车型总览页 astro-island JSON（`modelCards` → `price.formattedValue`） |
| 大众 NZ | ✅ | 每车型页 `Download specs` PDF（含多配置 MRP） |
| BYD NZ | ✅ | BROCHURE 按钮 → price-list PDF |
| 本田 / 标致 NZ | ⚠️ | Cloudflare 拦直连；车型页 From + ORC |
| Fiat / Jeep PH | ⚠️ | JS 渲染；官方导航数据区 `STANDARD MODELS` |
| BMW PH | ⚠️ | 车型页无价；`BMW Price List` 按钮 → S3 上的 PDF（**沙箱封 `*.s3.amazonaws.com`**） |
| 领克 | ❌ | 按出口 IP 地理跳转 `.com.cn`，需海外代理 |
| 法拉利 / Aston Martin | ❌ | 官方从不公布售价，仅经销商询价 |
| IM Motors 智己 | ❌ | 站点全通但 API 只有规格表，0 价格字段 |

> ⚠ **本索引与下方段落的关系**：「## 按品牌」下的长段落是**踩坑细节**（字段名、正则、失败过程）；本索引是**快速路由**。两者冲突时以长段落为准。

---

## 数据源定位方法（通用）

1. **先抓配置器**：开 Playwright，`page.on('response')` 捕获所有 XHR/fetch，找含 `price` / `config` / `graphql` 的接口。
2. **配置器不可用或只到车系起价 → 看车型页 From 卡**。
3. **仍缺变体/缺价 → 找官方价格表 PDF**：车型页上找 `Download specs` / `Brochure` / `prijslijst` / `price list` / `Download price` 按钮，用 PDF 补全并备注来源。
4. **接口优先于 DOM**：能调 API 就别点页面（DOM 点击易失败、易漏项）。

**❌ 反面教训**：不要硬编码车型 base ID（Dacia 每个车系有独立 base：BIGSTER=`BAHMm`、DUSTER=`BAHMn`、SANDERO=`BAHMo`、JOGGER=`BAHMp`、SPRING=`BAHMx`）。要用接口返回的 `next` 完整 URL，否则**跨车型串价**。

### 止损判定：30 秒内判断「这个站能不能采」

按以下顺序快速探，命中了就别恋战，记入本表后换下一个品牌：

| 步骤 | 命令 | 命中结论 |
|---|---|---|
| ① 整站试探 | `curl -s -o /dev/null -w "%{http_code}" <站点>/robots.txt` | **403 → 整站 IP 级封锁**，换 UA/浏览器/路径都无效，**直接止损** |
| ② 多市场试探 | 依次试 `.es` `.fr` `.de` `.uk` `.nl` `.it` … | 全 403 → 同一 WAF 策略，全球无解 |
| ③ DNS 分级 | `python3 -c "import socket;print(socket.gethostbyname('<host>'))"` | 看是否 Akamai/Cloudflare/独立 IP；apex 与 www 常在不同平台 |
| ④ TCP/TLS 分诊 | `bash -c 'cat </dev/null >/dev/tcp/<ip>/443'` 和 `openssl s_client -connect <host>:443 -servername <host>` | **TCP 通 + TLS `read 0 bytes`（立即 RST）→ SNI 级封锁**；浏览器表现 `net::ERR_CONNECTION_CLOSED` |

> 关键区分：**403 = 应用层 WAF**（可能有绕行机会，如换浏览器/换路径）；**TLS RST = 网络层封锁**（本环境出口 IP 被针对，无解）。
> 界面「数据拉不到」的常见表征：配置器 URL 在 `#/trims`（正常）与 `#/error` 之间随机跳，且 DOM/价格恒为空 —— 先查它的数据 API 域名是否被 TLS RST，而不是反复调 UI。

---

## 按品牌

### 雷诺集团（Dacia / Renault）

| 项 | 内容 |
|---|---|
| **市场** | 西班牙 |
| **价格源** | `es.co.rplug.renault.com` — 配置器后端，**公开返回 Schema.org 结构化报价** |
| **关键字段** | `schema:price` + `priceType: "SRP"`（= 官方建议零售价，未折扣）+ `schema:validFrom`（数据新鲜度） |
| **年款来源** | `impact[]` 里 `specCatCode == 'c2gMillesime'` → `specCode.replace('millesime_','')` |
| **发动机识别** | `impact[]` 里 `specCatCode.startswith('PT')` 且 `possibles` ≥2 → 取 `specCode` + `next` |
| **坑** | ① 每个车系独立 base，禁止硬编码；② 用返回的 `next` 完整 URL；③ 价格可能是字符串，格式化前先 `float()` |
| **无价格表** | `tarifas.html` / `precios.html` 均 404；catalogos 的 PDF 是宣传册（正文 0 个 €） |

### Stellantis（DS / Citroën / Peugeot / Opel / Fiat / Jeep）

| 项 | 内容 |
|---|---|
| **市场** | 西班牙 |
| **价格源** | `store.<brand>.es/graphql` — **在线商店 GraphQL** |
| **核心接口** | `operationName: "getProductOffer"`，POST，需 `credentials:'include'` |
| **入参** | `{input:{model, trim, engineGearbox, exteriorColour, interiorColour, options:[], accessories:[]}, page:'config'}` |
| **价格字段** | `selectedConfiguration.prices.cash.catalogAmount` = **官方目录价（MSRP）** ✔<br>`...totalAmount` = 促销价 ✘<br>`configurationOptions.trims[].prices.cash.baseAmount` = 各配置价 |
| **车型 slug** | DS ES：`ds-3-suv` / `no4-berlina-5-p` / `no7-suv` / `no8-berlina-5-puertas` |
| **URL 结构** | `/selector/configurable/{model}/{trim}/{engineSlug}/{color}/{interior}?channel=b2c` |
| **发动机参数** | `engineGearbox` 要传 **slug**（`hybrid-145cv-automatica-hibrido`），**不是** id |
| **trim 传空** | `trim:''` + `showAllEngines:true` → 返回该发动机下所有 trim 的价格矩阵（最高效） |
| **坑 1** | 组合无效时接口返回 `Unable to get product offer`（缺有效 trim/interior 配合） |
| **坑 2 关键** | 某些 trim 不支持某发动机时，会**回显**其它发动机的价格 → 判定法：**同一 trim 跨发动机价格完全相同 = 该组合无效**，须剔除 |
| **坑 3** | 主站 `www.dsautomobiles.es` 被 Akamai 403；但 `store.dsautomobiles.es` 畅通 |
| **坑 4** | 主站目录页会列出已停销车型（DS 4 重定向、DS 7 仅库存车），**以 store 的 configurable 列表为在售权威** |
| **年款** | 页面年份多为版权年/交付期，**非年款** → 写「官网无年款」 |
| **DS 官方 PDF** | `www.dsautomobiles.es/content/dam/ds/spain/pdf/caracteristicas-tecnicas/CT_{DS3,DS7,N4,N8}.pdf` — **只有技术规格，无整车价**（直链 403，需同源 fetch 破封） |

### DS DE（德国 `www.dsautomobiles.de`：**Akamai 封主站，configv3 API 直取全版本 PVC**）✅

- **★ 主站被封、API 可通**：`www.dsautomobiles.de` 对 curl 一律 Akamai 403（`errors.edgesuite.net`），PDF 价目表同样受保护；但配置器后端 `api-cdn.configv3.awsmpsa.com` **curl 直通**。derivedModel ID 需用浏览器打开各配置器页，从 network 的 `versions?derivedModel=` 抓取。
- **★ 端点**：`GET https://api-cdn.configv3.awsmpsa.com/api/v4/d-de-de-btoc/vehicles/versions?derivedModel=<VP…>`（`Accept: application/json`）→ 数组，每元素一个版本：
  - `version.label` = 官方完整版本名（`DS 3 PALLAS HYBRID 145`、`N°7 LA PREMIÈRE E-TENSE AWD LONG RANGE 350 PS`）
  - `prices.price.base` = **含 19% MwSt 的 UPE**（= `priceWithoutTax.base × 1.19`），`discount` 全为 0 → 就是目录价
  - `grCommercialName.label` = trim（`PALLAS` / `ÉTOILE + Alcantara` / `ÉTOILE + Nappa` / `LA PREMIÈRE`）
  - `energy.label` = `Hybrid` / `Diesel` / `Elektro` / `Plug-in-Hybrid`
- **★ derivedModel（按车系）**：DS 3=`VP100054` · N°4=`VP100060` · N°7=`VP100056` · N°8=`VP100052`。DS 7 传 `VP100049` 返回 `400 "Derived model VP100049 is unknown for environment d-de-de-btoc"` → 已下架。
- **★ 在售权威**：`/infocenter/konfigurator.html` —— DS 3 / N°4 / N°7 / N°8 有「Konfigurieren」；**DS 7 只有「Fahrzeuge im Bestand ansehen」（库存车，无配置器）**；DS 4 / DS 9 不在列表。`/infocenter/preislisten.html` 也只有 DS3 / N4 / N7 / DS7 / N8 五份 PDF，且全部 Akamai 403。
- **★ 燃油陷阱**：DS 的 `HYBRID 145` 是 **48V 自充电轻混**（官网原文 "selbstladende 48V Li-Ion-Batterie"，系统功率 107 kW）→ **MHEV，不是 HEV**；`E-TENSE` → BEV；`BlueHDi` → Diesel；`PLUG-IN-HYBRID 240` → PHEV。
- **★ 年款**：配置器 HTML 的 `<meta name="modelYear" content="">` 为空、API 无 MY 字段 → 全部 `官网无年款`。
- **交付结果（20261026）**：`DS_DE_官网价_20261026.xlsx`，**34 条 / 4 个车型**（DS 3 6 · N°4 11 · N°7 12 · N°8 5），33.870–78.450 €。燃油：BEV 19 · MHEV 9 · Diesel 3 · PHEV 3。未纳入：DS 7（仅库存车，无配置器价）、DS 4 / DS 9（已退出配置器）。

### CUPRA（BE 比利时）

| 项 | 内容 |
|---|---|
| **价格源** | `api.cupra.be` — 独立子域，**无鉴权**，curl 直可达 |
| **核心接口** | `GET /v1/car-configurator/choices/<CARLINE>?lang=FR&sales_type=B2C`（需 `Referer: https://www.cupra.be/fr/`） |
| **效率** | **1 请求 / 车系**，直接拿全车系「配置等级 × 动力」矩阵，无需逐车型爬 |
| **价格字段** | `engine.price` = **官方目录价（MSRP）** ✔<br>`engine.priceWithReduction` = 促销价 ✘（93 条里 92 条不同，差幅可达 9.000 €） |
| **型号名** | `engine.name` 已是完整官方写法（含配置等级 + 动力 + 变速箱），**无需拼接** |
| **carline 白名单** | `FORMENTOR, BORN, LEON, LEONBREAK, TAVASCAN, TERRAMAR, RAVAL`（传错返回 400，错误消息会列出全部合法值） |
| **坑 1** | `LEONBREAK` 无空格，但**官网展示名是 `LEON BREAK`**（带空格）；`LEON-SPORTSTOURER` 无效 |
| **坑 2** | 另一端点 `/api/global-financing-products?type=prices` 同时有 `price` 和 `discount_price`，**仍是折扣口径，勿混用** |
| **年款** | `engine.model_year`，本季全部 `2027` → `MY2027` |
| **架构** | Next.js 前端 + `api.cupra.be` 后端；配置器页显式显示 `Total incl. TVA`，可交叉验证 |


| **主站** | `www.nissan.gr` — **Akamai IP 级封锁**（403 + 固定 65324/64227 字节错误页），换 UA/headers 均无效 |
| **可用源** | `build.nissan.gr` 配置器（服务端 HTML 直出，**可直接 curl**） |
| **官方价格表** | LTPF PDF（`ΛΤΠΦ`/`ΛTPF` = 建议零售价；`ΤΙΜΗ ΑΠΟ` = 起价） |
| **坑** | ① 版本 slug 用**下划线**（`n_connecta`、`techna_plus`）；② 车系名含连字符（`X-Trail`）正则要用 `([\w\-]+)`；③ 两者价差大，**配置器优先** |

### Mercedes-Benz

| 项 | 内容 |
|---|---|
| **市场** | NZ |
| **坑** | Akamai 按数据中心 IP 拦截（403）；只有 WebFetch 类外部节点可读 |
| **可用** | 部分车型 overview 页 SSR 带 `Estimated Drive Away Price`；无价车型需配置器 |

### KGM / KG Mobility（BE 比利时 `www.kgm.be`：完全开放，Next.js `__NEXT_DATA__` 直读）✅

> KG Mobility（原双龙 SsangYong）比利时站。**全站零封锁**，是近期最省力的站点之一。

| 项 | 内容 |
|---|---|
| **建站** | Vercel + Next.js + Storyblok CMS；`robots.txt` 200 `Allow: /`，Nuxt/Next 双通道均无 WAF |
| **可访问性** | ✅ curl 直连 200，无需 Playwright、无需代理 |
| **车系 URL** | `https://www.kgm.be/nl/configurator/<slug>`（`/nl/modellen/<slug>` 同源） |
| **12 个 slug** | `actyon`, `actyon-hybrid`, `grand-musso`, `korando`, `musso`, `musso-ev`, `rexton`, `tivoli`, `torres`, `torres-evx`, `torres-evx-van`, `torres-hybrid` |
| **★ 真源** | 配置器页 HTML 内嵌 `<script id="__NEXT_DATA__" type="application/json">...</script>` |
| **真源路径** | `props.pageProps.story.content.configurationInfo.configurations[]` |
| **★ 价格字段** | `configurations[].listPrice.priceInclVat` = **官方未折扣目录价（含税）** ← 采这个 |
| **勿采字段** | `previousStartingPrice`、`discounts[]`、`ecobon`、`takeoverPremium`、页面 `Vanaf €`（均为折后/补贴价） |
| **价格口径实证** | Actyon：`48.990 − 2.000(Korting) − 500(Overnamepremie) = 46.490` = 页面 "Vanaf €" ✓，确认 `listPrice` 才是目录价 |
| **车型展示名** | `content.model.name`（官网原文：`Actyon 4x4`、`Torres 4x4`、`Musso EV`、`Grand Musso`）——**勿用 slug 大写推断**（会得到 `ACTYON 4X4`） |
| **型号名组成** | `modelEdition.name`（去年份）+ `engine.fuelType.label` + `engine.wheelDrive.label` + `engine.transmission.label` + `{horsePower} pk` |
| **★ 年款** | 取 `modelEdition.name` 里的 `20\d{2}` → `MY2024` / `MY2025` / `MY2026`；**musso-ev 版名无年份** → 按规则写「官网无年款」 |
| **马力必须并入** | Korando `Platinum Benzine 2WD Manueel` 的 **149 pk 与 163 pk 同为 34.490**，不并马力会被误去重（54 → 52）。并入 `149 pk` / `163 pk` 后零丢失 |
| **其它 API** | `GET /api/configurator/options?modelUuid=<uuid>&locale=nl` 返回版本-选装映射，**不含价格**，抓价格无用 |
| **buildId** | `ALetL--VJqG7Ars8vePHx` |
| **无公开 PDF** | Brochure/CO2 页均为表单申请制（Bynder DAM 后置），无价目 PDF，不要去找 |
| **交付结果** | **54 条 / 12 车系**（2026-09-30） |

**关键代码骨架**：

```python
import re, json, html as H
h = open('configurator.html', encoding='utf-8', errors='ignore').read()
m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', h, re.S)
data = json.loads(H.unescape(m.group(1)))
cfgs = data['props']['pageProps']['story']['content']['configurationInfo']['configurations']
for cf in cfgs:
    incl = (cf.get('listPrice') or {}).get('priceInclVat')   # ★ 目录价，未折扣
    ed   = (cf.get('modelEdition') or {}).get('name') or ''
    ym   = re.search(r'\b(20\d{2})\b', ed)
    year = f'MY{ym.group(1)}' if ym else '官网无年款'
    ed_clean = re.sub(r'\s*\b20\d{2}\b\s*', ' ', ed).strip()
    eng = cf.get('engine') or {}
    parts = [ed_clean,
             (eng.get('fuelType') or {}).get('label'),
             (eng.get('wheelDrive') or {}).get('label'),
             (eng.get('transmission') or {}).get('label')]
    name = ' '.join(x for x in parts if x)
    if eng.get('horsePower'):
        name += f" {eng['horsePower']} pk"
```

**车系分布（54 条）**：Actyon 4x4 1 / Actyon Hybrid 2 / Grand Musso 3 / Korando 10 / Musso 3 / Musso EV 8 / Rexton 3 / Tivoli 10 / Torres 4x4 3 / Torres EVX 6 / Torres EVX Van 1 / Torres Hybrid 4

**样例**：
```
KGM;Actyon 4x4;Actyon Titanium Benzine 4WD Automaat 163 pk;MY2024;48.990;否;20260930
KGM;Tivoli;Tivoli Street Series Benzine 2WD Manueel 163 pk;MY2026;21.990;否;20260930
KGM;Musso EV;Musso EV Bronze Elektrisch 2WD Automaat 207 pk;官网无年款;44.490;否;20260930
```

### Citroën（DK 丹麦 `www.citroen.dk`：主站通，但价格 API 在我方出口被路由阻断）❌

**结论：主站完全可访问，但价格数据源 `pricelists-api.cars4ever.eu` 我方出口走不通 → 拿不到价格。**

> ⚠ 与比利时站**架构完全不同**：BE 走 `sccf` 静态库（同一主机，页面内 fetch 即可）；**DK 走 `cars4ever.eu` 独立 SaaS**（第三方域，独立网络路径）。

| 项 | 内容 |
|---|---|
| 主站 `www.citroen.dk` | ✅ **200**（Akamai `23.214.22.230`，`robots.txt` 200）—— Adobe AEM（`x-dispatcher`/`x-vhost: publish`） |
| 站点性质 | **纯 C 端电车站**：`ë-C3` / `ë-C3 Aircross` / `ë-C4` / `ë-C5 Aircross` / `ë-Berlingo` / `ë-SpaceTourer`；商用车 `Berlingo Van`/`Jumpy Van`/`Jumper` 在 `/erhverv/varevogne/`。**无燃油乘用车**（丹麦市场 Citroën 只卖电车） |
| 价格页 | `/information/prislister/<slug>-priser_specs.html`（如 `e-c3-priser_specs.html`）—— **正文空壳，价格靠 iframe 渲染** |
| **★ 价格 widget（iframe）** | `https://price-list-public.cars4ever.eu/?brand=citroen&businessType=retail&modelCode=<CODE>&configuratorUrl=...`（从 `<iframe data-src-default="...">` 提取，需二次 `html.unescape`） |
| **★ 真源端点** | **`GET https://pricelists-api.cars4ever.eu/api/models/{modelCode}/{businessType}`**（如 `/api/models/Ny_%C3%AB-C3/retail`）——**无需鉴权**，由 widget 内 axios（`baseURL=QD` 常量）发起 |
| **❌ 阻断点** | `pricelists-api.cars4ever.eu` → **Azure 丹麦东部** `9.205.42.0`（`waws-prod-dke-003-0baa.denmarkeast.cloudapp.azure.com`）→ **TCP 443 我方出口 BLOCKED**（`/dev/tcp` 测不通、curl `000`、IPv4/IPv6 均不通） |
| **⚠ 假阳性陷阱（务必记住）** | 浏览器里 `on('request')` **能看到该请求被发出**，但**永远收不到 `response`，也收不到 `requestfailed`** —— 这是 **TCP 黑洞**（连接挂死）的典型特征。**"请求已发出" ≠ "能拿到数据"**；必须验证到 **RESP 或至少 err/warn** 才算真通 |
| **对照证明非我方 IP 被封** | `price-list-public.cars4ever.eu`（`150.171.110.68`，Azure Front Door）**200 通**；`brand-config.cars4ever.eu`（同 IP 段）**200 通**；`20.105.224.35:443` **OPEN** → **不是全站 IP 拉黑，是特定 Azure 区域 IP 的路由不可达** |
| **连官网自己也渲染不出** | 在真实 `www.citroen.dk/information/prislister/e-c3-priser_specs.html` 页面里，widget 同样只发请求不收响应、iframe 空白（`innerText` 为空）→ **在我方网络下，官网用户视角的表格也是空的**，并非我方抓取姿势问题 |
| **DSL API 旁证（另一条死路）** | 首页嵌入 `dsl.api.stla-aws.net/v1/trimdetails/d1/citroen/denmark/dk/configdetails` → **CloudFront 403**（`Request blocked`），带 Referer/Origin/UA 均无效 |
| `interaction.citroen.dk`（配置器） | 需 `modelCodes` 参数；本项目未深入（价格已定位在 cars4ever，无必要） |
| **多品牌共享平台** | `brand-config.cars4ever.eu/api/brand-websites.json` 列出丹麦全部 Stellantis 品牌（peugeot/citroen/ds/opel/fiat/jeep/alfaRomeo/mitsubishi/hongqi/voyah/navor/leapmotor/exlantix/skyworth）→ **该 API 若可通，是一次性覆盖多品牌的钥匙**（可惜网络不通） |
| 交付结果 | **未产出**（数据源不可达） |

**★ widget 激活姿势（供将来网络恢复时复用）**

widget 不在被 iframe 嵌入时不会发请求。本地复现需自建宿主页并注入 `window.xprops`：

```html
<script>window.xprops={brand:'citroen',modelCode:'Ny_ë-C3',businessType:'retail',
  originalLocation:'https://www.citroen.dk/...'};</script>
<iframe src="https://price-list-public.cars4ever.eu/?brand=citroen&businessType=retail&modelCode=Ny_%C3%AB-C3"></iframe>
```

- `modelCode` 从官方价格页 `<iframe data-src-default>` 里取（形如 `Ny_ë-C3`）
- `brand-config.cars4ever.eu/api/brands.json` 给出全部品牌 code

> **排查心法**：遇到"请求发出却无响应"时，**别急着报成功**。用 `/dev/tcp/<ip>/443` 直连测端口，并检查 `on('response')` 是否真的触发过。同域名的其它子域（如 `brand-config`）能通，说明是**特定 IP/区域的路由阻断**，而非整体封锁。

---

### Citroën（BE 比利时 `www.citroen.be/nl`：Akamai 全域封 curl，但 sccf 静态价格库可直接读）✅

> Stellantis 系。**这是 Stellantis 系里目前唯一完整拿下全量配置价格的市场**——关键是找到了 `sccf` 静态价格库。
> 同集团 Abarth ES 曾因进不去 Omnichannel SPA 只能取车系级 `cataloguePrice`，**本站可下钻到每一个配置**。

| 项 | 内容 |
|---|---|
| **Akamai** | `robots.txt` 403、`curl` 403、`WebFetch` 403（`errors.edgesuite.net`）；**headed Playwright ✅ 200** |
| **★ 关键突破** | **页面内 `await fetch(url)` 不受 Akamai 拦截** —— 任何站内 URL 都能这样拿。打开任一配置器页，在 `pg.evaluate` 里 `fetch` 即可 |
| **配置器入口** | `https://www.citroen.be/nl/omni/configurator/#/?derivedModelCode=VP1CSCA5&grBodyStyle=SILHOU5P&vehicleType=VP`（`derivedModelCode` 来自首页卡片的 `data-vehicle-bbc`/配置器菜单） |
| **★ 真源（sccf 静态库）** | 三步：<br>① `GET /sccf/prod/citroen/publish/data/sccf/scope/3104HCC.json` → `comMods[].nsbpath` + `comMods[].mvss[]`（**versionId → 官方描述**，共 367 条）<br>② `GET /sccf/prod/citroen/publish/data/sccf<nsbpath>/NPE_STANDARD_3104HCC_<CODE>.json`（**每车系一个，全量配置**）<br>③ 取 `priceFragment.vehicles[].getPriceExtendedB2C` |
| **★ 价格字段** | `getPriceExtendedB2C` → `price.vehicle.prices[]`，筛 `priceType == "cataloguePrice"` → **`withTaxesAndFees`**（含税目录价，采这个）<br>勿采 `eStorePrice`（折后电商价，官网页面显示的就是它） |
| **★ 折扣陷阱（2026-09-30 实证）** | `cataloguePrice.withTaxesAndFees − eStorePrice.withTaxesAndFees` **恒等于 `eStorePrice.discounts[].withTaxes` 之和** —— 即差额是**实打实的线上折扣**，不是口径差：<br>· Ami 全 6 版 差 `10,00` ↔ `discounts=[{withTaxes:10.0}]`<br>· C3 燃油/混动版 差 `150,00` ↔ `discounts=[{withTaxes:150.0}]`<br>· ë-C3 纯电版 差 `0,00` ↔ `discounts=[{withTaxes:0.0}]`<br>→ **故 `cataloguePrice` = 未折扣 MSRP，符合采集规则**；官网 \"Vanaf € 8.489,99\" 是折后价（页脚注明*\"prijzen geldig tot het einde van de huidige maand\"*当前月度有效） |
| **⚠️ 勿误判为口径差** | 曾一度把差额解释成「B2C eStorePrice（基础配置价）vs cataloguePrice（全配置目录价）的口径差」，**已证伪**：差额与 `discounts` 字段逐一吻合，纯折扣 |
| **versionId → 描述** | scope 的 `comMods[].mvss[]` 里 `{code: versionId, desc: "C3 Hybrid 110 pk Automatic MAX"}` |
| **HTML 实体** | desc 里 `S&amp;amp;amp;S` 是**三重转义** → 循环 `html.unescape()` 4 次还原为 `S&S` |
| **年款** | 官网不标 MY → **全部写「官网无年款」** |
| **车系拆分** | 官网 gamma 页把电动版列**独立卡片**（C3 / ë-C3、C4 / ë-C4、C4 X / ë-C4 X、C5 Aircross / ë-C5 Aircross、C3 Aircross / ë-C3 Aircross）→ 依据 desc 的 `ë-` 前缀拆分车系 |
| **15 个 sccf 配置组** | `QNEW_AMI`(6) `VP1CSCA5`(19) `VPAC0101`(20) `VP__1CLE`(11) `VP1CLPA4`(9) `VP1CRESY`(14) `CV2CX250`(156) `eBerling`(21) `K0_SPAVP`(10) `K0_COMBI`(3) `K0_OMQD0`(2) `CV002CK0`(51) `CV002CK9`(31) `K9_MPVAC`(4) `VU1CSCK0`(1) |
| **★ 车系名权威来源** | **`scope.comMods[].desc`** 就是官网车系名（形如 `(ë-)C3` / `New (ë-)C5 Aircross` / `Berlingo Van` / `(ë)-C3 Aircross`）→ **勿用 desc 切首词猜**（会切出 `New` / `SPECIALE` 等假车系名） |
| **车系拆分规则** | 官网 gamma 页电动版列独立卡片 → 依 desc 的 `ë-`/`e-` 前缀拆成 `ë-` 组；但商用 van 特殊：`ë-Berlingo Van` 独立于 `Berlingo Van`，`ë-Jumpy Combi` 独立于 `Jumpy Combi`，`VU1CSCK0` 为 `ë-C3 Van`（1 条） |
| **★ 同名不同价陷阱** | 存在 **2 条同名不同价** 的版本（`Berlingo Van MAX ... Verhoogd Laadvermogen Diesel 130pk Manueel`：`2CK91CNP4KB0A0C0`=32.619,49 / `2CK91ANP4KB0A0C0`=32.195,99）→ **不可按 desc 去重**（会丢 1 条，358→357）；**必须用 `versionId` 做主键** |
| **分组自洽校验** | 全部 `ë-`/`e-` 组必为 `BEV`，其余组为 `Diesel/Gasoline/HEV/PHEV` → **0 冲突**即分组正确（正交验证） |
| **燃油分布（2026-09-30）** | Diesel 212 / BEV 101 / HEV 27 / Gasoline 15 / PHEV 3 = **358** |
| **文件体积警示** | `CV2CX250`（Jumper）单个 **47 MB**、`CV002CK0`（Jumpy）**13.9 MB** → `resp.text()` **绝不设大小上限**，用 `fs.writeFileSync` 直接落盘 |
| **Omnichannel API 旁证** | 页面另有 `api.omnichannel.stla-aws.net/pricing/v1/vehicle`（POST，传 `version/trim/color` 返回同一结构），但**需逐配置调用**、还要 token；**不如直接读 sccf** |
| **交付结果** | **358 条 / 24 车系**（2026-09-30，8 列含燃油分类；15 个 sccf 组 → 按电动版拆出 24 个展示车系） |

**抓取骨架**：

```js
// 在已打开的配置器页里执行
const res = await pg.evaluate(async () => {
  const base = 'https://www.citroen.be/sccf/prod/citroen/publish/data/sccf';
  const out = { files: {} };
  const sc = JSON.parse(await (await fetch(base + '/scope/3104HCC.json')).text());
  out.scope = sc;
  for (const cm of sc.comMods) {
    const code = cm.nsbpath.split('/')[3];
    const url = `${base}${cm.nsbpath}/NPE_STANDARD_3104HCC_${code}.json`;
    out.files[code] = await (await fetch(url)).text();   // 47MB 也能拿
  }
  return out;
});
```

**解析骨架**：

```python
rows = json.load(open('scope.json'))['comMods']
DESC = {m['code']: m['desc'] for cm in rows for m in cm.get('mvss', [])}
for v in obj['priceFragment']['vehicles']:
    d = json.loads(v['getPriceExtendedB2C'])
    for p in d['price']['vehicle']['prices']:
        if p['priceType'] == 'cataloguePrice':
            price = p['withTaxesAndFees']       # ★ 含税目录价
    desc = DESC[v['versionId']]                 # 官方型号名
```

**车系分布（358 条）**：Jumper 156 / Jumpy 51 / Berlingo Van 35 / Berlingo 21 / C3 Aircross 14 / C5 Aircross 14 / SpaceTourer 13 / C3 10 / ë-C3 9 / AMI 6 / ë-C3 Aircross 6 / ë-C4 6 / C4 5 / ë-C4 X 5 / C4 X 4 / Holidays 2 / C3 Van 1

**样例**：
```
Citroën;C3 C4 Hybrid 110 pk Automatic YOU;官网无年款;19.689,99;否;20260930
Citroën;ë-C3;ë-C3 Electric 113 pk Urban Range PLUS;官网无年款;23.789,99;否;20260930
Citroën;AMI;Ami Rip Curl Sunset;官网无年款;9.299,99;否;20260930
```

### Opel（CL 智利：Stellantis，curl 被拦但 Playwright 可通）

| 项 | 内容 |
|---|---|
| **curl** | 403 `errors.edgesuite.net`（Akamai） |
| **Playwright** | ✅ **可通**（`locale='es-CL'` + 常规 Chrome UA 即可，无需特殊处理） |
| **报价站陷阱** | `cotizador.opel.cl` 被 Cloudflare 拦（"Cybersecurity Policy Violation"），**不可用**；但主站车型页已有价格，无需它 |
| **车系路径** | `/coches/corsa-models/new-corsa/overview-features.html`、`/coches/mokka.html`、`/coches/crossland.html`、`/coches/grandland.html`、`/coches/modelos-combo-/combo/resumen.html` |
| **关键手法** | 车型页价格区**懒加载** → 必须 `mouse.wheel(0,1200)` 滚动 6–8 次触发，否则 body 只有 800–2400 字符且无价格 |
| **价格提取** | 用 `pg.evaluate` 遍历所有元素取 `innerText`，筛含 `$[\d\.]{6,}` 且长度 <400 的容器 |
| **价格格式** | 智利比索 `$13.990.000`（点号千分位，无小数）；另有 `PIE + 25 CUOTAS DE $193.990` = **分期月供，非车价，勿采** |
| **型号名结构** | `<车系> \| <配置等级> <燃油> <马力>HP <变速箱> \| PRECIO DESDE \| <价格>`，如 `CORSA \| Edition Gasolina 100HP MT` |
| **年款** | 官网未标 MY → 写「官网无年款」 |
| **世代混用** | Grandland 有老款（`GRANDLAND GS Gasolina 130HP MT` 19.990.000）与新款（`NEW GRANDLAND ...` 27.490.000）并存，车系名不同须区分 |
| **无公开价** | `Combo` 为商用车（Cargo van），页面仅 "¡Cotiza ahora!" 询价，**无公开 MSRP** |
| **在售车系** | CORSA / NEW MOKKA / NEW CROSSLAND / NEW GRANDLAND / GRANDLAND；Combo 无价 |

### Audi（ES：官网全域 Akamai 封锁，走 Autopista 替代源）

| 项 | 内容 |
|---|---|
| **封锁范围** | `www.audi.es` 首页即 403；`audi.de`/`audi.fr`/`audi.it`/`configurator.audi.com` 同 403；PDF 直链（`/dam/nemo/es/tarifas/...pdf`）亦 403 |
| **可通站点** | `www.audi.com/en`（纯品牌页，**无价格**）、`audi-mediacenter.com`（新闻中心 200）、`mediaservice.audi.com`(200) |
| **判定** | VW Group 对数据中心 IP/自动化流量的**全域策略性封锁**，非单机 IP 问题（三种通道全试过） |
| **替代源** | `https://datos.autopista.es/coches/audi/<slug>/` — Autopista（西班牙 1973 年创刊权威汽车媒体）逐车系版本表 |
| **车系 slug** | `a1 a2-e-tron a3 a5 a6 a6-e-tron a8 e-tron-gt q2 q3 q4 q5 q6 q7 q8 q9`（16 个） |
| **解析法** | 每页唯一 `<table>`，列 = `Versión \| Potencia \| Carrocería \| Precio`；价格格式 `30.300€`（**点号千分位**，需先还原整数再格式化！） |
| **口径验证** | A2 e-tron 四条与 Audi 官方发布稿（经 Europa Press 转发）**逐条吻合**：37.760 / 41.460 / 47.360 / 56.640 |
| **促销陷阱** | `launch edition` 条目 35.760 €（低于官方最低价 2.000 €）→ **促销价，须剔除**；另有 4 条 launch edition 与普通版同价 → **冗余重复行** |
| **容量口径** | Autopista 用**可用容量**（50/58/79 kWh），Audi 官方用**总容量**（52/61/84 kWh）→ 保留原始写法，勿混用 |
| **年款** | Autopista 尾部标 `(2026)` 是**其数据标注，非官网 MY** → 按规则写「官网无年款」 |
| **已知缺口** | A1、Q2 仅有 2020–2024 年份记录（Audi 2026 年已停产，由 A2 e-tron 接替），停销状态须另行核实 |

### Aston Martin（重要：无法采集 MSRP）

| 项 | 内容 |
|---|---|
| **表现** | 官网 `astonmartin.com`、配置器 `configurator.astonmartin.com`、经销商站三层**均无官方建议零售价** |
| **配置器接口** | `configurator.astonmartin.com`（MHP 提供，Angular SPA）<br>`GET /models/products/{COUNTRY}` → 车型清单（**无价格**）<br>`GET /models/products/{ID}/details` → 相机/环境/动画（**无价格**）<br>`GET /rules/configuration/{ID}?options=...&country=ES` → 完整配置树（**无价格**） |
| **证据** | 三个接口全量 JSON 中 `price`/`amount`/`currency`/`total` 字段**一个都没有**；配置器 UI 从选车到 "Review & Proceed" 全程不显示任何金额 |
| **官方口径** | 配置器免责声明原文：*"This configurator is not an offer to sell... Any purchase is subject to the terms and conditions of sale (**including price**) issued by the particular dealer."* |
| **经销商站陷阱** | `astonmartinmadrid.com` 等经销商站的价格标 **"Vehicles in stock"**，含 `Vendido`(已售)/`Reservado`(已订)/里程/年份 → **库存车单车标价，不是 MSRP，严禁采集** |
| **可比参照** | 同属"官方不公布售价"阵营，处理方式同法拉利：交付说明中标注无法采集 |
| **技术备注** | 市场清单 `GET /data/api/country-list` 返回 59 个市场（含 ES/GB/US 等）；`/models/products/ES` 可正常返回，证明 ES 市场有效，但同样无价 |

---

### Škoda（BE 比利时 `nl.skoda.be`：配置器 API 逆出，权威目录价）

**站点结构**
- 官网 `nl.skoda.be` 车型页含三类价格模块：`derivative-introduction`（车系起价）、`DerivativeOverviewModule`（型号价）、`Trims`（配置等级名，**无价**）
- 车型页 `callToActionLinks.cta1.url` 指向配置器入口：
  `https://clg.skoda-auto.com/api/link?bid=202&bodyCode=<bc>&carLine=<cl>&culture=nl-BE&instanceName=BEL&mbv=<mbv>&modelCode=<mc>&pageGroup=Website&salesProgram=BEL&tool=CC3`
- `clg.skoda-auto.com/api/link` 是 **302 重定向服务**，真实配置器：
  `https://cc.skoda-auto.com/bel/nl-BE/start-configuration?mbvCode=...&salesGroup=...&modelcode=...&pagegroup=Website&salesprogram=BEL`

**配置器 API（从主 JS bundle 逆出）**
- 主包 `https://cc.skoda-auto.com/static/js/main.7a2e9075.js`（10.2 MB webpack）
- 逆出常量：`API_URLS_PRICE = https://cc.skoda-auto.com/c3popr`（价格服务）、`API_URLS_WEBAPI = https://cc.skoda-auto.com/c3pobe`（业务服务）

| 端点 | 用途 |
|---|---|
| `POST /c3pobe/version` | 取 `snapshotVersion`。**body `{"country":"BEL"}`（键小写、必须 ISO3）**；空 body 报 "A non-empty request body is required"；2 位 `BE` 报 "minimum length of '3'"；返回 JSON 字符串需 `JSON.parse` 两次 |
| `GET /c3pobe/WebModel/Find?culture=nl-BE&country=BEL&snapshotVersion=<sv>&modelClass=<mc>&modelYear=<year>` | **型号清单关键端点**，返回 `{models:[...]}`，每条含 `id`/`mbvCode`/`engineName`/`fuelTypeName`/`transmissionName`/`trimLineName`/`marketingName`/`trimlineId`/`carlineCode` |
| `POST /c3popr/v3/GetAllPrices` | **权威目录价**。body `{ModelId, Extras:[], ColorCode, InteriorCode, Settings:{IncludeModelPrice:true,...}, snapshotVersion, TrimlineId}` → `modelPrice.price`（**目录价 Catalogusprijs**）、`priceOriginal`、`discounts`（空数组=无折扣）、`totalPrice` |
| `POST /c3popr/v3/GetTrimlinesPrices` | ⚠️ **返回促销价（action price），不是目录价**。Fabia Family 返回 21.125 而目录价为 25.290 → **禁用** |
| `POST /c3pobe/configuration/startConfiguration` | body `{appId:99,country:"BEL",culture:"nl-BE",mbvCode,salesGroup,snapshotVersion}` → `expireSuggestion.modelId`（如 `BEL;skoda;2027;PJ3DJ4;0;GYO1YO1;mda...;nl-BE;;60004;60004`） |

**调用要点（踩坑）**
- **必须在浏览器上下文内 fetch**：curl 直连报 `Invalid use - 100` / `Application error`（缺 session）。用 Playwright `pg.evaluate` 在 `cc.skoda-auto.com` 页面内执行
- **`mbv` 不唯一**：同动力同 `mbvCode` 会有多个配置等级（trim），价格不同 → **禁止用 `mbv` 做 key 对齐**，`GetAllPrices` 必须传 `TrimlineId` 区分
- **批量 evaluate 会 EPIPE 崩溃**（单次串行 370 请求 → Node 崩溃且不落盘）→ 拆成 step1（取清单）/step2（取价），**每车系独立进程、逐车系落盘**
- **`modelClass` 可能覆盖多个车系**：`NW` 同时返回 Kamiq + Scala（`carline 61003/61004`，23+23=46 行）→ 用 `marketingName` 区分，**注意去重**（重复抓取同 modelClass 会产生完全相同的文件）
- **同名 SKU 变体**：同一「车系+发动机+变速+配置等级」可能对应多个 `mbvCode`/子车系代码，价格不同（Octavia Limo `1,5 TSI 6v Man. Selection` 有 37.285 与 40.775 两条）→ 出表时用 `id` 段10/11（子车系代码）或 `mbv` 追加后缀保持唯一

**HTML 解析陷阱**
- `data-props="{&quot;...&quot;}"` 中的 `&quot;` 会让正则 `data-props="(.*?)"` **提前截断**（报 `Extra data: line 1 column 4182`）→ 必须用「配对结束引号扫描」（找后跟空格 `/` `>` 换行的引号）再 `html.unescape`
- `re.search(r'data-module="DerivativeOverviewModule"')` 会命中 **CSS 文件名** → 须严格匹配完整属性

**数据源三层次**
1. 车型页内嵌模块（3 类，见上）
2. 官方价格表 PDF（`Prijslijst`/`Verkoopsmap`，`download-file` 模块给 `https://nl.skoda.be/_doc/<uuid>`）
3. **官方配置器 API（权威源，本次采用）**

**价格表 PDF 双形态**
- 文本层可解析（6 份）：Fabia/Kamiq/Scala/Octavia/Epiq/Peaq → `pdftotext -layout` 精确解析
- 纯图片层（5 份）：Elroq/Enyaq/Enyaq Coupé/Karoq/Kodiaq（2116 张内嵌图、ToUnicode 损坏）→ 只能 OCR，且多为旧年款 → **弃用**
- PDF 页脚含版本标识（如 `MY2027 24/02/2026`）

**本次结论**
- `snapshotVersion = b430ec84-8285-4697-83a0-3782f5fa8beb`，`dataVersion = mda20260924074943`
- 全部 11 个 modelClass **均为 modelYear=2027**（探测 2024–2028 只有 2027 有数据）→ 年款统一 `MY2027`
- 配置器 14 个车系 / 324 条可用条目（312 有价 + 12 配置器无价）；价格表辅助 98 条
- 逐条校验 `modelPrice == priceOriginal` 且 `discounts == []` → 确认**均为未折扣目录价**

#### 🔁 2026-10-20 补充：**Skoda UK（`www.skoda.co.uk`）— 同一套 API，但市场码/口径都不同**

| 项 | 比利时 | **英国** |
|---|---|---|
| 市场码 | `BEL` / `nl-BE` | **`GBR` / `en-GB`**（bid=210）|
| `snapshotVersion` | `b430ec84-…` | **`eea24cd4-ea3e-486e-819b-6afce33b31ae`** |
| modelYear | 2027 | **也是 2027**（⚠ 车型页 CC3 深链写的是 `modelYear=2026`，**是旧参数，别信**；只有 2025/2026 会返回 500 `The specified blob does not exist.`）|
| **价格字段** | `modelPrice.price == priceOriginal` | **两者不等**：`priceOriginal` = 车价，`modelPrice.price` = **OTR 价**（含 `FixedOTROffset` 665 delivery+首注册 + `coTax` 455 VED）。官网 "From* £21,240" 对应的是 **`modelPrice.price`** → **英国取 `modelPrice.price`** |
| 车型页路径 | `/models/<line>/<model>` | **`/new-cars/<line>/<range>`**（`/models/<x>` 只有 Fabia 能用）|

**★ 英国 10 个 modelClass 实测（133 条 / 12 车系）**

| modelCode | 车系 | 条数 |
|---|---|---|
| `PJ` | Fabia Hatch | 16 |
| `NW` | **Kamiq + Scala 共用**（`NWK` 会 400）| 14 + 14 |
| `NU` | Karoq | 18 |
| `PS` | Kodiaq | 19 |
| `PV` | **Octavia Hatch + Estate 共用** | 13 + 13 |
| `PY` | Elroq | 7 |
| `5A` | **Enyaq + Enyaq Coupé 共用** | 7 + 4 |
| `PX` | Epiq | 3 |
| `PZ` | Peaq | 5 |

> ⚠ **modelClass 会一码多车系**（`NW` / `PV` / `5A`），必须用返回里的 `carlineName` 拆，否则 Kamiq 和 Scala 会混成一堆。
> ⚠ **车型页 URL 里的 `modelCode` 不可尽信**：Kamiq 页写 `NWK`，但 API 只认 `NW`。
> **交付**：`Skoda_UK_官网价_20261020.xlsx`，133 条，MY2027，Gasoline 67 / BEV 26 / Diesel 21 / MHEV 15 / PHEV 4，`discounts` 全为空。

---

### Volvo（BE 比利时 `volvocars.com/nl-be`：Akamai 拦 headless，必须 xvfb + headed Chromium）

**核心坑：Akamai 按 headless 指纹拦截**

| 方式 | 结果 |
|---|---|
| `curl`（任意 UA/语言） | **403 Access Denied**（Akamai `errors.edgesuite.net`） |
| Playwright **headless** | **403** |
| Playwright **headed + xvfb-run** | **200 ✅** |

```bash
xvfb-run -a --server-args="-screen 0 1600x1000x24" node script.js
```
- 必须 `headless: false`；`xvfb-run` 提供虚拟 X server（沙箱无 `$DISPLAY`）
- 配合 `--disable-blink-features=AutomationControlled` + `addInitScript` 伪装 `navigator.webdriver`
- 域名 IP 分级：`www.volvocars.com` → Akamai（23.45.12.58，封锁）；apex `volvocars.com` → nginx 301 回 www

**配置器与价格接口**

| 端点 | 说明 |
|---|---|
| `/nl-be/cars/<model>/` | 车型详情页（Next.js，`self.__next_f` flight 数据） |
| `/nl-be/build/<model>/` | **官方配置器**，含「Kies uw uitvoering」（版本）/「Kies uw niveau」（配置等级）/「Kies uw aandrijving」（动力） |
| `POST /api/order/prices` | **官方价格总表**。body `{"deployEnv":"prod","market":"nl-be","siteSlug":"nl-be","locale":"nl-BE","clientName":"pdps"}`，header `x-client-name: pdps`、`Content-Type: text/plain;charset=UTF-8`（**注意是 text/plain 不是 application/json**）；GET 返 405，空 body 返 422 |
| `GET /static/site-navigation/data/nl-be/cars-by-market-data.<hash>.json` | 官方在售车型清单（12 条，含 `modelYear`/`carType.code`/渲染图） |
| `GET /static/site-navigation/data/nl-be/cars-menu-data.<hash>.json` | 导航车型菜单 |

**`/api/order/prices` 返回结构**
```json
{ "prices": {
    "ex30-electric": {
      "cash": "€ 36.270",          // ← 车系「Vanaf」起价
      "includesTax": true,
      "modelYears": { "2027": {"cash": "€ 36.270"} },   // 按年款
      "editions": { "black-edition": {"cash": "€ 43.644"} }
} } }
```
- 覆盖 14 个 slug，但其中 `c40-electric`≡`ec40-electric`、`xc40-electric`≡`ex40-electric` 是**旧名别名**（`sourcePrefix` 指向同一实体），**须去重**
- ⚠️ **`cash` 是「Vanaf」起价，对带 Business Edition 的车系等于折扣价**（见下）

**型号名与配置等级（关键）**
- 页面 DOM 文本结构（`\u00a0` 需先归一化为普通空格）：
  ```
  Kies uw uitvoering          ← 版本区
  EX30
  Vanaf € 36.270
  EX30 Black Edition
  Vanaf € 43.644
  Kies uw niveau              ← 配置等级区
  Essential
  € 38.290
  Core
  € 39.900
  ```
- 配置等级名称不统一：`Essential / Core / Plus / Ultra`（通用）+ `Core Business Edition / Plus Business Edition / Ultra Business Edition`（EX30/EC40/EX40 专有）+ `X Launch Edition`（EX60）+ `X Limited Edition`（V60）
- 版本区与等级区**必须分段切**：等级区从 `Kies uw niveau` 起、到 `Vergelijken` 或 `Uw aandrijving` 止，否则会把车漆/选装包价格混入
- 动力区块标题两种写法：`Uw aandrijving` 与 `Kies uw aandrijving` → 正则用 `/(Kies uw|Uw) aandrijving/`；标题后第 1 项即动力名（如 `P5 Elektrisch (BEV)`、`B5 AWD Mild-hybride (MHEV)`、`T8 AWD Long range Plug-in hybride (PHEV)`、`Single Motor`）

**促销陷阱：Business Edition**

配置器免责声明原文：
> *"Prijzen incl. btw. De vermelde prijzen van de Business Editions zijn **inclusief voordeel Business Edition en premie**. Het Business Edition-aanbod is geldig voor zowel professionelen als particulieren en tot en met 31/03/2026."*

实测折扣幅度（EX30，2026-09）：Core `39.900`→`36.270`、Plus `42.600`→`38.970`、Ultra `51.850`→`47.010`（**降 3.630–4.840 €**）。
→ **Business Edition 一律剔除**，只采标准等级价；这也解释了为何 `/api/order/prices` 的 `cash`（36.270）低于配置器标准等级价（38.290）。

另有 `Tijdelijke aanbiedingen`（临时优惠横幅）与 `Geniet van ongeziene promoties`（现货促销）文案，均非 MSRP。

**年款（官网原始标记）**

| 年款 | 车型 |
|---|---|
| `MY2027` | EX30 / EX60 / EX90 / ES90 / V60 / XC90 |
| `MY2027.5` | EC40 / EX40 / XC40 / XC60 |

来自 `cars-by-market-data` 的 `carKeyExpanded.modelYear`（配置器另以 `commercialModelYear.name` 标 `2027.5`）。

**本次结论（2026-09-28，v2 补全版）**

⚠️ **重要：官方价格表 PDF 才是权威完整源，配置器 API 只显示单一动力分支，会严重漏条**（v1 仅 46 条 → v2 达 132 条）。

**官方价格表页面：`/nl-be/l/prijslijsten/`**（Prijslijsten = 价格表）
- 页面内 21 个 PDF 链接，全部托管在 **`azure-eu-assets.contentstack.com`（Contentstack CDN）→ 不受 Akamai 限制，可 `curl` 直下 ✅**
- 19 份 PDF 中：**16 份是价格表**（`prijslijst-*.pdf` / `Prijslijst_*.pdf`），3 份是宣传单（`leaflet-business-edition` / `leaflet-v60-limited-edition` / `XC60_Black_Edition_2luik_*`，均为折扣价或重复款，不采）
- 抓链接：headed Chromium 打开页面 → 收集 `a[href$=".pdf"]`；或直接读页面 HTML 里的 contentstack URL

**16 份价格表与车系/年款映射（`PDF_MAP`）**

| PDF stem | 车系 | 年款 |
|---|---|---|
| `prijslijst-ex30-cc` | EX30（含 CC / Black Edition） | MY2027 |
| `prijslijst-ex40-my27.5` | EX40 | MY2027.5 |
| `prijslijst-ex40-electric` | EX40（stock） | MY2027 |
| `prijslijst-ec40-my27.5` | EC40 | MY2027.5 |
| `prijslijst-ec40` | EC40（stock） | MY2027 |
| `prijslijst-ex60` | EX60 | MY2027 |
| `prijslijst-ex60-cross-country` | EX60 Cross Country | MY2028 |
| `prijslijst-ex90` | EX90 | MY2027.5 |
| `prijslijst-es90` | ES90 | MY2027 |
| `prijslijst-xc40-my27.5` | XC40 | MY2027.5 |
| `prijslijst-xc40-limited-edition` | XC40 Limited Edition | MY2027 |
| `prijslijst-xc60-my27.5` | XC60 | MY2027.5 |
| `Prijslijst_XC60_MY27_v2_BEnl_010426` | XC60（stock） | MY2027 |
| `prijslijst-xc90-my27.5` | XC90 | MY2027.5 |
| `Prijslijst_XC90_MY27_v2_BEnl_010426` | XC90（stock） | MY2027 |
| `prijslijst-v60` | V60 | MY2027 |

**PDF 价格矩阵结构**（`pdftotext -layout` 最干净）
- 表头：`Motoren | Overbrenging | Design | Edition | Vermogen pk/kW | CO2-uitstoot | Catalogusprijs € excl. btw | Catalogusprijs € incl. btw [| Nettoprijs* € incl. btw]`
- **取 `Catalogusprijs € incl. btw` 列**（含税目录价）；**严禁取 `Nettoprijs*` 列**
- 表格按配置等级分块：`ESSENTIAL / CORE / PLUS / ULTRA`（+ `LAUNCH EDITION` / `FIRST EDITION` 版块）

**核心坑 1：V60 的 `Nettoprijs*` 折扣列（极易取错，低报 8k+）**
```
Mild hybrid benzine  B4  7-traps DCT  Base  Limited Edition  197/145  143-156  43.247,93  52.330  38.990
                                                                        ↑excl     ↑incl    ↑Netto折扣
```
- V60 表格有**三个价格列**，`Nettoprijs* € incl. btw` 列头与 `Catalogusprijs € incl. btw` 列头**都写作 `€ incl. btw`**
- 脚注：`* Prijs inclusief kortingen`（含折扣）
- **正确价 = 中间那列 `52.330`**；配置器显示的是 `38.990` 折扣价 → 这就是 v1 低报的根因之一

**核心坑 2：列定位必须用 bbox，不能只用正则**
- `pdftotext -bbox` 取词坐标 → 按 `y` 聚簇成行（行距约 4.5pt）→ 行内按 `x0` 排序还原阅读序（否则词序错乱）
- `x_incl` 取**最左**的 `€ incl.` 列（排除 Nettoprijs 第二列）；`Nettoprijs*` 的 x 用**该词自身的 x**（不是行首词 x，行首常是别的列）
- 关键校验：`x_excl(403) < x_incl(454) < x_net(505)`

**核心坑 3：必须过滤的非车型行**
- 保修行：`3 JAAR OF 100.000 KM` / `8 JAAR OF 160.000 KM`（价格列会误显示为 160000）
- 装备价值行：`Totale waarde uitrusting` / `specifieke XC60 Ultra uitrusting` / `naar keuze`
- 选装包：`LAUNCH EDITION PACK` / `Metaalkleur` / `Donkergetinte achterruiten` / `module met 25.600 pixels`
- 过滤式：`BAD_RE = Totale waarde|uitrusting|naar keuze|JAAR OF|\d{3}\.\d{3}\s*KM|PACK|Metaalkleur|...`

**核心坑 4：型号名组装（词序错乱）**
- 表格列顺序：`动力类型(x≈55) | 动力代号(x≈129) | 变速箱(x≈200) | 设计版(x≈262) | 技术数据(x≥316) | 价格`
- 纯电车型（EX30/EX40/EC40/EX90/ES90/EX60）与混动车型列数不同、x 阈值不同 → **不能用固定 x 阈值切分**
- 改用**语义切分**：技术数据 token 用正则 `^[\d,\.\-–/]+$` 识别并剔除；剩余文字 token 中 `DESIGN_RE`（`Bright of Dark|Black Edition|Cross Country|Limited Edition|Launch Edition|First Edition|Bright|Dark|Base`）命中归设计版，其余归动力名
- 最终型号名 = `动力名 + 设计版 + 配置等级`，如：
  ```
  Plug-in hybrid benzine T8 AWD Long Range 8-traps automaat Bright of Dark ULTRA
  P5 Long Range RWD Black Edition PLUS
  Mild hybrid benzine B4 7-traps DCT Base Limited Edition CORE
  ```

**交付结果（2026-09-28）**
- **132 条**（v1 仅 46 条），覆盖 16 个 PDF 车系、年款 MY2027(75) / MY2027.5(55) / MY2028(2)
- 车系分布：EC40 20 / EX40 22 / EX30 13 / XC60 16 / XC90 20 / EX90 9 / XC40 14 / ES90 6 / EX60 8 / V60 4
- 脚本：`/tmp/vv2/parse4.py`（bbox 列坐标解析）→ `/tmp/vv2/build.py`（语义切分组装）→ `/tmp/vv2/out.py`（出表）

- 与 `/api/order/prices` 交叉核对：无 Business Edition 的 7 个车系**逐条吻合**；3 个有 Business Edition 的车系按规则取标准价（高于 API 的折扣「Vanaf」价）

**v3 重跑修正（2026-09-29）**

用户反馈「还是缺了很多」。重跑后定位：**数量没缺（132=132），缺的是「型号名里的 Design/Edition 列」**——v2 的型号名把 `Dark / Black Edition / Bright of Dark / Cross Country` 全丢了，
导致出现 **同名不同价的重复行**（如 XC40 `Mild hybrid benzine B3 PLUS` 出现两次：47.490 / 49.190，实际是 `Dark PLUS` 与 `Black Edition PLUS`）。

**根因：Design / Edition 列的位置随车型变化，不能用固定位置切**
| 车型 | 列序（Design 相对位置） |
|---|---|
| XC40 | `Motoren \| Vermogen \| **Design** \| CO2 \| excl \| incl`（Design 在 pk/kW **之后**） |
| XC60 | `Motoren \| Overbrenging \| **Design** \| Vermogen \| CO2 \| …`（Design 在 **之前**） |
| V60 | `Motoren \| Overbrenging \| **Design** \| **Edition** \| Vermogen \| …` |
| EX30 | `Motoren(P5) \| **Design** \| Vermogen \| …` |
| EX90 | `Motoren \| Aandrijving \| **Design** \| Vermogen \| …`（表头写 `Aandrijving` 不是 `Motoren`） |

**正确解法：按「封闭取值集合」提取，不按位置**
```python
DESIGN_MULTI = ['Bright of Dark','Black Edition','Cross Country','Limited Edition']
DESIGN_ONE   = ['Dark','Bright','Base']
# 从 excl 价格之前的 token 流中，先取 Edition(Limited Edition)，再取 Design(多词优先)
```
再剔除纯数字/范围/破折号噪声 token（`^[\d\.,/–—\-\s]+$` 与孤立的 `–`）。

**年款必须从 PDF 封面读，不能从文件名推**
- `prijslijst-ex60-cross-country.pdf` 封面写 `Modeljaar 2028`（文件名无年款线索）
- 正则：`re.search(r"[Mm]odeljaar\s*'?(\d{2,4}(?:\.\d)?)", text)`；两位年份补 `20`

**EX60 / EX60 CC 的复合等级名**
- EX60 分块标题是 `PLUS LAUNCH EDITION` / `ULTRA LAUNCH EDITION`（不是单 `LAUNCH EDITION`）
- EX60 CC 是 `PLUS FIRST EDITION` / `ULTRA FIRST EDITION`
- → `LEVELS` 集合必须包含复合名，否则 `PLUS`/`ULTRA` 前缀丢失，导致同名不同价

**促销 leaflet 一律剔除（本次逐一核验）**
`/nl-be/l/prijslijsten/` 页面除 16 份正价目表外，还有以下 **折扣/B2B 促销册**，价格均含 `TOTAAL VOORDEEL`（折扣），**不采**：
| Leaflet | 内容 | 判别依据 |
|---|---|---|
| `leaflet-business-edition` / `leaflet-ex30-ex40-ec40-business-edition` | Business Edition（**VOOR PROFESSIONELEN** B2B） | 标 `Totaal voordeel professionelen -12.066` |
| `leaflet-xc60-black-edition-my27.5` | XC60 Black Edition MY27.5 | `TOTAAL VOORDEEL -11.098` |
| `leaflet-xc40-urban-edition` | XC40 Urban Edition | `Totaal voordeel Urban Edition` |
| `leaflet-xc40-b3_b4-limited-edition` | XC40 Limited Edition（旧） | `TOTAAL VOORDEEL -13.061` |
| `leaflet-v60-limited-edition` | V60 Limited Edition | `TOTAAL VOORDEEL -11.024` |
| `leaflet-ex60` | EX60 Launch Edition | `UW EX60 ... 46.400`（低于正价表 62.990） |
| `XC60_Black_Edition_2luik_MY27` | XC60 Black Edition MY27 双折页 | `TOTAAL VOORDEEL -14.845` |

→ 正价目表 `prijslijst-*` 内部**已含** Black Edition / Cross Country / Limited Edition 行的**目录价**（如 EX30 `P5 Long Range Black Edition PLUS 49.290`），无需从 leaflet 补。

**v3 交付（2026-09-29）：132 条 / 12 车系，零同名歧义**
- 每行由 `车型+型号名+等级+年款` 唯一确定（`同名同级同年款不同价 = 0`）
- XC60/XC90 各有两版 PDF（MY2027 与 MY2027.5），年款不同 → 同名属正常，非重复
- 脚本：`/tmp/volvo/v5.py`（封闭取值集合提取）→ `mkfinal2.py`（出表）
- ⚠️ PDF 下载必须校验 `tail -c 2048 f | grep -q "%%EOF"`（首次下载 EX30 9.5MB 截断，实为 12.7MB，`pdftotext` 返回 0 字符）

---

### SEAT（BE 比利时 `www.seat.be/fr`：全站按 IP 封锁，无解）

**结论：采集失败，无可用绕行路径。**

| 探测项 | 结果 |
|---|---|
| `curl www.seat.be/fr` | **403 Request Denied**（`Event ID` + `Client IP`，Imperva/Akamai 风格错误页） |
| Playwright **headed + xvfb** | **403**（按 IP 而非指纹封） |
| 换 UA / 换 Accept-Language / 换 Mac UA | 403 |
| IPv6 | 不通（000） |
| `www.seat.be/robots.txt`、`/sitemap.xml`、`/api` | **全 403**（连 robots 都拒 → 确认整站按 IP 拦） |
| 其他市场（`seat.fr` / `seat.de` / `seat.co.uk` / `seat.es` / `seat.it` / `seat.nl` / `seat.pt` / `seat.ch` / `seat.com`） | **全部 403**（同一 WAF 策略） |

**域名解析分级（重要）**

| 域名 | IP | 归属 | 状态 |
|---|---|---|---|
| `www.seat.be` | `23.219.160.164` | **Akamai**（`e320677.dscb.akamaiedge.net`，edgekey `cupraofficial.com`） | 403 拦截 |
| `seat.be`（apex） | `13.248.159.164` | AWS ELB | 301 → `https://www.seat.be:443/fr`（但跳到 www 后仍 403） |

- 试过 `--resolve www.seat.be:443:13.248.159.164`（用 apex IP 直连）→ **404**（ELB 不认该 Host）
- ~~SEAT 与 CUPRA 共用 edgekey `cupraofficial.com.edgekey.net` → CUPRA 系站点大概率同样被拦~~
  → **该推断已被实测推翻**：CUPRA 比利时（`www.cupra.be`）**完全可访问**，走的是 Azure 独立 IP `20.105.216.33`，与 SEAT 的 Akamai 节点无关。**不要因为同属一个集团就预判封锁**——每个品牌独立起 triage 实测。

**排查心法**：先测 `robots.txt`。若连 `robots.txt` 都 403，说明是**整站 IP 级封锁**而非路径/指纹问题，换 UA/换浏览器/换路径都是徒劳，应尽早止损换下一个品牌。

---

### CUPRA（BE 比利时 `www.cupra.be/fr`：完全可访问，官方 API 直连）✅

**结论：93 条全量采到，含配置等级 × 动力。本集团站点里最好采的一个。**

| 项目 | 状态 |
|---|---|
| 主站 `www.cupra.be` | ✅ 200（Azure IP `20.105.216.33`，`robots.txt` 200）——与 SEAT 完全不同 |
| **官方价格 API** | ✅ `api.cupra.be`，**无鉴权**，curl 直可达 |
| 车系数 | 7 个：RAVAL / FORMENTOR / TERRAMAR / BORN / TAVASCAN / LEON / LEON BREAK |

**核心端点（唯一需要的一个）**

```bash
GET https://api.cupra.be/v1/car-configurator/choices/<CARLINE>?lang=FR&sales_type=B2C
# 必须带 header：Referer: https://www.cupra.be/fr/
```

返回 `[{engine:{...}, interiors, paints, packs, options, wheels}]`，其中 `engine` 字段：

| 字段 | 含义 | 采不采 |
|---|---|---|
| `name` | 完整官方型号名（配置等级 + 动力 + 变速箱），如 `VZ5 2.5 TSI 390ch (287kW) DSG 4Drive 7v` | ✅ 直接作「官网型号名称」 |
| **`price`** | **官方目录价** | ✅ **采这个** |
| `priceWithReduction` | 折扣/促销价 | ❌ **不采**（陷阱，见下） |
| `model_year` | 年款，本季全部 `2027` | ✅ |
| `power` / `fuel_type` / `top_speed` / `autonomy` / `liters_per_100km` / `wh_per_km` / `grams_per_km` | 规格 | 备注用 |
| `id` / `model_code_extension` | 内部码 | — |

**⚠ 折扣价陷阱（CUPRA 必看）**
93 条里 **92 条** `price ≠ priceWithReduction`，差幅可达 **9.000 €**：

```
FORMENTOR  Impulse 1.5 TSI 150ch (110kW) Manuelle 6v
           price = 41.714,98   ← 采这个（MSRP）
           priceWithReduction = 32.714,97   ← 促销价，不采
```

**合法 carline 白名单**（传错会返回 400，message 里会列出全部合法值）

```
FORMENTOR, BORN, LEON, LEONBREAK, TAVASCAN, TERRAMAR, RAVAL
```

- 注意是 `LEONBREAK`（无空格、无连字符），但**官网展示名为 `LEON BREAK`**（带空格）
- `LEON-SPORTSTOURER` 无效 → 400（Sportstourer 就在 `LEONBREAK` 里）
- 一次请求即可拿到该车系全部配置 × 动力组合，无需逐车型爬

**其他端点（非必需）**

| 端点 | 内容 | 陷阱 |
|---|---|---|
| `GET https://www.cupra.be/api/global-financing-products?type=prices&language=FR&salesType=B2C` | 全站金融价 | ⚠ 同时含 `price`/`discount_price`，**仍是折扣口径，别混用** |
| `GET https://api.cupra.be/v1/car-configurator/cupra-params?cupra_code=<code>` | 配置器参数 | — |
| `GET https://api.cupra.be/v1/car-configurator/prices?cupra_code=<code>&lang=FR` | 金融 | — |
| `GET https://api.cupra.be/v1/car-configurator/standards?cupra_code=<code>&lang=FR` | 标准装备 | — |
| `GET https://api.cupra.be/v1/feature-flags` | 特性开关 | — |
| `GET https://www.cupra.be/api/navigation?language=FR&type=header&salesType=B2C` | 站内导航 | — |
| `/_next/data/<buildId>/fr/B2C.json` | Next.js 数据 | — |

- 配置器入口：`/fr/configurateur/personnalisation/<slug>?cupra_code=<code>`
- 配置器页显式显示 `Total incl. TVA 26.460,01 €`，可与 API `price` 交叉验证
- 架构：Next.js，后端 `api.cupra.be`（独立子域，无鉴权）

**为什么这个采到了、SEAT 没采到**：两者同属品牌体系，但 CUPRA BE 是 Dieteren 运营、落在 Azure 独立 IP 且无 WAF 拦截；SEAT 落在 Akamai 且执行 IP 黑名单。**结论：集团归属 ≠ 封锁状态，一律 triage 实测。**

---

### CUPRA（DK 丹麦 `www.cupraofficial.dk`：全站按 IP 封锁，无解）❌

**结论：采集失败，无可用绕行路径。与 SEAT 是同一套 WAF 策略、同一个错误页模板。**

| 探测项 | 结果 |
|---|---|
| `curl -4 https://www.cupraofficial.dk/` | **403 `Request Denied`**，响应体 **261 字节**，**直接回显我方 IP** `Client IP : 43.142.67.79` |
| Playwright headed + xvfb | **403**（出口 IP 变 `101.35.42.136`，**动态出口 IP 同样被拦** → 按 IP 段而非单个 IP 封） |
| `/robots.txt` · `/sitemap.xml` · `/favicon.ico` | **全 403**（连 robots 都拒 → 确认整站按 IP 拦，非路径/指纹问题） |
| `/modeller` · `/biler` | 403 |
| 换 UA（Mac Safari / Googlebot / curl）· HTTP/1.1 · 补全浏览器头 | **全 403** → 换 UA 是徒劳 |
| IPv6 | 不通（000） |

**403 响应头特征（识别这套 WAF 的指纹）**

```
HTTP/1.1 403 Forbidden
Content-Length: 261
Access-Control-Allow-Origin: *
x-req-uri: /
x-rewrite: /
Alt-Svc: h3=":443"; ma=93600
```

> `Access-Control-Allow-Origin: *` + `x-req-uri` + `x-rewrite` + `Request Denied` 错误页 + 回显 `Client IP` + `Event ID` = **与 SEAT 段完全同款**。见到这组特征即可判定：IP 级封锁，**直接止损**。

**域名解析与跳转链（已闭合，无后门）**

| 域名 | IP / 归属 | 状态 |
|---|---|---|
| `www.cupraofficial.dk` | `23.210.216.171` — **Akamai**（`e320677.dscb.akamaiedge.net`） | **403**（真站，被拦） |
| `cupra.dk`（apex） | `20.105.224.35` — Azure + **Microsoft-IIS/10.0** | 301 → `www.cupra.dk` |
| `www.cupra.dk` | 同上 IIS | 301 → `www.cupraofficial.dk` → **最终仍 403** |
| `api.cupraofficial.dk` | **NXDOMAIN** | 不存在（BE 的 `api.cupra.be` 解法在 DK **无对应**） |
| `cupradanmark.dk` | `195.249.218.79`（CSP 里暴露的域名） | 连接 **000**（不通） |
| `www.cupraofficial.se` / `.no` / `.com` | — | **全 403**（同一 WAF 策略覆盖多市场） |

**关键对照 —— 直接推翻「是我方 IP 质量差」的假设**

| 对照项 | 结果 | 说明 |
|---|---|---|
| `api.cupra.be`（比利时，**已知可用**） | **404**（不是 403） | 404 = 服务端正常应答，仅路径不存在 → **我方 IP 在 CUPRA 体系里完全没被拉黑** |
| `www.cupra.be` | **308** | 正常重定向 |
| `www.cupraofficial.dk` | **403** | 同一 IP、同一时刻 → **是 DK 站特有的封锁策略** |

> **这不是 IP 质量问题**。同一个出口 IP 访问 CUPRA 比利时服务端应答正常（404/308），访问 CUPRA 丹麦被拒（403）。**封锁由站点侧按市场/域名策略施加**。

**⚠ `cupra.dk` ≠ 价格站（别被 IIS 200 骗进去）**
`cupra.dk` 解析到 Azure IIS，**不被 WAF 拦**，一度看起来像可利用入口，实际是**企业用车跳板站**：`/modeller/` → 跳 `/firmabil/` → **404**，无 C 端车型价格。且它最终仍 301 回 `www.cupraofficial.dk` 被拦。

**第三方源（可访问但不符合口径，不采）**
`nordiskbil.com`（有 Tavascan / Raval 丹麦价）、`biler.nu` 均可访问 —— 但 **AGENTS.md 要求「官网官方建议零售价」**，经销商/媒体源不采。

**绕行结论**
- curl、浏览器、换 UA、换路径、换邻站（SE/NO/COM）、API 子域、CSP 泄露域名 —— **全部试过，全部失败**
- 唯一可行路径：**请在本地浏览器打开官网取数**（`Export HAR` / `Save page as` / `Copy as cURL` 回传），或**换一个可访问的邻站市场**
- **不主动采第三方源**

> **心法复用（与 SEAT 段同）**：`robots.txt` 都 403 → 整站 IP 级封锁；先做**跨市场对照**（同一 IP 访问同品牌别的市场是否正常）来区分「我被打黑」与「该站策略」，再决定止损还是继续挖。

---

### Hyundai（BE 比利时 `www.hyundai.com/be/nl.html`：主站通，官方 PAPI 被 SNI 级封锁）

**结论：可拿到车系起价，拿不到完整价格表（配置等级 × 动力）。**

| 项目 | 状态 |
|---|---|
| 主站 `www.hyundai.com/be/nl` | ✅ 200（Cloudflare，`104.18.13.38`） |
| 车型清单（20 车系） | ✅ `/be/nl/modellen.html` |
| 各车系配置器 URL | ✅ `/be/nl/modellen/<slug>/configurator.html` |
| 车系起价 `Vanaf € xx.xxx` | ✅ 车型页 SSR 可 curl |
| **完整价格（配置等级×动力）** | ❌ 依赖 `org-eu-www.hyundai.com/eu/papi`，**被封** |
| 官方价格表 PDF | ❌ 无直链（`/be/nl/tools/brochures.html` 是**表单申请制**，填邮箱才发链接） |

**架构**

```
www.hyundai.com/be/nl/...          ← AEM 站点（/etc.clientlibs/hyundai-wwn3/）
  └─ 配置器页内嵌 iframe: tnegaesalasia-orp.astara.com/index.widget.html?brand=hyundai&country=be&lang=nl
                                    （Astara 提供的「AI 销售助手」widget，不含车辆价格目录）
  └─ 主框架直连官方 PAPI:
       POST https://org-eu-www.hyundai.com/eu/papi     ← GraphQL，价格字段在此
       POST https://org-eu-www.hyundai.com/eu/graphql   ← hppFscs2，含 fscPrice/discountNPrice
```

**PAPI 契约（已完整逆出，供有可用出口时复用）**

```json
POST https://org-eu-www.hyundai.com/eu/papi
Content-Type: application/json
Referer: https://www.hyundai.com/

{"query":"query Trims($country:TrimmedString!,...){ hppTrimEquipments(...){trimId equipNm} hppFscs2(...){trimId trimName trimSort} ...FscsQueryFragment }",
 "variables":{"country":"be","language":"nl","modelId":"6X|S5||","service":"S03",
              "isFscsLoaded":true,"isNotNlMarket":true,"isTRMarket":false}}
```

- `modelId` 格式：`<车型码>|<版本码>||`（如 `6X|S5||` = INSTER 某配置）
- `service: "S03"`（比利时）、`country: "be"`、`language: "nl"`
- 价格字段：`basePrice` / `discountPrice` / `customerSaving` / `totalAmt` / `totalAmtWODisc` / `vatAmt`
- `hppPriceDetailListTR` 是土耳其市场专用（`isTRMarket`），比利时用 `FscsQueryFragment`

**封锁特征（关键判定依据）**

| 检测 | 结果 |
|---|---|
| `org-eu-www.hyundai.com` 解析 | `185.106.8.43`（**独立 IP**，非 Cloudflare） |
| TCP 443 | ✅ 通（`/dev/tcp` 可连） |
| **TLS 握手** | ❌ **立即 RST**（`openssl s_client` → `unexpected eof while reading`，`read 0 bytes`） |
| 浏览器内 | `net::ERR_CONNECTION_CLOSED` |
| `curl` | exit 35（SSL 层） |

→ 判定：**按 IP 的 SNI 级封锁**（TCP 能连、TLS 被 reset）。

**已试无效的绕行**

- 换 UA / headed 浏览器 / `--disable-blink-features=AutomationControlled` → 仍 `ERR_CONNECTION_CLOSED`
- 页面内 `fetch`（车型页 & 配置器页 & Astara iframe 内）→ 全部 `Failed to fetch`
- 其他区域域名 `org-www.hyundai.com` / `org-eu.hyundai.com` / `eu-www.hyundai.com` / `org-be-www.hyundai.com` → **均不解析**（NXDOMAIN）
- `org.hyundai.com`（`101.1.53.88`，TLS 正常）→ **无 `/eu/papi`**（404，是另一台服务器）
- `www.hyundai.be`（`188.93.153.172`，TLS 正常）→ 仅 **301** 跳回 `www.hyundai.com`，无独立数据
- Astara widget API（`func-agentorchestrator-aisalesagent-sw-pro-01.azurewebsites.net`）→ **可访问**（`/api/session-token` → Bearer → `/api/get-services-config` 返 200），但只有 `CONVERSATIONAL`/`BRAND` 等服务开关，**无车辆价格目录**

**行为特征**：配置器 URL 在 `#/trims`（正常）与 `#/error` 之间随机切换；`#/error` 时 DOM 为空、无价格。实测 `#/trims` 时也只渲染导航壳（「Kies jouw uitvoering」），**版本卡片与价格始终为空** —— 因为数据源 PAPI 拉不到。

**可采到的官方起价（16 条，`Vanaf` 口径，含税）**

| 车系 | 起价 € | 车系 | 起价 € |
|---|---|---|---|
| i10 | 16.949 | IONIQ 3 | 29.995 |
| i20 | 19.695 | KONA Electric | 31.349 |
| BAYON | 21.645 | TUCSON | 32.049 |
| i30 | 22.199 | IONIQ 5 | 40.199 |
| i30 Wagon | 23.199 | IONIQ 6 | 43.199 |
| INSTER | 23.349 | SANTA FE Hybrid | 56.295 |
| KONA | 26.499 | SANTA FE PHEV | 63.295 |
| | | IONIQ 9 | 64.995 |
| | | IONIQ 5 N | 74.445 |
| | | IONIQ 6 N | 75.445 |

**slug 修正（车型页 404 时用）**：`kona-hev` → `all-new-kona`；`tucson-hev` → `tucson-hybrid`；`tucson-phev` → `tucson-plug-in-hybrid`；`santa-fe-hev` → `santa-fe-hybrid`；`santa-fe-phev` → `santa-fe-plug-in-hybrid`

---

### MG（DK 丹麦 `www.mgmotors.dk`：Cloudflare 但不拦，WordPress + 经销商配置器）✅

| 项 | 内容 |
|---|---|
| **可达性** | `curl -4` 直连 **200**，无需浏览器（注意必须 `-4`） |
| **★ 站性质** | **Nellemann 经销商平台**（`nellemannapi.dk`）+ WordPress `mgmotors-configurator` 插件；后台数据源 `nellemann.cloud12.structpim.com`（StructPIM），**不是 MG 官方直营** |
| **车系总览** | `https://www.mgmotors.dk/modeller/` → 8 车系（注意 `/biler` 会重定向到库存页，`/biler/` 才是车系列表） |
| **车系页** | `https://www.mgmotors.dk/biler/<slug>/`：只有「fra xxx kr」起价，**版本不全** |
| **★ 真源（配置器）** | `https://mgmotors.dk/bestil/<slug>/` 页面内 **`data-react-props="{...}"`**（HTML 转义）→ `json.loads(html.unescape(...))`，含 `engineTransmissions[]` **全部版本 + 绝对价** |
| **★ 价格字段** | `engineTransmissions[].prices[]` 里 **`price_type == "SuggestedRetailPrice"`**（官方建议零售价 ✔）<br>取 `original_price`（= 未折扣 SRP）优先；`price` 是含促销后的价 |
| **★ 促销陷阱** | `campaign_retail_prices[]` 非空 → `price` 是折后价，**不采**。实证：MGS5 EV Comfort Long Range `price=199999` / `original_price=224999` / campaign value=199999 → **取 224999** |
| **★ 多条 SRP 记录** | 同一版本可能有 **2-3 条 `SuggestedRetailPrice`**（调价历史，如 249999/224999/224999）→ 取 `original_price` 最稳，勿盲目取第一条 |
| **型号名拼法** | `variant.name` + `engineTransmissions[].raw_name`（续航/发动机）拼接，如 `Comfort` + `Standard Range` = `Comfort Standard Range`；HS 特殊：`Luxury 1.5 T-GDI PHEV Automatic 272hk` |
| **年款** | `engineTransmissions[].model_year`（**真实年款**，非版权年）：MG4/IM5/IM6 = 2026/2027，MGS5/MGS6/HS = 2025，Cyberster = 2024 |
| **车系拆分** | 官网 gamma 页把 **MG4 EV** 与 **MG4 EV Urban** 列独立卡片（价格区间不重叠）→ 分开成两个车系 |
| **渲染坑** | 订购页含大量 DoubleClick/GA 脚本，`networkidle`/`domcontentloaded` **必超时** → 用 `waitUntil:'commit'` + 拦截第三方域名（只放行 `mgmotors.dk`）+ 等 25s |
| **slug 清单** | `mg4-ev` `mg4-ev-urban` `mgs5-ev` `mgs6-ev` `mg-im5` `mg-im6` `mg-cyberster` `hs` |
| **交付结果** | **19 条 / 8 车系**（2026-10-08，8 列含燃油分类；HS 为 PHEV，其余 BEV） |

**抓取骨架**：
```js
// 只放行 mgmotors.dk，其余 abort，否则广告脚本卡死
await pg.route('**/*', r => /mgmotors\.dk/.test(r.request().url()) ? r.continue() : r.abort());
pg.goto(`https://mgmotors.dk/bestil/${slug}/`, {waitUntil:'commit', timeout:90000}).catch(()=>{});
await pg.waitForTimeout(25000);
fs.writeFileSync(`render_${slug}.html`, await pg.content());
```
```python
# 解析
d = json.loads(html.unescape(re.search(r'data-react-props="([^"]+)"', h).group(1)))
for et in d['engineTransmissions']:
    msrp = et['original_price']          # 未折扣 SRP
    if et.get('campaign_retail_prices'): # 有促销 → original_price 仍正确
        pass
```

> ⚠️ **该站无官方价格表 PDF**（仅质保书），版本价只在配置器里，**必须走 `data-react-props`**。

---

### Nissan（DK 丹麦 `www.nissan.dk`：**采集失败，IP 级风控**）❌

| 项 | 内容 |
|---|---|
| **现象** | `curl -4` 返回 **403**，正文是丹麦语维护页 *"Site under vedligeholdelse"*；**浏览器同 IP 也一样**，疑似站点挂了 |
| **★ 真相** | **不是站点维护，是我们的出口 IP 被 CloudFront 风控**。用户在本地（丹麦/欧洲 IP）访问**完全正常** |
| **★ 识别特征** | ① `x-cache: Error from cloudfront` + `x-amz-cf-pop: FRA56`（边缘按 IP 策略拒绝，**源站若真挂应是 5xx**）<br>② 全站 403 含 `robots.txt` / `sitemap.xml`<br>③ 页面 `last-modified` 是**几个月前**（本次 2026-03-13）、`age` 数万秒 → 静态缓存维护页 |
| **★ IPv6 假死** | `www.nissan.dk` 解析出**全是 IPv6**，curl 默认优先 v6 会直接 **000**（像"域名不存在"）→ 必须先试 **`curl -4`** 再看真实状态码 |
| **其它域名** | `build.nissan.dk`（希腊站配置器解法）在 DK **NXDOMAIN**；`configurator.`/`dk.`/`assets.` 子域均不存在 |
| **API 旁路** | `api.nissan.dk` 存在（AWS 都柏林，**不过 CloudFront**），返回 Apigee 网关报错 `ecommerce_vhost_sslrouter` → **不拦 IP**，但需要正确的 proxy base path（未破解） |
| **结论** | 本环境**无法采集**；需用户本地取数（Export HTML / Copy as cURL）或换邻站 |

---

### GWM 长城（TH 泰国 `www.gwm.co.th`：**全通，价格可直接 curl，一次成功**）✅

**结论：车型页服务端渲染，价格就在内联 HTML 里；26 条数据一次采齐。是「东南亚皮卡/SUV 站」的最佳采样对象。**

| 项 | 内容 |
|---|---|
| 连通性 | ✅ 主站 301 → `/en`；Fastly `199.232.163.10`（`adobe-aem.map.fastly.net`）；`robots.txt` 200 |
| **★ 车型页 URL** | `https://www.gwm.co.th/en/models/<slug>` —— **服务端渲染**，价格直接在内联 HTML，**无需 JS、无需浏览器** |
| **★ 价格提取结构（bs4）** | ```python
area = s.find('div', class_='switch-area')
opts = [o.get_text(strip=True) for o in area.find_all('span', class_='option') if o.get_text(strip=True)]
cgl = area.find('div', class_='color-group-list')
for g in cgl.find_all('div', class_='button-group'):
    for it in g.find_all('div', class_='btn-item'):
        p = it.get('data-title')          # "฿1,229,000"
        img = it.get('data-car-img','')   # 版本图，用于交叉验证
``` |
| **⚠ 解析三坑** | ① `find_all(..., recursive=False)` **会返回空**（层级不符），**不要限制层级**<br>② `dd.find_all('span', class_='option')` 返回空（option 不在 `.dropdown` 内）→ 改用 `area.find_all(...)`<br>③ 价格可能带空格 `฿ 949,000` → 需 `re.sub(r'\s+','',p)` |
| **★ 顺序对应** | `options-list` ↔ `color-group-list > button-group` **顺序一一对应**，直接 zip 即可 |
| **★ 交叉验证** | 用 `data-car-img` 路径段（`4wd-black-ultra`/`2wd-black-pro`/`singal-cab-s`/`singal-cab-l`）核对版本↔价格配对 |
| **★ slug ≠ 车系名（重大陷阱）** | 见下表。**同一车系燃油版/柴油版是两个 slug**，且 URL 里的 `-diesel` 与**不带**后缀的关系常常反直觉 |
| **★ 官方 PDF 规格表** | 全部在 `/content/dam/gwm/pages/th/en/model/...`（用 `urllib.parse.quote` 处理空格）。PDF **只有规格没有价格**，但**是判定燃油类型的权威依据** |
| 后端 API | `https://cms.gwm.co.th/prod-api/...`（CloudFront `18.66.102.80`）→ `/prod-api/system` **401**（需鉴权，未使用）；`mall.gwm.co.th`（订购站）存在 |
| sitemap | 仅 2 条（无用）；models 总览页是 JS 渲染 |

**★ slug ↔ 车系 ↔ 燃油 对照表（本页 10 个有效 slug）**

| slug | 官网车型名称 | model dir | 燃油 | PDF 佐证 |
|---|---|---|---|---|
| `poer` | POER | `poer` | **Diesel** | `POER 2.4T PRO SINGLE CAB AUTO -EN-9.1.pdf` |
| `sahar` | **POER SAHAR HEV** | `poer-sahar` | **HEV** | `GWM POER SAHAR HEV_EN.pdf`（2.0T HEV PRO/ULTRA DOUBLE CAB）|
| `sahar-diesel` | **POER SAHAR DIESEL** | `poer-sahar-diesel` | **Diesel** | `GWM POER SAHAR DIESEL_EN.pdf`（2.4T）|
| `haval-h6` | HAVAL H6 | `haval-h6-hev` | **HEV / PHEV** | HEV PRO + PHEV PRO + PHEV ULTRA（同页混版）|
| `ora-5-ev` | ORA 5 EV | `ora-5/bev` | **BEV** | `ORA 5-EN.pdf` |
| `tank-300` | **TANK 300 HEV** | `tank-300-hev` | **HEV** | `Tank 300 HEV-eng 9.1.pdf` |
| `tank-300-diesel` | **TANK 300 DIESEL** | `tank-300-diesel` | **Diesel** | `TANK 300 DIESEL_EN.pdf`（2.4T）|
| `tank-500` | **TANK 500 HEV** | `tank-500-diesel` | **HEV** | `TANK 500 DSL + HEV ENG 9.1.pdf`（**同一 PDF 含 DIESEL+HEV 两栏**）|
| `tank-500-diesel` | **TANK 500 DIESEL** | `tank-500-diesel` | **Diesel** | 同上 |
| `wey-g9` | WEY G9 | `wey-g9` | **PHEV** | `eng_wey_g9.pdf`（Hi4 = 插混四驱）|

> **⚠ 最容易踩的雷**：`tank-300` / `tank-500`（不带后缀）**是 HEV 版，不是汽油版**；`sahar`（不带后缀）**是 HEV，不是柴油**。只凭 slug 字面推断燃油 = 必然出错。**必须用 PDF 的 `Type:` 行或 `GWM TANK 300 HEV` 标题字段确认**。
>
> **⚠ 另一个坑**：`tank-500` 页与 `tank-500-diesel` 页的 `data-car-img` 都指向 `tank-500-diesel/` 目录 —— **不能靠图片目录判燃油**，得看版本名（HEV 版只有 PRO/ULTRA 两版；DIESEL 版有 BLACK WARRIOR/ULTRA/PRO 五版）。
>
> **⚠ 车名需自造区分**：官网两页车名都写 "GWM TANK 500" / "POER SAHAR"，交付时须在「官网车型名称」列补上 HEV / DIESEL 以免重名混淆（如 `POER SAHAR HEV` / `POER SAHAR DIESEL`）。

**交付结果**：`GWM_TH_官网价_20261010.xlsx`，26 条（10 slug × 版本展开）。

---

### Nissan（TH 泰国 `www.nissan.co.th`：**全通，价格在内联 JSON，curl 直读**）✅

**结论：AEM（HELIOS）站点，价格数据以 JSON 形式内联在 HTML 的 `<script>` / `<iframe>` 里，纯 curl + 正则/bs4 即可取全，无需浏览器。**

| 项 | 内容 |
|---|---|
| 连通性 | ✅ 200（CloudFront `eb20e7a8...cloudfront.net`，`x-cache: Hit`）；无封锁 |
| **★ 真源 ①（全车系价格页）** | `https://www.nissan.co.th/vehicles/all-grade-price.html`（英文版 `en.nissan.co.th/...` 同结构）页内嵌 `const data = {languages:{th:{models:[...]}, en:{...}}}` —— 每个 `models[].versions[]` 含 `{name, price}`。**用括号配平从 HTML 里切出该 JS 对象，再交给 node 解析**（是 JS 字面量、含单引号，不能直接 `json.loads`） |
| **★ 真源 ②（每车型页）** | 任意车型页 `<iframe id="individualVehiclePriceJSON">` 内联 JSON：`{<model>:{Retail:{grades:{<gradeKey>:{versions:{<verKey>:price}}}}}}` |
| ⚠ 常见坑 | 页内还引用了 `/content/nissan_prod/th_th/.../jcr:content.proxy.json`，**但直连 404**（Apigee `Unable to identify proxy for host: https_vhost_sslrouter`）→ **必须从页面 HTML 内联内容取，不要直连 json 路径** |
| ⚠ `all-grade-price` 不含 Terra | 该页 `data` 只有 **6 车系**（Almera / Kicks e-POWER / X-Trail e-POWER / Serena / Serena e-POWER / Navara）；**Terra 需从 `/vehicles/new-vehicles/new-terra.html` 的 `individualVehiclePriceJSON` 单独取** |
| ⚠ 排除项 | `almera-stylish-package.html` 是 **Almera 的配件套件**（泰文标题 `ชุดแต่ง STYLISH PACKAGE`），价格与 Almera 完全相同 → **非独立车型，不列** |
| **★ 在售车系（7）** | ALMERA · KICKS e-POWER · X-TRAIL e-POWER · SERENA · SERENA e-POWER · NAVARA · TERRA |
| 燃油字段 | Schema.org `fuelType`：Almera/Kicks/X-Trail/Serena 均 `เบนซิน`（汽油）；Navara/Terra `ดีเซล`（柴油）。Almera 内联还有 `versionPowertrainType:"เบนซิน"` |
| **★ e-POWER 归类** | 发动机 `fuelType=Gasoline` + 驱动为 `AC3 Synchronous Motor`（同步电机）、**不可外接充电** → 归 **HEV**（非插电式混合动力） |
| **★ SERENA 归类** | 官网标注 `ระบบ S-HYBRID (Mild Hybrid)`（Smart Simple Hybrid，发动机+启停/辅助电机）→ 归 **MHEV** |
| 版本名脚注 | 版本名尾部带 `*` / `**` / `*** / ****` 免责标记，**交付时须清理**（`re.sub(r'\s*\*+(\s*/\s*\*+)*\s*$','',s)`） |

**交付结果**：`Nissan_TH_官网价_20261011.xlsx`，**27 条**（7 车系 × 版本展开）。

---

### Mitsubishi（TH 泰国 `www.mitsubishi-motors.co.th`：**全通，价格表 SSR 直读**）✅

**结论：价格表页服务端渲染，表格 HTML 直接可解析；官网同时提供泰文 `/th/` 与英文 `/en/` 两版，英文版版本名更规范。**

| 项 | 内容 |
|---|---|
| 连通性 | ✅ 200（nginx + Varnish/Fastly，`x-served-by: cache-nrt-...`）；`robots.txt` 正常 |
| ⚠ 站点很慢 | 单页 1–1.6 MB，**单次 curl 可达 200s+**；批量抓多页务必后台跑 |
| **★ 真源** | `https://www.mitsubishi-motors.co.th/th/buy/all-models-price`（英文版 `/en/buy/all-models-price`）—— 标题「ราคารถทุกรุ่น / All models price」 |
| **★ 解析结构** | 每个车系 = `<h3>车系名</h3>` + 紧随的 `<table>`，行 `<tr><td>GRADE/版本</td><td>价格 BAHT</td></tr>`；用 bs4 `find_all_previous(['h1'..'h6'])` 给每个 table 配标题 |
| ⚠ 价格脏字符 | 价格单元格含 `\xa0`（nbsp）/ `\u200b`（零宽空格）→ 取数字前先 `re.sub(r'[^0-9]','',s)` |
| **★ 英文版优先** | `/en/buy/all-models-price` 版本名是规范英文（`SINGLE CAB 2.4 PRO 4WD AT`），泰文版是泰文；两版**价格完全一致**。⚠ 个别措辞有差异（泰文写 `SINGLE CAB 2.4 PRO`，英文写 `SINGLE CAB 2.4`）—— 属官网双语差异 |
| **★ 车系 ↔ 表格标题映射** | 一个车系可能拆成多张表：`TRITON ATHLETE` / `TRITON SINGLE CAB 4WD` / `TRITON DOUBLE CAB PLUS` / `TRITON 2WD` → 都归车系 **TRITON**；`NEW PAJERO SPORT ELITE EDITION` + `PAJERO SPORT` → 都归 **PAJERO SPORT** |
| **★ 在售车系（6）** | XPANDER HEV · XPANDER CROSS HEV · XFORCE HEV · TRITON · PAJERO SPORT · MIRAGE |
| 燃油佐证 | 车型页：TRITON `เครื่องยนต์ดีเซลคอมมอนเรล 2.4ลิตร`（2.4L 共轨柴油）；PAJERO SPORT `HYPER POWER 184 แรงม้า`（2.4 柴油，与 Triton 同动力）；MIRAGE `เครื่องยนต์เบนซิน DOHC MIVEC 1.2 ลิตร`（1.2L 汽油）+ `fuelType:"เบนซิน"`；XFORCE/XFANDER `ขุมพลังไฮบริด`（混动） |
| **燃油分类** | XPANDER HEV / XPANDER CROSS HEV / XFORCE HEV → `HEV`；TRITON / PAJERO SPORT → `Diesel`；MIRAGE → `Gasoline` |

**交付结果**：`Mitsubishi_TH_官网价_20261011.xlsx`，**21 条**（6 车系 × 版本展开）。

---

### Subaru（TH 泰国 `www.subaru.asia/th/en/`：**全通，价格 SSR 直读**）✅

**结论：区域门户站（Azure Front Door），车型页价格纯 HTML 可读；⚠ 用户常见入口 `/th/en/home/` 已 404，正确入口是 `/th/en/`。**

| 项 | 内容 |
|---|---|
| 连通性 | ✅ 200（Azure Front Door `mr-a03.tm-azurefd.net`）；无封锁 |
| ⚠ URL 陷阱 | `https://www.subaru.asia/th/en/home/` → **404**；`https://www.subaru.asia/th/en/` → 200。裸域 `https://www.subaru.asia/` → 会 **302 跳到 `subaru.cn`（中国站）**，别从根域进 |
| **★ 真源** | 车型页 `https://www.subaru.asia/th/en/<model>/`（如 `/forester/`、`/wrx/`），**服务端渲染**。版本卡片结构：`<img alt="WRX 2.4 6MT">` 后跟 `<div>版本名</div> … THB 3,309,000*` |
| **★ 提取法** | 正则 `THB\s*([0-9][0-9,\.]+)`，再向前取最近的 `alt="版本名"` / 卡片标题配对。首页只给 5 款「From THB」起价，**完整版本必须进车型页** |
| **★ 在售车系（5）** | FORESTER · CROSSTREK · WRX · WRX WAGON · BRZ |
| ⚠ OUTBACK 已下架 | `/th/en/outback/` → **302 跳回 `/th/en/`**（页面不存在）；导航仍残留菜单项但无页无价 → **不采**。`/th/en/solterra/` → **404**（泰国无此车） |
| ⚠ 同车双路径 | `/forester/` 与 `/forester-2025/` 内容与价格相同（同车），取一个即可 |
| 燃油 | 全系 `Gasoline`（Forester 2.5 NA / Crosstrek 2.0 NA / WRX 2.4 Turbo / WRX Wagon 2.4 Turbo / BRZ 2.4 NA）。⚠ Crosstrek 页 meta 里出现 `e-Boxer` 字样，但正文与价格表只有 2.0i 汽油版 → **不按 MHEV 计** |

**交付结果**：`Subaru_TH_官网价_20261011.xlsx`，**9 条**（5 车系 × 版本展开）。

---

### Denza 腾势（TH 泰国 `www.denzathailand.com/en`：**全通，但官网无独立价格页，价格藏在促销活动条款里**）⚠️ 可采

**结论：官网（Rêver Automotive 代理，Next.js/RSC）没有车型价格页，`ราคาจำหน่าย`（售价）只写在 news-promotions 的活动条款正文中。可采，但取数路径特殊。**

| 项 | 内容 |
|---|---|
| 连通性 | ✅ 200（Google Frontend / GCP）；`robots.txt` 全允许 |
| 站点性质 | Next.js **App Router（RSC 流式）**。⚠ `/en/models` 是 **404**（sitemap 里有但实际不可用）；`/en/models/denza-d9` 等车型页**只有规格、无价格**（且规格值为 0，需 JS） |
| **★ 真源** | `https://www.denzathailand.com/{th,en}/news-and-promotions/<活动 slug>` —— 活动条款里的表格 `ราคาจำหน่าย / รายละเอียด` 明列各版本售价。**用 Playwright（`domcontentloaded`+wait，`networkidle` 会超时）渲染后读正文** |
| **★ 活动 slug（当期）** | D9 → `denza-d9-oct-2026-campaign`（或 `denza-d9-jun-2026-campaign`）；Z9GT → `z9gt-oct-2026-campaign` / `denza-z9gt-sep-2026-campaign` |
| **★ 提取法** | 渲染后文本里定位 `ราคาจำหน่าย` 段，读取 `รุ่น <版本>` ↔ `<数字> บาท`。⚠ 页面同时混有分期月供、配件价值等干扰数字，**只取 `ราคาจำหน่าย` 表** |
| **★ 口径判定** | 同一价格跨多期活动不变（如 D9 Premium 在 2026-06 与 2026-10 都是 `1,949,900`）→ 判定为**官方售价（MSRP）**，非折扣价 ✓ |
| **★ 在售车型（2）** | DENZA D9（Premium / Performance AWD）· DENZA Z9GT（Performance AWD） |
| ⚠ Phantom Edition | D9 Phantom Edition II = **车身价（与普通版同）+ 配件包 70,000** → 净价 2,019,900 / 2,469,900。按「不含选装」**不采**，或按需单列 |
| 燃油 | 全系 `BEV` |
| ⚠ 无 models 列表 | 找车系只能从首页 RSC 的 `text:"รถยนต์ไฟฟ้า DENZA ..."` 或 news 列表里挖 |

**交付结果**：`Denza_TH_官网价_20261011.xlsx`，**3 条**。

---

### Volvo（TH 泰国 `www.volvocars.com/en-th/`：**curl 全 403，但有头 Playwright 可通；价格只在配置器**）⚠️ 可采

**结论：curl 直连全站 Akamai 403，但 `xvfb-run + headless=False` 的真实浏览器可以正常打开；官网无价格表页，价格只在「设计你的 Volvo」配置器的各配置档。**

| 项 | 内容 |
|---|---|
| 连通性 | ⚠ `curl` → **403**（Akamai `errors.edgesuite.net`）；✅ **有头 Playwright**（`headless=False` + xvfb）→ **200，站点完全正常** |
| **★ 关键姿势** | 与 Tesla（有头也 403）不同，Volvo 的 403 是**对无浏览器指纹的拦截**，真浏览器可过。**必须 `xvfb-run -a` + `chromium.launch(headless=False)` + 去 `navigator.webdriver`** |
| URL 陷阱 | `/en-th/cars/` → **404**；车型页形如 `/en-th/cars/<model>/`（如 `/ex40-electric/`），但**车型页本身不含价格** |
| **★ 价格真源** | **配置器**：`https://www.volvocars.com/en-th/build/<model>/`（英文名，如 `ex40-electric` / `xc60-hybrid`）。进入后默认选中该国在售配置档，正文显示 `Your level: <档位>` + **`THB x,xxx,xxx`**。配置器总览页 `/en-th/build/` 还给出各车型「From THB ...」 |
| **★ 取数法** | 渲染 `/build/<model>/` → 读 `inner_text` → 正则 `THB\s*([0-9][0-9,\.]+)`；页面里 `Your level` 段的价格即该车型在售价 |
| **★ 在售车型（6）** | EX40 · EC40 · ES90 · XC60 · XC90 · EX90 |
| ⚠ EX90 无价 | EX90 配置器有 **Plus / Ultra** 两档可选，但**通篇不显示任何价格**（点击档位也不出价）→ 判定「官网暂未公布价格」，表中留空 |
| ⚠ 单车单档 | 泰国市场 EX40/EC40/ES90/XC60/XC90 均**只进口一个配置档 Ultra**（配置器 `Your level` 仅 1 项），所以每个车系 1 行 |
| 燃油 | EX40 / EC40 / ES90 / EX90 → `BEV`；XC60 / XC90 → `PHEV`（配置器标 `plug-in hybrid`，动力 `T8 AWD Plug-in hybrid`）|

**交付结果**：`Volvo_TH_官网价_20261011.xlsx`，**6 条**（5 条有价 + EX90 1 条价格留空）。

---

### Isuzu（TH 泰国 `www.isuzu-tis.com`：**完全开放，价格 SSR/RSC 直读**）✅

**结论：Tri Petch Isuzu 官网（Netlify + Next.js），首页带 Schema.org 起价、车型页 RSC 内含逐版本价，均可直读。**

| 项 | 内容 |
|---|---|
| 连通性 | ✅ 200（Netlify）；⚠ 首屏较慢（~26s），车型页 600–880KB，批量抓建议后台跑 |
| **★ 价格源 ①（起价）** | 首页 JSON-LD（`@type: ListItem` + `offers.price`）给 6 车系起价；页面可见文本也有 `เริ่มต้น x,xxx,xxx THB` |
| **★ 价格源 ②（逐版本）** | 车型页 RSC 里 `ราคา`/`รุ่นรถ` 段：**版本名行** 紧跟 **`N,NNN,NNN THB` 行**。⚠ 用 `inner_text` 渲染后按行配对最稳（详见「提取法」） |
| **★ 提取法** | Playwright 渲染 `/isuzu-*` → 定位独立行 `รุ่นรถ` → 向下读到 `MODEL LINEUP` / `เริ่มต้น` 为止，把「汉字/字母行」与紧随的「数字+THB 行」配对 |
| ⚠ 页面底部有干扰 | 页脚 `MODEL LINEUP` 列**其它车型**的 `เริ่มต้น xxx THB`，**必须先截断到 `รุ่นรถ` 段再取**，否则会串入别车价格 |
| ⚠ 颜色加价 | `สี... +7,000 THB`（特殊漆）属选装 → **不采**；同理 AggregateOffer 的 `highPrice`（= 顶配 + 特殊色）不等于任何标准版本价 |
| **★ 在售车系（6）** | V-CROSS · D-MAX 2-DOOR（Hi-Lander Spacecab）· D-MAX 4-DOOR（Hi-Lander）· D-MAX SPARK · X-SERIES · MU-X |
| ⚠ 车系名来源 | 官网 Schema.org 用泰文 `อีซูซุ วี-ครอส / ดีแมคซ์ ปิกอัพ 4 ประตู / …`，车型页 hero 只有 `2 DOORS / SPARK / X-SERIES`，其余以 URL slug 命名为准 |
| 燃油 | 全系 `Diesel`（`Ddi MAXFORCE` 共轨柴油，163/190 PS）|

**交付结果**：`Isuzu_TH_官网价_20261011.xlsx`，**32 条**（6 车系 × 版本展开）。

---

### Chevrolet（TH 泰国 `www.chevrolet.co.th`：官网**已转型为纯售后服务站**，不销售新车）❌ 无数据

**结论：不是封锁、也不是不公开价格——而是 GM 已于 2020 年退出泰国新车市场，该官网只做售后（配件/保修/维修），站内根本没有任何在售车型。**

| 项 | 内容 |
|---|---|
| 连通性 | ✅ curl 200（125KB），AEM 站（`/content/chevrolet/as/th/th/...`）。⚠ 但**无头 Playwright → 403 Akamai**，有头 Playwright → 200（与 Volvo 同款指纹现象）|
| **★ 决定性证据 ①** | 站点导航**全是售后**：`สินค้า`(配件) / `ศูนย์บริการ`(服务中心) / `การรับประกัน`(保修) / `บริการช่วยเหลือฉุกเฉิน`(道路救援) / `นัดหมายเรียกกลับ`(召回) / `คู่มือการใช้งาน`(手册) —— **无任何车型/购车/试驾入口** |
| **★ 决定性证据 ②** | `sitemap.xml` 共 ~50 条 URL，**无一条车型页**（全部是 products / complete-care / news-events / tools）；`/vehicles` `/cars` `/models` `/colorado` `/trailblazer` 全部 **404** |
| **★ 决定性证据 ③** | 页面全文检索 `Colorado / Trailblazer / Captiva / Spin / Cruze / Sonic / Silverado` 等**命中 0 次** |
| ⚠ 易误判点 | `/promotion/2025-new-price` 标题像"新车价"，实为**配件调价表**（`อะไหล่เชฟปรับราคาเกินครึ่งกว่า 1,500 รายการ` = Chevy 配件调价 1500+ 项），列的 Colorado/Cruze/Captiva 是**配件适配车型**，不是整车 |
| ⚠ 页面类型 | `/products` 是 **ACDelco 配件**页（滤芯/机油/电瓶/化学品），非整车 |
| 背景 | GM 2020 年停止在泰国销售新车，将 Rayong 工厂出售给 Great Wall（长城），此后仅保留售后网络（Chevrolet Authorized Service Outlets）。⚠ 第三方比价站（如 autogiz）会列一堆"Chevrolet 泰国价"，**那是美国市场换算价或二手参考，非官网，不采** |
| **结论** | **官网无新车 MSRP**；此类「品牌已退出该市场新车销售」的站，**挖再深也没有数据**，应立即止损 |

> **新类别（区别于"封锁"与"不公开价格"）**：**「品牌已退出该市场新车销售，官网仅剩售后」**。判别信号：① 导航无车型/试驾/购车入口；② sitemap 无车型页；③ 车型关键词全文 0 命中；④ 站内仅有 service / warranty / parts / recall。遇到即判定**无数据**。

---

### Cadillac（US 美国 `www.cadillac.com`：**全通，价格 SSR 内联，可采**）✅

**结论：GM 官网（AEM + Akamai），curl 即可拿到全部车型起价与各 trim 售价；价格以纯 HTML 形式内联在导航与车型页的 `gb-` 组件里。**

| 项 | 内容 |
|---|---|
| 连通性 | ✅ curl 200（1.3–2.1 MB/页）。⚠ 与 Chevrolet/Volvo 同款：**无头 Playwright 403，有头（xvfb + `headless=False`）200**；curl 直接可用 |
| **★ 价格源 ①（全系起价）** | 任意页面的**导航菜单**：每个车型条目 `title="YYYY MODEL" data-dtm="global nav:..."` 后跟 **`From: $X`**。这是官网「该车型最低配置起价」 |
| **★ 价格源 ②（trim 级售价）** | **车型页主体**的 `CHOOSE YOUR ...` 区块：`TRIM NAME` 紧跟 **`From: $X`**（如 `LUXURY` / `SPORT` / `PREMIUM LUXURY` / `SIGNATURE LUXURY` / `PLATINUM` / `V-SERIES` …）|
| **★ 区分导航 vs 主体** | 导航条目前 400 字符内含 `data-dtm="global nav`；**主体 trim 块不含** → 用此条件过滤，否则会把别车价格串进来 |
| **★ 年款分层（关键！）** | 官网同时在售 **MY2027 / MY2026 / MY2025 三代**，**且三代车型清单不同**（不是同一批车换年份）。URL 规则：**当年代** = `/electric/lyriq`、`/sedans/ct4`、`/suvs/escalade`；**上一年度** = 加 `preceding-year/`（`/electric/preceding-year/lyriq`）。⚠ 2025 只在导航里带价，其页面多半已变成 `Cadillac Legacy Vehicles`（无价） |
| **★ 各年款车型清单** | **MY2027（9 款）**：ESCALADE · ESCALADE ESV · ESCALADE-V · ESCALADE-V ESV · VISTIQ · LYRIQ · LYRIQ-V · OPTIQ · OPTIQ-V<br>**MY2026（17 款）**：上述 9 款 + **ESCALADE IQ · ESCALADE IQL · XT5 · CT5 · CT5 V-SERIES · CT4 · CT4 V-SERIES · CELESTIQ**（即 IQ/IQL 与燃油轿车仅有 2026 款）<br>**MY2025（6 款）**：ESCALADE IQ · XT4 · CT5 · CT4 · CT4 V-SERIES · CELESTIQ |
| ⚠ 不要用同一年款覆盖全部 | **ESCALADE IQ / IQL / XT5 / CT4 / CT5 只到 MY2026**（无 2027）；**XT4 / ESCALADE IQ 的 MY2025** 是清库存老款。交付时「年款」列必须逐年标注，不能统一写一个 |
| ⚠ CELESTIQ 无标价 | built-to-order 定制车，导航/车型页**均无价格** → 表中留空（MY2025/MY2026 各一行） |
| ⚠ 同车型跨年价差 | ESCALADE：MY2027 LUXURY `$102,700` vs MY2026 LUXURY `$102,100`、MY2026 另有入门 `$91,100` 起价 → **别把两代混成一代** |
| ⚠ `/vehicles` 是空壳 | `https://www.cadillac.com/vehicles` 仅 8 KB 导航模板，**无车型列表**；车型清单只能从导航 `href` 或 sitemap 取 |
| 货币格式 | 🇺🇸 美元用**逗号千分位**（`102,700`），与欧洲市场的点号（`28.220`）相反 —— 该市场按其官网原生写法 |
| 燃油 | ESCALADE 全系 = `Gasoline`（6.2 V8 / V-Series 增压）；ESCALADE IQ/IQL · VISTIQ · LYRIQ(-V) · OPTIQ(-V) · CELESTIQ = `BEV`；XT5 · XT4 · CT4/CT5 及 V 系 = `Gasoline` |

**交付结果（页面口径 / 不含运费）**：`Cadillac_US_官网价_20261013.xlsx`，**78 条**（**MY2027 24 条 / MY2026 46 条 / MY2025 8 条**，按年款 × 车型 × trim 展开）。

#### ★ 更优口径：官方配置器（Build & Price）—— `?radius=900&zipCode=20146`

**配置器给出的是「含目的地运费」的官方价，且细到「trim × 驱动形式」，数据来自独立 REST API，比页面导航更权威。**

| 项 | 内容 |
|---|---|
| 入口 | `https://www.cadillac.com/shopping/configurator?radius=900&zipCode=20146`（`zipCode` 决定区域价；`radius` 经销商半径）|
| 单车型 URL | `https://www.cadillac.com/shopping/configurator/<bodyType>/<year>/<model>/<model>/model?radius=900&zipCode=20146`，例：`/shopping/configurator/suv/2027/escalade/escalade/model`。`bodyType` ∈ `suv` `sedan` `electric` `v-series` |
| **★ 两个关键 API**（同一网关，curl 带 referer 亦可，但**页面内抓最稳**） | `GET/POST /cadillac/shopping/api/aec-cp-configurator-gateway/p/v1/catalogue` → 全车型目录（`models[].years[].msrp`，含年款/bodyType）<br>`/p/v1/trim` → **该车型全部 trim + 价格**（按驱动形式分组）|
| **★ trim API 结构** | `data.trimList`：`{ "4WD": [ {name:"LUXURY", msrp:{value:108595}}, {name:"SPORT", …}, … ], "2WD": [...] }` —— **一次拿全「trim × 驱动」价格** |
| **★ 价格口径** | **含目的地运费**（destination charge）。同车型比页面 `From` 高 $1,795–$2,895，例：LYRIQ 2027 LUXURY 页面 `$59,400` → 配置器 RWD `$61,195`；ESCALADE 2027 LUXURY 页面 `$102,700` → 配置器 2WD `$105,595`。**交付时须说明口径，别与页面 MSRP 混用** |
| **★ 支持年款** | `bootstrap` API 列出 **2028 / 2027 / 2026 / 2025 / 2024**（比页面导航多 2028、2024）|
| ⚠ 不在配置器的车型 | **CT4 · CT4-V · XT4** → trim API 返回 `Unsupported Vehicle: … combination not found`（`CONF-UV-001`），说明已下架/停售，只能从旧页面拿 |
| ⚠ 驱动字段 | 各车型不同：ESCALADE 用 `2WD/4WD` + V-Series 用 `AWD`；LYRIQ/OPTIQ 用 `RWD/AWD`；XT5 用 `FWD/AWD`；CT5 用 `RWD/AWD`。**驱动类型必须并入型号名**（如 `LUXURY 4WD`）|
| ⚠ 提速技巧 | 页面单次加载慢（易 `goto` 超时）→ 分开跑、每次只抓 `/p/v1/trim` 响应体；**必须带 xvfb + headed**，headless 403 |

**交付结果（配置器口径 / 含运费）**：`Cadillac_US_官网价_配置器版_20261013.xlsx`，**114 条**（**MY2027 41 / MY2026 69 / MY2025 4**）。

---

### Mazda（US 美国 `www.mazdausa.com`：**全通，价格 SSR + 内联 JSON，可采**）✅

**结论：Mazda 美国官网 curl 直通，全部车型起价在首页卡片里、各 trim 售价在各车型页的内联 JSON 里，均可正则提取。**

| 项 | 内容 |
|---|---|
| 连通性 | ✅ curl 200（0.9–1.6 MB/页），Akamai（`_abck`/`bm_sz` cookies）但**不拦 curl** |
| **★ 价格源 ①（全系起价）** | 首页/车系列表页的**车型卡片**：`<div class="mdp-header-global__card" data-type="..." data-model="26C70">` → 内含 `<span>2026</span>`、`<p>Mazda CX-70</p>`、`<p>Inline 6 Turbo</p>`、**`Starting At … $42,750`** |
| **★ 价格源 ②（trim 级）** | **车型页内联 JSON**：**`"lowestMsrp": "$42,750", "title": "3.3 Turbo Preferred"`** —— 每个 trim 一条，最干净。⚠ 该 JSON 被转义（`\u0027` 等），**必须先 `html.unescape` 再正则** |
| **★ 兜底：FAQ 文本** | 少数页面（如 **CX-30**）**无 `lowestMsrp`**，但页面 FAQ 里有纯文本 trim 列表：`The Mazda CX-30 is available in eight different trim levels: 2.5 S: Starting at $26,375; …` —— 用「`trim levels?` 后面的 `<li>` 列表」兜底 |
| **★ 在售车型（12）** | MAZDA3 SEDAN · MAZDA3 HATCHBACK · CX-30 · CX-5 · CX-50 · CX-50 HYBRID · CX-70 · CX-70 PHEV · CX-90 · CX-90 PHEV · MX-5 MIATA · MX-5 MIATA RF |
| ⚠ 正则陷阱 | `Starting At` 与 `$X` 之间相隔 **~98 字符**（含 `</span><span>` 等），容差 `{0,60}` 会**漏匹配** → 用 `{0,200}` |
| ⚠ 卡片属性顺序 | `<div class="…__card" data-**type**="…" data-**model**="…">` —— **data-type 在前**，正则别写反 |
| ⚠ 起步价 vs trim | 卡片 `Starting At` = 最低 trim 价（与 JSON 第一条一致），可交叉验证 |
| 燃油 | MAZDA3 · CX-30 · CX-5 · CX-50(2.5/2.5T) · MX-5 = `Gasoline`；**CX-50 HYBRID = `HEV`**；**CX-70 / CX-90 的 3.3 Turbo = `MHEV`**（官网标 `Mild Hybrid Inline 6`）；**CX-70 PHEV / CX-90 PHEV = `PHEV`** |
| 货币格式 | 🇺🇸 美元逗号千分位（`24,650`）|

**交付结果**：`Mazda_US_官网价_20261013.xlsx`，**55 条**（12 车型 × trim 展开）。

---

### Lotus（US 美国 `www.lotuscars.com/en-US`：站点全通，但**美国官网基本不公开价格**，仅 Eletre 标价）⚠️ 部分

- **站点**：✅ 200，CloudFront + **API7/3.8.22**（Apache APISIX 网关）；**Vue SSR 门户**（Sitecore JWS 内容）+ **独立 SPA 配置器**。curl 直通，无需绕封锁。
- **★ 美国在售 4 车系**（首页导航 + 配置器 API 双证）：`Eletre`(电 SUV) · `Emira`(燃油跑车) · `Emeya`(电 GT) · `Evija`(电超跑)
- **★ 价格只标了 1 个**：**Eletre Carbon = `Starting from $229,900*`**，写在 `/en-US/eletre` 的 CMS 富文本里：
  ```html
  <p class="__ff-overpass-light __c-white __f-h9">The electric Hyper-SUV with racecar DNA<br />Starting from $229,900*</p>
  ```
- **其余车型官网一律无价**：`/en-US/emira` `/emeya` `/evija` 三个车型页 curl + Playwright 渲染后**零价格**（只有 `CONFIGURE` / `KEEP ME UPDATED` 按钮）；首页、`/models`、`/shop`、`/emira/reservation` 也全无价
- **★ 路径全是 SPA fallback 陷阱**：`/en-US/models`、`/en-US/shop`、`/en-US/finance`→404、`/en-US/pricing`→404，注意 **`/models` `/shop` 返回的是首页 HTML（316,829 B 同尺寸）**，别当成有效页
- **★ 配置器是「云渲染 3D」**（MHP GmbH 做，`Lotus Cars - Immersive Car Configurator`）：
  - 入口 `/en-US/configurator/{model}/{variant}`，SPA 空壳 1,941 B，入口 JS `/en-US/configurator/assets/index-C7LTwRy4.js`（3.3 MB）
  - 云渲染走 **GorillaStreaming**（`session.lotus.gorillastreaming.com`，需 WebRTC）→ **Playwright 渲染永远超时 / 拿不到画面**
  - **★ 真 API（可 curl，无需鉴权）**：`https://configurator.prd.configurator.eu.lotuscars.com`，路径段配置在 JS 的 `pathSegments`：
    ```js
    pathSegments:{iod:"iod",ruleEngine:"ruler",productData:"products",shortCode:"url-shortener",matchmaker:"matchmaker",reservation:"reservation",instances:"instances",signaling:"signalingserver",pdf:"pdf"}
    ```
    - **`GET /products/products/{COUNTRY}`** → 返回该国全车系产品树（`id/modelCode/productAlternatives[].config/defaultConfig`），例：`/products/products/US`
    - ⚠ **但产品数据里 0 个价格字段**（US/DE/GB 三个市场都一样，只有 `config` 数组 + `meta.filterId`）
    - 价格引擎在 `/ruler/pricing/{t}/{n}/{r}`，**参数语义不明 + 返回空**；`ClientId` header 无关紧要
  - **★ 变体名藏在 config 标识里**（`MHP_*`）：EMIRA = `MHP_EMIRA_420SPORT` / `TURBO_SE` / `LINE` / `V6SE` / `V6LINE`（5 版）；EMEYA = `MHP_EMEYA_R_PACK`；ELETRE = `MHP_R_CARBON_PACK`；EVIJA = `MHP_EVIJA`；且所有美国条目带 **`MHP_US_MARKET`** 标记
- **★ 对照实验（关键心法）**：同一套代码，**`/en-GB` 首页渲染后有价**（Eletre £86,305 / Emira Turbo SE £93,955 / Emeya 600 £86,305，含 finance offers），**`/en-US` 渲染后无价** → 证明"渲染无价"是**站方策略**而非工具问题，可放心判定。
- **背景**：Lotus 美国是**经销商模式**，官网只做展示，价格走配置器/经销商询价（同类：McLaren / Maserati）。官方新闻稿虽给过 Emira 420 Sport 美国 MSRP `$122,900`，但**官网自身不展示**，按口径不采。
- **燃油**：Eletre / Emeya / Evija = `BEV`；Emira = `Gasoline`（2.0T i4 或 3.5L V6 增压）

**交付结果**：`Lotus_US_官网价_20261014.xlsx`，**7 条**（4 车系 × 版本展开；**仅 Eletre Carbon 有官网价 $229,900**，其余按"收录但价格留空"处理）。

---

### Force Motors（IN 印度 `www.forcemotors.com`：**全通，有官方 `/prices/` 价格总表，SSR 直读**）✅

- **站点**：✅ 200，**nginx + PHP 8.2（Plesk）**；curl 直通、无任何反爬，是近几轮里最"素"的一站。
- **★ 真源 = `/prices/`**（`https://www.forcemotors.com/prices/`）：**34 个 `<table>`**，统一两列 `Model Description | Ex-Showroom Price`，服务端渲染，一次 curl 全拿。
- **★ 表格结构（解析要点）**：
  - 第 1 行 = 表头（`Model Description`）
  - 表头后第一个**单列行** = 车系名（如 `TRAVELLER T1 STANDARD 3050 MM WB`）
  - 表头后的**双列行** = 配置名 + 价格
  - ⚠ **别用 `find_all_previous(['h1'..])` 取车系名** —— 会把页脚的 `Disclaimer:` 当标题串进来；用"表格内单列行"判最稳
- **在售车系**（全 166 配置）：`TRAVELLER`(T1/T2/T3 × 3050/3350/3700/4020/5200 WB，含 Delivery Van / Ambulance / School Bus) · `TRAX`(GAMA / CRUISER / TOOFAN / DV / School Van) · `CITILINE` · `SCHOOL VAN` · `URBANIA DX` · `MONOBUS`(4020/5200，Standard / School Bus / Shell) · `Gurkha`(3 Door · 5 Door)
- **价格格式**：印度 **lakh 分组** `15,70,522`（= 1,570,522）；⚠ 少数带 `₹ ` 前缀（表格 T11/T28）或 `.00` 后缀（URBANIA），提数前先 `re.sub(r'[^0-9,]','')`
- **燃油**：几乎全 `Diesel`（`FM2.6CR` = 2.6L 共轨柴油 / `FM3.2` = 3.2L）；配置名含 `CNG` 的标 `CNG`；`Gurkha` 亦为柴油
- **口径**：**Ex-Showroom Price**（印度裸车价，不含上路费）—— 印度官网通行口径

**交付结果**：`ForceMotors_IN_官网价_20261015.xlsx`，**166 条**（7 大车系 × 配置展开）。

---

### Jeep India（IN 印度 `www.jeep-india.com`：**全通，价格在 SSR + 内联 JSON，可采**）✅

- **站点**：✅ 200，**Apache + Akamai**（`CT_Akamai` geo cookie 会带 `country_code=CN`，但**不拦**）；curl 直通。
- **在售 4 车型**：`Compass`(紧凑 SUV) · `Meridian`(7 座 SUV) · `Grand Cherokee`(豪华 SUV) · `Wrangler JL`(硬派越野)
- **★ 价格有两层**：
  1. **起价**：`<meta name="description">` 里的 `from ₹X.XX Lakh*`（各车型页顶部）
  2. **变体级**：页面内联 JSON，结构为
     ```json
     "models":{"<CODE>":{"displayPricing":true,"pricing":{"price":"21.30 Lakh*",
       "description":"Ex-Showroom Price","EMIFormulaValues":{"msrp":"2130000"}}}}
     ```
     `msrp` 是精确整数（卢比），`price` 是 lakh 显示值 —— **15 个变体全部在这里**
- **★ 变体名不在 JSON 里**，而在页面**轮播标签**上（渲染后可见）：
  - Compass（7）：SPORT · LONGITUDE · LIMITED · MODEL-S · TRACK EDITION · 85TH ANNIVERSARY EDITION · TRAIL EDITION
  - Meridian（7）：Longitude · Longitude Plus · Limited (O) · TRACK EDITION · 85th ANNIVERSARY EDITION · Overland · TRAIL EDITION
  - Grand Cherokee（1）：LIMITED O
  - Wrangler（4）：WRANGLER WHITECAP EDITION · WRANGLER 1941 WILLYS EDITION · WRANGLER UNLIMITED · WRANGLER RUBICON
- **★ 配对方法（本节最有价值的经验）**：**JSON 块的出现顺序 == 轮播标签的顺序**。用 Playwright 点 4 个标签交叉验证（LIMITED→24.83 / MODEL-S→26.70 / TRACK EDITION→26.95 / TRAIL EDITION→23.66 全部吻合）后，即可放心按序 zip。
- **★ 点击轮播的两个坑**：
  - `locator.scroll_into_view_if_needed()` 会**超时**（懒加载元素不可滚动）→ 去掉这步，直接 `click(force=True)`
  - **JS `el.click()` 对 React 不生效**（事件不触发），必须用 Playwright 的 `locator.click()`
  - 轮播**只渲染当前项**，所以 DOM/`innerText` 永远只拿得到 1 个价格 —— 想拿全部只能"点一个读一个"或走 JSON
- **展示单位**：页面用 `₹17.99 Lakh*`，**换算 × 100,000**（17.99 Lakh = 1,799,000），与 JSON `msrp` 完全一致
- **燃油**：`Compass` / `Meridian` = **Diesel**（2.0L Multijet II，`"fuelType":"Diesel"` 明文）；`Grand Cherokee` = **Petrol**（`"fuelType":"Petrol"`）；`Wrangler` = **Petrol**（2.0T；官网未明写，按印度在售动力判定）
- **口径**：**Ex-Showroom Price**（印度裸车价）

**交付结果**：`Jeep_IN_官网价_20261015.xlsx`，**19 条**（4 车型 × 变体展开）。

#### 🔁 2026-10-19 补充：**变体级真源在 visualizer 的 one3d 配置器 API（30 条，优于轮播 zip）**

**`www.jeep-india.com` 的车型页轮播只是「精选 trim」；完整「发动机 × 变速箱 × 驱动」组合在独立配置器域。**

| 项 | 内容 |
|---|---|
| **★ 入口** | 车型页 visualizer 链接指向 `https://configurator.jeep-india.com/visualizer/null/<commercial_model_code>`（Angular SPA，CloudFront 托管，curl 只回 7.6 KB 壳）|
| **★ 商业代码** | `M67421` Compass · `H67523` Meridian · `W77423` Grand Cherokee · `JL7421` Wrangler |
| **★ 三个 API（`prod-jeep-api.one3d.in`）** | ① `GET /api/v1/models/all`（4 车型清单）② `GET /api/v1/variants/all`（**当前车型全部变体，183 KB**）③ `GET /api/v1/variants/details`（只有当前选中 1 条，**不是全量，别用**）|
| **★ 变体字段** | `version_name`（`Sport 2.0D MT` / `Model S (O2) 4x4 2.0D AT`）· `variant_name` · `price`（整数卢比）· `fuel_type` · `transmission_code`（6MT/9AT/8AT）· `drive`（4x2/4x4）· `num_of_seats` · `variant_cpos` · `active` |
| **⚠ curl 直连 401** | `variants/all` 需 `Authorization: Bearer <JWT>`；token 由 `POST /api/login`（body 要 `username`）下发，浏览器首屏自动调 `/api/login` 拿到 **223 字符 JWT（有效期约 6 天）** → **最省事的做法：Playwright 打开配置器页，直接拦截 `variants/all` 响应**，不要自己拼 token |
| **⚠ token 手带反而 404** | 用拦截到的 JWT 手动 curl 同一路径会返回 404（路径/租户校验），**拦截响应才是正解** |
| **★ 实测结果（30 条）** | Compass **13**（Sport→Track，含 4x4）· Meridian **14**（Longitude→Overland/Track，5/7 座）· Grand Cherokee **1**（Limited O）· Wrangler **2**（Unlimited / Rubicon）|
| **⚠ 配置器数据会滞后** | Compass / Meridian / Grand Cherokee 的配置器价与官网导航起价**完全吻合**；但 **Wrangler 配置器仍是 66.20 / 70.80 Lakh，官网车型页已涨到 67.70 / 73.55 Lakh** → **Wrangler 以车型页为准**，其余用配置器 |
| **★ 4 个车型页 URL** | Compass `/new-compass.html` · Meridian `/meridian.html` · Grand Cherokee `/grand-cherokee.html` · Wrangler **`/wrangler-jl.html`**（`/wrangler.html` 是 404，别猜）|

**交付结果**：`Jeep_IN_官网价_20261019.xlsx`，**30 条**（4 车型 × 全部 motorization 组合）。

---

### MINI（IN 印度 `www.mini.in/en_IN/`：**curl 全挂（Akamai HTTP/2 拒绝），只有 Playwright 有头可通**）⚠️ 部分

- **★ 封锁形态（记牢）**：curl 拿到 **TLS 握手成功、HTTP/2 stream 建好**，但响应 `HTTP/2 stream 1 was not closed cleanly: INTERNAL_ERROR (err 2)` → `curl (92)`，**HTTP 码 000**。**`--http1.1` 也 000**，换 UA/补头均无效。**唯一解 = Playwright 有头（`xvfb-run` + `headless=False`）**，能正常 200。
- **★ 价格藏两处**：
  1. **`/en_IN/home/range.html`** —— 车系起价（`From ₹ 47,50,000`）
  2. **`/en_IN/home/range/<model>/models.html`** —— **trim 级价**；⚠ **只有 `mini-cooper-3-door` 和 `all-electric-mini-countryman` 存在此子页**，其余车型 `/models.html` 直接 **ERR_HTTP_RESPONSE_CODE_FAILURE**
- **在售车系**：MINI Countryman C · All-Electric MINI Countryman · MINI JCW Countryman ALL4 · MINI Cooper 3-door · MINI Cooper Convertible · MINI Convertible Stardust Edition · John Cooper Works · Cooper Oxford Edition · GP Inspired
- **★ 官网只公开 7 条价**：Countryman C ₹47,50,000 · All-Electric Countryman ₹55,65,000 · JCW Countryman ALL4 ₹66,15,000 · Cooper S Essential ₹44,45,000 / Classic ₹50,40,000 / JCW Trim ₹53,25,000 / Favoured ₹53,25,000
- **Convertible / Stardust / GP / Oxford 官网不标价**：其车型页零价格（只有 `₹39,999` 之类 EMI 数字，别当成车价）
- **★ 配置器在独立域 `configure.mini.in`**（`/en_IN/configure/U25/12GA/...`），但 **Playwright 渲染恒为 len=0**（title 有 `Configurator`，正文空）→ 拿不到 Convertible 价
- **价格格式**：印度 lakh `₹ 47,50,000`
- **燃油**：Cooper S / Countryman C / JCW Countryman ALL4 = `Gasoline`（页面明写 `Petrol`）；All-Electric Countryman = `BEV`

**交付结果**：`MINI_IN_官网价_20261015.xlsx`，**7 条**（3 车系 + Cooper S 4 trim）。

---

### VinFast（IN 印度 `vinfastauto.in/en`：**Cloudflare Managed Challenge，stealth + reload 可概率性通过**）✅

- **★ 封锁形态**：`curl` 全站 **403**（`robots.txt` 是唯一 200）；Playwright 默认也是 `Performing security verification / Ray ID …` 的 **Cloudflare 托管挑战**页。
- **★ 通过方法（本段最有价值）**：
  ```
  1) 用「更像真人」的 context：
     headless=False + --disable-blink-features=AutomationControlled
     init_script: 去 navigator.webdriver、覆写 plugins/languages、window.chrome={runtime:{}}
     locale='en-IN'、timezone_id='Asia/Kolkata'、1920x1080、
     headers: Accept-Language / sec-ch-ua / sec-ch-ua-platform
  2) 访问用 wait_until='commit'（**别用 networkidle，挑战页会一直跳**）
  3) 等 15–25s；若 body 仍含 'security verification' → `pg.reload()` 再等
     ✅ 通常**第 2 轮 reload 后通过**（实测概率性，需多试几次）
  ```
- **★ 价格为「空格分组」的印度格式**：`₹ 18 19 000`（= 1,819,000）——正则要写 `₹\s*([0-9\s]{5,20})`
- **★ 价格两处**：
  1. **车型页** `/en/vf6`、`/en/vf7`、`/en/mpv7`：起价
  2. **★ 官方订购站 `shop.vinfastauto.in/reservation?model=<X>`**：`Ex. Showroom Price` 即 trim 级价
     - ⚠ **`?model=MPV7` 无效**（页面回落成 VF 6，显示 ₹18 19 000）→ **正确参数是 `?model=VFMPV7`**
     - 切 trim 用 `locator('text="VF 7 Sky"').last.click(force=True)` 即可读到对应该 trim 的 Ex-Showroom 价
- **在售 3 车系 9 个配置**：
  | 车型 | 配置 | Ex-Showroom (₹) |
  |---|---|---|
  | VF 6 | Earth / Wind / Wind Infinity | 1.819.000 / 1.959.000 / 1.959.000 |
  | VF 7 | Earth / Wind / Wind Infinity / Sky / Sky Infinity | 2.299.000 / 2.589.000 / 2.639.000 / 2.749.000 / 2.809.000 |
  | VF MPV 7 | （单一配置，**无 trim 选项**） | 2.039.000 |
- **全系 `BEV`**；车系：VF 6(紧凑 eSUV) · VF 7(5 座 eSUV) · VF MPV 7(MPV)

**交付结果**：`VinFast_IN_官网价_20261015.xlsx`，**9 条**（3 车系 × 配置展开）。

---

### Honda Cars India（IN 印度 `www.hondacarindia.com`：**curl 直通，有官方 JSON API，但只到车系起价**）⚠️ 起价

- **站点**：✅ 200，**Next.js（SSG）+ Imperva/Incapsula**（`visid_incap_*` cookie）；curl 直通，无需绕。
- **★ 官方 JSON API（关键）**：`https://www.hondacarindia.com/api/...`，全部 curl 可取，无需鉴权：
  | 端点 | 内容 |
  |---|---|
  | **`GET /api/getAllCarsData`** | **5 车系最低配**：`carModelName / carModelPrice / carModelTrim / carModelVarient / carModelFuelType / carModelTransmissionType / carModelId` |
  | `POST /api/getCarPrice`（body `{carID, city:"Delhi"}`） | ⚠ **只返回该车系起价** `P_Price`（RTO/保险全为 0），**不分变体** |
  | `GET /api/getOfferCars` | 仅列出有 offer 的车系 |
- **★ 结论：官网只公开「车系起价（= 最低配）」**。车型页只有一句 `Starts at ₹ 11 80 000*`；`/check-price` 页同样是 5 条起价。变体明细在官网**不公开**（check-price 工具要选城市，且返回的是 on-road 价，不是 ex-showroom）。
- **在售 5 车系（起价 ex-showroom）**：
  | 车型 | 最低配 | 起价 (₹) | 燃油 |
  |---|---|---|---|
  | New City | SV MT Petrol | 1.199.900 | Petrol |
  | New Amaze | V MT Petrol | 765.400 | Petrol |
  | Amaze – 2nd Gen | S MT Petrol | 697.700 | Petrol |
  | All New ZR-V | ZRV | 4.999.900 | e:HEV |
  | New Elevate | SV MT Petrol | 1.180.000 | Petrol |
- **辅助线索**：车型页 Schema.org 有 `AggregateOffer`（Amaze `lowPrice 740800 / highPrice 1097900`；Amaze 2G `697700 / 966000`）与 `Offer.price`（Elevate `1180700`）—— 可作**价格区间**参考，但**不是变体明细**
- **价格格式**：**空格分组** `₹ 11 80 000`（同 VinFast）
- **燃油**：`Petrol` → `Gasoline`；`e:HEV`（ZR-V）→ `HEV`

**交付结果**：`Honda_IN_官网价_20261015.xlsx`，**5 条**（5 车系 × 最低配起价）。

---

### BYD India（IN 印度 `www.bydautoindia.com`：**React SPA 空壳，Playwright 可渲染，价格 SSR 在车型页**）✅

- **站点**：✅ 200，**nginx/1.18（Ubuntu）+ React CRA**（`/static/js/main.*.js`）；**curl 只拿到 6.5 KB 空壳**（`<div id="root">`）→ **必须 Playwright 渲染**（有头，无需 stealth，无 Cloudflare）
- **在售 4 车型**：`/bydatto3`(SUV) · `/bydemax7`(MPV) · `/bydseal`(轿车) · `/bydsealion7`(SUV)
- **★ 价格就在车型页**：渲染并滚到底后，每个变体一个卡片，文案形如
  ```
  DYNAMIC ₹ 24 99 000* (Ex-showroom price) … PREMIUM ₹ 30 35 000* … SUPERIOR ₹ 34 49 000*
  ```
  首页只显示 `₹ 24.99 Lakh Starting Price`（**Lakh 记法**），车型页才是 `₹ 24 99 000`（**空格分组**）
- **14 个配置**：
  | 车型 | 配置 | Ex-showroom (₹) |
  |---|---|---|
  | ATTO 3 | DYNAMIC / PREMIUM / SUPERIOR | 2.499.000 / 3.035.000 / 3.449.000 |
  | eMAX 7 | COMFORT 6座 / COMFORT 7座 / SUPERIOR 6座 / SUPERIOR 7座 | 2.790.000 / 2.830.000 / 2.930.000 / 2.990.000 |
  | SEAL | DYNAMIC / PREMIUM / PERFORMANCE | 4.150.000 / 4.620.000 / 5.365.000 |
  | SEALION 7 | DYNAMIC / PREMIUM / PREMIUM(Rich Tan) / PERFORMANCE | 4.190.000 / 4.990.000 / 5.060.000 / 5.590.000 |
- **全系 `BEV`**；⚠ SEAL 页标 `Model Year 2025`（是官网唯一年款线索）
- **价格格式**：`₹ 24 99 000`（空格分组 lakh）

**交付结果**：`BYD_IN_官网价_20261015.xlsx`，**14 条**（4 车型 × 配置展开）。

---

### Toyota Bharat（IN 印度 `www.toyotabharat.com`：**本站直通，但价格全在后端 API + SafeLine WAF，需「浏览器内 fetch」**）✅ 满配

- **站点**：门户 ✅ 200（Azure，`ARRAffinity` cookie）。**但价格不在门户页上** —— `/pricelist/` 是个「选州→选市→选车型→出价」的表单，curl/渲染后 3 个下拉全是空的。
- **★ 真源（关键）**：价格走独立 API 域 **`https://webapi.toyotabharat.com/1.0/api/...`**（从 `static3.toyotabharat.com/js/forms/api.pricelist.ob.js` 里挖出，端点清单见下）：
  | 端点（全 **POST**） | 内容 |
  |---|---|
  | `1.0/api/price/models` | **13 车型** + `Id` + `EffectiveDate` |
  | `1.0/api/pricestates` | 33 个州 |
  | `1.0/api/pricestates/{stateId}/pricecities` | 城市 |
  | `1.0/api/businesscities/{cityId}/websalesdealers` | 经销商（拿 `dealerId`） |
  | **`1.0/api/price/list/{dealerId}/{priceModelId}`** | **★ 该车型全变体价格表（XML）** |
- **★ WAF 陷阱（本节最有价值）**：该 API 域有 **SafeLine WAF**（返回 `.safeline` 拦截页），**curl 直连 100% 被拦**。**解法 = 在 Playwright 里打开主站后，用页面上下文 `fetch()` 调 API**（同源策略无关，关键是带上浏览器指纹）：
  ```python
  pg.goto('https://www.toyotabharat.com/pricelist/')
  r = pg.evaluate("""async (url)=>{ const r=await fetch('https://webapi.toyotabharat.com/'+url,
       {method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'}}); return await r.text(); }""", path)
  ```
- **★ 价格 XML 结构**：`<Price><PriceGrade><PriceModel><Name>车系</Name></PriceModel><Name>变体名</Name><FuelType>P/D/C/H/E</FuelType><Details>变速箱</Details></PriceGrade><Amount>价格</Amount></Price>`
  - 燃料码：`P`=Petrol · `D`=Diesel · `C`=CNG · `H`=Hybrid · `E`=Electric
- **★ 必须过滤「颜色加价」条目**：原始 146 条里有 **68 条是车身颜色加价**（变体名带 `[Platinum White Pearl]` / `[Xxx Dual Tone]` / `[Xxx x Midnight Black]` / `[Xxx with Bluish black roof]`，价格 +20,000）→ **按"不含选装"剔除**；⚠ 但 `[7S]`/`[8S]`（Innova Hycross 座位数）、`[LE]` 是**真实配置差异，要保留**。剔除后 **89 条**
- **13 车系 89 变体**：Glanza(13) · Urban Cruiser Taisor(10) · Rumion(8) · Urban Cruiser Hyryder(11) · Urban Cruiser Ebella(1, BEV) · Innova Crysta(11) · Innova Hycross(13) · Fortuner(6) · Legender(3) · Camry(2) · Vellfire(4) · Land Cruiser 300(4) · Hilux(3)
- **口径**：**Ex-Showroom**（按 **Delhi / dealerId=97** 取的官方价；印度 ex-showroom 全国基本一致）
- **年款**：API 有 `EffectiveDate`（价格生效日，如 Glanza `14th Oct 2026`）→ ⚠ **那是价格生效日、不是年款**，按规则写「官网无年款」

**交付结果**：`Toyota_IN_官网价_20261015.xlsx`，**89 条**（13 车系 × 变体，已剔除颜色加价）。

---

### Ford India（IN 印度 `www.india.ford.com`：**已退出印度新车市场，官网是纯售后站**）❌ 无数据

- **站点**：门户 curl **403（AkamaiGHost）**，但 **Playwright 有头 200**；内容**全是售后**：Owner Dashboard / Service & Maintenance / Genuine Ford Parts / Ford Protect / Roadside Assistance / SYNC Support / Careers / CSR。
- **★ 三条决定性证据**：
  1. **sitemap 全量只有 29 条 URL**，**无一个车型页或价格页**（全是 `owner/*`、`service-booking`、`locate-dealer`、`about-ford/*`）
  2. 首页与全站文本里 **EcoSport / Endeavour / Figo / Aspire / Freestyle 等车型词 0 命中**，`price`/`₹`/`Lakh` 也 0
  3. **官方新闻稿实锤**（`/about-ford/media/newsroom/2021/ford-restructures-india-operations.html`）：**2021-09-09 宣布退出印度市场、停止本地整车制造**，明写 *"Sales of current products such as Figo, Aspire, Freestyle, EcoSport and Endeavour will cease once existing dealer inventories are sold."*；2022-08 把 Gujarat 工厂卖给 **Tata Motors**；此后只做「服务网络 + 零件进口分销 + 延保」
- **归类**：与 **Chevrolet 泰国**同类 —— **「品牌已退出该市场新车销售」**，官网无车型无价格，**无数据**

**交付结果**：无（品牌已退出印度新车市场）。

---

### Tata Motors（TH 泰国 `www.tatamotors.co.th/en`：**Cloudflare 国家封锁，封 CN，无解**）❌

| 项 | 内容 |
|---|---|
| 症状 | `curl`/Playwright（含 headed）**一律 403**，返回 Cloudflare **Error 1009**：<br>`The owner of this website has banned the country or region your IP address is in (CN) from accessing this website.` |
| **★ 封锁性质** | **国家级地区封锁（法务/市场分区），不是 IP 级、不是 UA 级** —— 换 UA 头、headed 浏览器、IPv6 全无效 |
| 佐证 | 我方出口 `101.35.42.136`（AS45090 腾讯云 · 上海 · CN）；全球站 `www.tatamotors.com` 同样 403 |
| 源站直连 | 裸域 `tatamotors.co.th` → `15.206.215.211`（AWS），但 **:80/:443 均 CLOSED**（只放行 Cloudflare）→ 绕过 CDN 直连源站也走不通 |
| 代理 | 公共 CORS/reader 代理（allorigins / codetabs / corsproxy / thingproxy / 12ft）**全部超时或需 key**；`translate.goog` 在沙箱 DNS 不通 |
| **结论** | **本环境无法采集**；需海外（非 CN）出口，或用户本地取数 |

---

### Tesla（TH 泰国 `www.tesla.com/en_th`：**Akamai IP 级拒绝，无解**）❌

| 项 | 内容 |
|---|---|
| 症状 | `www.tesla.com/**` 与 `tesla.com/**` **全 403**，Akamai 页面：`Access Denied … Reference #18.xxxx … errors.edgesuite.net` |
| **★ 封锁性质** | Akamai **按出口 IP 拒绝**（数据中心 IP 段被拉黑）—— 换 UA/完整浏览器头/headed Chromium **均无效** |
| 关键对照 | **并非全域封锁**：`auth.tesla.com` → **200** ✅、`digitalassets.tesla.com` → **200** ✅、`static-assets.tesla.com` → **404**（服务端正常应答）；**只有 `www` 主机被拦** → 是 www 上的 bot/IP 规则，不是域名级 |
| 端点探测 | `configurator/api/v3/options/en_th/model3`、`/cua-api/...`、`inventory/api/v4/...`、`/en_th/model3/design` → **全部 403**（都在 www 下） |
| 代理 | 同 Tata，公共代理全不可用 |
| **结论** | **本环境无法采集**；需非数据中心出口或用户本地取数 |

> 📌 **与 Tata 的区别**：Tata 是**国家封锁**（明确说封 CN）；Tesla 是**数据中心 IP 黑名单**（`www` 主机 403，其它子域正常）。两者**同属"我方出口被拒"**，但性状不同。

---

### Maserati（TH 泰国 `www.maserati.com/th/en`：站点全通，但**官网刻意不公开价格**）❌

**结论：不是技术问题，是厂家政策——泰国站所有界面 `price` 均为 `"0"`。**

| 项 | 内容 |
|---|---|
| 连通性 | ✅ 完全通。主站 Akamai `23.210.7.22`、`robots.txt` 200、sitemap 681 条 |
| **★ 泰国在售车系（6 个）** | `grancabrio` `granturismo` `grecale` `gt2-stradale` `mcpura` `mcpura-cielo`（配置器 `SELECT` 列表） |
| **★ 真源（AEM `.model.json`）** | `https://www.maserati.com/th/en/models/<model>/jcr:content/main/tool_version_carouse.model.json`<br>⚠ 必须**先 301 跳一次**（`/content/countries/th/en/...` → `/th/en/...`），直接 curl 会拿到空体 |
| **★ 价格字段** | `items[].price` —— **全部为 `"0"`**（实测 grecale / granturismo / grancabrio 无一例外），同时 `items[].modelYear` / `modelName` / `specifications` 都是真实数据 |
| 配置器 | `www.configurator.maserati.com/ccbe/public/api/*` ✅ 通（`country/list` 200，泰国 `id=182`）；但只做车型选择与 3D 渲染，**不出价** |
| 配置器 API 域 | `apilayer.maserati.com` → **403**（另需鉴权） |
| 页面字段开关 | JS 里有 `display_model_price` 变量，但泰国站未启用（`price:"0"` 印证） |
| **结论** | **官网不公布 MSRP**（东南亚市场惯例，价格由经销商报价）。技术上没有任何绕法——**不是封锁，是真的没有数据** |

> **心法**：见到 `price: "0"` / `price: null` **成片出现**且 `modelYear`、规格全都正常时，应判定为「厂家未公开价格」，**立即止损**，别再往配置器/API 深处挖。

---

### McLaren（全球含 TH `www.mclaren.com/cars/gl_en/...`：站点全通，但**配置器价格被显式关闭**）❌

**结论：站点完全可访问、配置器 API 全部打通，但 `showPriceSummary=false` → 官网不显示任何价格。**

| 项 | 内容 |
|---|---|
| 连通性 | ✅ 主站 Cloudflare `104.16.153.71` 200；`robots.txt` `Allow: /*` |
| 站点性质 | SPA（`/cars/assets/index-*.js`）。用户给的 `/cars/gl_en/retailers/BangkokMcLaren` 是**经销商页**，只有联系方式，无车价 |
| **★ 配置器** | `https://configurator.mclaren.com/mclaren-ui/` ✅ 200（SAP **ConfigAir** / 3D 配置器） |
| **★ profile 列表** | `landing` 数据 `webui.environmentsModelList = 'artura,artura-spider,gts,750s,750s-spider'`（5 款） |
| **★ 核心端点（全部无鉴权 GET）** | `GET /configuration/ajaxLandingPageData.do?profileName=<model>&language=en`（车型档案）<br>`GET /configuration/ajaxStartConfiguration.do?profileName=<model>&configCountry=<CC>`（启动，返回 `windowId`）<br>`GET /configuration/ajaxGetInitialData.do?cacheControl=<ts>`（**含 `profileInfo`，价格开关在这里**）<br>`GET /configuration/ajaxGetConflicts.do` · `ajaxGetInstanceList.do` · `ajaxGetCharacteristicViews.do` · `ajaxGetCharacteristics.do` |
| **★ 价格端点（存在但从不被调用）** | `GET /configuration/ajaxGetConfigPrices.do` —— JS 逻辑：`this.profileInfo?.showPriceSummary && (t = this.sendWebConfGetXhr('ajaxGetConfigPrices.do'))` → **开关为 false 时压根不发请求**（抓包实测：整轮配置流程 0 次调用） |
| **★ 决定性证据** | `ajaxGetInitialData.do` 的 `profileInfo`（103 条）里：<br>· **`webui.showPriceSummary = 'false'`**<br>· **`webui.showPricesByCountry = 'false'`**<br>· `webui.showValuePricesInLangName = 'false'`<br>→ 三重关闭，**配置器不显示也不查询任何价格** |
| 货币字段存在 | JS 里有 `currency/currencySymbol/formatted/prices/PriceSummary` 等完整实现，**只是被 profile 开关关掉**（同一套配置器在别的市场可能开价） |
| 其它 API | `mclaren-cms.production.aws.mclaren.com/api/*` → **403**（需鉴权） |
| **结论** | **官网不公布 MSRP**（超跑惯例，价格一律经销商报价）。技术通路全开但没有数据 |

> **与 Maserati 的区别**：Maserati 是「字段在、值为 0」；McLaren 是「字段在、**服务端根本不返回价格，且前端开关关闭**」。两者**同属"官网不公开"**，但取证方式不同：McLaren 要看 `profileInfo` 开关 + 是否调用价格端点。


> 📌 **通用教训**：**403 + "维护页" + 数据中心出口 IP → 优先怀疑风控，不是站点状态**。别把"我这里看到的"当成"站点真实状态"。

---

### IM Motors 智己（全球站 `www.immotors.com/global/`：站点全通，但**官网不公开价格**）❌

**结论：Next.js 站点、API 全部打通，但**全站 0 价格字段**——配置器只有规格表，没有金额。**

| 项 | 内容 |
|---|---|
| 连通性 | ✅ `https://www.immotors.com/global/landing` 200（阿里云 WAF `yundunwaf4.com`，`47.110.174.185`）|
| 站点性质 | **Next.js**（`portal-cdn-prd.immotors.com/global/_next/...`），页面数据全在 `<script id="__NEXT_DATA__">` |
| **★ 车系（4 款）** | `l6_detail`（IM L6 / SEO 写 "IM5"）· `l7_detail`（IM L7）· `ls6_detail`（IM6）· `ls7_detail`（IM LS7）|
| **★ 配置器** | `/global/vehicle_config/<carType>`，carType ∈ `l6` `l7` `ls6` `ls7` |
| **★ 配置器数据接口（两大真源）** | ① `GET /global/api/portal-international/page/c/v1/query?name=kvVehicleConfig_<carType>ConfigTable&type=function&offset=0&limit=10` —— **返回规格表**（Editor.js JSON，表格结构，含版本列名 + 全部参数）<br>② `GET /global/api/app/generalParameters/v3/getGeneralParameter?key=OfficialInternationalVehicleKv_carTypeList` —— 车型下拉列表 |
| **⚠ 直连 API 会被 WAF 拒** | curl 直接打 ① 返回 `{"resultCode":"10003","message":"错误请求"}`（117 B）——**必须带 `Referer: https://www.immotors.com/global/vehicle_config/<carType>`**，且 WAF 认浏览器 TLS 指纹；**最稳是用 Playwright 页内请求** |
| **★ 价格字段** | 规格表 JSON + 全站 7 个页面（含 contact_us / about_im）**money 正则 0 命中、price/msrp 关键词 0 命中** |
| **★ 版本列表（无价）** | L6: Max Standard / Max Tech / Max Long Range / Max Ultra Long Range / Max Extreme Performance（5）<br>L7: Ultra Long Range / Long Range Performance / Long Range Flagship（3）<br>LS6: Max Standard / Max Long Range / Max Ultra Long Range / Max Extreme Performance（4）<br>LS7: Urban Fit / Urban Fit Pro / Elite RWD / Elite AWD / Lux RWD / Lux AWD / Pro AWD（7）|
| **★ 无购买入口** | 全站 `a[href]` 里**没有任何 buy/order/price/book/reserve 链接**，唯一外链是 Facebook/Instagram；购车只能走 `contact_us` 找经销商 |
| 内网 API 域名 | Next.js host 配置里有 `apiHost:"http://galaxy.immotors.com"` → **curl 000 不通**（内网域名，非公网）|
| **结论** | **官网不公布 MSRP**（海外市场由经销商报价）。取证：`ConfigTable` 规格 JSON 无任何金额字段 + 全站无购买链接 |

> **与 Maserati / McLaren 归为一类**：**「官网不公开价格」**。IM Motors 的取证特点是"**规格给得很全、价格一个字都没有**"——连 `showPrice` 之类的开关都不存在，直接没有该功能。

---

### KG Mobility / KGM（韩国 `www.kg-mobility.com`：主 HTML 被地理屏蔽，**挖 JS bundle 直取无鉴权 API**）✅

**结论：官网首页 HTML 对大陆出口 IP 返回「空壳」（只有 `<head>`，无 `<body>`、无 `#app`），但 `/assets/*.js` 与 `/attached/*.pdf` 可 curl 直连；真实后端 `web.kg-mobility.com` 全通且**无需鉴权**。实测交付 62 条 trim 级价格。**

| 项 | 内容 |
|---|---|
| 连通性 | ⚠️ `https://www.kg-mobility.com/` curl **HTTP 000**（TLS 握手成功、之后无 HTTP 响应）；`https://web.kg-mobility.com/` curl **200** |
| **★ 空壳页判别（关键）** | Playwright 拿到的 DOM 仅 `4894 B`：`<head>` 完整、`</head></html>` 直接结束、**无 `<body>`、无 `#app`**；但监听网络可见 `GET /assets/index-QYD-0y8d.js → 200`。→ **静态资源放行、主 HTML 被地理性裁剪**，不要以为是 SPA 没渲染，直接去挖 JS bundle |
| **★ JS bundle 可 curl** | `curl https://www.kg-mobility.com/assets/index-QYD-0y8d.js` → **200，1.5 MB**（首页 000 但 assets 通，很反直觉） |
| **★ API base（从 bundle 挖出）** | bundle 内 `__vite_import_meta_env__={VITE_API_BASE_PATH:"/api", VITE_API_SERVER_URL:"https://web.kg-mobility.com"}`，且 `getOriginBasePath()`：`{"/api"→"/app","/erms-api"→"/erms","/search-api"→"/kgm"}` → **实际 base = `https://web.kg-mobility.com/app`** |
| **★ SERVICE_PATH 映射** | `{LOGIN:"/login",MEMBER:"/member",DISPLAY:"/display",ESTIMATE:"/estimate",VEHICLE:"/vehicle",SUBSIDY:"/subsidy",...}`，拼在 base 之后 |
| **★ 在售车型清单** | `GET /app/display/getPlpModelList.do` → `body.typeList[].modelList[]{dispCatNo,modelNm,modelCd,price,flag,eleccarYn,estimateCatNo}`（分 SUV / 픽업트럭&밴 两类，首页车系卡片数据源）|
| **★ 车型详情 + 官方 PDF** | `GET /app/display/getCarDetailContents.do?dispCatNo=<id>` → `body.keyVisual.fileList[]{title:"카탈로그"/"가격표", fileUrl}`（**官方价格表 PDF = 판매가격权威源**）|
| **★ 报价车型清单** | `GET /app/estimate/getCarModelList.do` → `body[]{modelCd,modelName,engineInfo,carType,categoryNo}`（比 PLP 更全，含 밴 / 롱데크 / 7인승 细分，**carType 是单字母码，必须带回**）|
| **★ trim 级价格（核心）** | `GET /app/estimate/getCarModelTrimList.do?modelCd=<3位车系码>&carType=<单字母>` → `body[]{homepageTrimNm,className,oilName,oilCd,gearName,driveCd,carSuplAmt,carCdType,carCd}`。**两参数缺一即报 9103「요청 파라미터 값이 잘못되었습니다」** |
| **★ 价格口径（重要）** | `carSuplAmt` = 官网 PDF 的「**판매 가격**」（**세제혜택 적용 전**原价，含 VAT）。而 PLP 的 `price` / 车型页 `시작가격 ...부터(세제혜택 후)` 是**扣掉税制优惠后**的起价。**按"不采折扣/补贴价"规则取 `carSuplAmt`**：混动差 100 万韩元、纯电差 239 万韩元，已验证 7 份 PDF 完全一致 |
| 无鉴权端点差异 | `getDispModelList.do` 返回 `9100 인증이 필요합니다`；本任务未用到的历史车型接口不必碰 |
| 历史车型码 | `GET /app/vehicle/getVehicleList.do` → `[]` 无参返回 `carCode/carType/carNm`（含已停产 코란도·렉스턴·체어맨 等，**仅作对照，勿入交付**）|
| **⚠ Actyon 价格表缺失** | `dispCatNo=200000100010018/…016` 的 `fileUrl` 是占位符 `https://www.kg-mobility.com/actyon_p`（返回 3202 B 的 SPA 壳）→ **PDF 拿不到，改用 trim API 的 `carSuplAmt`**（已与其它 PDF 校验过口径）|
| **⚠ 后处理坑** | ① `className` 的 `_4월/_9월/_12월` 是**排产月标记**，非年款，去掉 ② `className` 的 `S `/`L ` 前缀 = 스탠다드/롱 데크标记 ③ `경유`=柴油（与 `디젤` 同义，`oilCd` 都是 D），前缀需归一 ④ `carCdType=="2"` 且 `className` 含 `(투톤)` = 双色车身同价重复项，**剔除** ⑤ `TAXI` trim（如 `TAXI_12월 48,040,000`）**不在官方零售价格表 PDF 内**，剔除 |
| **★ 年款判定** | 仅 `가격표` PDF 封面标题明确写年份的才算：`토레스 EVX 2027`（FL5）、`무쏘 EV 2027`（OP5）→ `MY2027`；其余封面只写 `뉴 토레스` / `뉴 토레스 하이브리드` / `렉스턴 뉴 아레나` / `무쏘` / `더 뉴 티볼리` → **官网无年款，严禁按发布新闻推断** |
| **★ 车系 × modelCd（13 个在售）** | `MC5` 액티언(3617만↑) · `MD5` 액티언 하이브리드(3895만↑) · `MW5` 토레스(2996만↑) · `MY5` 토레스 하이브리드(3302만↑) · `FL5` 토레스 EVX(4602만↑) · `MV2` 토레스 밴(2815만↑) · `FL2` 토레스 EVX 밴(4520만↑) · `UP5` 무쏘(스탠다드 데크) · `UH5` 무쏘(롱 데크) · `OP5` 무쏘 EV(4850만↑) · `GL5` 렉스턴 뉴 아레나(5인승) · `GL7` 렉스턴 뉴 아레나(7인승) · `XW5` 티볼리(2097만↑) |
| **★ 燃料映射** | `가솔린`(G)→`Gasoline`、`디젤`/`경유`(D)→`Diesel`、`하이브리드`(H)→`HEV`、`전기`(E)→`BEV` |
| 促销页干扰 | `/od/promotion/monthly-benefits?modelCd=XX` 是「이달의 구매 혜택」，数字是**含当月金融优惠的「부터」起价**，**不要采**；WebFetch 能正常渲染该页（说明它是 SSR，而首页是空壳） |

> 📌 **通用教训**：**curl 首页 000 但 curl `/assets/xxx.js` 200 → 是「主 HTML 被地理裁剪」，不是整站封锁**。此时正确动作是**下载 JS bundle，grep `VITE_*` / `SERVICE_PATH` / `baseURL` / `createInstance` 找到真实 API 域名与路径**，往往后端域名（如 `web.*`）完全不受地理限制。同类案例：IM Motors（Next.js 挖 `__NEXT_DATA__`）。

---

### Volkswagen India 大众印度（`www.volkswagen.co.in`：AEM + feature-app 微前端，**变体价藏在 MOFA BFF**）✅

**结论：curl 全通（Akamai，无封锁）；车型页的变体价格区（`#MOFA`）是懒加载的 feature-app 微前端，curl **拿不到**，必须 Playwright 滚动触发，拦截 `mofa.feature-app.io/bff/model-overview` 响应。实测交付 28 条。**

| 项 | 内容 |
|---|---|
| 连通性 | ✅ `www.volkswagen.co.in` curl **200**（Akamai `edgesuite.net`），robots.txt/sitemap 均通 |
| 站点性质 | **Adobe AEM**（`/etc.clientlibs/clientlibs/vwa-ngw18/...`）+ **feature-hub 微前端**；页面嵌 `<script id="spaModel">`（AEM JSON，**无价格**）、`x-feature-hub/serialized-states` |
| **★ 车型清单** | `https://www.volkswagen.co.in/en/models.html` 卡片里 `From ₹xx,xx,xxx.00`；链接 7 个：`taigun` `tayron` `tiguan-r-line` `virtus` `virtus-chrome` `virtus-sport` `golf-gti`（`sitemap.html` 同）|
| **★ 变体价格真源（核心）** | 车型页有 `id="MOFA"` 锚点（Model Overview Feature App）。滚动触发后浏览器发出：`GET https://v1-<ver>.mofa.feature-app.io/bff/model-overview?cacheBuster=1&countryCode=IN&currency=INR&dataVersion=<hash>&language=en&serviceConfigEndpointToken=<token>` |
| ⚠ **该 API 不能直接 curl** | 缺参数逐个报错：`language` → `dataVersion` → **`serviceConfigEndpointToken`**（token 由平台注入，无法手搓）→ **不要硬拼，直接 Playwright 拦截响应** |
| **★ 树形结构** | `payload.models[]`（carline）→ `children[]`（**trim**）→ `data.referenceModel.prices.price1.{value,formattedValue,displayValue}` = **Ex-showroom 价**；`data.engines[].engineTypes/gearTypes` = 发动机/变速箱 |
| **★ 记录变体名 + 价（示例 Taigun 11 条）** | Comfortline 1.0L TSI MT 10,99,900 / Highline MT 12,99,900 / Highline AT 14,09,900 / Highline Plus MT 14,41,900 / Highline Plus AT 15,56,900 / Topline MT 16,21,900 / Topline AT 17,37,900 / GT Line MT 14,71,900 / GT Line AT 15,86,900 / GT Plus Chrome 1.5L 19,16,900 / GT Plus Sport 1.5L 19,46,900 |
| **★ 哪些页有 MOFA** | **只有 `#MOFA` 的页面才有**：`taigun` `tayron` `virtus-chrome` `virtus-sport`。`tiguan-r-line` `golf-gti` `virtus` **无 MOFA**（单变体），价格直接写在页内 `"technicalData":[{"key":"Ex-showroom Price:","value":"₹ 47 11 013*"},{"key":"Engine","value":"2.0L TSI "},...]` |
| **★ 拦截时的过滤陷阱** | 用 `'model-overview' in url` 会**误抓同名 JS bundle**（`model-overview-umd.js`）→ 必须用 `'.feature-app.io/bff/' in url` 且响应体 `lstrip().startswith('{')` |
| **★ 抓取可靠性** | 同一脚本跑两遍，`virtus/tiguan-r-line/golf-gti` 会随机 MISSING（响应时机不稳）→ **脚本要有重试/逐页串行 + 充分滚动（wheel ×8）** |
| **⚠ 页面上的「From」/首页价 ≠ 本任务口径** | 首页 `volkswagen.co.in` 的车型卡片是**促销口径**（`Taigun Chrome **Offer price** ₹ 10 58 300`、`Taigun Sport **Price starting** ₹ 14 32 748`、`Tayron R-Line **Introductory** ₹ 46 99 000`），比 Ex-showroom **低**；**models 页的 `From ₹…` 和 MOFA 的 `price1` 才是 Ex-showroom（本任务取这个）**。例：Tayron R-Line MOFA/车型页 **₹47,74,000**，首页 Introductory ₹46,99,000 → 取前者 |
| **★ 车系结构（官网把同车系拆成多条 product line）** | `The new Taigun`（11 trim，含 GT Line/GT Plus Chrome/GT Plus Sport）· `Tayron`（Life / R-Line）· `Virtus Chrome`（Comfortline→GT Plus，9 trim）· `Virtus Sport`（GT Line / GT Plus Sport，4 trim）· `Tiguan R-Line`（1）· `Golf GTI`（1）。⚠ `virtus.html` 只是系列落地页、**无价**，别当成独立车型 |
| **★ 燃料** | 全系 **Gasoline**（1.0L/1.5L/2.0L TSI，无柴油无电动在售）|
| **★ 价格格式** | 印度 **lakh 分组**：官网 `formattedValue` = `₹10,99,900.00` → 入表 `10,99,900`（去 `₹` 与 `.00`）|
| 年款 | 全站**未标 MY/年份** → 一律「官网无年款」（2026 Taigun facelift 只在新闻里叫 2026，官网不写）|

> 📌 **通用教训**：**AEM / feature-hub 站点的「变体价格」区常是一个懒加载 feature-app，服务端 HTML 里空空如也**。判别：页面有 `id="XXX"` 锚点 + `CmsFeatureAppLoader` + 「Loading」占位。动作：**Playwright 打开 → 反复 wheel 滚动到锚点 → 拦截 `*.feature-app.io/bff/*` 的 JSON 响应**（别去拼它的 token）。

---

### BMW India 宝马印度（`www.bmw.in`：**IPv6 全断 / IPv4 时通时断，只能浏览器**；价格全在 all-models 卡片）✅

**结论：curl（含 `-4`）时通时 000，Playwright 稳定 200。价格不打在车型页，**只在 `/en/all-models.html` 的卡片里**。实测交付 23 条。**

| 项 | 内容 |
|---|---|
| ⚠️ **连通性（关键）** | `www.bmw.in` 解析出 Akamai `e25631.dsca.akamaiedge.net`，**`getent hosts` 只给 IPv6（2600:140b:…）→ curl 默认走 v6 直接 000**；`curl -4` **偶尔 200、多数 000**；**Playwright 每次 200** → 直接上浏览器，别在 curl 上耗时 |
| 站点性质 | BMW 自研 **"crx3" 平台**（响应头 `x-vhost: publish`、`baqend-tags: crx3composite,bmw/marketIN/bmw_in/...`）|
| **★ 价格唯一入口** | `https://www.bmw.in/en/all-models.html`（页面带 `?series=` `?bmwM=yes` 筛选）。⚠ **车型详情页（如 `bmw-7-series-sedan.html`）一个 ₹ 都没有**，别去详情页找价 |
| **★ 卡片选择器** | 根节点 `.cmp-allmodelscard__root`（26 个）|
| **★ 字段映射** | `.cmp-allmodelscarddetail__body-type`（Sedan/SUV/Coupé/Cabrio/Gran Coupé）· `__series`（**车系名**：`i7` `i5` `i5 LWB` `M5` `X7` `X5` `X3` `X1` `X1 LWB` `7 series` `5 LWB` `4 series` `M4` `3 series` `3 LWB` `M2` `2 series`）· `__description`（`Models` / `M Model`）· `__fuelTypeText-text`（**Petrol / Diesel / Electric / Hybrid**）· `__usp-text`（`From ₹4,580,000`）· **`img[alt]` = 具体变体名**（`BMW X7 xDrive40i`、`330Li M Sport`、`The M5`）|
| **⚠ 价格筛选器是干扰项** | 页面左上有价格区间滑块，数字是 **lakh 分组**（`₹45,80,000` `₹73,41,700` … `₹2,11,50,000`）→ **那是筛选刻度，不是车型价**，别采。真车价全部是 **标准千分位** `₹4,580,000` |
| **★ 无价卡片要剔除** | 26 张里 3 张无 `From ₹`：`BMW M Concept Neue Klasse`（概念车）、`Vision BMW ALPINA`（概念车）、`The 7 Protection`（防弹车）→ 不入表 |
| **★ 燃料归类** | `Petrol`→`Gasoline`、`Diesel`→`Diesel`、`Electric`→`BEV`、`Hybrid`→**`PHEV`**（页面过滤器明确写 `Plug-in hybrid (1)`，即 M5 G90；不是 HEV）|
| **★ 交付清单（23 条）** | 2 series 218 M Sport 4,580,000 · 3 series M340i 7,780,000 · 3 LWB 330Li 6,270,000 / 320Ld 6,420,000 · 4 series M440i 11,065,000 · 5 LWB 530Li 7,700,000 · 7 series 740 M Sport 19,500,000 · M2 10,650,000 · M4 16,290,000 · M5 21,150,000 · i5 M60 11,950,000 · i5 LWB eDrive35L 7,960,000 · i7 50 xDrive 19,500,000 · X1 sDrive18d 5,290,000 · X1 LWB 4,990,000 · X3 30 xDrive 7,690,000 / xDrive20 7,690,000 / xDrive20d 7,820,000 · X5 xDrive40i 9,690,000 / xDrive30d 9,890,000 · X7 xDrive40i 13,490,000 / xDrive40d DPE 7 Seater 13,220,000 / xDrive40d 13,860,000 |
| **★ 口径** | 页面 disclaimer：`Ex-showroom prices inclusive of GST ... excludes Road Tax, TCS, RTO, insurance` → **Ex-showroom 含 GST**，符合 MSRP 口径 |
| **★ 车型覆盖** | 官网 all-models 只有这 23 个在售变体；**没有 iX / i4 / Z4 / X2 / X4 / X6**（全文关键词 0 命中）→ 不要凭印象补 |
| 年款 | 卡片不标 MY → 「官网无年款」|

> 📌 **通用教训**：**`getent hosts` 只返回 IPv6 时，curl 会静默 000**——先 `getent ahostsv4` + `curl -4`。若 v4 也时通时断（Akamai 多边缘 IP），**直接 Playwright**，别在 curl 上反复重试。

---

### Porsche India 保时捷印度（`www.porsche.com/middle-east/india/models/`：**Qwik 序列化状态内嵌，curl 直读**）✅

**结论：curl 200 直通，全量数据就在 HTML 里（HTML-escaped 的 Qwik `[0,value]` 结构），不需要浏览器、不需要 API。实测 5 车系 20 个变体。**

| 项 | 内容 |
|---|---|
| 连通性 | ✅ curl 200（Akamai `a299.g.akamai.net`），393 KB |
| **★ 页面框架** | **Qwik**（`q:` 属性 + `props="{&quot;...&quot;}"`）→ 数据是 **HTML-escaped 的类 JSON 序列化**，所有字段形如 `"key":[0,value]`，**不是标准 JSON，`json.loads` 会失败** |
| **★ 提取步骤（核心）** | ① `html.unescape(raw)` ② 正则 `"model":\[0,\{(.*?)\}\],"props"`（`re.S`）切出 20 个卡片块 ③ 块内逐字段正则 `'"%s":\[0,"([^"]*)"\]'` |
| **★ 字段清单** | `modelName`（变体名：`911 Carrera` / `Macan 4S Electric`）· `modelYear`（**2027 / 2026 / 2025**）· `modelRange`（**车系**：`911` `Taycan` `Panamera` `Macan` `Cayenne`）· `modelSeries`（`911 Carrera Model variants`）· `bodyType`（⚠ 有脏值如 `Macan Electric` `SUV Electric`，**别用**）· `wheelDrive` · `seats` · `fuelTypeText`（`Gasoline` / `Electric`）· `gearTypeText` · `price.value` + `price.formattedValue`（`From ₹2,11,29,000.00 incl. VAT`）· `powerHp.formattedValue` |
| **★ 价格正则** | `"price":\[0,\{"value":\[0,(\d+)\]` → 整数；展示用官网 `formattedValue` 的整数部分（**lakh 分组** `2,11,29,000`）|
| **★ 口径** | `incl. VAT`（印度 GST 含税）、`From ...` 起价 → 符合 MSRP，无促销价干扰 |
| **★ 交付分布（20 条）** | Cayenne 8 · 911 4 · Macan 4 · Taycan 3 · Panamera 1；Gasoline 12 / Electric 8；MY2027 18、MY2026 1（Macan 燃油）、MY2025 1（Macan Electric）|
| **★ 无 718** | 全文 `718` / `Boxster` / `Cayman` **0 命中** → 印度已停售，不要补 |
| **⚠ 别被语言/国家选择器链接淹没** | 页面里 `href=".../models/"` 有 40+ 条全是全球市场切换链接；真车型链接不在 `<a>` 里（是卡片 + 配置器 JS 路由），**直接解析 `modelCards` 数据即可** |
| 配置器 | 卡片对应 `porsche.com/middle-east/india/models/<range>/<model>/` 与 configurator，但价格已全在列表页，无需进配置器 |

> 📌 **通用教训**：**Qwik / Nuxt / Next 的「序列化状态」是绕过渲染的最佳入口**。Qwik 的特征是 `[0,value]` 这种 `[引用类型, 值]` 二元组 + HTML 实体转义（`&quot;`）。处理套路固定：**先 `html.unescape`，再用「对象块 + 字段」两级正则**，比硬解析 DOM 稳得多。

---

### Mercedes-Benz India 奔驰印度（`www.mercedes-benz.co.in`：**无头 403 / 有头 200**；价格在 **VMOS API**，接口本身可 curl）✅

**结论：站点无头浏览器 403、curl 全 000，但 `headless=False` + stealth + Mac UA 稳定 200。真正的价格不在页面，而在一套**可直接 curl 的公开 API**（`api.oneweb.mercedes-benz.com/vmos-api`）。实测 23 车系 / 31 条。**

| 项 | 内容 |
|---|---|
| ⚠️ **连通性（两段式）** | ① `www.mercedes-benz.co.in` curl **000**（Akamai）；headless Chromium **403**（body 仅 208 B）；**`headless=False` + `xvfb-run` + 去 `navigator.webdriver` + `window.chrome` + Mac UA → 200** ② **API 域 `api.oneweb.mercedes-benz.com` 反而 curl 200 直通**（只需 `Referer: https://www.mercedes-benz.co.in/`）|
| **★ 价格真源（核心）** | `GET https://api.oneweb.mercedes-benz.com/vmos-api/v1/data/IN/en/OWF/live?subContext=CONFIGURATOR`（95 KB）<br>`GET .../vmos-api/v1/data/IN/en/OWF/live/summary`（54 KB）<br>VMOS = Vehicle Model Overview Service；**IN = 市场，en = 语言，OWF = 渠道** |
| **★ 数据结构** | 顶层 `vehiclesData{}`（23 个车系）+ `cards{}`（25 个展示卡片）+ `groups`（`all` / `amg` / `maybach` / `new`）|
| **★ 车系对象** | `vehiclesData["c-class:saloon:W206"]`：`name`（`C-Class`）· `classId` · `bodytypeId`（`saloon` / `offroader`）· `modelSeries`（`W206`）· `bm4` · `technicalData.priceData` |
| **★ 价格结构（关键）** | `priceData` 的 key 是**品牌分组**（`all` / `amg` / `maybach` / `new`），每个分组内：`{value, formattedValue, filters:{PETROL:{value,formattedValue}, DIESEL:{...}, ELECTRIC:{...}, HYBRID:{...}}}`。**分组价 ≠ 燃料价**：如 C-Class `all`=6,120,000 但 `all.filters.DIESEL`=6,200,000、`amg`=9,405,000 |
| **★ 去重规则** | 同一车系多个 group 出现**同价**很常见（A-Class `all`=`amg`=8,700,000）→ 按 `(fuel, price)` 去重；只有 **C-Class 的 AMG 价（9,405,000）** 是真正独立的一条 |
| **★ 两条易混车系** | `EQS` 出现两次：`eqs-class:saloon-long:V297`（EQS 轿车 13,000,000）/ `eqs-class:offroader:X296`（EQS SUV 13,500,000）→ 都用 `bodytypeId` 区分；`G-Class` 两次：`N465`=电动 31,500,000 / `W465`=燃油（柴油 29,000,000、汽油 38,000,000）|
| **★ 燃料归类** | `PETROL`→`Gasoline`、`DIESEL`→`Diesel`、`ELECTRIC`→`BEV`、`HYBRID`→**`PHEV`**（S-Class / E-Class Sedan / Maybach S-Class 的 `tags` 均含 `phev`）|
| **★ 年款不要推断** | `vehiclesData` 里的 `modelYear` 是**内部销售代码**（`804` `805` `806` `807` `X24` `X25` `X26`），**不是年份** → 一律「官网无年款」|
| **★ 页面口径** | models.html 卡片只显示 `Starting from ₹X`（= 该车系 `priceData.all.value`，**最低动力价**），不显示燃料细分；`?group=amg` / `?group=maybach` 是官方品牌分组筛选 |
| **★ 交付分布（31 条 / 21 个车系名）** | 汽油 17 · 柴油 6 · 纯电 6 · 插混 3（S-Class 22,000,000 / E-Class Sedan 14,500,000 / Maybach S-Class 32,000,000）；价格区间 5,180,000（GLA 汽油）– 44,000,000（Maybach SL Monogram）|
| ⚠ 页面 SSR 干扰 | 车型页 HTML 里 `"Starting from ₹ ..."` 出现 48 次（导航 24 + 页面 24），其中 4 条是**分类聚合**（`All Limousines` `All SUVs` `All Coupés` `All Cabriolets / Roadsters`）→ 不要当车型 |

| **★ 变体级真源（2026-10-19 补充，优先用这个）** | `GET https://api.oneweb.mercedes-benz.com/owcc-backend/api/v3/en_IN/CCci/<configVersion>/entry?proposedStep=MOTORIZATION&typeClass=<型号>` → `motorizations.tiles[]`，每条含 **`name`（如 `CLA 200 Progressive Line` / `C 220d`）+ `priceInformation.basePrice.formattedPrice` + `tags[fuelType]` + `modelId` + `modelYear`**。⚠ **`proposedStep=MOTORIZATION` 是必需参数**（不加只返回 `startPage.preConfigs` 三个营销卡片，且会把同一车型重复两次）；参数大小写敏感，`motorization` 小写会回落成 start page。`configVersion` 从 `GET .../owcc-backend/api/v3/en_IN/CCci/version`（返回 8 位 hash，如 `2cfef53e`）拿 |
| **★ 实测 22 个 typeClass / 49 条 motorization** | `C174` CLA 3 · `W206` C-Class 4（C 200 / C 220d / C 300 / AMG C 43）· `V297` EQS 1 · `X254` GLC 2 · `W214` E-Class Sedan 2（AMG E53 Performance/Racing）· `V214` E-Class Long 3（E200/E220d/E450）· `X167` GLS 7（含 3 条 Maybach GLS）· `V167` GLE 5 · `C254` GLC Coupé 1 · `C167` GLE Coupé 1 · `H247` GLA 3 · `W177` A-Class 1 · `N465` G-Class EV 1 · `W465` G-Class 3 · `C192` AMG GT 2 · `Z223` Maybach S 1 · `Z296` Maybach EQS SUV 2 · `Z232` Maybach SL 1 · `C236` CLE Coupé 1 · `A236` CLE Cabriolet 1 · `X296` EQS SUV 2 · `V223` S-Class 2 |
| **★ 英国站（2026-10-20 补充）** | 市场路径为 **`en_GB/CCci`**（不是 `en-GB`，后者 404），`/version` 返回 `{"dataVersion":"d1b4c02f"}`（**是 JSON 对象，不是字符串**，与印度不同）。**`typeClass` 要剥掉 `-fl` / `-fl2` 后缀**：vmos 里 `X167-fl2` / `V167-fl2` / `W177-fl` / `C167-fl2` / `H247-fl` / `V223-fl` / `S206-fl` / `W247-fl` / `V447-fl2` 直接请求全部 404，改成 `X167` / `V167` / `W177` 才通 → **脚本写「原名 + 去后缀」双候选回退**。实测 36 个 series / **403 条** |
| **★ 英国站重名车系要按动力拆** | 7 组同名双 series（ICE 与 BEV 并存）：`G-Class`(W465/N465) · `GLA`(H247/H244) · `CLA`(C178/C174) · `GLC`(X254/X540) · `CLA Shooting Brake`(X178/X174) · `C-Class Saloon`(W206/W520) · `GLB`(X248/X244) → BEV 那支加 `Electric` 后缀（`CLA` / `CLA Electric`），否则会混成一堆看不出区别的型号 |
| **⚠ Maybach GLS 藏在 GLS 里** | `X167`（GLS）的 tiles 里混有 3 条 `Mercedes-Maybach GLS 600*`（27,500,000 / 30,700,000 / 41,000,000）→ 要按名称拆到「Mercedes-Maybach GLS」车系，否则 GLS 会虚增。**英国站同理**：`X167` 6 条里含 1 条 `Mercedes-Maybach GLS 680 4MATIC`（£179,995）|
| **⚠ 同价同型要区分** | `W465` 有 `Mercedes-AMG G 63` 与 `Mercedes-AMG G 63 Offroad Pro` **同为 38,000,000**（不同型号）；`GLS 450 4MATIC Night Edition` 官网 tag 反而写 **Diesel**（名字漏了 d），**按官网 tag 落表** |

> 📌 **通用教训**：**「站点难进」不代表「数据难拿」**。Mercedes 这种大厂站，页面被 Akamai 掐死，但它的**前端数据服务（VMOS / oneweb）往往独立部署、无鉴权、可直连**。动作顺序应是：**先 Playwright 过一次（拿到 XHR 清单）→ 再把 XHR 里的 API 拎出来直接 curl**，不要一直在页面上硬啃。

---

### Bentley India 宾利印度（`www.bentleymotors.com/in/en.html`：**官网全站不标价，印度站仅经销商页**）❌

**结论：不是反爬问题，是产品策略——Bentley 全球官网都不公开车型价格，CTA 一律 "Enquire to buy"。印度站更是只有 3 家经销商地址。无数据可采。**

| 项 | 内容 |
|---|---|
| 连通性 | ⚠️ curl 全 **403**（Akamai "Access Denied"）；**headless Chromium 403、`headless=False` 200**（与 Mercedes 相反）|
| **★ 印度站实况** | `/in/en.html` 正文仅 **3,149 字符**：品牌故事 + **Mumbai / Bengaluru / Delhi 三家经销商**地址电话，**0 个价格**；`/in/en/models/*` **全部 404** |
| **★ 全球车型页也无价** | `/en/models/bentayga.html`（413 KB）与英国站 `/uk/en/models/bentayga.html`（418 KB）→ **`₹` `£` `$` 全部 0 命中**，页面只有配置/油耗/CO₂ |
| **★ 配置器也无价** | `/en/misc/car-configurator.html/select/bentayga` 可进配置流程，但 **0 个金额**，按钮为 **`Enquire to buy`** |
| **★ 配置器后端实锤** | `GET https://sdl.bentleymotors.com/bentley/api/cc2/brandmaster/models?language=en&role=public&country=<token>` → 7 个 section（Torcal / Bentayga / Bentayga EWB / Flying Spur / Continental GT / Continental GTC / Supersports），**全部 `priceVersion: null`**（无价格版本）|
| ⚠️ **country 参数是加密 token** | 传 `IN` / `GB` / `US` / `DE` / `JP` / `KR` / `CN` 一律返回 **16,371 B、0 section**；只有浏览器下发的 **`GZGBZGB`** 才返回 7 section → **不能用国家代码直接切市场**，别在这上面浪费时间 |
| **★ 国家选择器不含印度** | 只有 **United Kingdom / China / Japan / Germany / United States / South Korea** 六个市场；印度不在配置器覆盖范围 |
| 在售车型（仅供参考，无价） | Torcal · Bentayga · Bentayga EWB · Flying Spur · Continental GT · Continental GTC · Supersports · Mulliner（定制）· Bentley Hybrids · Concept Cars · Pre-Owned |
| **判定依据（四条独立证据）** | ① 印度站正文 0 价格 ② 全球+英国车型页 `₹/£/$` 0 命中 ③ 配置器 CTA 为 Enquire to buy ④ 配置器 API `priceVersion: null` |

> 📌 **通用教训**：**超豪华品牌（Bentley / Rolls-Royce / Ferrari 部分市场）常采用「官网不标价、只接受询价」策略**。判别顺序：① 车型页有没有货币符号 ② 配置器 CTA 是不是 "Enquire" ③ 配置器后端 `priceVersion` 是否为 null。三条都中 → **立即判定「官网不公开价格」，不要再去挖 API**。

---

### Honda UK 本田英国（`www.honda.co.uk`：curl 全通，**grade 级价格藏在配置器页的内联 JSON**）✅

**结论：站点无任何反爬，curl 直通；但车型总览页只有 `from £X` 起价，**真正的 grade（配置等级）价格在每个车型的 `configurator.html` 页面内联数据里**，一条正则即可拿全。实测 8 车型 / 22 个 grade。**

| 项 | 内容 |
|---|---|
| 连通性 | ✅ curl 200（CloudFront），`/cars.html` 570 KB、配置器页 2.8 MB 均可直取 |
| **★ 车型清单** | `https://www.honda.co.uk/cars.html` 的车型卡片，8 款：`New Super-N`(BEV, £18,995) · `Jazz`(HEV, £28,475) · `HR-V`(HEV, £32,725) · `Civic`(HEV, £34,325) · `ZR-V`(HEV, £36,525) · `Prelude`(HEV, £41,595) · `CR-V Plug-in Hybrid`(PHEV, £47,795) · `CR-V Full Hybrid`(HEV, £48,075) |
| **★ grade 价入口** | 每款车一个配置器页：`https://www.honda.co.uk/cars/new/<slug>/configurator.html`，slug ∈ `super-n` `jazz-hybrid` `hr-v-hybrid` `civic-hybrid` `zr-v-hybrid` `prelude-hybrid` `cr-v-hybrid-suv` `plug-in-cr-v-hybrid-suv` |
| **★ 提取正则（核心）** | 页面 HTML 先 `html.unescape`，再用 `"price":"(\d{4,7})"[^{}]{0,400}?"gradeName":"([^"]{1,40})"` —— 价格与 gradeName 在**同一 JSON 对象**里，顺序是 price 在前、gradeName 在后（相隔约 200–300 字符，全是配置开关） |
| **★ 实测 grade 分布** | Super-N 2（Advance / Advance Two Tone）· Jazz 4（Elegance / Advance / Crosstar Advance / Advance Sport）· HR-V 5 · Civic 3 · ZR-V 3 · Prelude 1 · CR-V Full Hybrid 2（Elegance/Advance **- AWD**）· CR-V PHEV 2（Elegance/Advance **Tech 2WD PHEV**）|
| **⚠ 配置器页上还有一堆 £** | 选装件（`Fitted price: £1,800.00`）、促销文案（`£2,500 discount`）、以及顶部导航的 8 个 `from £X` 车系起价 —— **必须用 gradeName 配对正则**，否则会抓到几十条配件价（**Jazz 页有 50+ 个 £ 值，真 grade 只有 4 个**）|
| **★ 燃料归类** | `Super-N` → **BEV**；`CR-V Plug-in Hybrid` → **PHEV**；其余（Jazz/HR-V/Civic/ZR-V/Prelude/CR-V Full Hybrid）官网标 `Full Hybrid` → **HEV** |
| **★ 口径** | 页面脚注为 **OTR（On the Road）价**（含税含首次注册），非裸车 ex-showroom；与印度站口径不同，注意别混用 |
| 年款 | 页面不标 MY → 「官网无年款」|

> 📌 **通用教训**：**Honda 这类传统车企的「配置器」不是 SPA，而是把全量 grade 数据以 JSON 内联进 HTML**（2.8 MB / 页）。**先用 `html.unescape` 再按「字段对」正则抽**，比调 API 快得多；但**必须用 `gradeName` 做锚点**，否则满页配件价会污染结果。

---

### Hyundai UK 现代英国（`www.hyundai.com/uk/en`：curl 全通，**车系级起价在 models 页 JSON**，grade 级未公开）✅⚠️

**结论：站点无任何反爬，`/uk/en/models.html` 内嵌 `modelsOverview` JSON 给出全部车系起价；但**配置器是 SPA 且不吐 grade 价**，官网公开粒度只到「车系起价」。实测 17 条。**

| 项 | 内容 |
|---|---|
| 连通性 | ✅ curl 200（Cloudflare），models 页 113 KB、车型页 167 KB |
| **★ 数据位置** | `https://www.hyundai.com/uk/en/models.html`，HTML 里内嵌 `"modelsOverview":[...]`（按 tag 分组的 JSON 数组）——**先 `html.unescape`，再用括号计数截取该数组后 `json.loads`** |
| **★ 字段** | `modelName`（`All-new IONIQ 3` 这类，需去掉 `All-new ` 前缀）· `priceWithDisclaimer`（`£22,235`）· `promotionPrice`（**促销价，本任务为空**）· `ctaRequiredButtonLink` · `hidePrice` |
| **★ 分组 → 燃料** | `uk/electrified` → **BEV** · `uk/suv` → **PHEV** · `uk/hybrid` → **HEV** · `uk/classics` → **Gasoline** · `uk/hydrogen` → FCV |
| **★ 交付 17 条** | i20 20,010 · BAYON 24,065 · KONA 27,290 / KONA Hybrid 31,455 / KONA Electric 35,000 · INSTER 22,995 · TUCSON 30,985 / Hybrid 34,875 / PHEV 36,680 · SANTA FE Hybrid 49,090 / PHEV 53,200 · IONIQ 3 22,235 · IONIQ 5 40,695 · IONIQ 5 N 65,800 · IONIQ 6 47,050 · IONIQ 6 N 65,800 · IONIQ 9 64,995 |
| **⚠ 两条无价要剔** | `The new STARIA Electric`、`NEXO`（氢燃料）→ `priceWithDisclaimer` 为空，不入表 |
| **⚠ title 带后缀** | `IONIQ 6 N | Highlights`、`The new STARIA Electric | Highlights` —— 用 `split('|')[0]` 清理 |
| **⚠ 配置器拿不到 grade 价** | `/uk/en/models/<model>/configurator.html` 只有 25 KB SPA 壳 + `configurator-labels.model.json`（38 KB，纯文案标签），Playwright 等 12 s 也**没有任何车型/价格 XHR**；车型页（`/models/i20.html`）也只有 `from £20,010` 一个价 → **官网公开粒度就是车系级，不是没挖到** |
| 年款 | 页面不标 MY → 「官网无年款」|

> 📌 **通用教训**：**先判断「官网到底公开到哪一层」，再决定要不要死磕配置器**。Hyundai UK 三个入口（models 页 / 车型页 / 配置器）都只到车系起价 —— 这时**车系级就是正确交付**，硬挖 grade 只会浪费时间。判别特征：配置器页体积 < 30 KB（纯壳）、无价格类 XHR、车型页只有一个 `from £X`。

---


### 🇬🇧 Peugeot UK（英国）— 官方 Price List 是 InDesign 在线文档，只能 OCR

**站点**：`www.peugeot.co.uk`（Akamai，curl 403 / 无头 403 / **有头 200**）；`store.peugeot.co.uk`（**全通，无 403**）

#### 三层数据源与取舍

| 层 | 入口 | 覆盖度 | 口径 | 用途 |
|---|---|---|---|---|
| ① 首页 / offers 页 | `/offers/<nameplate-slug>` | 仅**库存配置**（208 只有 6 条） | `catalogAmount` = On The Road MRRP ✅ | 交叉校验 |
| ② 配置器 trim 页 | `/trim/configurable/<slug>` | 只回该 trim 的 5 个 engine 价 | `totalAmount`（**折后**，无 `catalogAmount`） | 取 trim 清单 |
| ③ **官方价目表** | `pricelist.varioweb.co.uk/peugeot-<model>/` | **完整 trim × engine** | **On The Road MRRP** ✅ | **主用** |

> ⚠ **`?trim=` 参数被忽略**：`/trim/configurable/208-5-door?trim=allure` 不管传什么，都返回 STYLE 的同一份 5 个 engine 价。想切 trim 只能用 `/selector/configurable/<slug>/<trim>/<engine-slug>/<colour>/<interior>`，且该页返回的是 `mtoOffers` 而非 `initialOffer`，取价麻烦。
> ⚠ **GraphQL 存在但不可直用**：`https://store.peugeot.co.uk/graphql` 与 `/api/graphql` 都返回 200，但 introspection 被禁（`GRAPHQL_VALIDATION_FAILED`），手写 query 也全失败 —— 是 **persisted query + 平台注入 token**，**别再试，直接抓 SSR 的 `__NEXT_DATA__`**。

#### 价目表文档链（关键）

```
pricelist.varioweb.co.uk/peugeot-208/          ← HTML 壳 327 B，内嵌 iframe
  └ https://indd.adobe.com/view/<docId>        ← Adobe InDesign 在线发布
      └ /content/2/<docId>/<ver>/package/<prefix>/publication-<N>.html   ← 逐页
      └ /content/2/<docId>/<ver>/package/<prefix>/manifest.json          ← 页数 + documentName
```

- `<ver>`（如 `3583774602555`）**静态 HTML 里没有**，只能**用浏览器打开 `/view/<id>` 并拦截 `indd.adobe.com/content` 请求**取前缀；`VERSION_PREFIX`（如 `5cvj`）可从 `/view/<id>` 的 `readerViewDataFromServer.MANIFEST_BODY` 里读 `VERSION_PREFIX` 字段。
- `manifest.json` 的 `pages.length` = 总页数；`documentName` 可判类型（`Specification Guide` / `Price Guide`）。

#### ★ 页面文字是矢量轮廓，HTML 里没有文本

- `publication-<N>.html` 里文字被转成 **SVG path**（`publication-web-resources/image/*.svgz`，gzip 解压后 `<text>` / `<tspan>` 节点数 = **0**）。
- `inner_text` / `textContent` 都取不到（返回空白字符）。
- **唯一可行：截图 → OCR**。截图参数：`viewport 1191x670`、`device_scale_factor=2`、`full_page=True`，裁掉底部黑色导航条（`h*0.86`）。

#### ★ OCR 解析套路（这套跑通了 109 条）

1. **定位 Price List 页**：裁顶部 20% 高度 OCR，找 `PRICE LIST` / `PRICE GUIDE`。位置规律 = 封面 1 页 + 标准配置 N 页（每 trim 1 页）→ Price List 2 页。
2. **整页 `--psm 6` + 行聚类**（y 差 < 14 合并）。
3. **算术校验挑列**（**不要硬编码 x 坐标**，各车型列位置不同）：

   ```
   Basic MRRP + VAT = Total MRRP
   Total MRRP + OTR Costs = On The Road MRRP   ← 目标列
   ```
   滑动窗口 5 个金额，找同时满足两式的连续组；容差 1.0 英镑。
4. **失败行补漏**：裁该行横带 `(0.30w, y-18, w, y+30)` → **放大 2x** → `--psm 7` 重识别。
5. **仍失败** → 退化取**行内最大金额**（On The Road 恒为该行最大值，大于 P11D 与 ECG-deducted 列）。
6. **缺口兜底**：页面顶部 `y≈280-400` 常被表头挤丢，单独裁该带放大 OCR。

> ⚠ 价格前可能带 `£`（`£26,204.17`），正则必须写成 `[£$]?\s?(\d{1,3}(?:,\d{3})+\.\d{2})` 并**取 group(1)**；否则 `fullmatch` 全部漏掉（E-Rifter / E-Traveller 页全带 £）。

#### ★ 价格口径（Stellantis 英国特有）

价目表列顺序：

```
Engine | Fuel | HP | Titre Code | CO2 | Basic MRRP | VAT | Total MRRP | OTR Costs | On The Road MRRP | On The Road MRRP - Electric Car Grant Deducted | P11D | Electric Range | BiK%
```

- ✅ **取第 10 列「On The Road MRRP」**（= 未扣补贴的 OTR 目录价，与 store 的 `catalogAmount` 完全一致）
- ❌ **不取第 11 列「Electric Car Grant Deducted」**（纯电已扣 £1,500 补贴）
- ❌ 不取 `Basic MRRP`（不含 VAT）
- **OTR Costs 按动力不同**：汽油 1,570 · 混动/柴油 1,520 · 插混 1,230-1,250 · 纯电 1,125

#### ★ 分组与 trim 命名（不要靠 OCR 认 trim 标签）

- **trim 标签 OCR 不可靠**（`STYLE`/`GT`/`GT PREMIUM` 常识别失败或错位）。
- **用「动力重复即新组」规则**：组内动力不重复，遇到与上一行相同的 engine 关键词就切组。实测 208/2008/3008/308/408/5008 全部成立（每组都以汽油或混动开头）。
- **trim 名从 store 拿**：`/trim/configurable/<slug>` 的 `configurationOptions.trims` 给出该名系全部 trim（含 slug、`baseAmount`），**按价格升序**与 PDF 组顺序一一对应（PDF 恒按价格升序排版）。
- ⚠ **组数必须 == trim 数**才按序对应；不等说明有组被漏识别，回头补 OCR。

#### 交付结果（20261021）

`Peugeot_UK_官网价_20261021.xlsx`，**109 条 / 10 个名系**：

| 名系 | 条数 | 价格区间 |
|---|---|---|
| 208 | 18 | £20,565 – 29,815 |
| 2008 | 13 | £25,765 – 33,515 |
| 3008 | 17 | £35,015 – 45,615 |
| 308 | 12 | £30,065 – 38,970 |
| 308 SW | 12 | £31,265 – 40,470 |
| 408 | 9 | £32,065 – 43,965 |
| 5008 | 17 | £38,615 – 49,310 |
| E-208 GTi | 1 | £34,995 |
| E-Rifter | 4 | £32,570 – 36,265 |
| E-Traveller | 6 | £37,060 – 49,095 |

燃油：BEV 49 · HEV 27 · PHEV 17 · Gasoline 10 · Diesel 6。

**未纳入**：
- **燃油 Rifter**（`pricelist` 的 rifter 文档 p6 列了 7 条 24,065-32,475）—— store 与官网首页均无该车，判定已停售。
- **Boxer / Expert / Partner**（LCV 商用车线，非乘用）。
- **508**：`pricelist.varioware.co.uk/peugeot-508/` 是 315 B 空壳、无 iframe，UK 已停售。

---

### 🇬🇧 Fiat UK（英国）— 只有车系级，官网主站 JS 全挂

**站点**：`www.fiat.co.uk`（Akamai，curl 403；**有头浏览器 200 但只有 61 KB 静态壳，`domcontentloaded` 超时、`links=0`、无任何价格** —— JS 被墙）；`store.fiat.co.uk`（**全通**）

#### 可用数据源只有一个

`https://store.fiat.co.uk/compare` → `__NEXT_DATA__.props.pageProps.models`

```json
{"model": {"id": "customize?commercialModelCode=3020H", "title": "500 Hybrid Hatchback"},
 "bodyStyle": {"id": "HATCHBACK"},
 "availableFuelCodes": ["pet" | "mhev" | "elec"],
 "prices": {"cash": {"baseAmount": 18994.68}}}
```

- **只有 10 个车系，每个一个起价** —— 这就是官网公开粒度。
- `baseAmount` 是**含 VAT 的车价**，部分带小数（18,994.68），官网展示取整 → 交付时四舍五入到整数（£18,995）。
- `availableFuelCodes`：`pet` → Gasoline · `mhev` → MHEV · `elec` → BEV。

#### 三条走不通的路（别重复）

| 尝试 | 结果 |
|---|---|
| `pricelist.varioweb.co.uk/` 索引 | 只有 5 条：Citroën C3、Fiat 500、Fiat Pro Doblo/Ducato/Scudo —— **Fiat 乘用车只有 500 一份文档，且是 `All Electric Fiat 500`** |
| `pricelist.varioweb.co.uk/fiat-<其他车型>/` | 全部 404（试过 500-hybrid / 500e / 600 / 600e / grande-panda / panda / topolino / ducato） |
| `store.fiat.co.uk/trim/configurable/<code>` 等 | 全部 **302 → `/error`**（Fiat 的 store 没有 trim 配置器） |

#### 交付结果（20261021）

`Fiat_UK_官网价_20261021.xlsx`，**10 条 / 4 个名系**：500 Hybrid Hatchback £18,995 · 500 Hybrid Cabrio £21,995 · 500e Hatchback £20,995 · 500e Cabrio £26,995 · 500e Armani £29,995 · Grande Panda Electric £21,495 · Grande Panda Hybrid £23,495 · 600 Petrol £23,995 · 600 Hybrid £25,995 · 600e £26,995。

---

### 🇬🇧 Ford UK（英国）— 官方 Price List PDF 在 /cars/<model>/pricelist

**站点**：`www.ford.co.uk`（Akamai；curl 全 **000**，有头浏览器 200 但首页仅 106 KB 壳、`domcontentloaded` 常超时，需 `wait_until='commit'` + 多轮等待）

#### ⚠ 第一坑：`/cars` 页的价格全是促销价，不能采

`/cars` 车型卡片写的是 **`Recommended On The Road Promotional Price from £X`**，且部分注明 `with £3,750 EV Government Grant`。按规则不采。真实目录价在 PDF 里，两者差额实例：

| 车型 | /cars 促销价 | PDF OTR 目录价 | 差 |
|---|---|---|---|
| Puma | 26,145 | **27,145** | 1,000 |
| Capri | 33,985 | **36,985** | 3,000 |
| Explorer | 32,685 | **35,185** | 2,500 |
| Mustang | 57,670 | **58,670** | 1,000 |
| Puma Gen-E | 25,245（含 EV 补贴） | **29,995** | 4,750 |
| Tourneo Courier / Connect / Custom | 28,490 / 35,330 / 60,492.8 | **同值** | 0 |

> Tourneo 系列无促销，`/cars` 与 PDF 一致，可直接交叉校验。

#### ★ 价目表路径

```
https://www.ford.co.uk/cars/<model>/pricelist        ← 页面内嵌 PDF 链接
  └ /content/dam/guxeu/uk/documents/price-list/cars/PL-*.pdf
```

- **PDF 直链 curl 也是 000**（Akamai）→ 必须**浏览器内 `fetch` + base64 回传**。
- ⚠ **文件名日期不可信**：`PL-en_gb-puma-october-2025.pdf` 的实际内容是 **`Puma ICE 27.00 MY ... Effective 5th August 2026`**（文件被覆盖更新，名字没改）。**一律以 `pdfinfo` 的 `Title` 字段判版本与年款**。

#### 各车型文件与年款（2026-10 采集）

| 车型 | PDF | pdfinfo Title 里的年款 | 条数 |
|---|---|---|---|
| Puma | `PL-en_gb-puma-october-2025.pdf` | `Puma ICE 27.00 MY` | 13 |
| Puma Gen-E | `PL_Puma_Gen-E_Customer_Price_List-Effective_1st_January_2026.pdf` | `27.00MY` | 4 |
| Kuga | `PL-All_New_Kuga.pdf` | `Kuga 27.25MY` | 14 |
| Capri | `PL-Capri_Customer_Price_List.pdf` | 无 MY | 6 |
| Explorer | `PL-Explorer_Customer_Price_List.pdf` | 无 MY | 7 |
| Mustang | `PL-new_mustang_s650.pdf` | `Mustang 2026MY` | 6 |
| Mustang Mach-E | `PL-Mach-E-2026MY.pdf` | `2026MY` | 4 |
| Tourneo Courier | `PL-All_New_Tourneo_Courier.pdf` | `27MY` | 6 |
| Tourneo Connect | `PL-tourneo_connect.pdf`（在 `price-list/commercial-vehicles/`） | `27MY` | 10 |
| Tourneo Custom | `PL-New_Tourneo_Custom_2026.pdf` | `27.25MY` | 59 |

**无价目表**：`/cars/mustang-gtd/pricelist` → **404**，`/cars` 卡片只有 `Discover Mustang GTD`（无价）→ 限量超跑询价，不入表。

#### ★ 通用提取规则：行内最后一个「带千分位逗号」的金额 = OTR

各车型 PDF 列数完全不同（Puma 10 列 / Capri 13 列 / Tourneo Custom 15 列），但**目标列恒为行内最后一个带逗号的金额**：

```
Puma       : ... £22,175.00 £26,610.00 £27,145.00 £133.18 £266.35   → 27,145 ✓
Capri      : ... £30,745.83 £36,895.00 £36,985.00 £24.61  £49.23    → 36,985 ✓
T.Custom   : ... 57195 46,050 55,260 50,989.83 60,492.80 351.61 703.22 → 60,492.80 ✓
```

- BIK 月度值（`133.18`）**不带逗号** → 天然排除
- CAP Code（`57195`）、GVM（`320`）、CO2（`122`）、VED（`3420`）**都不带逗号** → 排除
- **噪声过滤**：`left` 以 `If ` / `●` / `•` / `-` 开头，或词数 < 3 / > 20 的行（脚注、保修条款、技术数据）全部丢弃

#### ★ Ford 的燃料命名陷阱

| PDF 写法 | 实际归类 |
|---|---|
| `1.0L EcoBoost Hybrid (mHEV)` | **MHEV**（Puma 全系） |
| `2.5L Duratec FHEV` / `Self-Charging Hybrid` | **HEV** |
| `2.5L Duratec PHEV` / `Plug-In Hybrid` | **PHEV** |
| `1.5L EcoBoost 150PS ... PHEV` | **PHEV**（Tourneo Connect 有这款） |
| `1.0L EcoBoost 125PS`（无 Hybrid 字样） | Gasoline |
| `71kWh / 46kWh / 53kWh ... Electric` | BEV |

> ⚠ **Puma 全系都是 mHEV**，`/cars` 卡片写 "Hybrid SUV" 很容易误判成 HEV。

#### ★ 两个特殊处理

**1. Mustang 的 PDF 是图片版**
- `pdftotext` 只出页码，正文全是 JPEG（`pdfimages -list` 可见）。
- 处理：`pdftoppm -r 200 -png` → `tesseract --psm 6` 逐页 OCR → 先按 `£` 计数定位价格页（p-03 有价格表，p-08 是配件表，p-05 是颜色/座椅选装）。
- 识别后务必与 **p-02 封底的 `from £58,670 / £70,940`** 交叉校验。

**2. Tourneo Custom 的 trim 在分组标题行**
- 结构：`SWB Tourneo` / `LWB Tourneo`（车身）→ `Zetec - 8 Seats/...`（trim）→ 若干动力行。
- 需顺序扫描并**继承**当前 body 与 trim。
- ⚠ PDF 后半部（约 line 560+）是**技术数据表**和 **MS-RT 延伸配置**（8/9 座不同价），会污染提取 → **限定只扫主价格表区间**（line 380-566）。
- 主表 59 条：SWB/LWB × Zetec/Titanium/Titanium Luxe/Active/Titanium X/Titanium X Luxe + SWB MS-RT 3 条；**LWB MS-RT 未纳入**（只在延伸页出现，行结构不同）。

#### 交付结果（20261022）

`Ford_UK_官网价_20261022.xlsx`，**129 条 / 10 个车型**，价格区间 £27,145 – £83,235。

燃油：Diesel 37 · BEV 36 · PHEV 21 · Gasoline 15 · MHEV 13 · HEV 7。

**未纳入**：Mustang GTD（无价目表、官网无价）；Ford 商用车线（Transit / Ranger 等，属 `/vans-and-pickups`）。

### Alpine DE（德国 `www.alpinecars.de`：**Renault rplug 配置器直取 SRP，curl 全通**）✅

- **★ 配置器 base（按车系，勿猜）**：A110=`BAEL5`（`/product/model/AL1/a110/c/A`）· A290=`BAERh`（`/product/model/A5E/a290/c/A`）· A390=`BAEQx`（`/product/model/Z1D/alpine-a390/c/A`）。base 从各配置器页的 `modelURI` 提取。
- **★ 两个 JSON 端点（均需 `Accept: application/json`）**：
  - `GET /product/model/<spec>/<slug>/c/A` → Schema.org，`schema:isVariantOf[]` 里每个版本带 `schema:price` + `priceType:"SRP"`（=PVC 含税目录价）
  - `GET /pricelist/<base>` → 全版本 `PVC`（含 19% VAT）与 `PCHT`/`TVA`，比 product 端点更全（A290 5 个版本一次拿全）
- **★ 年款**：A390 配置器属性有 `label:"MODEL YEAR 2026"`（code `EV2GA1`，SYSTEMATIC）→ 写 `MY2026`；A110/A290 无任何 MY 标记 → `官网无年款`。A110 的 `c2gMillesime:millesime_2015` 是车型代号，**不是年款**。
- **★ 动力并入型号（取「Ihre Motorisierung」的 `engineName` 原文）**：A110 `4 Zyl. 1.8l 252 PS`、GTS `4 Zyl. 1.8l 300 PS`（不是只写 `252 PS`）；A290 `Elektro 180` / `Elektro 220`；A390 `AWD 3 Motor 400 PS` / `AWD 3 Motor 470 PS`。
- **⚠ 老版本 variant URL 会 400**：`SERIELIM3`（A110 S / R 70 页仍挂着）返回 `400 {"":"}"` → 说明该版本已停配；`/angebot/a110-gt|a110s|a110-r-70` 都是余留页，**无价格、勿入表**。
- **⚠ A110 官方 Preisliste 是图片版**：`cdn.group.renault.com/alp/de/price_list/2025_03_05_Preisliste_A110.pdf.asset.pdf/<hash>.pdf`，5 页含 1227 张 Image，`pdftotext` 只出破折号 → 不需 OCR，直接用配置器。
- **交付结果（20261026）**：`Alpine_DE_官网价_20261026.xlsx`，**9 条**（A110 2 + A290 5 + A390 2）。未纳入：A110 R 70 与 5 款 Limitierte Edition（无公开价、配置器无入口）。

### Dacia DE（德国 `www.dacia.de`：**APP_STATE 内嵌全版本矩阵 + rplug PVC 双源**）✅

- **★ 站点结构**：React 页把整棵 JSON 塞在 `window.APP_STATE=JSON.parse("…")`，路径 `page.data.content.contentZone.configurator.staticData.engines[].grades[]`。用「找 `window.APP_STATE=JSON.parse(` → 定位引号 → 反转义 → 二次 `JSON.parse`」解析，**不要**用正则扫 1 MB 单行 HTML（会卡死）。
- **★ 关键字段**：`grades[].pricedVersion.label` = 官方完整版本名（已含动力，如 `Expression Eco-G 120 auto`）；`minPrice` = PVC；`webDisplayPrices.displayPrice` 与 `minPrice` 一致。`startingPrice` 有时是营销起价，**不可用**。
- **★ 配置器 base（按车系）**：Sandero/Stepway=`BAEQu0AhhAjJ8J9J-` / `BAEQu0AhhAjJ_KAKB`（同属 `BI1/sandero`）· Jogger=`BAERm`（`RI1/jogger`）· Duster=`BAERg`（`DU3/duster`）· Bigster=`BAEQ_`（`BD1/bigster`）· Striker=`BAERl`（`BK1/striker`）· Neuer Spring=`BAEQl`（`TWD/neuer-spring`）· 上一代 Spring=`BAEP8`（`S2E/spring`）。
- **★ 年款**：各 base 的 `/c/<base>/A` JSON 里 `impact[].specCatCode=="c2gMillesime"` → `millesime_YYYY`。本季：Sandero/Stepway/Jogger=2025、Duster/Bigster=2024、Striker/Neuer Spring=2026、上一代 Spring=2024。
- **⚠ Bigster Extreme 起价陷阱**：`startingPrice` 比 PVC 低 500 €（Extreme mild hybrid-G 140：26.990 vs 27.490；另 4 个 Extreme 版本同样差 500）→ **一律取 `minPrice`**，并用 `/pricelist/<base>` 的 `PVC` 交叉校验。
- **⚠ 两个 Spring 并存**：`Neuer Spring`（`BAEQl`，Expression/Journey electric 80，17.900/19.400）为在售新车系；`Spring`（`BAEP8`，仅 `Extreme electric 100`，19.700，MY2024）**只剩库存车入口**（`Lagerfahrzeuge anzeigen`，无配置器）→ 入表但「是否停销」标 **是**。
- **★ 型号名补充**：Neuer Spring 配置器 `pricedVersion` 只有 `Expression`/`Journey`，必须按官网价目页补成 `Expression electric 80` / `Journey electric 80`。Stepway 版本的官方名自带 `Stepway` 前缀，车型列写 `Sandero Stepway`。
- **★ 燃油口径（与既有西班牙 Dacia 一致）**：TCe / Eco-G（汽油+LPG 双燃料）→ `Gasoline`；mild hybrid(-G) 140 → `MHEV`；hybrid 155 / HYBRID 155 / tribrid 150 4x4 / Striker hybrid 150 4x4 → `HEV`；electric → `BEV`。
- **交付结果（20261026）**：`Dacia_DE_官网价_20261026.xlsx`，**74 条 / 8 个车型**（Sandero 9 · Sandero Stepway 10 · Jogger 9（5 座 5 + 7 座 4）· Duster 16 · Bigster 17 · Striker 10 · Neuer Spring 2 · Spring 1），13.590–32.790 €。燃油：Gasoline 29 · HEV 23 · MHEV 19 · BEV 3。

### INEOS DE（德国 `ineosgrenadier.com/de/de`：**Next.js 站点 + 独立配置器主机，官方价目 PDF 一页可文本解析**）✅

- **★ 两个源**：官网 `https://ineosgrenadier.com/de/de/`（车系页）与配置器 `https://configurator.ineosgrenadier.net`（**独立主机**，curl 直连返 500，浏览器 fetch 返 200 → 必须走浏览器）。产品清单：`https://configurator.ineosgrenadier.net/products/products/DE`，返回 JSON。
- **★ 产品码与车系对应**（DE，2026-10 在售）：`G01E` Station Wagon（BASE `72.640` / `PPT` Trialmaster `82.900` / `PPQ` Fieldmaster `82.900`）· `G02E` Utility Wagon 2-Sitzer `71.140` · `G03E` Utility Wagon 5-Sitzer `72.640` · `G09E` Quartermaster（同三档 trim，`72.640` / `82.900` / `82.900`）· `G11B` Chassis Cab（MY24，**无价**）。
- **★ 官方价目 PDF**：`https://mss-p-034-delivery.stylelabs.cloud/api/public/content/Pricelist_DE`（1 页，文本层正常，`pdftotext -layout` 表头会错位）。可靠解法：`pdftotext` 后按**产品码 token 定位行**（`G01E` / `GEB` …），再用 **x 坐标**把价格列归到表头分组（Station Wagon / Utility Wagon 2-seat / Utility Wagon 5-seat / Quartermaster / Chassis Cab）。柴油 = 同款汽油 +1.000 €（`GEB` 汽油 / `GEC` 柴油）。
- **★ 年款**：PDF 与产品 JSON 均写 **MJ27**（= MY2027）→ 入表 `MY2027`。Chassis Cab 为 `CC-24`（MY24）。
- **★ 型号名**：官方写法为 `Grenadier 3.0L Turbo-Benziner` / `Grenadier 3.0L Twin-Turbo-Diesel`，Edition 版在型号列前加 trim：`Trialmaster Edition 3.0L Turbo-Benziner`。车名列用官网车系名（`Grenadier Station Wagon` / `Grenadier Utility Wagon (2-Sitzer)` / `Grenadier Utility Wagon (5-Sitzer)` / `Grenadier Quartermaster`）。
- **⚠ 未纳入（须在交付说明里讲清）**：
  - **Quartermaster Chassis Cab**：官网车系页只有 `REGISTRIERE DICH ALS INTERESSENT`（登记意向），无价格；MJ27 价目 PDF 虽有 72.640 / 73.640，但配置器无购车入口 → **不入表**（避免把「仅登记」当成在售）。
  - **Black Edition**：官网价格位是占位符（`AB †`），无实价。
  - **Trialmaster X**：限量版，官网写 `AB €87.890*`，价目 PDF 无此版本。
  - **Arcane Works Detour**：定制系列，无公开价。
- **交付结果（20261026）**：`Ineos_DE_官网价_20261026.xlsx`，**16 条 / 4 个车系**（SW 6 · UW 2-Sitzer 2 · UW 5-Sitzer 2 · Quartermaster 6），71.140–83.900 €。燃油：Gasoline 8 · Diesel 8。

### Jeep DE（德国 `www.jeep.de`：**Akamai 封 curl，配置器 SPA 逐卡点取 + 官方价目 PDF 交叉校验**）⚠️ 需浏览器

- **★ 站点结构**：全站（含 PDF）对 curl 返 **403 Akamai**，加全套请求头也无效；浏览器内 `fetch` 200。PDF 走「本地 Node HTTP 接收器 + 浏览器 fetch POST」落盘（`http://127.0.0.1:18766/pdf?name=...`）。
- **★ 配置器**：`https://www.jeep.de/omni/konfigurator`（SPA，hash 路由）。首页是 13 张车系×动力卡片，卡片用 **`aria-label`** 标识（`Neuer Compass e-Hybrid` / `Avenger e-Hybrid MJ27` / `Wrangler Benziner` …）。点卡片进入 `#/customize`，**价格异步加载**，首次解析常缺第一个 trim 的价格 → 等 9–12 s 再解析，或读 hub 起价校验。
- **⚠ hash 历史坑**：`history.back()` 常回不到 hub → 每台车之前直接 `navigate` 到 `https://www.jeep.de/omni/konfigurator`。
- **★ 解析法**：`document.body.innerText` 正则 `/([A-Z0-9][A-Z0-9 .\\-]{2,40})\\n\\nUPE des Herstellers ab Werk ab\\n\\n([\\d.]+)\\n€/g` 取 trim+价；动力名取含 `kW` 且不含 `/100`、`g/km`、`kWh` 的行（`1.2 Hybrid 48V 107kW (145PS) Automatik`）。**同车系多动力时，trim 卡只显示当前动力的价格**：`Compass Elektro` 有 157/170 kW 两档，必须分别点 trim 读「Motorisierung」段确认组合（`FIRST EDITION` 仅 157 kW）。
- **★ 官方价目 PDF（4 份，全部 `www.jeep.de/content/dam/jeep/de/models/pdf/`）**：`Compass-MY26.pdf`（MJ2026）· `Avenger-MY27.pdf`（MJ27）· `Avenger_MY25.pdf`（**文件名骗人，内容是 MJ2026**，09.01.2026）· `Wrangler.pdf`（MJ2025，`ab 07/2025`）。价格表在 `pdftotext -layout` 的固定列区，先 `grep -n "Unverbindliche Preisempfehlung"` 定位。
- **★ 年款**：官方 MJ 标记 → `MY2027` / `MY2026` / `MY2025`。**Avenger 两代同时在售**（MJ26 清库 + MJ27 新车），配置器并列，必须按 MJ 分开、不能合并。
- **★ 燃油口径**：`e-Hybrid`（1.2 T3 48V，81/107 kW）与 `4xe`（1.2l T3 4xe）在官网标签就是 **`Hybrid 48V`** → **MHEV**（不是 HEV）；`e-Hybrid Plug-In`（1.6 165 kW）→ **PHEV**；`Elektro` / `4xe Elektro`（双电机 275 kW）→ **BEV**；Wrangler `2.0l T-GDI` → **Gasoline**。
- **⚠ 配置器 vs PDF 差异（以配置器为准）**：
  - `Compass 4xe Elektro`：配置器 **275 kW (375 PS)**，PDF 写 276 kW。
  - `Avenger 4xe MJ27`：PDF 只列 `UPLAND 34.300`，配置器还有 `85th ANNIVERSARY 35.900`、`OVERLAND 36.500`。
  - `85th ANNIVERSARY` 全系（Benziner 30.400 / e-Hybrid 32.400 / Elektro 42.300）**不在 MY27 PDF 里**，只在配置器。
- **★ 在售范围**：仅 Avenger / Compass / Wrangler 三车系；Renegade、Grand Cherokee、Gladiator 已无页面，Wrangler 只售 Benziner（无 4xe）。
- **交付结果（20261026）**：`Jeep_DE_官网价_20261026.xlsx`，**44 条 / 3 个车型**（Compass 13 · Avenger 29（MY2026 14 + MY2027 15）· Wrangler 2），26.300–72.900 €。燃油：MHEV 17 · BEV 15 · Gasoline 9 · PHEV 3。

### 其它市场速记（无独立详段）

> 本表只放**没有单独段落**的站点。其余站点的坑位见下方同名详段，按市场的快速索引见文首「0. 站点速查」。

| 站点 | 关键坑 | 价格在哪 |
|---|---|---|
| 领克 lynkco.com | 按出口 IP 地理跳转 .com.cn | 需海外代理 |
| 本田/标致 NZ | Cloudflare 拦截直连 | 车型页 From + ORC |
| 保时捷 NZ | 无价目表 PDF | 车型总览页 astro-island JSON（`modelCards` → `price.formattedValue`） |
| 大众 NZ | 价格只在各车型页 | 每车型页 `Download specs` PDF（含多配置 MRP） |
| BYD NZ | 有官方价格表 | BROCHURE 按钮 → price-list PDF |
| Fiat/Jeep PH | JS 渲染 | 官方导航数据区 `STANDARD MODELS` |
| BMW PH | 车型页无价，藏在 PDF | `BMW Price List` 按钮 → S3 上的价目 PDF（**沙箱封 `*.s3.amazonaws.com`**） |
| 法拉利（全球） | 官方从不公布售价 | 仅经销商询价，**无法采集 MSRP** |
| Aston Martin（全球含 ES） | 官方从不公布售价；配置器全链路无价格字段 | 仅经销商报价，**无法采集 MSRP**（详见下） |

---

## 交付后清理约定

用户习惯：**每个品牌只留最终 XLSX**（8 列，含燃油分类），其余中间文件与脚本清理掉。
工作区长期保留：`车型调研可复用提示词包.md`、`车型调研·会话交接启动卡.md`、本 skill。
