@echo off
echo ========================================
echo Building MazeGame Executable
echo ========================================
echo.

REM 检查 PyInstaller 是否已安装
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    echo.
)

REM 清理旧的构建文件
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "main.spec" del main.spec

REM 使用 PyInstaller 打包
echo Building executable...
pyinstaller --onefile ^
    --name MazeGame ^
    --add-data "config.yaml;." ^
    --add-data "src;src" ^
    --hidden-import yaml ^
    --hidden-import pathlib ^
    --hidden-import collections ^
    --console ^
    main.py

if errorlevel 1 (
    echo.
    echo Build failed!
    pause
    exit /b 1
)

REM 复制配置文件到 dist 目录
echo.
echo Copying configuration files...
copy config.yaml dist\config.yaml

REM 创建 res 目录
if not exist "dist\res" mkdir dist\res

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Executable location: dist\MazeGame.exe
echo.
echo To run the executable:
echo   1. Navigate to the dist folder
echo   2. Edit config.yaml to customize settings
echo   3. Run MazeGame.exe
echo.
pause
