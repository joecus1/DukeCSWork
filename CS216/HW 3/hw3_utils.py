official_match = {(75, 592), (319, 555), (263, 277), (343, 656), 
                    (235, 619), (230, 550), (48, 233), (523, 639),
                    (542, 681), (228, 388), (166, 451), (312, 793),
                    (13, 253), (395, 782), (138, 705), (6, 54),
                    (516, 629), (285, 392), (131, 224), (177, 288),
                    (324, 496), (758, 851), (334, 780), (20, 755),
                    (836, 853), (46, 852), (62, 89), (219, 489),
                    (11, 326), (74, 223), (95, 743), (304, 735),
                    (87, 753), (73, 513), (661, 801), (128, 212),
                    (655, 712), (546, 556), (8, 785), (84, 325),
                    (12, 22), (184, 191), (35, 229), (204, 424),
                    (371, 511), (79, 635), (756, 759), (305, 389),
                    (207, 407), (561, 828), (171, 269), (240, 265),
                    (70, 683), (353, 538), (276, 597), (236, 257),
                    (405, 617), (176, 666), (121, 290), (406, 476),
                    (214, 734)}

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