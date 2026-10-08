#!/bin/zsh
set -e
cd "$(dirname "$0")"
print '肩部三维学习：http://127.0.0.1:5178/'
print '请在浏览器打开上方地址。关闭此窗口或按 Control+C 可停止。'
/usr/bin/python3 -m http.server 5178 --bind 127.0.0.1 --directory dist
