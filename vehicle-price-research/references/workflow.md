# 通用提示词模板（给不支持 Skill 的 agent 用）

> 适用：ChatGPT / Kimi / 豆包 / Gemini 等**没有 skill 机制**的 agent。
> 用法：复制下面模板 → 替换 `<尖括号>` → 发送。
> 若对方 agent 能联网/能跑代码，效果最好；纯对话 AI 只能给方法，需要你自己执行。

---

## 0. 全局纪律（每次任务结尾都加上）

```
完成后检查并遵守：
1. 每条数据必须给出来源 URL；无法确认的标"未核实"。
2. 官网标 preliminary / 预发布 / target 的值原样保留，不当最终值。
3. 第三方来源必须注明"非官网"，与官网数据分开。
4. 不臆造、不四舍五入"美化"数字，页面写多少填多少。
5. 只采官方指导价/MSRP/含税指导价/上路价，不采选装后价格。
6. 促销价、折扣价、补贴价一律不采（只备注原价）。
7. 已停售/下架车型也要入表，`是否停销` 标"是"，并注明数据来源。
```

---

## 1. 主模板：查某市场官网全系价格 → XLSX

```
请帮我查 <品牌> <市场>官网在售全部车型的官方建议零售价（MSRP），整理成 XLSX（8 列，含燃油分类）。

【第一步：配置器（最优先）】
1. 打开官网配置器（configurador / configure / car-configurator）
2. 用浏览器开发者工具抓网络请求，找返回价格的接口（JSON/GraphQL）
3. 接口里找 MSRP 字段：
   - 一般叫 price / msrp / baseAmount / catalogAmount
   - ⚠️ 若同时有 catalogAmount 和 totalAmount，取 catalogAmount（=未折扣目录价）
   - totalAmount / discountedPrice = 促销价，不采
4. 逐版本采集，记录来源

【第二步：配置器不可用或只到车系起价 → 看车型页 From 卡】
- 记录每个车系的 From 起价（含税口径）；官网公开粒度只到这一层时，车系级就是正确交付。

【第三步：仍缺变体/缺价 → 用官方价格表补全】
1. 找官网是否有"官方价格表"：
   - 独立价目页（prijslijst / price list / tarifas / 价格总览）
   - 车型页上的下载按钮：Download specs / Brochure / Prijslijst / Download price
     → 指向的 PDF 常是该车型的《价格与规格表》，含全部版本 + MSRP
2. 有 → 以这些 PDF 补配置器未收录的版本，并备注来源。

【输出格式（严格遵守）】
只交付 XLSX，固定 8 列（不再出 CSV）：
品牌 | 官网车型名称 | 官网型号名称 | 年款 | 官网MSRP | 是否停销 | 数据日期 | 燃油分类

- 官网车型名称 = 车系名（SANDERO / DUSTER / DS 3）
- 官网型号名称 = 官方完整版本名，【发动机/动力必须并入此列】，用官网原始写法
  例：DUSTER expression tribrid 150 4*4   （不要写成 4x4，不要单独列"三擎混动"）
- 年款 = 官网标 MY/millesime 就原样写（MY2024）；没标一律写"官网无年款"，禁止推断
- 官网MSRP = 纯数字，按该市场货币的【原生千分位】写法，单元格设为文本格式：
    · 欧元区：点号千分位  28.220,00
    · 美元/英镑/泰铢：逗号千分位  102,700 / 1,229,000
- 是否停销 = 在售写"否"，已停售/下架写"是"（下架车也入表）
- 数据日期 = 抓取当天 YYYYMMDD
- 燃油分类 = 取英文原名：Gasoline / Diesel / MHEV / HEV / PHEV / BEV / FCV / LPG / Dual Fuel / REEV
    · 官网写 "Hybrid" 不等于 HEV —— 48V 轻混要归 MHEV（如 Ford EcoBoost Hybrid (mHEV)）
    · 插电式归 PHEV；无法判定写"未标注"

示例：
Dacia|DUSTER|DUSTER expression tribrid 150 4*4|MY2024|28.220,00|否|20260917|HEV
Dacia|SANDERO|NUEVO SANDERO Stepway Extreme eco-G 120 auto|MY2025|19.890,00|否|20260917|Gasoline

XLSX 要求：MSRP 列为文本格式、冻结首行、加自动筛选。

完成后再按"全局纪律"自查。
```

---

## 2. 年款怎么查（用户常问）

```
年款来源优先级：
1. 配置器接口里的 millesime / modelYear / MY 字段 → 有就采
2. 官网页面明确标注的 MY/MY25/年款 → 采
3. ⚠️ 页面上的年份若属于以下情况，【不是年款】，写"官网无年款"：
   - 版权年份（© DS Automobiles 2025）
   - 交付日期（Entrega en 11/2026）
   - 促销有效期（OFERTA VALIDA HASTA EL 30/09/2026）
4. 绝不根据车型上市时间自己推断年款
```

---

## 3. 遇到网站拦截怎么办

```
症状 → 对策：
- 403 + errors.edgesuite.net / 固定字节错误页 → Akamai。curl 无效，需真实浏览器（Playwright）
- "Just a moment..." → Cloudflare。需真实浏览器
- 自动跳转其他国家站 → 按 IP 地理跳转。需海外出口或让用户截图
- 页面结构在但价格空白 → 价格 JS 渲染。需渲染后读取
- PDF 直链 403 但页面能打开 → 在浏览器控制台执行同源 fetch：
    fetch(PDF_URL,{credentials:'include'}).then(r=>r.arrayBuffer())
  然后转 base64 下载

- curl 000 但 TLS 握手成功（HTTP/2 INTERNAL_ERROR）→ Akamai 在 HTTP/2 层拒 bot，
    --http1.1 也无效，直接上有头浏览器
- curl 000 但同域 /assets/*.js 能下载 → 不是整站封锁，是主 HTML 被地理屏蔽；
    下载 JS bundle 后 grep 出后端域名，常能直连无鉴权 API
- API 被 WAF 拦 curl，但浏览器能开页面 → 在 Playwright 页面上下文里 fetch() 调 API
    （WAF 拦的是浏览器指纹，不是 URL）
- PDF 直链 403，下载后在浏览器里打开是图片（pdftotext 只有页码）
    → pdftoppm -r 200 转图 + tesseract OCR；先用封面 from £X 交叉校验

兜底：若以上都不行，让对方 AI 生成"提示词"，用户带去能联网的 agent 执行。
```

---

## 4. 交付后

- 只交付 XLSX（8 列，含燃油分类），不再出 CSV
- 文件命名：`<品牌>_<市场>_官网价_YYYYMMDD.xlsx`，写入工作区
- 交付说明必须写清：价格口径（含税/OTR/Ex-showroom）、粒度（车系级还是变体级）、
  未纳入的车型及原因、数据来源 URL
- 清理中间文件，只留最终交付物
