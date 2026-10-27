#!/usr/bin/env node
/*
把采集结果写成 vehicle-price-research 规定的 8 列 XLSX。

用法：
  node write_xlsx.js <rows.json> <输出前缀> --date YYYYMMDD
  node write_xlsx.js <rows.json> <输出前缀> --date YYYYMMDD --money euro|lakh|comma
  node write_xlsx.js <rows.json> <输出前缀> --date YYYYMMDD --year-basis <year_basis.json>

year_basis.json（可选，写了就在工作簿里加「年款依据」副表）：
  [{"brand","model","year","basis","quote","source"}, ...]
  按 brand+model+year 分组，覆盖型号数由主表自动统计；有主表行未被覆盖会告警。

rows.json: [{"brand","model","version","year","price","discontinued","fuel"}, ...]
  price 为数字；格式化方式由 --money 决定（默认 comma）
    euro  -> 28.220,00   （欧元区，点千分位、逗号小数）
    comma -> 102,700     （美元/英镑/泰铢等，四舍五入到整数）
    lakh  -> 2,11,29,000 （印度 lakh 分组）
  year 缺省 -> 官网无年款；discontinued 缺省 -> 否；fuel 缺省 -> 未标注
*/
const fs = require('fs');
const path = require('path');
const ExcelJS = require('exceljs');

const FUEL = {
  gasoline: 'Gasoline', diesel: 'Diesel', mhev: 'MHEV', fcv: 'FCV', lpg: 'LPG',
  bev: 'BEV', 'dual fuel': 'Dual Fuel', phev: 'PHEV', hev: 'HEV', reev: 'REEV',
  汽油: 'Gasoline', 柴油: 'Diesel', 轻混: 'MHEV', 燃料电池: 'FCV', 液化石油气: 'LPG',
  纯电: 'BEV', 双燃料: 'Dual Fuel', 插电式混合动力: 'PHEV', 非插电式混合动力: 'HEV', 增成型电动: 'REEV',
};
const ALIAS = {
  petrol: 'Gasoline', benzine: 'Gasoline', gas: 'Gasoline', essence: 'Gasoline',
  electric: 'BEV', elektrisch: 'BEV', ev: 'BEV', hybrid: 'HEV', hybride: 'HEV',
  'mild hybrid': 'MHEV', 'plug-in hybrid': 'PHEV', 'plug in hybrid': 'PHEV',
  cng: 'LPG', 'fuel cell': 'FCV', hydrogen: 'FCV', 'range extender': 'REEV', erev: 'REEV',
};

function fuelClass(v) {
  if (!v) return '未标注';
  const s = String(v).trim();
  const low = s.toLowerCase();
  if (FUEL[low]) return FUEL[low];
  if (Object.values(FUEL).includes(s)) return s;
  if (ALIAS[low]) return ALIAS[low];
  for (const [k, val] of Object.entries(ALIAS)) if (k.length > 1 && low.includes(k)) return val;
  if (low.includes('phev') || low.includes('plug')) return 'PHEV';
  if (low.includes('mhev') || low.includes('mild')) return 'MHEV';
  if (low.includes('hev') || low.includes('hybrid') || low.includes('hybride')) return 'HEV';
  if (low.includes('bev') || low.includes('electric') || low.includes('elektrisch') || s.includes('纯电')) return 'BEV';
  if (low.includes('hydrogen') || low.includes('fuel cell')) return 'FCV';
  if (low.includes('diesel')) return 'Diesel';
  if (low.includes('petrol') || low.includes('benzine') || low.includes('gasoline') || low.includes('essence')) return 'Gasoline';
  return '未标注';
}

function fmtPrice(p, mode) {
  const n = Number(String(p).replace(/[^\d.-]/g, ''));
  if (!Number.isFinite(n)) throw new Error('price 不是数字: ' + p);
  if (mode === 'euro') {
    const [ip, dp] = n.toFixed(2).split('.');
    return ip.replace(/\B(?=(\d{3})+(?!\d))/g, '.') + ',' + dp;
  }
  if (mode === 'lakh') {
    const s = String(Math.round(n));
    if (s.length <= 3) return s;
    const last3 = s.slice(-3);
    const rest = s.slice(0, -3).replace(/\B(?=(\d{2})+(?!\d))/g, ',');
    return rest + ',' + last3;
  }
  return Math.round(n).toLocaleString('en-US');
}

async function main() {
  const [inp, prefix] = process.argv.slice(2);
  if (!inp || !prefix) {
    console.error('用法: node write_xlsx.js <rows.json> <输出前缀> --date YYYYMMDD [--money euro|lakh|comma] [--year-basis <year_basis.json>]');
    process.exit(1);
  }
  const arg = (k, d) => {
    const i = process.argv.indexOf(k);
    return i > -1 ? process.argv[i + 1] : d;
  };
  const date = arg('--date', new Date().toISOString().slice(0, 10).replace(/-/g, ''));
  const money = arg('--money', 'comma');

  const rows = JSON.parse(fs.readFileSync(inp, 'utf8'));
  const wb = new ExcelJS.Workbook();
  const ws = wb.addWorksheet('官网价');
  const widths = { A: 16, B: 20, C: 62, D: 14, E: 16, F: 10, G: 12, H: 12 };

  ws.columns = [
    { width: widths.A }, { width: widths.B }, { width: widths.C }, { width: widths.D },
    { width: widths.E }, { width: widths.F }, { width: widths.G }, { width: widths.H },
  ];
  ws.addRow(['品牌', '官网车型名称', '官网型号名称', '年款', '官网MSRP', '是否停销', '数据日期', '燃油分类']).eachCell(c => {
    c.font = { bold: true, color: { argb: 'FFFFFFFF' } };
    c.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF1F4E79' } };
    c.alignment = { horizontal: 'center', vertical: 'middle' };
  });

  for (const r of rows) {
    ws.addRow([
      r.brand ?? '',
      r.model ?? '',
      r.version ?? '',
      r.year || '官网无年款',
      fmtPrice(r.price, money),
      r.discontinued || '否',
      date,
      fuelClass(r.fuel),
    ]);
  }

  const thin = { style: 'thin', color: { argb: 'FFBFBFBF' } };
  ws.eachRow((row, i) => {
    row.eachCell({ includeEmpty: true }, (cell, col) => {
      cell.border = { top: thin, left: thin, bottom: thin, right: thin };
      if (i === 1) return;
      if (col === 5) {                       // MSRP 文本格式
        cell.numFmt = '@';
        cell.alignment = { horizontal: 'right' };
      } else if ([4, 6, 7, 8].includes(col)) {
        cell.alignment = { horizontal: 'center' };
      }
    });
  });

  ws.views = [{ state: 'frozen', ySplit: 1 }];
  ws.autoFilter = { from: 'A1', to: `H${ws.rowCount}` };

  const basisPath = arg('--year-basis', null);
  if (basisPath) {
    const basis = JSON.parse(fs.readFileSync(basisPath, 'utf8'));
    const rowCount = new Map();
    for (const r of rows) {
      const k = [r.brand ?? '', r.model ?? '', r.year || '官网无年款'].join('||');
      rowCount.set(k, (rowCount.get(k) || 0) + 1);
    }

    const ws2 = wb.addWorksheet('年款依据');
    [14, 28, 14, 10, 70, 52, 60].forEach((w, i) => { ws2.getColumn(i + 1).width = w; });
    ws2.addRow(['品牌', '官网车型名称', '年款', '覆盖型号数', '年款依据（判定过程）', '官网原文（逐字）', '来源位置']).eachCell(c => {
      c.font = { bold: true, color: { argb: 'FFFFFFFF' } };
      c.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF1F4E79' } };
      c.alignment = { horizontal: 'center', vertical: 'middle' };
    });

    const covered = new Set();
    for (const b of basis) {
      const k = [b.brand ?? '', b.model ?? '', b.year || '官网无年款'].join('||');
      covered.add(k);
      ws2.addRow([
        b.brand ?? '', b.model ?? '', b.year || '官网无年款',
        rowCount.get(k) ?? 0, b.basis ?? '', b.quote ?? '', b.source ?? '',
      ]);
    }

    ws2.eachRow((row, i) => {
      row.eachCell({ includeEmpty: true }, (cell, col) => {
        cell.border = { top: thin, left: thin, bottom: thin, right: thin };
        if (i === 1) return;
        cell.alignment = [3, 4].includes(col)
          ? { horizontal: 'center', vertical: 'top' }
          : { vertical: 'top', wrapText: true };
      });
    });
    ws2.views = [{ state: 'frozen', ySplit: 1 }];
    ws2.autoFilter = { from: 'A1', to: `G${ws2.rowCount}` };

    const missing = [...rowCount.keys()].filter(k => !covered.has(k));
    if (missing.length) console.warn('[WARN] 年款依据未覆盖主表分组: ' + missing.join(' ; '));
  }

  const out = prefix.endsWith('.xlsx') ? prefix : prefix + '.xlsx';
  fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
  await wb.xlsx.writeFile(out);
  console.log(`[OK] ${rows.length} 行 -> ${out}`);
}

main().catch(e => { console.error('[FAIL]', e.message); process.exit(1); });
