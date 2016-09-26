"""
Quicksort app implements Quicksort Active Sampling Algorithm
author: Sumeet Katariya, sumeetsk@gmail.com
last updated: 09/20/2016
"""

import numpy as np
import next.utils as utils

class Quicksort:
    app_id = 'ActiveRanking'
    def initExp(self, butler, n=None, params=None):
        nquicksorts = 8
        butler.algorithms.set(key='n', value=n)
        butler.algorithms.set(key='nquicksorts', value=nquicksorts)
        arrlist = []
        for _ in range(nquicksorts):
            arrlist.append(np.random.permutation(range(n)))
        butler.algorithms.set(key='arrlist', value=arrlist)
        butler.algorithms.set(key='llist', value=[0]*nquicksorts)
        butler.algorithms.set(key='hlist', value=[n-1]*nquicksorts)
        butler.algorithms.set(key='ptrlist', value=[0]*nquicksorts)
        butler.algorithms.set(key='lmaxlist', value=[-1]*nquicksorts)
        butler.algorithms.set(key='pivotlist', value=[n-1]*nquicksorts)
        butler.algorithms.set(key='stacklist', value= [[]]*nquicksorts)

        rankinglist = []
        for _ in range(nquicksorts):
            rankinglist.append(np.zeros(n))
        butler.algorithms.set(key='rankinglist', value=rankinglist)
        return True

    def getQuery(self, butler, participant_uid):
        #print arr
        #print arr[ptr],arr[pivot]
        nquicksorts = butler.algorithms.get('nquicksorts')
        quicksortID = np.random.randint(nquicksorts)
        arrlist = butler.algorithms.get('arrlist')
        arr = arrlist[quicksortID]
        ptrlist = butler.algorithms.get('ptrlist')
        ptr = ptrlist[quicksortID]
        pivotlist = butler.algorithms.get('pivotlist')
        pivot = pivotlist[quicksortID]
# pick a random Quicksort
# get a query from this chosen Quicksort
# Add to the butler dictionary a key with the query_uid and a value equal to the chosen quicksort number
# return this query
        return [arr[ptr], arr[pivot], quicksortID]


    def processAnswer(self, butler, left_id=0, right_id=0, winner_id=0, quicksortID=0):
        arrlist = butler.algorithms.get('arrlist')
        arr = arrlist[quicksortID]
        llist = butler.algorithms.get('llist')
        l = llist[quicksortID]
        hlist = butler.algorithms.get('hlist')
        h = hlist[quicksortID]
        lmaxlist = butler.algorithms.get('lmaxlist')
        lmax = lmaxlist[quicksortID]
        pivotlist = butler.algorithms.get('pivotlist')
        pivot = pivotlist[quicksortID]
        stacklist = butler.algorithms.get('stacklist')
        stack = stacklist[quicksortID]
        ptrlist = butler.algorithms.get('ptrlist')
        ptr = ptrlist[quicksortID]
        rankinglist = butler.algorithms.get('rankinglist')
        ranking = rankinglist[quicksortID]
        #pdb.set_trace()

        if winner_id==arr[pivot]:
            lmax = lmax + 1
            arr[lmax],arr[ptr] = arr[ptr],arr[lmax]
        ptr = ptr + 1
        if ptr == h:
            arr[lmax+1],arr[pivot] = arr[pivot],arr[lmax+1]
            if l<lmax:
                stack.append([l,lmax])
            if lmax+2<h:
                stack.append([lmax+2,h])
            if stack==[]:
                ranking = ranking + np.array(arr)
                n = len(arr)
                arr = np.random.permutation(arr)
                l = 0
                h = n-1
                ptr = 0
                lmax = -1
                pivot = n-1
                stack = []
            else:
                x = stack.pop(0)
                l = x[0]
                h = x[1]
                lmax = l-1
                pivot = h
                ptr = l

        arrlist[quicksortID] = arr
        llist[quicksortID] = l
        hlist[quicksortID] = h
        lmaxlist[quicksortID] = lmax
        pivotlist[quicksortID] = pivot
        stacklist[quicksortID] = stack
        ptrlist[quicksortID] = ptr
        rankinglist[quicksortID] = ranking

        butler.algorithms.set(key='arrlist', value=arrlist)
        butler.algorithms.set(key='llist', value=llist)
        butler.algorithms.set(key='hlist', value=hlist)
        butler.algorithms.set(key='lmaxlist', value=lmaxlist)
        butler.algorithms.set(key='pivotlist', value=pivotlist)
        butler.algorithms.set(key='stacklist', value=stacklist)
        butler.algorithms.set(key='ptrlist', value=ptrlist)
        butler.algorithms.set(key='rankinglist', value=rankinglist)
        #print ranking
        return True

    def getModel(self,butler):
        return range(n), range(n)
