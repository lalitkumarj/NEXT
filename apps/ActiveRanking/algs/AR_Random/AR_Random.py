"""
AR_Random app implements Active ranking Random
author: Sumeet Katariya, sumeetsk@gmail.com
last updated: 09/24/2016

AR_Random implements random sampling 
"""

import numpy
import numpy.random
import next.utils as utils

class AR_Random:
    app_id = 'ActiveRanking'
    def initExp(self, butler, n=None, params=None):
        """
        This function is meant to set keys used later by the algorith implemented
        in this file.
        """
        butler.algorithms.set(key='n', value=n)

        W = np.zeros((n,n))

        butler.algorithms.set(key='W', value=W)

        return True

    def getQuery(self, butler, participant_uid):
        n = butler.algorithms.get(key='n')

        index = numpy.random.randint(n)
        alt_index = numpy.random.randint(n)
        while alt_index == index:
            alt_index = numpy.random.randint(n)

        return [index, alt_index]

    def processAnswer(self, butler, left_id=0, right_id=0, winner_id=0):
        W = butler.algorithms.get(key='W')
        if left_id == winner_id:
            W[left_id, right_id] = W[left_id, right_id] + 1
        else:
            W[right_id, left_id] = W[right_id, left_id] + 1

        butler.algorithms.set(key='W', value='W')

        return True

    def getModel(self,butler):
#        keys = butler.algorithms.get(key='keys')
#        key_value_dict = butler.algorithms.get(key=keys)
#        n = butler.algorithms.get(key='n')
#
#        sumX = [key_value_dict['Xsum_'+str(i)] for i in range(n)]
#        T = [key_value_dict['T_'+str(i)] for i in range(n)]
#
#        mu = numpy.zeros(n, dtype='float')
#        for i in range(n):
#            if T[i]==0 or mu[i]==float('inf'):
#                mu[i] = -1
#            else:
#                mu[i] = sumX[i] * 1.0 / T[i]
#
#        prec = [numpy.sqrt(1.0/max(1,t)) for t in T]
#        return mu.tolist(), prec
        return range(n), range(n)


