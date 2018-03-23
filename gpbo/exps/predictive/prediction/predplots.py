import numpy as np
import scipy as sp
from matplotlib import pyplot as plt
import prediction

import sys
import os
from gpbo import datapath
import pickle
print(sys.executable)
basevar=1e-4
basenum=100.

Lsupport = sp.stats.gamma.ppf(np.linspace(0,1,202)[1:-1],4.,scale = 0.2)
Lprior = np.ones_like(Lsupport)/float(Lsupport.size)
#Lsupport = np.linspace(0.05,1.25,25)
#Lprior = sp.stats.gamma.pdf(Lsupport,4.,scale=0.2)
#Lprior = Lprior/np.sum(Lprior)
B = np.array([1.,1.,1.])*3600
A = np.array([1e-2,1e-4,1e-6])*36.
R=[]
fig,axA = plt.subplots(nrows=len(B),ncols=2,sharex=True,figsize=(12,9))
axt = axA[:,1]
ax = axA[:,0]

for i in range(len(B)):
    b = B[i]
    #cfncoef = b*basevar/basenum
    cfn = lambda v: A[i]/v
    ax[i].set_title('$B = {} $, $c(\sigma)= {:.3g} /\\sigma^2$'.format(b,A[i]))
    r = prediction.optatBcfoverL(b,cfn,Lsupport,Lprior,ax=ax[i],axt=axt[i],bnds=(-6,-1))
    ax[i].set_xscale('log')
    ax[i].set_yscale('log')
    R.append(r)


#################
ind = [[0,1,2],[1,1,4],[2,1,6]]
for e in ind:
    V,R,TR = pickle.load(open(os.path.join(datapath,'exps/predictive/prediction/scenarios/results_{}h_v{}/cache/out.p'.format(e[1],e[2])),'r'))
    ax[e[0]].plot(V,R,'g',label='Observed mean regret')
    am = np.argmin(R)
    ax[e[0]].plot(V[am],R[am],'go')
    axt[e[0]].plot(V,TR,'g',label='Observed overhead fraction')
    axt[e[0]].plot(V[am],TR[am],'go')
#################

ax[0].legend(loc='lower left')
axt[0].legend(loc='upper left')
ax[-1].set_xlabel('Observartion Variance')
axt[-1].set_xlabel('Observartion Variance')
fig.text(0.05, 0.5, 'Regret', ha='center', va='center', rotation='vertical')
fig.text(0.95, 0.5, 'Overhead Fraction', ha='center', va='center', rotation='vertical')
ax[0].set_xlim(1e-6,1e-1)

fig.savefig('figs/margpredictions.pdf')
#print('header\n')
#for i in range(len(B)):
#    s = "{:.3g} & $ \\frac{{ {:.3g} }}{{\\sigma^2}}$ & {:.3g} & {:.3g} & {:.3g} & {:.3g} \\\\".format(B[i],B[i]*basevar/basenum, R[i]['obsvar'],R[i]['Esteps'],R[i]['Rmean'],R[i]['Eover']/B[i])
#    print(s)
#
#B = np.array([1.,2.])*3600
#R=[]


#for i in range(len(B)):
#    b = B[i]
#    cfn = lambda v: B[0]*basevar/basenum/v
#
 #   r = prediction.optatBcfoverL(b,cfn,Lsupport,Lprior,bnds=(-5,-1))
 #   R.append(r)

print('header\n')
#for i in range(len(B)):
#    s = "{:.3g} & $ \\frac{{ {:.3g} }}{{\\sigma^2}}$ & {:.3g} & {:.3g} & {:.3g} & {:.3g} \\\\".format(B[i],B[0]*basevar/basenum, R[i]['obsvar'],R[i]['Esteps'],R[i]['Rmean'],R[i]['Eover']/B[i])
#    print(s)