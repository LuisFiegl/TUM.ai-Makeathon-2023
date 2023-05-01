#%%
import numpy as np
#Arrays initialisieren für Beispiel:
C = np.array([[98,100,100,100],[98,100,100,100],[102,103,100,100],[102,103,100,100],[102,103,100,100]])
G = np.array([[0,1,1,1,1],[1,0,1,1,1],[1,1,0,1,1],[1,1,1,0,1],[1,1,1,1,0]])
P = np.array([[0,0,0.5,0,0],[0,0,0,0,0],[0.5,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
 
#%%
def find_optimal_transport(C, G, P):
    N = len(C)
    transportation_plan = []
    
    for ind_selling in range(N):
        profit_per_unit = []
        possible_units = []
        for ind_buying in range(N):
            sell_Q = C[ind_selling][3]
            sell_price = C[ind_selling][1]
            buy_Q = C[ind_buying][2]
            buy_price = C[ind_buying][0]
            quant = min(buy_Q, sell_Q)
            prob = P[ind_selling][ind_buying]
            if (quant > 0) & (buy_price > sell_price):
                profit_per_unit.append((buy_price-sell_price-G[ind_selling, ind_buying])*(1-prob))
            else:
                profit_per_unit.append(0)
            possible_units.append(quant)
        
        max_ppu = 0
        for i in range(len(profit_per_unit)):
            max_ppu = max(profit_per_unit)
            max_ppu_index = profit_per_unit.index(max(profit_per_unit))
            if (max_ppu > 0) & (possible_units[max_ppu_index] > 0):
                if (possible_units[max_ppu_index] <= C[ind_selling][3]):
                    if (possible_units[max_ppu_index] <= C[max_ppu_index][2]):
                        transportation_plan += [[ind_selling, max_ppu_index, possible_units[max_ppu_index]]]
                        C[ind_selling][3] = C[ind_selling][3] - possible_units[max_ppu_index]
                        C[max_ppu_index][2] = C[max_ppu_index][2] - possible_units[max_ppu_index]
                    else:
                        transportation_plan += [[ind_selling, max_ppu_index, C[max_ppu_index][2]]]
                        C[ind_selling][3] = C[ind_selling][3] - C[max_ppu_index][2]
                        C[max_ppu_index][2] = C[max_ppu_index][2] - C[max_ppu_index][2]

                else:
                    if (C[ind_selling][3] <= C[max_ppu_index][2]):
                        transportation_plan += [[ind_selling, max_ppu_index, C[ind_selling][3]]]
                        C[ind_selling][3] = C[ind_selling][3] - C[ind_selling][3]
                        C[max_ppu_index][2] = C[max_ppu_index][2] - C[ind_selling][3]
                    else:
                        transportation_plan += [[ind_selling, max_ppu_index, C[max_ppu_index][2]]]
                        C[ind_selling][3] = C[ind_selling][3] - C[max_ppu_index][2]
                        C[max_ppu_index][2] = C[max_ppu_index][2] - C[max_ppu_index][2]

            profit_per_unit[max_ppu_index] = 0
            possible_units[max_ppu_index] = 0

    right_plans = []
    for i in range(len(transportation_plan)):
        if (transportation_plan[i][2] >0):
            right_plans.append(transportation_plan[i])
             
    return np.array(right_plans)

find_optimal_transport(C, G, P)
# %%
