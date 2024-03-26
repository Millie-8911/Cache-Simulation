import math
import pandas as pd
import matplotlib.pyplot as plt

class print_table_dict:
    '''table1 for part 2 & part 4'''
    print_table1_data = { 
        'Assoc. Level': [],
        'L1I accesses': [],
        'L1I misses': [],
        'L1D accesses': [],
        'L1D misses': [],
        'L1I hit rate': [],
        'L1D hit rate': [],
        'AMAT': [],
    }
    '''table1 for part 5'''
    print_table2_data = { 
        'Assoc. Level': [],
        'L1I accesses': [],
        'L1I misses': [],
        'L1I hit rate': [],
        'L1D accesses': [],
        'L1D misses': [],
        'L1D hit rate': [],
        'L2 accesses': [],
        'L2 misses': [],
        'L2 hit rate': [],
        'AMAT': [],
    }
    print_table3_data = { 
        'Assoc. Level': [],
        'L1I accesses': [],
        'L1I misses': [],
        'L1I hit rate': [],
        'L1D accesses': [],
        'L1D misses': [],
        'L1D hit rate': [],
        'L2 accesses': [],
        'L2 misses': [],
        'L2 hit rate': [],
        'L3 accesses': [],
        'L3 misses': [],
        'L3 hit rate': [],
        'AMAT': [],
    }
    L1I_accesses = []
    L1I_misses = []
    L1D_accesses = []
    L1D_misses = []
    L1I_hit_rate = []
    L1D_hit_rate = []
    L2_accesses = []
    L2_misses = []
    L2_hit_rate = []
    L3_accesses = []
    L3_misses = []
    L3_hit_rate = []
    AMAT = []

    def clear_lisr():
        print_table_dict.L1I_accesses = []
        print_table_dict.L1I_misses = []
        print_table_dict.L1D_accesses = []
        print_table_dict.L1D_misses = []
        print_table_dict.L1D_hit_rate = []
        print_table_dict.L2_accesses = []
        print_table_dict.L2_misses = []
        print_table_dict.L2_hit_rate = []
        print_table_dict.L3_accesses = []
        print_table_dict.L3_misses = []
        print_table_dict.L3_hit_rate = []
        print_table_dict.AMAT = []


    def table1_print():
        # print(len(print_table_dict.L1I_accesses))
        # print(len(print_table_dict.L1I_misses))
        # print(len(print_table_dict.L1D_accesses))
        # print(len(print_table_dict.L1D_misses))
        # print(len(print_table_dict.L1I_accesses))
        # print(len(print_table_dict.L1I_hit_rate))
        # print(len(print_table_dict.L1D_hit_rate))
        # print(len(print_table_dict.AMAT))
        print_table_dict.print_table1_data.update({
                    'Assoc. Level': [1, 2, 4, 8, 16, 32],
                    'L1I accesses': print_table_dict.L1I_accesses,
                    'L1I misses': print_table_dict.L1I_misses,
                    'L1D accesses': print_table_dict.L1D_accesses,
                    'L1D misses': print_table_dict.L1D_misses,
                    'L1I hit rate': print_table_dict.L1I_hit_rate,
                    'L1D hit rate': print_table_dict.L1D_hit_rate,
                    'AMAT': print_table_dict.AMAT
                })
        df = pd.DataFrame(print_table_dict.print_table1_data)
        # Use Matplotlib to create a table and remove axis
        fig, ax = plt.subplots(figsize=(12, 2))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', rowLabels=None)
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)
        plt.show()
        print_table_dict.clear_lisr()

    def table2_print():
        print_table_dict.print_table2_data.update({
                    'Assoc. Level': [1, 4, 16, 64,128],
                    'L1I accesses': print_table_dict.L1I_accesses,
                    'L1I misses': print_table_dict.L1I_misses,
                    'L1I hit rate': print_table_dict.L1I_hit_rate,
                    'L1D accesses': print_table_dict.L1D_accesses,
                    'L1D misses': print_table_dict.L1D_misses,
                    'L1D hit rate': print_table_dict.L1D_hit_rate,
                    'L2 accesses': print_table_dict.L2_accesses,
                    'L2 misses': print_table_dict.L2_misses,
                    'L2 hit rate': print_table_dict.L2_hit_rate,
                    'AMAT': print_table_dict.AMAT
                })
        df = pd.DataFrame(print_table_dict.print_table2_data)
        # Use Matplotlib to create a table and remove axis
        fig, ax = plt.subplots(figsize=(12, 2))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', rowLabels=None)
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)
        plt.show()
        print_table_dict.clear_lisr()

    def table3_print():
            print_table_dict.print_table3_data.update({
                        'Assoc. Level': [1, 2, 4, 8, 16, 32],
                        'L1I accesses': print_table_dict.L1I_accesses,
                        'L1I misses': print_table_dict.L1I_misses,
                        'L1I hit rate': print_table_dict.L1I_hit_rate,
                        'L1D accesses': print_table_dict.L1D_accesses,
                        'L1D misses': print_table_dict.L1D_misses,
                        'L1D hit rate': print_table_dict.L1D_hit_rate,
                        'L2 accesses': print_table_dict.L2_accesses,
                        'L2 misses': print_table_dict.L2_misses,
                        'L2 hit rate': print_table_dict.L2_hit_rate,
                        'L3 accesses': print_table_dict.L3_accesses,
                        'L3 misses': print_table_dict.L3_misses,
                        'L3 hit rate': print_table_dict.L3_hit_rate,
                        'AMAT': print_table_dict.AMAT
                    })
            df = pd.DataFrame(print_table_dict.print_table3_data)
            # Use Matplotlib to create a table and remove axis
            fig, ax = plt.subplots(figsize=(12, 2))
            ax.axis('tight')
            ax.axis('off')
            table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', rowLabels=None)
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.2, 1.2)
            plt.show()
            print_table_dict.clear_lisr()
# for i in range(6):
# #     print("Current value of i:", i)
# #     print("Length of L1I_accesses:", len(print_table_dict.L1I_accesses))
# #     print("Length of L1I_misses:", len(print_table_dict.L1I_misses))
# #     print("Length of L1D_accesses:", len(print_table_dict.L1D_accesses))
# #     print("Length of L1D_misses:", len(print_table_dict.L1D_misses))
# #     print("Length of L1I_hit_rate:", len(print_table_dict.L1I_hit_rate))
# #     print("Length of L1D_hit_rate:", len(print_table_dict.L1D_hit_rate))
# #     print("Length of AMAT:", len(print_table_dict.AMAT))
#     print_table_dict.L1I_accesses.append(i)
#     print_table_dict.L1I_misses.append(i)
#     print_table_dict.L1D_accesses.append(i)
#     print_table_dict.L1D_misses.append(i)
#     print_table_dict.L1I_hit_rate.append(i)
#     print_table_dict.L1D_hit_rate.append(i)
#     print_table_dict.L2_accesses.append(i)
#     print_table_dict.L2_misses.append(i)
#     print_table_dict.L2_hit_rate.append(i)
#     print_table_dict.L3_accesses.append(i)
#     print_table_dict.L3_misses.append(i)
#     print_table_dict.L3_hit_rate.append(i)
#     print_table_dict.AMAT.append(i)

# print_table_dict.table3_print()