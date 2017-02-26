import plotly.tools as tls
tls.set_credentials_file(username='ChristinaChung', api_key='9Qz7ub7MJHtBqdy6N6OX')
import plotly.plotly as py
import plotly.graph_objs as go
from numpy import array, percentile
from scipy import stats
import json

def parse_color_list():
    res = []
    with open('../query_results/thresholded.txt', 'r') as f:
        for row in f:
            row = row.strip('\n')
            res.append(row) 

    f.close()
    return res

def get_dramatic(lobf):
    res = []
    slopes = [lobf[color]['slope'] for color in lobf]
    p = percentile(slopes, 90)

    for color in lobf:
        if lobf[color]['slope'] >= p:
            res.append(color)

    return res

def plot_dramatic(mentions, co, decades, wc, tit):
    data = []
    for color in co:
        vals = [mentions[decade][color]/wc[decade] if color in mentions[decade].keys() else 0 for decade in decades]

        trace = go.Scatter(
            x =  ['1800', '1810', '1820', '1830', '1840', '1850', '1860', '1870', '1880', '1890', '1900'],
            y = vals,
            name = color
        )


        data.append(trace)   

    layout = dict(title = tit,
                  xaxis = dict(title = 'Decade'),
                  yaxis = dict(title = 'Number of Mentions'),
                  )

    fig = dict(data=data, layout=layout)

    py.iplot(fig, filename=tit)

decades = ['1800_1810', '1810_1820', '1820_1830', '1830_1840', '1840_1850', '1850_1860', '1860_1870', '1870_1880', '1880_1890', '1890_1900']
d = array([1800, 1810, 1820, 1830, 1840, 1850, 1860, 1870, 1880, 1890])
mentions = json.loads(open('../query_results/indiv_color_mention_per_decade.txt', 'r').read())
co = parse_color_list()
wc = json.loads(open('../query_results/word_count_per_decade.txt', 'r').read())

inc = {}
dec = {}

for color in co:
    a = []
    for decade in decades:
        if color in mentions[decade].keys():
            a.append(mentions[decade][color])
        else:
            a.append(0)
            
    slope, intercept, r_value, p_value, std_err = stats.linregress(d, a)
    line = slope*d+intercept

    if (slope >= 0):
        inc[color] = {'slope': slope, 'intercept': intercept}
 
    if (slope <= 0):
        dec[color] = {'slope': abs(slope), 'intercept': intercept}

print(len(inc))
print(len(dec))

inc = get_dramatic(inc)
dec = get_dramatic(dec)

plot_dramatic(mentions, inc, decades, wc, 'Most Dramatic Colors (Increasing)')
plot_dramatic(mentions, dec, decades, wc, 'Most Dramatic Colors (Decreasing)')


f = open('../query_results/dramatic_inc.txt', 'w')
f.write(json.dumps(inc))
f.close()

f = open('../query_results/dramatic_dec.txt', 'w')
f.write(json.dumps(dec))
f.close()





