import sys
from cx_Freeze import setup, Executable

base = None

include=["common","Enemy","EnemyBullet","items","SElibrary","imglibrary"]

if sys.platform == "win32": base = "Win32GUI"
# CUIの場合はこのif文をコメントアウトしてください。

exe = Executable(script="main.py", base=base)
# "main.py"にはpygameを用いて作成したファイルの名前を入れてください。

setup(name='KosukeAtsumi',
      version='0.1',
      options = {"build_exe": {"includes": include}},
      description='danmaku',
      executables=[exe])

# 'your_filename'は好みの名前でどうぞ。
