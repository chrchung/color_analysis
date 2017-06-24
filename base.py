import sqlite3
import csv

#change[primID] = correct base color
change = {}
with open('A:/color_analysis/base.csv', 'rb') as inp, open('A:/color_analysis/base_edit.csv', 'wb') as out:
    basereader = csv.reader(inp, delimiter=' ', quotechar='|')
    writer = csv.writer(out)
    mark = False
    for row in csv.reader(inp):
        #null val, get base col from next row
        if row[1] == 'NULL':
            mark = True
            id = row[2]
            continue
        
        if mark:
            change[id] = row[2]
            mark = False
        #write non-duplicate rows to new csv
        writer.writerow(row)
        

conn = sqlite3.connect('color_analysis_merged.db')
c = conn.cursor()
#now change the base colors in the mention table
for item in change:
    c.execute("update mention set color=:new_col where color=:old_col", {"old_col": item, "new_col": change[item]})
    
conn.commit()
c.close()
    
