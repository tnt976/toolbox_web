#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙华滢水山庄1区房屋编码爬虫 - 使用真实 API
"""

import requests
import csv
import json
import time
import urllib.parse
from datetime import datetime


class RealHouseCodeSpider:
    """真实房屋编码爬虫"""
    
    def __init__(self):
        self.base_url = "https://spatydz.sz.gov.cn"
        self.search_api = "/addrdatapc/standard/search/customSearch"
        self.ak = "d129375bf07f409a8e5d2ae232712b2a"
        self.house_data = []
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://spatydz.sz.gov.cn/web/'
        }
        
        self.session = requests.Session()
    
    def search_address(self, query, region_code="440300", page=1, page_size=100):
        """搜索地址"""
        try:
            timestamp = int(time.time() * 1000)
            url = f"{self.base_url}{self.search_api}"
            params = {
                't': timestamp,
                'query': query,
                'region': region_code,
                'page': page,
                'pageSize': page_size,
                'ak': self.ak
            }
            
            print(f"正在搜索: {query}")
            print(f"请求URL: {url}?{urllib.parse.urlencode(params)}")
            
            response = self.session.get(url, params=params, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print(f"搜索响应状态码: {response.status_code}")
                print(f"响应内容长度: {len(response.content)}")
                return result
            else:
                print(f"搜索失败 - 状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                return None
                
        except Exception as e:
            print(f"搜索出错: {e}")
            return None
    
    def parse_search_results(self, search_result):
        """解析搜索结果"""
        if not search_result:
            return []
        
        print(f"搜索结果类型: {type(search_result)}")
        print(f"完整搜索结果: {json.dumps(search_result, ensure_ascii=False, indent=2)}")
        
        addresses = []
        
        # 尝试解析不同的数据结构
        if isinstance(search_result, dict):
            # 检查常见的数据字段
            for field in ['data', 'result', 'list', 'addressList', 'items']:
                if field in search_result:
                    data = search_result[field]
                    if isinstance(data, list):
                        addresses.extend(data)
                        print(f"找到 {len(data)} 条结果在 '{field}' 字段")
                    elif isinstance(data, dict):
                        # 继续在嵌套字典中查找列表
                        for sub_field in ['list', 'items', 'data']:
                            if sub_field in data and isinstance(data[sub_field], list):
                                addresses.extend(data[sub_field])
                                print(f"找到 {len(data[sub_field])} 条结果在 '{field}.{sub_field}' 字段")
        
        # 如果直接就是列表
        elif isinstance(search_result, list):
            addresses = search_result
            print(f"直接找到 {len(addresses)} 条结果")
        
        print(f"总共解析到 {len(addresses)} 条地址记录")
        return addresses
    
    def extract_house_info(self, address_item):
        """从地址项中提取房屋信息"""
        result = {
            '楼栋': '',
            '单元': '',
            '楼层': '',
            '房号': '',
            '房屋编码(25位)': '',
            '楼栋编码(19位)': '',
            '详细地址': ''
        }
        
        # 尝试提取各种可能的字段
        if isinstance(address_item, dict):
            # 尝试不同的字段名
            name = address_item.get('name') or address_item.get('title') or address_item.get('address') or ''
            address = address_item.get('address') or address_item.get('fullAddress') or name
            house_code = address_item.get('houseCode') or address_item.get('house_code') or address_item.get('code') or ''
            building_code = address_item.get('buildingCode') or address_item.get('building_code') or ''
            
            result['详细地址'] = str(address)
            result['房屋编码(25位)'] = str(house_code) if house_code else ''
            result['楼栋编码(19位)'] = str(building_code) if building_code else ''
            
            # 尝试从地址中解析出楼栋、单元等信息
            addr_str = str(address)
            if '栋' in addr_str:
                parts = addr_str.split('栋')
                result['楼栋'] = parts[0] + '栋'
                if len(parts) > 1:
                    if '单元' in parts[1]:
                        unit_parts = parts[1].split('单元')
                        result['单元'] = unit_parts[0] + '单元'
                        if len(unit_parts) > 1:
                            if '楼' in unit_parts[1]:
                                floor_parts = unit_parts[1].split('楼')
                                result['楼层'] = floor_parts[0] + '楼'
            
            # 也尝试从名称中解析
            name_str = str(name)
            if not result['楼栋'] and '栋' in name_str:
                parts = name_str.split('栋')
                result['楼栋'] = parts[0] + '栋'
        
        return result
    
    def run_search(self):
        """运行搜索任务"""
        print("=" * 80)
        print("龙华滢水山庄1区房屋编码爬虫 - 真实API版本")
        print("=" * 80)
        
        # 搜索"滢水山庄"
        print("\n" + "=" * 80)
        print("搜索1: '滢水山庄一区'")
        print("=" * 80)
        result1 = self.search_address("滢水山庄一区")
        
        if result1:
            addresses1 = self.parse_search_results(result1)
            
            for idx, addr in enumerate(addresses1[:20]):  # 显示前20个结果
                print(f"\n结果 {idx+1}:")
                print(json.dumps(addr, ensure_ascii=False, indent=2))
                
                house_info = self.extract_house_info(addr)
                if house_info['详细地址']:
                    self.house_data.append(house_info)
        
        # 搜索更多变体
        print("\n" + "=" * 80)
        print("搜索2: '滢水山庄'")
        print("=" * 80)
        result2 = self.search_address("滢水山庄")
        
        if result2:
            addresses2 = self.parse_search_results(result2)
            
            for idx, addr in enumerate(addresses2[:20]):
                print(f"\n结果 {idx+1}:")
                print(json.dumps(addr, ensure_ascii=False, indent=2))
                
                house_info = self.extract_house_info(addr)
                if house_info['详细地址'] and house_info not in self.house_data:
                    self.house_data.append(house_info)
        
        # 搜索"滢水"
        print("\n" + "=" * 80)
        print("搜索3: '滢水'")
        print("=" * 80)
        result3 = self.search_address("滢水")
        
        if result3:
            addresses3 = self.parse_search_results(result3)
            
            for idx, addr in enumerate(addresses3[:20]):
                print(f"\n结果 {idx+1}:")
                print(json.dumps(addr, ensure_ascii=False, indent=2))
                
                house_info = self.extract_house_info(addr)
                if house_info['详细地址'] and house_info not in self.house_data:
                    self.house_data.append(house_info)
        
        # 保存结果
        print(f"\n" + "=" * 80)
        print(f"总共获取到 {len(self.house_data)} 条房屋编码记录")
        print("=" * 80)
        
        if self.house_data:
            # 保存为CSV
            self.save_to_csv("滢水山庄一区_真实API_房屋编码.csv")
            self.save_to_json("滢水山庄一区_真实API_房屋编码.json")
            
            # 显示部分结果
            print("\n部分数据预览:")
            for i, house in enumerate(self.house_data[:30], 1):
                print(f"{i:3d}. 地址: {house['详细地址']}, 编码: {house['房屋编码(25位)']}")
        else:
            print("\n警告: 没有获取到真实数据，生成示范数据...")
            self.generate_sample_data()
            self.save_to_csv("滢水山庄一区_示范数据_房屋编码.csv")
            self.save_to_json("滢水山庄一区_示范数据_房屋编码.json")
    
    def generate_sample_data(self):
        """生成示范数据"""
        for building in range(1, 29):
            for unit in [1, 2, 3]:
                for floor in range(1, 9):
                    for room in [1, 2]:
                        room_num = f"{floor:02d}{room:02d}"
                        
                        # 生成符合深圳编码规范的示例编码
                        region_code = "440309"  # 龙华区
                        b_code = f"{building:02d}{unit:01d}{floor:02d}{room:02d}"
                        full_code = f"{region_code}{b_code}{building:03d}{unit}{floor:02d}{room}001"
                        building_code = full_code[:19]
                        
                        self.house_data.append({
                            '楼栋': f"{building}栋",
                            '单元': f"{unit}单元",
                            '楼层': f"{floor}楼",
                            '房号': room_num,
                            '房屋编码(25位)': full_code,
                            '楼栋编码(19位)': building_code,
                            '详细地址': f"深圳市龙华区滢水山庄一区{building}栋{unit}单元{floor}楼{room_num}室"
                        })
    
    def save_to_csv(self, filename):
        """保存为CSV"""
        if not self.house_data:
            return
        
        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            fieldnames = ['楼栋', '单元', '楼层', '房号', '房屋编码(25位)', '楼栋编码(19位)', '详细地址']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.house_data)
        
        print(f"✓ 已保存为 {filename}，共 {len(self.house_data)} 条记录")
    
    def save_to_json(self, filename):
        """保存为JSON"""
        if not self.house_data:
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.house_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 已保存为 {filename}")


def main():
    spider = RealHouseCodeSpider()
    spider.run_search()


if __name__ == "__main__":
    main()
