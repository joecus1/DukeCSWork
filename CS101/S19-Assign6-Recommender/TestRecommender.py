'''
@author: 
'''

import SmallDukeEatsReader
import RecommenderEngine


def driver():
    
    (items,ratings) = SmallDukeEatsReader.getdata()
    print("items = ",items)
    print("ratings = ", ratings)

    
    avg = RecommenderEngine.averages(items,ratings)
    print("average",avg)
     
    for key in ratings:
        slist = RecommenderEngine.similarities(key,ratings)
        print(key,slist)
        r3 = RecommenderEngine.recommendations(key,items,ratings,3)
        print("top",r3)
        
        
        
if __name__ == '__main__':
    driver()