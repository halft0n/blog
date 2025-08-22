#!/usr/bin/env python3
import os
import sys

def has_readme(directory):
    """检查目录及其子目录是否包含README.md文件"""
    try:
        for root, dirs, files in os.walk(directory):
            if "README.md" in files:
                return True
        return False
    except PermissionError:
        return False

def generate_toc(base_path=".", indent_level=0):
    """递归遍历目录，生成层次化目录"""
    toc = []
    indent = "  " * indent_level
    
    # 获取当前目录下的所有文件和文件夹
    try:
        items = sorted(os.listdir(base_path))
    except PermissionError:
        return []
    
    # 分离文件和目录
    dirs = []
    
    for item in items:
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            dirs.append(item)
    
    # 处理子目录
    for dir_name in dirs:
        dir_path = os.path.join(base_path, dir_name)
        
        # 检查目录及其子目录是否包含README.md
        if has_readme(dir_path):
            # 检查当前目录是否有README.md
            readme_path = os.path.join(dir_path, "README.md")
            if os.path.exists(readme_path):
                # 获取相对路径用于链接
                relative_path = os.path.relpath(readme_path, ".")
                toc.append(f"{indent}- [{dir_name}]({relative_path})")
            else:
                # 如果当前目录没有README.md，但子目录有，则只显示目录名（不带斜杠）
                toc.append(f"{indent}- {dir_name}")
            
            # 递归处理子目录
            sub_toc = generate_toc(dir_path, indent_level + 1)
            if sub_toc:
                toc.extend(sub_toc)
    
    return toc

def main():
    """主函数"""
    # 确保在项目根目录运行
    doc_path = "./doc"
    
    if not os.path.exists(doc_path):
        print(f"错误: 找不到目录 {doc_path}", file=sys.stderr)
        sys.exit(1)
    
    # 生成目录
    toc = generate_toc(doc_path)
    
    # 输出目录
    print("# 目录")
    print()
    for line in toc:
        print(line)

if __name__ == "__main__":
    main()