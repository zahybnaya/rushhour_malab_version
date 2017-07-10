from pymc import MCMC
import lrta_pymc

iter_=200
burn_=100
thin_=1

M = MCMC(lrta_pymc)

M.sample(iter=iter_, burn=burn_, thin=thin_)

for s in lrta_pymc.sample_data.iteritems():
    print s

"""
Method 1: for every point in the array of thetha calculate f(stimuli,point). Average the results
Method LOOCV: sum([log(sum([w_s* p(h(i)|s) for s in samples])/all_w) for i in instance])

Questions to answer:
    1) why not just to do method 1? Why the LOOCV?
    2) How MCMC knows P(thetha1|x)? can I use this data for method 1?

"""




