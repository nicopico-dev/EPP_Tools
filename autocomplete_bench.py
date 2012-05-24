# -*- coding: latin-1 -*-
# Autocomplete benchmarking
#    bonjour
#  bonsoir
#     allo?
#    bonsoir  
import cProfile
import pstats
from pprint import pprint

import autocomplete
import epp_utils as epp

# On se positionne après 'bonj' sur la 3e ligne -> ['bonjour']
args = ['-f', 'E:\\_Portable_Apps\\PortableApps\\EditPadPro\\Tools\\autocomplete_bench.py', '-l', '3', '-c', '65']
cProfile.run('autocomplete.main(args)', 'c:\\acprof_1')

# On se positionne après 'bon' sur la 3e ligne -> ['bonjour', 'bonsoir']
args = ['-f', 'E:\\_Portable_Apps\\PortableApps\\EditPadPro\\Tools\\autocomplete_bench.py', '-l', '3', '-c', '64']
cProfile.run('autocomplete.main(args)', 'c:\\acprof_2')


print("==================  UNIQUE  ==================")
p1 = pstats.Stats('c:\\acprof_1')
p1.strip_dirs()
p1.sort_stats('cumulative', 'time', 'calls')
p1.print_stats('.1')

print("")
print("==================  CHOIX  ===================")
p2 = pstats.Stats('c:\\acprof_2')
p2.strip_dirs()
p2.sort_stats('cumulative', 'time', 'calls')
p2.print_stats('.1')