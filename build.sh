#!/bin/bash
echo "开始打包优化样本选择系统..."

# 安装所需依赖
pip install pyinstaller flask

# 清理之前的构建文件
rm -rf build dist

# 执行打包
pyinstaller --clean app.spec

echo "打包完成！"
echo "可执行文件位于 dist/Optimal_Samples_Selection" 