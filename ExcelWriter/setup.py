from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = ['ast','re','random','sys','os','argparse','shlex','importlib','xlrd','xlutils.copy','faker'], excludes = [])

base = 'Console'

executables = [
    Executable('main.py', base=base, targetName = 'ExcelWriter.exe')
]

setup(name='ExcelWriter',
      version = '1.0',
      description = 'ExcelWriter',
      options = dict(build_exe = buildOptions),
      executables = executables)
