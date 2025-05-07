@echo off
echo ========================================
echo         优化样本选择系统打包工具
echo ========================================
echo.

rem 设置编码为UTF-8
chcp 65001 > nul

echo [1/5] 安装必要的Python依赖...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo [2/5] 清理之前的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo [3/5] 准备数据库文件...
if not exist ai_project.db (
    echo 创建空的数据库文件...
    type nul > ai_project.db
)

echo.
echo [4/5] 开始打包应用程序...
pyinstaller --clean app.spec

echo.
echo [5/5] 检查打包结果...
if exist dist\Optimal_Samples_Selection.exe (
    echo ========================================
    echo 打包成功完成！
    echo 可执行文件位于: dist\Optimal_Samples_Selection.exe
    echo ========================================
) else (
    echo ========================================
    echo 打包失败！请检查错误信息。
    echo ========================================
)

echo.
echo 按任意键退出...
pause > nul 