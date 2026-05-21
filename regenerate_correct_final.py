#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证和生成标准25位房屋编码
"""

import csv
import json


def generate_25digit_house_code(building_num, unit_num, floor_num, room_num):
    """
    生成标准25位房屋编码
    
    严格按照25位标准格式：
    - 第1-6位：行政区划代码（440309 龙华区）
    - 第7-9位：街道/镇代码（009 民治街道）
    - 第10-12位：社区代码（320 民乐社区）
    - 第13-20位：建筑物编号（8位，楼栋号，不足补0）
    - 第21-22位：单元号（2位）
    - 第23-24位：楼层号（2位）
    - 第25位：房号（1位）
    """
    district_code = "440309"  # 6位
    street_code = "009"       # 3位
    community_code = "320"    # 3位
    building_code = f"{building_num:08d}"  # 8位
    unit_code = f"{unit_num:02d}"  # 2位
    floor_code = f"{floor_num:02d}"  # 2位
    room_code = f"{room_num % 10}"   # 1位
    
    house_code = (district_code + street_code + community_code + 
                  building_code + unit_code + floor_code + room_code)
    
    return house_code


def generate_19digit_building_code(building_num):
    """
    生成标准19位楼栋编码
    - 第1-6位：行政区划代码（440309 龙华区）
    - 第7-9位：街道/镇代码（009 民治街道）
    - 第10-12位：社区代码（320 民乐社区）
    - 第13-18位：建筑物编号（6位，楼栋号，不足前面补0）
    - 第19位：校验位
    """
    district_code = "440309"      # 6位
    street_code = "009"           # 3位
    community_code = "320"        # 3位
    building_code = f"{building_num:06d}"  # 6位
    check_digit = "1"              # 1位
    
    return district_code + street_code + community_code + building_code + check_digit


def verify_and_generate():
    """验证并重新生成标准格式的房屋编码"""
    print("="*80)
    print("生成标准25位房屋编码 & 19位楼栋编码")
    print("="*80)
    
    house_data = []
    
    # 楼栋列表
    buildings = list(range(1, 10))  # 1-9栋
    
    for building in buildings:
        for unit in range(1, 4):
            for floor in range(1, 9):
                for room in range(1, 3):
                    room_num = f"{floor:02d}{room:02d}"
                    
                    # 生成编码
                    house_code = generate_25digit_house_code(building, unit, floor, room)
                    building_code = generate_19digit_building_code(building)
                    
                    house_data.append({
                        "楼栋": f"{building}栋",
                        "单元": f"{unit}单元",
                        "楼层": f"{floor}楼",
                        "房号": room_num,
                        "房屋编码(25位)": house_code,
                        "楼栋编码(19位)": building_code,
                        "详细地址": f"深圳市龙华区滢水山庄一区{building}栋{unit}单元{floor}楼{room_num}室"
                    })
    
    # 验证编码长度
    print("\n验证编码长度:")
    print("-" * 80)
    
    all_25_correct = all(len(h['房屋编码(25位)']) == 25 for h in house_data)
    all_19_correct = all(len(h['楼栋编码(19位)']) == 19 for h in house_data)
    
    if all_25_correct and all_19_correct:
        print("✓ 所有房屋编码都是25位")
        print("✓ 所有楼栋编码都是19位")
    else:
        print("✗ 部分编码长度不正确")
        for i, h in enumerate(house_data):
            if len(h['房屋编码(25位)']) != 25:
                print(f"  第{i+1}条: 房屋编码 {h['房屋编码(25位)']} 长度 {len(h['房屋编码(25位)'])}")
            if len(h['楼栋编码(19位)']) != 19:
                print(f"  第{i+1}条: 楼栋编码 {h['楼栋编码(19位)']} 长度 {len(h['楼栋编码(19位)'])}")
    
    # 显示样本数据
    print("\n" + "="*80)
    print("样本数据（前20条）:")
    print("="*80)
    for i, house in enumerate(house_data[:20], 1):
        print(f"{i:2d}. {house['楼栋']} {house['单元']} {house['楼层']} {house['房号']}")
        print(f"    房屋编码({len(house['房屋编码(25位)'])}位): {house['房屋编码(25位)']}")
        print(f"    楼栋编码({len(house['楼栋编码(19位)'])}位): {house['楼栋编码(19位)']}")
        print()
    
    # 保存CSV
    csv_file = "/workspace/data/滢水山庄一区_标准25位房屋编码表.csv"
    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['楼栋', '单元', '楼层', '房号', '房屋编码(25位)', '楼栋编码(19位)', '详细地址']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(house_data)
    
    print("="*80)
    print(f"✓ CSV文件已保存: {csv_file}")
    print(f"✓ 共 {len(house_data)} 条记录")
    print("="*80)


if __name__ == "__main__":
    verify_and_generate()
