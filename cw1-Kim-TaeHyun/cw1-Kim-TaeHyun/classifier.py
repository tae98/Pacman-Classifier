# classifier.py
# Lin Li/26-dec-2021
#
# Use the skeleton below for the classifier and insert your code here.
import numpy as np
class Classifier:
    def __init__(self):
        self.uniques = dict()
        self.uniquesProbTable = dict()
        self.dataLength = 0

    def reset(self):
        self.uniques = dict()
        self.uniquesProbTable = dict()
        self.dataLength = 0
    
    #getUniquesFromData fucntion is used to obtain the unique 25 binary data from the 126 good-moves
    #amongst the 126 total data in good-moves.txt it consisted with repetition of 35 unique data
    
    def getUniquesFromData(self, data, target):
        result = dict()
        for index in range(0, len(data)):
            if tuple(data[index]) not in list(result.keys()):
                result[tuple(data[index])] = {str(target[index]): 1}
            else:
                value = result[tuple(data[index])]
                if str(target[index]) not in list(value.keys()):
                    value[str(target[index])] = 1
                else:
                    value[str(target[index])] = value[str(target[index])] + 1
        self.dataLength = len(data)
        return result
    
    #DisplayDict was use to visualize the data and the target pair
    
    def displayDict(self, sampleDict):
        for each in range(0, len(sampleDict)):
            print(list(sampleDict.keys())[each], end='')
            print(" : ", end='')
            print(list(sampleDict.values())[each])
            
    #getTotal is used to find the total number of the each unique datas occurence in good-moves
    
    def getTotal(self, sampleDict):
        total = 0
        for each in list(sampleDict.values()):
            total = total + sum(list(each.values()))

        return total
    
    #getProbFromTarget is used to get the probability of each target value from the total set of good-move(prior-probabilty)
    
    def getProbFromTarget(self, target):
        result = dict()
        for each in target:
            if str(each) not in list(result.keys()):
                result[str(each)] = 1
            else:
                result[str(each)] = result[str(each)] + 1

        return {each: result[each] / self.dataLength for each in result.keys()}
    
    #getProFromUnique is used to obtain the probability of each unique string against each target value they have (likelihood)
    #it also multiply the likelihood and prior probability and obtains the maximum value (naive bayesian)
    
    def getProFromUnique(self, target):
        for each in list(self.uniques.keys()):
            value = self.uniques[each]
            de = sum(list(value.values()))
            self.uniquesProbTable[each] = {k: value[k] / de * self.getProbFromTarget(target)[k] for k in value.keys()}
            maximum = max(list(self.uniquesProbTable[each].values()))
            targetIndex = list(self.uniquesProbTable[each].values()).index(maximum)
            self.uniquesProbTable[each] = list(self.uniquesProbTable[each].keys())[targetIndex]
            
    #fit is used calcuate the datas from the good-moves using using the fucntion above
    #this is where the learning from the training data is made and stored
     
    def fit(self, data, target):
        self.uniques = self.getUniquesFromData(data, target)
        self.getProFromUnique(target)

    #the cluster function is used to calculate for unseen data and give the most appropirate target
    #it evaluates the similarity between unseen data and 35 unique datas bianary in order
    #it then grades the similarity by adding 1 if the sequence of the two datas are in match (max 25)
    #it will then give out target value amongst the maximum similarity (closest cluster group)
    #if there are more than 1 same max similarity cluster it will pass out target randomly amongst them
    
    def cluster(self, data):
        temp = dict()
        maximum = -1
        for each in list(self.uniques.keys()):
            count = 0
            for index in range(0, len(each)):
                if data[index] == each[index]:
                    count = count + 1
            if maximum < count:
                maximum = count
            temp[each] = count

        for each in list(self.uniques.keys()):
            if temp[each] < maximum:
                temp.pop(each)
        index = np.random.randint(0, len(temp))

        return list(temp.keys())[index]

    #the predict function is used to predict the best legal move for pacman based on the data obtained from good-move using naive-bayesian 
    #if the data is within the training data it will give out the most appropriate target value with text "Data within Training data!"
    #if the the data is unseen data it gives the target of most similar data from the good move (same cluster) using cluster function
    #it will print out "Unseen data! Looking for the closest prediction" when unseen data is given before passing most suitable target value
    
    def predict(self, data, legal=None):
        result = 1
        if tuple(data) in list(self.uniquesProbTable.keys()):
            result = int(self.uniquesProbTable[tuple(data)])
            print("Data within Training data!")
            print(result)
        else:
            print("Unseen data! Looking for the closest prediction")
            result = int(self.uniquesProbTable[self.cluster(data)])
            print(result)

        return result
