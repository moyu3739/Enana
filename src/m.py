# 记录导入前的模块
import sys
before_modules = set(sys.modules.keys())

# 导入你想检查的包
import main  # 替换为你要检查的包

# 查看导入后的新增模块
after_modules = set(sys.modules.keys())
new_modules = after_modules - before_modules

print("导入的模块:")
for module in sorted(new_modules):
    print(f"- {module}")