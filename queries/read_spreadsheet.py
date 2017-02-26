import json

def parse_color_list(f):
    res = []
    with open(f, 'r') as f:
        for row in f:
            row = row.strip('\n')
            res.append(row) 

    f.close()
    return res

f = open('../query_results/spreadsheet_clause.txt', 'r').read()
res = json.loads(f)
f2 = open('../query_results/spreadsheet_clause2.csv', 'w')

m = 0
c = 1000
avg = 0
count = 0
for color in res:
    rat = color['p']
    avg += sum(rat)
    count += len(rat)

    m = min(rat) if min(rat) > m else m
    c = max(rat) if max(rat) > c else c

##
##f2.write("""0-5 worded sentences,6-15,16-25,26-35,36-45,46-65,66-85,85+
##4543834,7844831,5138259,3111529, 1764319.9999999998,1636397,461570,265583 \n
##name, total occur,expected occur 0-5,actual occur 0-5,ratio 0-5,p-value 0-5,expected occur 6-15,actual occur 6-15,ratio 6-15,p-value 6-15,expected occur 16-25,actual occur 16-25,ratio 16-25,p-value 16-25,expected occur 26-35,actual occur 26-35,ratio 26-35, p-value 26-35,expected occur 36-45,actual occur 36-45,ratio 36-45,p-value 36-45,expected occur 46-65,actual occur 46-65,ratio 46-65,p-value 46-65,expected occur 66-85,actual occur 66-85,ratio 66-85,p-value 66-85,expected occur 85+,actual occur 85+,ratio 85+,p-value 85+,""")
##
##for color in res:
##    f2.write(color['name'] + ',')
##    f2.write(str(color['occur']) + ',')
##    for i in range(0, 8):
##        f2.write(str(round(color['expected'][i], 2)) + ',')
##        f2.write(str(round(color['actual'][i], 2)) + ',')
##        f2.write(str(round(color['ratio'][i], 2)) + ',')
##        f2.write(str(round(color['p'][i], 2)) + ',')
##
##    f2.write("\n")
##
##
##f2.close()
##f2.close()


# sent: avg = 0.16, m = 0.99, min = 0.24388898251660351
