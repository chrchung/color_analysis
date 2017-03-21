import json
import numpy as np
from sklearn.decomposition import PCA
import plotly.tools as tls
tls.set_credentials_file(username='ChristinaChung', api_key='9Qz7ub7MJHtBqdy6N6OX')
import plotly.plotly as py
import plotly.graph_objs as go
from sklearn.preprocessing import StandardScaler

def parse_color_list(f):
    res = []
    with open(f, 'r') as f:
        for row in f:
            row = row.strip('\n')
            res.append(row) 

    f.close()
    return res

def get_o(ob, name):
    for o in ob:
        if o['name'] == name:
            return o
height = json.loads(open('../query_results/distinctive_heights.json', 'r').read())
periodicity = json.loads(open('../query_results/distinctive_periods.json', 'r').read())
clause = json.loads(open('../query_results/clause_dep.json', 'r').read())

co = parse_color_list('../query_results/thresholded.txt')

num_comp = 0
num_comp += len(height[0]['actual'])
num_comp += len(periodicity[0]['actual'])
num_comp += len(clause[0]['actual'])

ar = [[] for x in range(0, num_comp)]

for color in co:
    i = 0
    a = get_o(height, color)['p']
    for comp in a:
        ar[i].append(comp)
        i+=1
        
    b = get_o(periodicity, color)['p']
    for comp in b:
        ar[i].append(comp)
        i+=1
        
    c = get_o(clause, color)['p']
    for comp in c:
        ar[i].append(comp)
        i+=1
    
f = open('../query_results/pca.json', 'w')
f.write(json.dumps(ar))
f.close()

#pca components
X1 = np.array(ar)
X = StandardScaler().fit_transform(X1)
pca = PCA(n_components=2)
pca.fit(X)
pca_res = list(pca.components_)

#eigenvectors
centered_matrix = X1 - X1.mean(axis=1)[:, np.newaxis]
cov = np.dot(centered_matrix, centered_matrix.T)
eigvals, eigvecs = np.linalg.eig(cov)

trace = go.Scatter(
    x = pca_res[0],
    y = pca_res[1],
    mode='text',
    name='Principal Component Analysis on All (all values)',
    text=co,
    textposition='bottom'
    )

data = [trace]

trace = go.Scatter(
    x =
    y =
    mode='text+lines'
    text = col
)




py.iplot(data, filename='PCA')

