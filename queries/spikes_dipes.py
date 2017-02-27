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

def get_dramatic(delta):
    res = []
    slopes = [delta[color] for color in delta]
    p = percentile(slopes, 95)

    for color in delta:
        if delta[color] >= p:
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
    inc[color] = -2000
    dec[color] = 2000

    for decade in range(0, len(decades) - 1):
        val = mentions[decades[decade]][color] / wc[decades[decade]]
        val2 = mentions[decades[decade + 1]][color] / wc[decades[decade]]

        res = val2 - val

        if res > 0:
            inc[color] = res if inc[color] < res else inc[color]
        elif res < 0:
            dec[color] = res if dec[color] > res else dec[color]            

print(len(inc))
print(len(dec))

incs = get_dramatic(inc)
decs = get_dramatic(dec)

plot_dramatic(mentions, incs, decades, wc, 'Colors with Dramatic Spikes')
plot_dramatic(mentions, decs, decades, wc, 'Color with Dramatic Dips')


f = open('../query_results/dramatic_inc.txt', 'w')
f.write(json.dumps(inc))
f.close()

f = open('../query_results/dramatic_dec.txt', 'w')
f.write(json.dumps(dec))
f.close()





