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
mentions = json.loads(open('../query_results/indiv_color_mention_per_decade.txt', 'r').read())
co = parse_color_list()
wc = json.loads(open('../query_results/word_count_per_decade.txt', 'r').read())

res_inc = {}
res_dec = {}

for decade in range(0, len(decades) - 1):
    res_inc[decades[decade]] = {}
    res_dec[decades[decade]] = {}

    for color in co:
        val = mentions[decades[decade]][color] / wc[decades[decade]]
        val2 = mentions[decades[decade + 1]][color] / wc[decades[decade]]

        res = val2 - val

        if res > 0:
            res_inc[decades[decade]][color] = res 
        elif res < 0:
            res_dec[decades[decade]][color] = abs(res)
        else:
            res_inc[decades[decade]][color] = res 
            res_inc[decades[decade]][color] = res 



for decade in range(0, len(decades) - 1):
    incs = get_dramatic(res_inc[decades[decade]])
    decs = get_dramatic(res_dec[decades[decade]])

    plot_dramatic(mentions, incs, decades, wc, 'Colors with Dramatic Spikes between ' + decades[decade] + ' and ' + decades[decade + 1])
    plot_dramatic(mentions, decs, decades, wc, 'Color with Dramatic Dips between ' + decades[decade] + ' and ' + decades[decade + 1])


