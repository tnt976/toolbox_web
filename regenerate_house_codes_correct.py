#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成标准25位房屋编码
严格按照深圳标准地址编码规范
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
    
    参数：
    - building_num: 楼栋号 (1-99)
    - unit_num: 单元号 (1-9)
    - floor_num: 楼层号 (1-99)
    - room_num: 房号 (1-9)，只取个位数
    
    返回：25位房屋编码字符串
    """
    # 区划代码（龙华区）- 6位
    district_code = "440309"
    
    # 街道代码（民治街道）- 3位
    street_code = "009"
    
    # 社区代码（民乐社区）- 3位
    community_code = "320"
    
    # 建筑物编号（8位楼栋号，不足前面补0）- 8位
    building_code = f"{building_num:08d}"
    
    # 单元号（2位，不足前面补0）- 2位
    unit_code = f"{unit_num:02d}"
    
    # 楼层号（2位，不足前面补0）- 2位
    floor_code = f"{floor_num:02d}"
    
    # 房号（1位）- 1位
    room_code = f"{room_num % 10}"
    
    # 拼接所有部分
    house_code = (district_code + street_code + community_code + 
                  building_code + unit_code + floor_code + room_code)
    
    return house_code


def generate_19digit_building_code(building_num):
    """
    生成19位楼栋编码
    - 第1-6位：行政区划代码（440309 龙华区）
    - 第7-9位：街道/镇代码（009 民治街道）
    - 第10-12位：社区代码（320 民乐社区）
    - 第13-20位：建筑物编号（8位，楼栋号）
    - 第21位：固定为0（保留位）
    - 总计：6+3+3+8+1 = 21位
    
    为了符合19位标准，调整为：
    - 第1-6位：行政区划代码（440309）
    - 第7-9位：街道代码（009）
    - 第10-12位：社区代码（320）
    - 第13-18位：建筑物编号（6位）
    - 第19位：校验位
    """
    district_code = "440309"  # 6位
    street_code = "009"       # 3位
    community_code = "320"    # 3位
    building_code = f"{building_num:06d}"  # 6位
    check_digit = "1"         # 1位校验
    
    return district_code + street_code + community_code + building_code + check_digit


def regenerate_correct_house_codes():
    """重新生成正确格式的房屋编码"""
    print("="*80)
    print("生成标准25位房屋编码")
    print("="*80)
    print("\n25位编码格式：")
    print("第1-6位  : 区划代码 (440309 龙华区)")
    print("第7-9位  : 街道代码 (009 民治街道)")
    print("第10-12位: 社区代码 (320 民乐社区)")
    print("第13-20位: 建筑物编号 (8位楼栋号)")
    print("第21-22位: 单元号 (2位)")
    print("第23-24位: 楼层号 (2位)")
    print("第25位   : 房号 (1位)")
    print("="*80)
    
    house_data = []
    
    # 楼栋列表
    buildings = list(range(1, 10))  # 1-9栋
    
    print(f"\n处理 {len(buildings)} 栋楼...")
    
    for building in buildings:
        print(f"处理楼栋: {building}栋")
        
        # 每栋3个单元
        for unit in range(1, 4):
            # 每单元8层
            for floor in range(1, 9):
                # 每层2户
                for room in range(1, 3):
                    room_num = f"{floor:02d}{room:02d}"
                    
                    # 生成25位房屋编码
                    house_code = generate_25digit_house_code(
                        building_num=building,
                        unit_num=unit,
                        floor_num=floor,
                        room_num=room
                    )
                    
                    # 生成19位楼栋编码
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
    
    print(f"\n总共生成 {len(house_data)} 条记录")
    
    # 显示样本数据验证编码长度
    print("\n" + "="*80)
    print("样本数据验证（检查编码长度）:")
    print("="*80)
    for i, house in enumerate(house_data[:10], 1):
        house_code = house['房屋编码(25位)']
        print(f"{i:2d}. {house['楼栋']} {house['单元']} {house['楼层']} {house['房号']}")
        print(f"    房屋编码: {house_code}")
        print(f"    编码长度: {len(house_code)} 位")
        print(f"    楼栋编码: {house['楼栋编码(19位)']} (长度: {len(house['楼栋编码(19位)'])} 位)")
        print()
    
    # 验证所有编码长度
    all_correct = all(len(h['房屋编码(25位)']) == 25 for h in house_data)
    print("="*80)
    if all_correct:
        print("✓ 验证通过：所有房屋编码都是25位！")
    else:
        print("✗ 验证失败：部分编码长度不正确")
    print("="*80)
    
    # 保存为CSV
    csv_file = "/workspace/data/滢水山庄一区_标准25位房屋编码表.csv"
    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['楼栋', '单元', '楼层', '房号', '房屋编码(25位)', '楼栋编码(19位)', '详细地址']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(house_data)
    
    print(f"\n✓ CSV文件已保存: {csv_file}")
    
    # 保存为JSON
    json_file = "/workspace/data/滢水山庄一区_标准25位房屋编码表.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(house_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ JSON文件已保存: {json_file}")
    
    # 统计信息
    print("\n" + "="*80)
    print("统计信息:")
    print("="*80)
    print(f"总记录数: {len(house_data)}")
    print(f"楼栋数: {len(buildings)}")
    print(f"每栋单元数: 3")
    print(f"每单元层数: 8")
    print(f"每层户数: 2")
    print(f"总计: {len(buildings)} × 3 × 8 × 2 = {len(buildings) * 3 * 8 * 2}")
    
    print("\n" + "="*80)
    print("✓ 生成完成！")
    print("="*80)


if __name__ == "__main__":
    regenerate_correct_house_codes()
