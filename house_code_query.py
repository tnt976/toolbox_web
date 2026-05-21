#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙华滢水山庄1区房屋编码查询与导出工具
"""

import csv
import json
from typing import List, Dict, Any


class HouseCodeManager:
    """房屋编码管理器"""
    
    def __init__(self):
        self.house_data = []
    
    def add_house(self, building: str, unit: str, floor: str, 
                  room: str, house_code: str = "", 
                  building_code: str = "", address: str = ""):
        """添加房屋信息"""
        self.house_data.append({
            "楼栋": building,
            "单元": unit,
            "楼层": floor,
            "房号": room,
            "房屋编码(25位)": house_code,
            "楼栋编码(19位)": building_code,
            "详细地址": address
        })
    
    def load_from_csv(self, filepath: str):
        """从CSV文件加载数据"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.house_data = list(reader)
            print(f"成功加载 {len(self.house_data)} 条记录")
        except Exception as e:
            print(f"加载文件失败: {e}")
    
    def save_to_csv(self, filepath: str):
        """保存到CSV文件"""
        if not self.house_data:
            print("没有数据可保存")
            return
        
        try:
            with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
                fieldnames = ["楼栋", "单元", "楼层", "房号", 
                              "房屋编码(25位)", "楼栋编码(19位)", "详细地址"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.house_data)
            print(f"成功保存 {len(self.house_data)} 条记录到 {filepath}")
        except Exception as e:
            print(f"保存文件失败: {e}")
    
    def save_to_json(self, filepath: str):
        """保存到JSON文件"""
        if not self.house_data:
            print("没有数据可保存")
            return
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.house_data, f, ensure_ascii=False, indent=2)
            print(f"成功保存 {len(self.house_data)} 条记录到 {filepath}")
        except Exception as e:
            print(f"保存文件失败: {e}")
    
    def display_table(self):
        """以表格形式显示数据"""
        if not self.house_data:
            print("没有数据")
            return
        
        # 打印表头
        print("=" * 120)
        print(f"{'楼栋':<8} {'单元':<6} {'楼层':<6} {'房号':<8} {'房屋编码(25位)':<20} {'楼栋编码(19位)':<20} {'详细地址'}")
        print("=" * 120)
        
        # 打印数据
        for house in self.house_data:
            print(f"{house.get('楼栋', ''):<8} {house.get('单元', ''):<6} {house.get('楼层', ''):<6} "
                  f"{house.get('房号', ''):<8} {house.get('房屋编码(25位)', ''):<20} "
                  f"{house.get('楼栋编码(19位)', ''):<20} {house.get('详细地址', '')}")
        print("=" * 120)
        print(f"总计: {len(self.house_data)} 条记录")


def main():
    manager = HouseCodeManager()
    
    print("=" * 60)
    print("龙华滢水山庄1区房屋编码管理工具")
    print("=" * 60)
    
    # 添加滢水山庄一区示例数据结构
    print("\n正在创建滢水山庄一区房屋编码表格模板...")
    
    # 滢水山庄一区约有28栋楼，我们创建一个示例模板
    for building in range(1, 29):
        # 假设每栋有多个单元和楼层
        for unit in ["1单元", "2单元", "3单元"]:
            for floor in range(1, 9):  # 假设每栋8层
                for room in ["101", "102", "201", "202", "301", "302", 
                             "401", "402", "501", "502", "601", "602",
                             "701", "702", "801", "802"]:
                    if int(room[:-2]) == floor:
                        manager.add_house(
                            building=f"{building}栋",
                            unit=unit,
                            floor=f"{floor}楼",
                            room=room,
                            address=f"龙华区滢水山庄一区{building}栋{unit}{floor}楼{room}"
                        )
    
    # 保存为CSV文件
    manager.save_to_csv("/workspace/滢水山庄一区房屋编码表.csv")
    manager.save_to_json("/workspace/滢水山庄一区房屋编码表.json")
    
    print("\n表格模板已创建！请按照以下步骤填写：")
    print("1. 打开 滢水山庄一区房屋编码表.csv")
    print("2. 访问 https://spatydz.sz.gov.cn/web/index.html#/ 查询真实编码")
    print("3. 将查询到的房屋编码填入对应位置")
    print("\n提示：您也可以通过门上二维码或咨询社区网格员获取房屋编码")


if __name__ == "__main__":
    main()
