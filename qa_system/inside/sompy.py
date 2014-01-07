from __future__ import division

## Kyle Dickerson
## kyle.dickerson@gmail.com
## Jan 15, 2008
##
## Self-organizing map using scipy
## This code is licensed and released under the GNU GPL

## This code uses a square grid rather than hexagonal grid, as scipy allows for fast square grid computation.
## I designed sompy for speed, so attempting to read the code may not be very intuitive.
## If you're trying to learn how SOMs work, I would suggest starting with Paras Chopras SOMPython code:
##  http://www.paraschopra.com/sourcecode/SOM/index.php
## It has a more intuitive structure for those unfamiliar with scipy, however it is much slower.

## If you do use this code for something, please let me know, I'd like to know if has been useful to anyone.

from random import *
from math import *
import sys
import scipy
import time

def min_max_range_matrix(matrix):
    l = 1000
    b = -1000
    for doc in matrix:
        l = min(min(doc),l)
        b = max(max(doc),b)

    return (l,b)


class SOM:

    def __init__(self, training_algorithm, height=10, width=10, FV_size=10, learning_rate=0.005):

        #print "DENTRO DE SOMPY __INIT__"
        #print "   FV_size"
        
        self.height = height
        self.width = width
        self.FV_size = FV_size
        self.radius = (height+width)/3
        self.learning_rate = learning_rate
        self.nodes = scipy.array([[ [random() for i in range(FV_size)] for x in range(width)] for y in range(height)])
        self.training_algorithm = training_algorithm


    # train_vector: [ FV0, FV1, FV2, ...] -> [ [...], [...], [...], ...]
    # train vector may be a list, will be converted to a list of scipy arrays
    def train(self, iterations=1000, train_vector=[[]], epsilon=0.1):
        #print "DENTRO DE SOMPY TRAIN"
        for t in range(len(train_vector)):
            #print "   train_vector[t]  =  " + str(len(train_vector[t]))
            train_vector[t] = scipy.array(train_vector[t])
        time_constant = iterations/log(self.radius)
        delta_nodes = scipy.array([[[0 for i in range(self.FV_size)] for x in range(self.width)] for y in range(self.height)])
        i = 0
        old = delta_nodes
        while i <= iterations and self.difference(old) > epsilon:
            print "difference(new,old)"
            print self.difference(old)
            print "epsilon"
            print self.difference(old) > epsilon
            print self.difference(delta_nodes)
            print i <= iterations
            time.sleep(3)
            i+=1
            st = "[["
            for x in range(self.height):
                for y in range(self.width):
                    for e in range(self.FV_size):
                        st+=str(int(self.nodes[x,y,e]))+" "
                    st+= "] , ["
                st+="]]\n\n"
            delta_nodes.fill(0)
            radius_decaying=self.radius*exp(-1.0*i/time_constant)
            #from PIL import Image
            #print "\nSaving Image: sompy_test_colors.png..."
            #img = Image.new("RGB", (self.width, self.height))
            #for r in range(self.height):
            #    for c in range(self.width):
            #        img.putpixel((c,r), (int(self.nodes[r,c,0]*255), int(self.nodes[r,c,1]*255 ), int(self.nodes[r,c,2]*255)))
            #img = img.resize((self.width*10, self.height*10),Image.NEAREST)
            #img.save("Test Colors/Test1/4_sompy_test_colors"+str(10000+i)+".png")
            rad_div_val = 2 * radius_decaying * i
            learning_rate_decaying=self.learning_rate*exp(-1.0*i/time_constant)

            sys.stdout.write("\rTraining Iteration: " + str(i) + "/" + str(iterations)+"\n")
            
            for j in range(len(train_vector)):
                #print train_vector 
                #print "   BEST_MATCH HERE WE GO "
                #print "      train_vector[t]  =  " + str(len(train_vector[t]))

                best = self.best_match(train_vector[j])
                for loc in self.find_neighborhood(best, radius_decaying):

                    influence = exp( (-1.0 * (loc[2]**2)) / rad_div_val)
                    #sys.stdout.write("Influence: " + "/" + str(influence) + "\n")
                    inf_lrd = influence*learning_rate_decaying
                    delta_nodes[loc[0],loc[1]] += inf_lrd*(train_vector[j]-self.nodes[loc[0],loc[1]])
            old = self.nodes
            self.nodes += delta_nodes
        sys.stdout.write("\n")
    
    # Returns a list of points which live within 'dist' of 'pt'
    # Uses the Chessboard distance
    # pt is (row, column)
    def find_neighborhood(self, pt, dist):
        min_y = max(int(pt[0] - dist), 0)
        max_y = min(int(pt[0] + dist), self.height)
        min_x = max(int(pt[1] - dist), 0)
        max_x = min(int(pt[1] + dist), self.width)
        neighbors = []
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                dist = abs(y-pt[0]) + abs(x-pt[1])
                neighbors.append((y,x,dist))
        return neighbors
    
    # Returns location of best match, uses Euclidean distance
    # target_FV is a scipy array
    def best_match(self, target_FV):
        print "INSIDE BEST_MATCH"
        #print "   " + str(target_FV) + str(len(target_FV))
        '''print "NODOS"
        for row_nodes in self.nodes:
            for node in row_nodes:
                print node
        print
        print 
        print "TARGET"
        print target_FV
        print "PASOS SEGUIDOS"
        print "self.nodes - target_FV"
        print str(self.nodes - target_FV)
        print "((self.nodes - target_FV)**2)"
        print str((self.nodes - target_FV)**2)
        print "((self.nodes - target_FV)**2).max(axis=2)"
        print str(((self.nodes - target_FV)**2).max(axis=2))
        print "((((self.nodes - target_FV)**2).max(axis=2))**0.5)"
        print str(((((self.nodes - target_FV)**2).max(axis=2))**0.5))
        print "scipy.argmin((((self.nodes - target_FV)**2).max(axis=2))**0.5)"
        print str(scipy.argmin((((self.nodes - target_FV)**2).max(axis=2))**0.5))
        exit(-1)'''
        if self.training_algorithm == "eu":
            print "USING EUCLIDEAN"
            loc = self.euclidean_coefficient(target_FV)
        elif self.training_algorithm == "co":
            print "USING COSINE"
            loc = self.cosine_coefficient(target_FV)
        elif self.training_algorithm == "ja":
            print "USING JACCARD"
            loc = self.jaccard_coefficient(target_FV)
        elif self.training_algorithm == "fe":
            print "USING FUZZY"
            loc = self.fuzzy_coefficient(target_FV)
        r = 0
        while loc > self.width:
            loc -= self.width
            r += 1
        c = loc
        return (r, c)

    def euclidean_coefficient(self,target_FV):
        return scipy.argmin((((self.nodes - target_FV)**2).max(axis=2))**0.5)

    def fuzzy_coefficient(self,target_FV):
        min_array = []
        for f in self.nodes:
            for c in f:
                min_array.append(scipy.amin([c,(1-target_FV)],axis=1))
        return scipy.argmin(min_array)
        
    def cosine_coefficient(self, target_FV):
        #print target_FV
        #print "temp = (self.nodes * target_FV)"
        temp = (self.nodes * target_FV)
        #print temp
        #print "temp = temp.sum(axis=2)"
        temp = temp.sum(axis=2)
        #print temp
        #print "temp_2 = (self.nodes**2)"
        temp_2 = (self.nodes**2)
        #print temp_2
        #print "temp_2 = temp_2.sum(axis=2)"
        temp_2 = temp_2.sum(axis=2)
        #print temp_2
        #print "temp_3 = (target_FV**2)"
        temp_3 = (target_FV**2)
        #print temp_3
        #print "temp_3 = temp_3.sum()"
        temp_3 = temp_3.sum()
        #print temp_3
        #print "temp_3 = temp_3**0.5"
        temp_3 = temp_3**0.5
        #print temp_3
        #print "temp_4 = temp_2*temp_3"
        temp_4 = temp_2*temp_3
        #print temp_4
        #print "temp_f = temp / temp_4"
        temp_f = temp / temp_4
        #print temp_f
        return scipy.argmin(temp_f)

        #(a*b).sum(axis=2) / (((a**2).sum(axis=2) * (b**2).sum())**0.5)
        return scipy.argmin((self.nodes * target_FV).sum(axis=2) / ((self.nodes**2).sum(axis=2) * (target_FV**2).sum()**0.5))

    def jaccard_coefficient(self,target_FV):
        return scipy.argmin((self.nodes * target_FV).sum(axis=2) / (((self.nodes**2).sum(axis=2)) + ((target_FV**2).sum()) - ((self.nodes * target_FV).sum(axis=2))))


    def similarity_measure_cosine(self):
        max_sim_number = -1000
        max_document_index = -1
        disordered_list = []
        for j in range(len(self.TF_IDF_matrix[:-1])):
            sum_wq_wj = float(sum([a*b for a,b in zip(self.TF_IDF_matrix[j],self.question_TF_IDF_vector)]))
            sum_wq_2 = float(sum([a**2 for a in self.question_TF_IDF_vector]))
            sum_wj_2 = float(sum([a**2 for a in self.TF_IDF_matrix[j]]))
            cosine_sim_ = sum_wq_wj / (sum_wq_2 * sum_wj_2)**.5
            disordered_list.append((j,self.document_list[j],cosine_sim_))
            if cosine_sim_ > max_sim_number:
                max_sim_number = cosine_sim_
                max_document_index = j
        print "El documento con mayor Cosine similitud es: " + self.document_list[max_document_index]
        print "Con un valor de similitud de: " + str(max_sim_number)
        self.most_similar_document_indexes = sorted(disordered_list, key= lambda similarity: similarity[2],reverse=True)


    # returns the Euclidean distance between two Feature Vectors
    # FV_1, FV_2 are scipy arrays
    def FV_distance(self, FV_1, FV_2):
        return (sum((FV_1 - FV_2)**2))**0.5

    def difference(self, delta_nodes):
        #print self.nodes
        #print delta_nodes
        delta = 0
        for x in range(len(self.nodes)):
            delta =+ ((self.nodes[x] - delta_nodes[x])**2).sum(axis=1)
        #print delta
        return sum(delta)

if __name__ == "__main__":
    print "Initialization..."
    colors = [[0, 0, 0], [0, 0, 255], [0, 255, 0], [0, 255, 255], [255, 0, 0], [255, 0, 255], [255, 255, 0], [255, 255, 255]]
    width = 32
    height = 32
    color_som = SOM(colors,width,height,3,5)
    print "Training colors..."
    color_som.train(100, colors)





        