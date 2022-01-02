from statistics import median
import numpy as np
from numpy import argmin
from aoc_utils import arithmetic

crabs = [1101,1,29,67,1102,0,1,65,1008,65,35,66,1005,66,28,1,67,65,20,4,0,1001,65,1,65,1106,0,8,99,35,67,101,99,105,32,110,39,101,115,116,32,112,97,115,32,117,110,101,32,105,110,116,99,111,100,101,32,112,114,111,103,114,97,109,10,322,659,689,304,1706,69,576,110,238,904,299,206,78,954,776,590,404,125,235,438,472,187,205,620,14,378,1056,496,1323,59,44,636,432,658,30,195,107,425,105,214,908,145,641,1467,441,346,455,1454,773,146,97,42,509,8,1217,503,901,1147,1654,45,1438,503,62,851,590,105,217,44,646,197,491,333,1224,90,262,1132,1499,864,128,165,36,646,422,1265,501,414,328,170,1566,115,1049,154,224,490,1018,1019,1484,315,614,816,207,240,423,132,196,484,532,857,341,723,69,294,787,1020,691,185,525,697,1435,62,156,21,314,489,640,93,415,446,902,15,510,91,104,317,971,108,187,616,794,416,1332,499,1086,443,514,258,383,162,1034,1,331,269,283,1835,150,1698,1020,318,1540,687,17,889,585,1682,67,547,1,1353,149,1650,145,13,151,1144,409,294,740,676,267,827,1624,804,44,795,297,265,426,508,11,1359,963,277,203,1093,450,1229,287,160,1913,914,512,1098,103,975,64,26,787,87,104,340,362,153,173,93,455,89,577,40,1459,320,398,1245,12,452,515,594,0,1497,1238,88,14,538,431,0,699,1033,483,574,593,612,770,1006,332,23,753,1334,536,109,164,250,86,333,1577,896,1199,521,73,467,1037,0,539,375,1243,238,301,262,191,415,88,515,1410,54,1019,934,81,1273,78,306,57,145,472,57,682,203,63,512,427,104,457,214,197,1766,350,355,536,839,7,586,1209,71,88,858,562,64,335,84,1161,1305,1203,102,52,193,47,852,718,885,146,111,1014,667,8,52,637,254,1453,674,1542,47,107,55,321,591,829,1113,40,215,398,254,327,181,200,20,129,265,109,705,1265,12,148,367,349,333,341,272,90,166,699,681,1927,1267,86,282,299,36,48,1594,110,645,569,724,199,334,239,117,448,108,67,1257,142,902,208,728,700,107,1,621,1036,1397,837,313,380,208,156,39,220,238,648,197,26,2,1010,98,458,271,1237,99,751,31,236,26,622,802,4,121,244,240,67,462,1181,100,1381,1494,446,23,35,95,357,212,90,820,56,96,171,11,1101,1020,149,125,1504,896,25,8,1704,193,421,134,135,1397,1052,1059,741,967,1537,373,585,279,46,398,654,305,435,89,11,702,27,102,573,497,139,530,805,3,122,1329,175,134,137,57,516,790,587,163,296,153,1124,1336,946,63,39,278,13,253,237,653,200,250,1067,1891,697,182,628,0,60,303,389,1821,189,295,41,619,71,795,1228,110,1198,306,941,59,72,666,610,850,984,564,330,636,111,1541,542,80,212,927,127,427,33,365,313,697,200,286,708,478,264,448,1159,256,28,273,7,238,176,956,735,264,361,1882,139,1345,1,271,508,0,190,110,119,76,715,1338,80,1026,132,286,966,337,1715,514,328,265,63,1376,1413,1421,457,66,1594,737,59,548,184,801,165,96,129,1200,50,604,1013,309,627,625,597,1012,77,670,177,264,115,174,109,148,270,24,346,33,1270,359,954,113,207,484,1756,1155,1067,991,1358,61,530,612,135,351,706,244,489,609,484,76,168,258,161,694,1019,1502,558,117,112,1041,1040,448,879,37,616,930,32,357,1650,231,458,1068,585,9,439,412,292,116,494,246,28,260,463,200,84,1106,750,667,1284,129,878,1077,453,960,409,1327,412,243,89,616,443,256,645,1083,526,95,818,9,59,76,541,312,1168,430,64,2,187,561,1322,369,1245,64,854,126,359,240,42,157,35,232,863,74,331,250,695,914,182,208,94,656,87,530,1444,163,429,46,299,1038,38,471,91,112,819,1644,244,1718,76,806,103,752,124,796,1183,15,829,1038,6,529,913,140,326,435,44,617,659,123,753,444,467,408,182,1387,202,684,60,55,26,155,902,1075,86,375,924,862,150,1230,700,143,417,156,933,872,639,1032,137,146,1649,1562,4,11,257,556,29,1440,177,935,741,492,300,1530,92,453,56,244,37,997,762,624,456,1182,845,150,367,393,334,338,100,278,1374,267,1261,25,106,332,25,2,14,123,288,600,880,838,323,183,1075,202,445,218,1538,73,300,555,322,587,7,606,753,676,28,57,557,1283,23,73,31,370,29,491,5,31,97,199,188,1088,276,1061,1043,42,1463,601,56,255,426,150,1451,562,0,408,7,701,111,1145,838,976,310,561,645,33,213,1020,73,81,849,2,586,825,183,2,704,59,1515,906,647,91,585,14,778,333,258,353,128,839,146,81,231,128,716,699,64,345,812,906,1180,286,243,295,1031,197,1392]
crabs = np.asarray(crabs)

# Linear case (optimum lies in median of all positions)
average = int(round(median(crabs)))
dist = sum([abs(x - average) for x in crabs])
print("Best distance is", dist, "for position", average)

# Non-linear case (simulate using the 'arithmetic sequence sum' formula)
limit = max(crabs)
costs = [sum([arithmetic(0, 1, abs(c - x) + 1) for c in crabs]) for x in range(limit + 1)]
min_c = argmin(costs)
print("Best distance is", int(costs[min_c]), "for position", min_c)