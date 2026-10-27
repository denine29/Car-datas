# 安装与速查（vehicle-price-research）

## 安装

把整个 `vehicle-price-research/` 目录放进 agent 的 skills 目录：

```bash
# CodeBuddy / Claude Code
cp -r vehicle-price-research ~/.codebuddy/skills/
# 或 Claude Code 的 skills 目录
cp -r vehicle-price-research ~/.claude/skills/
```

重启会话后生效。触发方式：发一个汽车品牌官网链接，或说「查某品牌某市场官网价格」。

## 这个 skill 干什么

输入「品牌 × 市场」官网 URL → 输出**官方 MSRP 的统一 8 列 XLSX**。

数据源**只用官网**（官网页面 / 官方 API / 官方 PDF 价目表），第三方来源必须标注且优先不用。

## 输出格式（8 列 + 年款依据副表，只出 XLSX）

```
品牌 | 官网车型名称 | 官网型号名称 | 年款 | 官网MSRP | 是否停销 | 数据日期 | 燃油分类
```

工作簿固定 **2 个 sheet**：`官网价`（上表 8 列）+ `年款依据`（品牌 / 车型 / 年款 / 覆盖型号数 / 判定过程 / 逐字原文 / 来源位置）。年款依据的覆盖型号数合计必须 = 主表行数。

| 列 | 规则 |
|---|---|
| 官网型号名称 | **发动机/动力必须并入此列**，用官网原始写法（`4*4` 不写 `4x4`） |
| 年款 | 官网标 MY/millesime 才写；没标写「官网无年款」，**严禁推断** |
| 官网MSRP | 按市场原生千分位（欧元 `28.220,00` / 美元英镑 `102,700`），单元格**文本格式** |
| 燃油分类 | 英文原名：`Gasoline` `Diesel` `MHEV` `HEV` `PHEV` `BEV` `FCV` `LPG` `Dual Fuel` `REEV` |

⚠ 官网写 "Hybrid" 不等于 HEV：48V 轻混 → **MHEV**；插电 → **PHEV**。

## 三条最常踩的坑

1. **促销价不能采。** 官网总览页的 `from £X` 常是 Promotional Price / 含政府补贴价。真价先在配置器（`catalogAmount` / 价格 API）里找，配置器拿不到再用官方 PDF 价目表。
2. **「站点难进」≠「数据难拿」。** 页面 403 时先抓一次 XHR 清单，把 API 拎出来直连；API 被 WAF 拦就改「浏览器内 fetch」。
3. **配置器只是纯壳时，车系级就是终局。** 判别：页面 < 30 KB、无价格类 XHR、车型页只有一个 `from £X`。

## 目录结构

```
vehicle-price-research/
├── SKILL.md                     主规则：格式 / 口径 / 流程 / 反爬按症状查表（A–E 五组）
├── INSTALL.md                   本文件
├── examples/                    ★ 7 份真实成品 XLSX + README（先看这个对样式）
├── references/
│   ├── sites.md                 站点坑位详表（2200+ 行）+ 文首「站点速查索引」（按市场分组）
│   └── workflow.md              给不支持 skill 的 agent 用的可复制提示词模板
└── scripts/
    ├── triage.py                站点可达性分诊（30 秒判断封锁级别）
    ├── fetch_pdf.py             Akamai 拦 PDF 的破封脚本（浏览器内 fetch + base64）
    ├── write_xlsx.js            ★ 唯一生成器：8 列 + 年款依据副表（需 `npm i exceljs`）
    └── format_output.py         旧版生成器（单 sheet / 仅欧元），已被 write_xlsx.js 取代
```

## examples/ 里有什么

7 份**真实交付过**的成品，覆盖不同规模与粒度，拿来对照「目标长什么样」：

| 文件 | 条数 | 看点 |
|---|---|---|
| Mercedes-Benz_UK | 403 | 规模上限；同名车系按动力拆分（`CLA` / `CLA Electric`） |
| Skoda_UK | 133 | 全量 `MY2027`；五种动力并存 |
| Ford_UK | 129 | 48V 轻混归 **MHEV**；价格来自官方 PDF |
| Peugeot_UK | 109 | 纯电/插混/轻混/汽油/柴油混排，动力标识并入型号名 |
| Cadillac_US（配置器版） | 114 | `MY2027`/`MY2026`/`MY2025` **三代并售**；价格含运费 |
| Porsche_IN | 20 | 印度 lakh 千分位 `2,11,29,000` |
| Hyundai_UK | 17 | **车系级**（官网只公开到这一层）的正确交付样式 |

`examples/README.md` 逐份说明了「要你看什么」，末尾还列了 6 条反面教材（促销价、税制优惠价、`totalAmount`、颜色加价、EMI 月供、硬凑变体）。


## 怎么用 sites.md 最快

1. 先看文首 **「0. 站点速查」**——按市场找到品牌，看结论（✅/⚠️/❌）和一句话方法。
2. 再 Ctrl+F 品牌名，读同名详段（字段名、正则、失败过程）。
3. 遇到表里没有的新站，按 `## 数据源定位方法（通用）` 的顺序走：配置器 → 车型页 From → 官方价格表补全。

## 已覆盖市场

西班牙 ES · 比利时 BE · 丹麦 DK · 智利 CL · 希腊 GR · 泰国 TH · 美国 US · 印度 IN · 韩国 KR ·
英国 UK · 德国 DE · 法国 FR · 新西兰 NZ · 菲律宾 PH · 全球站

共 50+ 个品牌站点，其中 ✅ 可采 30+ 个。
