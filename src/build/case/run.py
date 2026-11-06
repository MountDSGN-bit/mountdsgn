import sys, importlib
sys.path.insert(0,'/home/claude/build/case')
import casefx
for s in sys.argv[1:]:
    casefx.build(s, importlib.import_module('data_'+s).D); print('built',s)
