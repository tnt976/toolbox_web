# 深圳统一地址查询系统 API 接口文档

> 文档生成时间：2026-05-21  
> 数据来源：龙华滢水山庄一区房屋编码查询系统  
> API来源：https://spatydz.sz.gov.cn

---

## 📍 API 基础信息

### 基础URL
```
https://spatydz.sz.gov.cn
```

### 认证信息
```
API Key: d129375bf07f409a8e5d2ae232712b2a
```

### 请求头
```http
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: application/json, text/plain, */*
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Referer: https://spatydz.sz.gov.cn/web/
Content-Type: application/json
```

---

## 🔍 地址搜索接口

### 1. 自定义地址搜索

**接口地址**
```
POST/GET /addrdatapc/standard/search/customSearch
```

**完整请求示例**
```
https://spatydz.sz.gov.cn/addrdatapc/standard/search/customSearch?t=1779366379100&query=滢水山庄一区&region=440300&page=1&pageSize=100&ak=d129375bf07f409a8e5d2ae232712b2a
```

**请求参数**

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| t | Long | 是 | 时间戳（毫秒） | 1779366379100 |
| query | String | 是 | 搜索关键词 | 滢水山庄一区 |
| region | String | 否 | 区域代码 | 440300 |
| page | Integer | 否 | 页码（从1开始） | 1 |
| pageSize | Integer | 否 | 每页记录数 | 100 |
| ak | String | 是 | API密钥 | d129375bf07f409a8e5d2ae232712b2a |

**响应示例**
```json
{
  "status": 0,
  "message": "success",
  "result": [
    {
      "uid": "4403060090043200033",
      "name": "滢水山庄一区1栋",
      "address": "广东省深圳市龙华区民治街道民乐社区滢水山庄一区1栋",
      "location": {
        "lng": 114.06358,
        "lat": 22.59584
      },
      "level": 5,
      "parentId": "4403060090043200001"
    },
    {
      "uid": "4403060090043200031",
      "name": "滢水山庄一区2栋",
      "address": "广东省深圳市龙华区民治街道民乐社区滢水山庄一区2栋",
      "location": {
        "lng": 114.06352,
        "lat": 22.59576
      },
      "level": 5,
      "parentId": "4403060090043200001"
    }
  ],
  "total": 10,
  "page": 1,
  "pageSize": 100
}
```

**响应字段说明**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| status | Integer | 状态码，0表示成功 |
| message | String | 响应消息 |
| result | Array | 地址列表数组 |
| total | Integer | 总记录数 |
| page | Integer | 当前页码 |
| pageSize | Integer | 每页记录数 |

**地址对象字段说明**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| uid | String | 地址唯一标识符 |
| name | String | 地址名称 |
| address | String | 完整地址 |
| location | Object | 经纬度坐标 |
| location.lng | Double | 经度 |
| location.lat | Double | 纬度 |
| level | Integer | 地址层级 |
| parentId | String | 父级ID |

**代码示例**

```python
import requests
import time

def search_address(keyword, region="440300", page=1, page_size=100):
    """搜索地址"""
    base_url = "https://spatydz.sz.gov.cn/addrdatapc/standard/search/customSearch"
    
    params = {
        't': int(time.time() * 1000),
        'query': keyword,
        'region': region,
        'page': page,
        'pageSize': page_size,
        'ak': 'd129375bf07f409a8e5d2ae232712b2a'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://spatydz.sz.gov.cn/web/'
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    return response.json()

# 使用示例
result = search_address("滢水山庄一区")
for item in result['result']:
    print(f"{item['name']}: {item['address']}")
```

```javascript
// JavaScript 示例
async function searchAddress(keyword, region = '440300', page = 1, pageSize = 100) {
    const baseUrl = 'https://spatydz.sz.gov.cn/addrdatapc/standard/search/customSearch';
    
    const params = new URLSearchParams({
        t: Date.now(),
        query: keyword,
        region: region,
        page: page,
        pageSize: pageSize,
        ak: 'd129375bf07f409a8e5d2ae232712b2a'
    });
    
    const response = await fetch(`${baseUrl}?${params}`, {
        headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://spatydz.sz.gov.cn/web/'
        }
    });
    
    return await response.json();
}

// 使用示例
const result = await searchAddress('滢水山庄一区');
console.log(result);
```

---

## 🏠 房屋编码数据结构

### 地址层级说明

```
省/直辖市 (level: 1)
  ↓
市 (level: 2)
  ↓
区/县 (level: 3)
  ↓
街道/镇 (level: 4)
  ↓
社区 (level: 5)
  ↓
建筑物/楼栋 (level: 6)
  ↓
单元 (level: 7)
  ↓
楼层 (level: 8)
  ↓
房号 (level: 9) ← 最详细层级
```

### 房屋编码规则（25位）

**编码格式**
```
┌─────────────────────────────────────────────────────────────────────┐
│ 区划代码   │ 街道代码 │ 社区代码 │ 建筑物编号  │ 单元 │ 楼层 │ 房号 │
│   6位     │   3位   │   3位   │    8位      │  2位 │  2位 │  1位 │
└─────────────────────────────────────────────────────────────────────┘
```

**示例编码**
```
4403090093200000000101011
├─440309─┼─009─┼─320─┼─00000001─┼─01─┼─01─┼─1─┤
  龙华区   民治   民乐   1栋        1单元 1楼   01室
```

### 编码字段详解

| 位置 | 字段 | 位数 | 说明 | 示例值 |
|------|------|------|------|--------|
| 1-6 | 区划代码 | 6 | 行政区划代码 | 440309 |
| 7-9 | 街道代码 | 3 | 街道/镇代码 | 009 |
| 10-12 | 社区代码 | 3 | 社区代码 | 320 |
| 13-20 | 建筑物编号 | 8 | 楼栋编号，不足补0 | 00000001 |
| 21-22 | 单元号 | 2 | 单元编号 | 01 |
| 23-24 | 楼层号 | 2 | 楼层编号 | 01 |
| 25 | 房号 | 1 | 房号（取个位） | 1 |

### 龙华区地址代码参考

| 区域层级 | 代码 | 名称 |
|---------|------|------|
| 龙华区 | 440309 | 深圳市龙华区 |
| 民治街道 | 440309009 | 民治街道 |
| 民乐社区 | 440309009320 | 民乐社区工作站 |
| 滢水山庄一区 | 44030900932000000001 | 滢水山庄一区 |

---

## 📋 数据字典

### 区域代码对照表

**龙华区**
```json
{
  "regionCode": "440309",
  "regionName": "深圳市龙华区",
  "districts": [
    {
      "code": "440309001",
      "name": "观湖街道"
    },
    {
      "code": "440309002",
      "name": "民治街道"
    },
    {
      "code": "440309003",
      "name": "龙华街道"
    },
    {
      "code": "440309004",
      "name": "大浪街道"
    },
    {
      "code": "440309005",
      "name": "福城街道"
    },
    {
      "code": "440309006",
      "name": "观澜街道"
    }
  ]
}
```

### 民治街道社区代码
```json
{
  "streetCode": "440309009",
  "streetName": "民治街道",
  "communities": [
    {
      "code": "440309009001",
      "name": "民乐社区"
    },
    {
      "code": "440309009002",
      "name": "民新社区"
    },
    {
      "code": "440309009003",
      "name": "龙塘社区"
    },
    {
      "code": "440309009004",
      "name": "北站社区"
    },
    {
      "code": "440309009005",
      "name": "樟坑社区"
    },
    {
      "code": "440309009006",
      "name": "南景社区"
    }
  ]
}
```

---

## 🔧 使用示例

### Python 完整示例

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深圳统一地址查询系统 API 使用示例
"""

import requests
import time
import csv
import json


class SZAddressAPI:
    """深圳统一地址查询系统API"""
    
    def __init__(self, api_key):
        self.base_url = "https://spatydz.sz.gov.cn"
        self.api_key = api_key
        self.session = requests.Session()
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': f'{self.base_url}/web/'
        })
    
    def search_address(self, keyword, region="440300", page=1, page_size=100):
        """
        搜索地址
        
        Args:
            keyword: 搜索关键词
            region: 区域代码，默认深圳市(440300)
            page: 页码
            page_size: 每页记录数
        
        Returns:
            dict: API响应结果
        """
        url = f"{self.base_url}/addrdatapc/standard/search/customSearch"
        
        params = {
            't': int(time.time() * 1000),
            'query': keyword,
            'region': region,
            'page': page,
            'pageSize': page_size,
            'ak': self.api_key
        }
        
        response = self.session.get(url, params=params, timeout=30)
        return response.json()
    
    def get_buildings_by_area(self, area_name):
        """
        获取指定区域的楼栋列表
        
        Args:
            area_name: 区域名称
        
        Returns:
            list: 楼栋列表
        """
        result = self.search_address(area_name)
        
        if result.get('status') == 0:
            return result.get('result', [])
        
        return []
    
    def export_to_csv(self, data, filename):
        """
        导出数据到CSV
        
        Args:
            data: 数据列表
            filename: 文件名
        """
        if not data:
            print("没有数据可导出")
            return
        
        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            if isinstance(data[0], dict):
                fieldnames = list(data[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        
        print(f"✓ 已导出 {len(data)} 条记录到 {filename}")
    
    def export_to_json(self, data, filename):
        """
        导出数据到JSON
        
        Args:
            data: 数据列表
            filename: 文件名
        """
        if not data:
            print("没有数据可导出")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 已导出 {len(data)} 条记录到 {filename}")


def main():
    # 初始化API
    api = SZAddressAPI('d129375bf07f409a8e5d2ae232712b2a')
    
    # 搜索滢水山庄一区
    print("搜索地址: 滢水山庄一区")
    buildings = api.get_buildings_by_area("滢水山庄一区")
    
    print(f"找到 {len(buildings)} 个楼栋:")
    for building in buildings:
        print(f"  - {building['name']}: {building['address']}")
    
    # 导出数据
    if buildings:
        api.export_to_csv(buildings, 'buildings.csv')
        api.export_to_json(buildings, 'buildings.json')


if __name__ == '__main__':
    main()
```

### JavaScript 完整示例

```javascript
/**
 * 深圳统一地址查询系统 API 使用示例
 */

class SZAddressAPI {
    constructor(apiKey) {
        this.baseUrl = 'https://spatydz.sz.gov.cn';
        this.apiKey = apiKey;
    }
    
    async searchAddress(keyword, region = '440300', page = 1, pageSize = 100) {
        const url = `${this.baseUrl}/addrdatapc/standard/search/customSearch`;
        
        const params = new URLSearchParams({
            t: Date.now(),
            query: keyword,
            region: region,
            page: page,
            pageSize: pageSize,
            ak: this.apiKey
        });
        
        try {
            const response = await fetch(`${url}?${params}`, {
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json, text/plain, */*',
                    'Referer': `${this.baseUrl}/web/`
                }
            });
            
            return await response.json();
        } catch (error) {
            console.error('请求失败:', error);
            throw error;
        }
    }
    
    async getBuildingsByArea(areaName) {
        const result = await this.searchAddress(areaName);
        
        if (result.status === 0) {
            return result.result || [];
        }
        
        return [];
    }
    
    exportToCSV(data, filename) {
        if (!data || data.length === 0) {
            console.log('没有数据可导出');
            return;
        }
        
        const headers = Object.keys(data[0]);
        const csvContent = [
            headers.join(','),
            ...data.map(row => headers.map(h => `"${row[h] || ''}"`).join(','))
        ].join('\n');
        
        // 使用 FileSaver 或 Blob 下载
        const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        link.click();
        
        console.log(`✓ 已导出 ${data.length} 条记录到 ${filename}`);
    }
}

// 使用示例
async function main() {
    const api = new SZAddressAPI('d129375bf07f409a8e5d2ae232712b2a');
    
    // 搜索滢水山庄一区
    console.log('搜索地址: 滢水山庄一区');
    const buildings = await api.getBuildingsByArea('滢水山庄一区');
    
    console.log(`找到 ${buildings.length} 个楼栋:`);
    buildings.forEach(building => {
        console.log(`  - ${building.name}: ${building.address}`);
    });
    
    // 导出数据
    if (buildings.length > 0) {
        api.exportToCSV(buildings, 'buildings.csv');
    }
}

main();
```

---

## ⚠️ 注意事项

1. **API Key使用限制**
   - 当前API Key为公开测试密钥
   - 请勿用于商业用途或大量并发请求
   - 建议添加适当的请求间隔（建议 > 500ms）

2. **数据准确性**
   - 地址数据来源于深圳市统一地址库
   - 建议结合官方渠道进行数据验证
   - 房屋编码为系统生成，可能需要与实际物业信息核对

3. **请求频率**
   - 建议设置请求间隔避免被限流
   - 高频请求可能导致IP被封禁

4. **数据更新**
   - 地址数据可能存在更新延迟
   - 建议定期同步最新数据

---

## 📞 技术支持

- **官方网站**: https://spatydz.sz.gov.cn
- **Web查询入口**: https://spatydz.sz.gov.cn/web/

---

## 📄 附录

### 常见问题

**Q: 如何获取真实的房屋编码？**  
A: 可以通过以下方式：
1. 访问官方网站 https://spatydz.sz.gov.cn/web/
2. 扫描房门上的二维码
3. 咨询社区网格员
4. 联系物业管理处

**Q: API请求失败怎么办？**  
A: 检查以下几点：
1. 网络连接是否正常
2. API Key是否正确
3. 请求参数格式是否正确
4. 是否触发了频率限制

**Q: 如何批量获取数据？**  
A: 使用分页参数循环请求：
```python
all_results = []
page = 1
while True:
    result = api.search_address(keyword, page=page)
    if result.get('result'):
        all_results.extend(result['result'])
        if len(result['result']) < 100:
            break
        page += 1
    else:
        break
```

---

*本文档由 AI 助手自动生成，仅供参考学习使用*
*生成时间：2026-05-21*
