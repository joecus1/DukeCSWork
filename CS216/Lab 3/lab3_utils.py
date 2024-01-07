import csv

official_match = set()

with open('official_matches.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        official_match.add((int(row[0]), int(row[1])))

def order_matches(set_matches):
    return_matches = set()
    for pair in set_matches:
        return_matches.add((min(pair), max(pair)))
    return(return_matches)

def precision(my_match):
    return(precision_helper(my_match, official_match))    
    
def precision_helper(my_match, true_match):
    ordered_match = order_matches(my_match)
    return((len(ordered_match.intersection(true_match))/len(ordered_match)))

def recall(my_match):
    return(recall_helper(my_match, official_match))
    
def recall_helper(my_match, true_match):
    ordered_match = order_matches(my_match)
    return((len(ordered_match.intersection(true_match))/len(true_match)))

def f1_score(my_match):
    prec = precision(my_match)
    rec = recall(my_match)
    return(2.0*((prec*rec)/(prec+rec)))
    
def edit_dist(str1, str2):
    return(edit_helper(str1, str2, len(str1), len(str2)))
    
def edit_helper(str1, str2, m, n): 
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)] 
    for i in range(m + 1): 
        for j in range(n + 1): 
            if i == 0: 
                dp[i][j] = j    
            elif j == 0: 
                dp[i][j] = i    
            elif str1[i-1] == str2[j-1]: 
                dp[i][j] = dp[i-1][j-1] 
            else: 
                dp[i][j] = 1 + min(dp[i][j-1],       
                                   dp[i-1][j],       
                                   dp[i-1][j-1])
    return dp[m][n]