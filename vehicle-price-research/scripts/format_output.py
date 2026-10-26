#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把采集结果格式化为统一 8 列 XLSX（含燃油分类）。

列序：品牌,官网车型名称,官网型号名称,年款,官网MSRP,是否停销,数据日期,燃油分类

⚠️ 2026-09-30 起：**只输出 XLSX**，不再生成 CSV。

用法（作为模块）：
    from format_output import write_output
    rows = [
        {'brand':'Dacia','model':'DUSTER','version':'DUSTER expression tribrid 150 4*4',
         'year':'MY2024','price':28220.0,'discontinued':'否','fuel':'HEV'},
        ...
    ]
    write_output(rows, '/workspace/Dacia_ES_官网价_20260917', date='20260917')
    # 若环境无 /workspace，换成实际可写目录，如 '/data/Dacia_ES_官网价_20260917'

用法（命令行，读 JSON）：
    python3 format_output.py input.json /workspace/输出前缀 --date 20260917
    # 非本机环境：把 /workspace 换成你的工作区目录（如 /data）

JSON 格式：[{"brand":..,"model":..,"version":..,"year":..,"price":..,"discontinued":..,"fuel":..}, ...]
  - year 缺省 -> '官网无年款'
  - discontinued 缺省 -> '否'
  - fuel 缺省 -> '未标注'；取值见下表（英文原名）
"""
import json, sys, os

# 海外燃料分类（该列输出英文原名）
FUEL_CLASSES = {
    'gasoline':  'Gasoline',   # 汽油
    'diesel':    'Diesel',     # 柴油
    'mhev':      'MHEV',       # 轻混
    'fcv':       'FCV',        # 燃料电池
    'lpg':       'LPG',        # 液化石油气
    'bev':       'BEV',        # 纯电
    'dual fuel': 'Dual Fuel',  # 双燃料
    'phev':      'PHEV',       # 插电式混合动力
    'hev':       'HEV',        # 非插电式混合动力
    'reev':      'REEV',       # 增成型电动
}

# 中文 / 官网常见写法 -> 标准英文名 的宽松映射
FUEL_ALIAS = {
    # 中文
    '汽油': 'Gasoline', '柴油': 'Diesel', '轻混': 'MHEV', '燃料电池': 'FCV',
    '液化石油气': 'LPG', '纯电': 'BEV', '双燃料': 'Dual Fuel',
    '插电式混合动力': 'PHEV', '非插电式混合动力': 'HEV', '增成型电动': 'REEV',
    # 官网常见写法
    'petrol': 'Gasoline', 'benzine': 'Gasoline', 'gas': 'Gasoline', 'essence': 'Gasoline',
    'electric': 'BEV', 'elektrisch': 'BEV', 'ev': 'BEV', 'bev': 'BEV',
    'hybrid': 'HEV', 'hybride': 'HEV', 'mild hybrid': 'MHEV',
    'plug-in hybrid': 'PHEV', 'plug in hybrid': 'PHEV', 'phev': 'PHEV',
    'diesel': 'Diesel', 'lpg': 'LPG', 'cng': 'LPG',
    'fuel cell': 'FCV', 'hydrogen': 'FCV',
    'range extender': 'REEV', 'erev': 'REEV',
}


def fuel_class(v):
    """把各种写法归一为「海外燃料分类」英文原名"""
    if not v:
        return '未标注'
    s = str(v).strip()
    low = s.lower()
    # 精确命中表
    if low in FUEL_CLASSES:
        return FUEL_CLASSES[low]
    if s in FUEL_CLASSES.values():
        return s
    if low in FUEL_ALIAS:
        return FUEL_ALIAS[low]
    for k, val in FUEL_ALIAS.items():
        if len(k) > 1 and k in s:
            return val
    # 英文包含判断（PHEV 优先于 HEV）
    if 'phev' in low or 'plug' in low:
        return 'PHEV'
    if 'mhev' in low or 'mild' in low:
        return 'MHEV'
    if 'hev' in low or 'hybrid' in low or 'hybride' in low:
        return 'HEV'
    if 'bev' in low or 'electric' in low or 'elektrisch' in low or '纯电' in s:
        return 'BEV'
    if 'hydrogen' in low or 'fuel cell' in low:
        return 'FCV'
    if 'diesel' in low:
        return 'Diesel'
    if 'petrol' in low or 'benzine' in low or 'gasoline' in low or 'essence' in low:
        return 'Gasoline'
    return '未标注'


def eurofmt(p):
    """28220.0 -> '28.220,00'  （点千分位，逗号小数）"""
    s = f'{float(p):.2f}'
    ip, dp = s.split('.')
    return f'{int(ip):,}'.replace(',', '.') + ',' + dp


def write_output(rows, prefix, date):
    """
    rows: list[dict]，键 brand/model/version/year/price/discontinued/fuel
    prefix: 输出路径前缀（不含扩展名）
    date: 'YYYYMMDD'
    返回: xlsx 路径
    """
    header = ['品牌', '官网车型名称', '官网型号名称', '年款', '官网MSRP',
              '是否停销', '数据日期', '燃油分类']

    xlsx_path = prefix + '.xlsx'
    try:
        import openpyxl
        from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    except ImportError:
        raise SystemExit('需要 openpyxl：sudo pip3 install openpyxl')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = '官网价'
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True, color='FFFFFF')
        c.fill = PatternFill('solid', fgColor='1F4E79')
        c.alignment = Alignment(horizontal='center', vertical='center')

    for r in rows:
        ws.append([
            r.get('brand', ''),
            r.get('model', ''),
            r.get('version', ''),
            r.get('year') or '官网无年款',
            eurofmt(r['price']),
            r.get('discontinued', '否'),
            date,
            fuel_class(r.get('fuel')),
        ])

    thin = Side(style='thin', color='BFBFBF')
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, max_col=8):
        for cell in row:
            cell.border = Border(left=thin, right=thin, top=thin, bottom=thin)
            if cell.column == 5:                     # MSRP 文本格式
                cell.number_format = '@'
                cell.alignment = Alignment(horizontal='right')
            elif cell.column in (4, 6, 7, 8):
                cell.alignment = Alignment(horizontal='center')

    for col, wd in zip('ABCDEFGH', [16, 12, 62, 14, 14, 10, 12, 12]):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = f'A1:H{ws.max_row}'
    wb.save(xlsx_path)
    print(f'[OK] {len(rows)} 行 -> {xlsx_path}')
    return xlsx_path


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    inp, prefix = sys.argv[1], sys.argv[2]
    date = '20260917'
    if '--date' in sys.argv:
        date = sys.argv[sys.argv.index('--date') + 1]
    rows = json.load(open(inp, encoding='utf-8'))
    write_output(rows, prefix, date)


if __name__ == '__main__':
    main()
