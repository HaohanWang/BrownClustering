__author__ = 'haohanwang'
import math
import operator

class BrownCluster:
    def __init__(self, dictionaryfile = '../preprocessing/data/words.txt', textfile='../DATA/tokenizeddata'):
        self.text = [line.strip() for line in open(textfile)]
        init_words = {}
        for line in self.text:
            words = line.split()
            for w in words:
                w = w.lower()
                if w not in init_words:
                    init_words[w]=1.0
                else:
                    init_words[w]+=1.0
        s_w = sorted(init_words.iteritems(), key=operator.itemgetter(1))
        s_w.reverse()
        self.vocab = {}
        self.cluster = {}
        for i in range(len(s_w)):
            self.vocab[s_w[i][0]] = i+1
            self.cluster[i+1] = [s_w[i][0]]
        self.Nv = len(self.vocab)
        self.Nc = self.Nv
        self.getP_c_cPrime_Pw()
        # print self.cluster
        # print self.P_c

    def __str__(self):
        return 'This is an implementation of Brown Word Clustering Algorithm'


    def getP_c_cPrime_Pw(self):
        self.P_c_cPrime = {}
        self.P_c = {}
        self.P_cPrime = {}
        for line in self.text:
            words = line.split()
            for i in range(1, len(words)):
                c = self.vocab[words[i-1]]
                cP = self.vocab[words[i]]
                if c in self.P_c:
                    self.P_c[c]+=1.0
                else:
                    self.P_c[c]=1.0
                if cP in self.P_cPrime:
                    self.P_cPrime[cP]+=1.0
                else:
                    self.P_cPrime[cP]=1.0
                k = str(c)+'#'+str(cP)
                if k in self.P_c_cPrime:
                    self.P_c_cPrime[k]+=1.0
                else:
                    self.P_c_cPrime[k]=1.0
        for w in self.P_c_cPrime:
            self.P_c_cPrime[w]=self.P_c_cPrime[w]/self.Nc
        for w in self.P_cPrime:
            self.P_cPrime[w]=self.P_cPrime[w]/self.Nc
        for w in self.P_c:
            self.P_c[w]=self.P_c[w]/self.Nc
        #return self.P_c_cPrime, self.P_c, self.P_cPrime

    def qualify(self):
        r = 0.0
        for i in range(1, self.Nv+1):
            for j in range(1, self.Nv+1):
                if i!=j and i in self.P_c and j in self.P_cPrime:
                    k = str(i)+'#'+str(j)
                    if k in self.P_c_cPrime:
                        a = self.P_c_cPrime[k]
                        r+=a*math.log(a/(self.P_c[i]*self.P_cPrime[j]))
        return r

    def qualify_fast(self, m, l):
        r = 0.0
        for i in range(1, m+l+1):
            for j in range(1, m+l+1):
                if i!=j and i in self.P_c and j in self.P_cPrime:
                    if self.P_c!=None and self.P_cPrime[j]!=None:
                        k = str(i)+'#'+str(j)
                        if k in self.P_c_cPrime and self.P_c_cPrime[k]!=None:
                            a = self.P_c_cPrime[k]
                            r+=a*math.log(a/(self.P_c[i]*self.P_cPrime[j]))
        return r

    def merge(self, c1, c2):
        words = self.cluster[c2]
        self.cluster[c1].extend(words)
        for word in words:
            self.vocab[word] = c1
        self.cluster[c2]=None
        if c2 in self.P_c and self.P_c[c2]!=None:
            pc_tmp = self.P_c[c2]
            self.P_c[c2]=None
            if c1 in self.P_c and self.P_c[c1]!=None:
                self.P_c[c1]+=pc_tmp
            else:
                self.P_c[c1] = pc_tmp
        if c2 in self.P_cPrime and self.P_cPrime[c2]!=None:
            pcp_tmp = self.P_cPrime[c2]
            self.P_cPrime[c2] = None
            if c1 in self.P_cPrime and self.P_cPrime[c1]!=None:
                self.P_cPrime[c1]+=pcp_tmp
            else:
                self.P_cPrime[c1]=pcp_tmp
        pccp1 = {}
        for i in range(1, self.Nv+1):
            k1 = str(i)+'#'+str(c2)
            if k1 in self.P_c_cPrime and self.P_c_cPrime[k1]!=None:
                pccp1[i]=self.P_c_cPrime[k1]
                self.P_c_cPrime[k1] = None
                k2 = str(i)+'#'+str(c1)
                if k2 in self.P_c_cPrime and self.P_c_cPrime[k2]!=None:
                    self.P_c_cPrime[k2]+=pccp1[i]
                else:
                    self.P_c_cPrime[k2]=pccp1[i]
        pccp2 = {}
        for i in range(1, self.Nv+1):
            k1 = str(c2)+'#'+str(i)
            if k1 in self.P_c_cPrime and self.P_c_cPrime[k1]!=None:
                pccp2[i]=self.P_c_cPrime[k1]
                self.P_c_cPrime[k1] = None
                k2 = str(c1)+'#'+str(i)
                if k2 in self.P_c_cPrime and self.P_c_cPrime[k2]!=None:
                    self.P_c_cPrime[k2]+=pccp2[i]
                else:
                    self.P_c_cPrime[k2]=pccp2[i]

    def tmp_merge(self, c1, c2):
        words = self.cluster[c2]
        for word in words:
            self.vocab[word] = c1
        pc_tmp=0
        pcp_tmp=0
        if c2 in self.P_c and self.P_c[c2]!=None:
            pc_tmp = self.P_c[c2]
            self.P_c[c2]=None
            if c1 in self.P_c and self.P_c[c1]!=None:
                self.P_c[c1]+=pc_tmp
            else:
                self.P_c[c1] = pc_tmp
        if c2 in self.P_cPrime and self.P_cPrime[c2]!=None:
            pcp_tmp = self.P_cPrime[c2]
            self.P_cPrime[c2] = None
            if c1 in self.P_cPrime and self.P_cPrime[c1]!=None:
                self.P_cPrime[c1]+=pcp_tmp
            else:
                self.P_cPrime[c1]=pcp_tmp
        pccp1 = {}
        for i in range(1, self.Nv+1):
            k1 = str(i)+'#'+str(c2)
            if k1 in self.P_c_cPrime and self.P_c_cPrime[k1]!=None:
                pccp1[i]=self.P_c_cPrime[k1]
                self.P_c_cPrime[k1] = None
                k2 = str(i)+'#'+str(c1)
                if k2 in self.P_c_cPrime and self.P_c_cPrime[k2]!=None:
                    self.P_c_cPrime[k2]+=pccp1[i]
                else:
                    self.P_c_cPrime[k2]=pccp1[i]
        pccp2 = {}
        for i in range(1, self.Nv+1):
            k1 = str(c2)+'#'+str(i)
            if k1 in self.P_c_cPrime and self.P_c_cPrime[k1]!=None:
                pccp2[i]=self.P_c_cPrime[k1]
                self.P_c_cPrime[k1] = None
                k2 = str(c1)+'#'+str(i)
                if k2 in self.P_c_cPrime and self.P_c_cPrime[k2]!=None:
                    self.P_c_cPrime[k2]+=pccp2[i]
                else:
                    self.P_c_cPrime[k2]=pccp2[i]
        return words, pc_tmp, pcp_tmp, pccp1, pccp2

    def tmp_break(self, c1, c2, tmp):
        words = tmp[0]
        pc_tmp = tmp[1]
        pcp_tmp = tmp[2]
        pccp1 = tmp[3]
        pccp2 = tmp[4]
        for word in words:
            self.vocab[word]=c2
        if pc_tmp!=0:
            self.P_c[c1]-=pc_tmp
            if self.P_c[c1]==0:
                self.P_c[c1]=None
            self.P_c[c2]=pc_tmp
        if pcp_tmp!=0:
            self.P_cPrime[c1]-=pcp_tmp
            if self.P_cPrime[c1]!=0:
                self.P_cPrime[c1]=None
            self.P_cPrime[c2]=pcp_tmp
        for i in range(1, self.Nv+1):
            k1 = str(c2)+'#'+str(i)
            if k1 in self.P_c_cPrime:
                self.P_c_cPrime[k1] = pccp2[i]
                k2 = str(c1)+'#'+str(i)
                self.P_c_cPrime[k2]-=pccp2[i]
                if self.P_c_cPrime[k2]==0:
                    self.P_c_cPrime[k2]=None
        for i in range(1, self.Nv+1):
            k1 = str(i)+'#'+str(c2)
            if k1 in self.P_c_cPrime:
                self.P_c_cPrime[k1] = pccp1[i]
                k2 = str(i)+'#'+str(c1)
                self.P_c_cPrime[k2]-=pccp1[i]
                if self.P_c_cPrime[k2]==0:
                    self.P_c_cPrime[k2]=None

    def word_cluster_navie(self, k=1000):
        while self.Nc>k:
            print '\nNow there are', self.Nc, 'clusters'
            m = -1e5
            tc1 = 0
            tc2 = 0
            ct = 0
            st = int(self.Nv*self.Nv/20.0)
            ms = 1
            for i in range(1,self.Nv+1):
                for j in range(1, self.Nv+1):
                    if i!=j:
                        ct+=1
                        if ct>=ms*st:
                            print str(ms*100/20.0)+'%..',
                            ms+=1
                        if self.cluster[i]!=None and self.cluster[j]!=None:
                            tmp = self.tmp_merge(i, j)
                            r = self.qualify()
                            self.tmp_break(i, j, tmp)
                            #print i, j, r
                            if r>m:
                                tc1 = i
                                tc2 = j
                                m = r
            self.merge(tc1, tc2)
            print '\n',tc1, tc2, self.cluster[tc1],
            self.Nc-=1

    def word_cluster_fast(self, k=1000, m=1000):
        l = 0
        while self.Nc>k:
            l+=1
            print '\nNow there are', self.Nc, 'clusters'
            maxmum = -1e5
            tc1 = 0
            tc2 = 0
            ct = 0
            st = int(self.Nv*self.Nv/200.0)
            ms = 1
            for i in range(1,min(m+1+l, self.Nv+1)):
                for j in range(1, min(m+1+l, self.Nv+1)):
                    if i!=j:
                        ct+=1
                        if ct>=ms*st:
                            print str(ms*100/200.0)+'%..',
                            ms+=1
                            if ms%10==0:
                                print ''
                        if self.cluster[i]!=None and self.cluster[j]!=None:
                            tmp = self.tmp_merge(i, j)
                            self.getP_c_cPrime_Pw()
                            r = self.qualify_fast(m, l)
                            self.tmp_break(i, j, tmp)
                            print i, j, r
                            if r>maxmum:
                                tc1 = i
                                tc2 = j
                                maxmum = r
            self.merge(tc1, tc2)
            print '\n',tc1, tc2, self.cluster[tc1],
            self.Nc-=1

    def output(self):
        print 'Done, start to write'
        f = open('data/wordClustering.txt', 'w')
        c = 0
        for i in range(1, self.Nv+1):
            if self.cluster[i]!=None:
                c+=1
                words = self.cluster[i]
                print 'C'+str(c), words
                f.writelines('C'+str(c))
                for word in words:
                    f.writelines('\t'+word)
                f.writelines('\n')
        f.close()

#BC = BrownCluster(dictionaryfile='tmp/words.txt', textfile='tmp/text.txt')
BC = BrownCluster()
BC.word_cluster_fast(k=500, m=500)
BC.output()