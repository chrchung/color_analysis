import plotly.tools as tls
tls.set_credentials_file(username='ChristinaChung', api_key='9Qz7ub7MJHtBqdy6N6OX')
import plotly.plotly as py
import plotly.graph_objs as go


from numpy import array
from scipy import stats

decades = ['1800_1810', '1810_1820', '1820_1830', '1830_1840', '1840_1850', '1850_1860', '1860_1870', '1870_1880', '1880_1890', '1890_1900']
color_mentions = {"1840_1850": 99329, "1820_1830": 51872, "1850_1860": 105507, "1830_1840": 70965, "1890_1900": 87465, "1870_1880": 114312, "1810_1820": 20153, "1800_1810": 10167, "1880_1890": 137015, "1860_1870": 132651}
word_count = {"1880_1890": 4051207, "1800_1810": 553674, "1830_1840": 2051914, "1820_1830": 1606372, "1860_1870": 3718481, "1810_1820": 862606, "1870_1880": 3271786, "1840_1850": 2675601, "1890_1900": 2787196, "1850_1860": 3041237}

normalized = []
col = []
word = []

for decade in decades:
    normalized.append(color_mentions[decade]/word_count[decade])
    word.append(word_count[decade])
    col.append(color_mentions[decade])

trace = go.Scatter(
    x =  ['1800', '1810', '1820', '1830', '1840', '1850', '1860', '1870', '1880', '1890', '1900'],
    y = col
)

trace2 = go.Scatter(
    x =  ['1800','1810', '1820', '1830', '1840', '1850', '1860', '1870', '1880', '1890', '1900'],
    y = word
)

trace3 = go.Scatter(
    x =  ['1800', '1810', '1820', '1830', '1840', '1850', '1860', '1870', '1880', '1890', '1900'],
    y = normalized,
    name = 'color mentions normalized'
)


# linear regression
d = array([1800, 1810, 1820, 1830, 1840, 1850, 1860, 1870, 1880, 1890])
slope, intercept, r_value, p_value, std_err = stats.linregress(d, normalized)
line = slope*d+intercept

trace4 = go.Scatter (
    x = ['1800', '1810', '1820', '1830', '1840', '1850', '1860', '1870', '1880', '1890', '1900'],
    y = line,
    name = 'line of best fit'

)


data = [trace]

layout = dict(title = 'Number of Color Mentions per Decade',
              xaxis = dict(title = 'Decade'),
              yaxis = dict(title = 'Number of Color Mentions'),
              )

fig = dict(data=data, layout=layout)

py.iplot(fig, filename='basic-line')
