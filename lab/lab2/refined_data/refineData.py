file_names[] = {"eclipse_bugs_1.csv"
                '''
                "eclipse_bugs_10000.csv",
                "eclipse_bugs_100000.csv",
                "eclipse_bugs_110000.csv",
                "eclipse_bugs_120000.csv",
                "eclipse_bugs_130000.csv",
                "eclipse_bugs_140000.csv",
                "eclipse_bugs_150000.csv",
                "eclipse_bugs_160000.csv",
                "eclipse_bugs_170000.csv",
                "eclipse_bugs_180000.csv",
                "eclipse_bugs_190000.csv",
                "eclipse_bugs_20000.csv",
                "eclipse_bugs_200000.csv",
                "eclipse_bugs_210000.csv",
                "eclipse_bugs_220000.csv",
                "eclipse_bugs_230000.csv",
                "eclipse_bugs_240000.csv",
                "eclipse_bugs_250000.csv",
                "eclipse_bugs_260000.csv",
                "eclipse_bugs_270000.csv",
                "eclipse_bugs_280000.csv",
                "eclipse_bugs_290000.csv",
                "eclipse_bugs_30000.csv",
                "eclipse_bugs_300000.csv",
                "eclipse_bugs_310000.csv",
                "eclipse_bugs_320000.csv",
                "eclipse_bugs_330000.csv",
                "eclipse_bugs_340000.csv",
                "eclipse_bugs_350000.csv",
                "eclipse_bugs_360000.csv",
                "eclipse_bugs_370000.csv",
                "eclipse_bugs_380000.csv",
                "eclipse_bugs_390000.csv",
                "eclipse_bugs_40000.csv",
                "eclipse_bugs_400000.csv",
                "eclipse_bugs_410000.csv",
                "eclipse_bugs_420000.csv",
                "eclipse_bugs_430000.csv",
                "eclipse_bugs_440000.csv",
                "eclipse_bugs_450000.csv",
                "eclipse_bugs_460000.csv",
                "eclipse_bugs_470000.csv",
                "eclipse_bugs_480000.csv",
                "eclipse_bugs_490000.csv",
                "eclipse_bugs_50000.csv",
                "eclipse_bugs_500000.csv",
                "eclipse_bugs_510000.csv",
                "eclipse_bugs_520000.csv",
                "eclipse_bugs_530000.csv",
                "eclipse_bugs_540000.csv",
                "eclipse_bugs_550000.csv",
                "eclipse_bugs_60000.csv",
                "eclipse_bugs_70000.csv",
                "eclipse_bugs_80000.csv",
                "eclipse_bugs_90000.csv"
                '''
                }

for file_name in file_names:
    file_in = open(file_name)
    lines = file_in.read().splitlines()

for line in lines:
    print(line + '\n')
    
