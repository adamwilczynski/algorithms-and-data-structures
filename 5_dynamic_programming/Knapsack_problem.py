import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from timeit import default_timer as timer

def generate_random_elements(N, M):
    l=[[0, 0] for i in range(N)]
    for i in range(N):
        l[i][0]=random.randint(1, 1000) #value
        l[i][1]=random.randint(1, int(M/2)) #size
    return l

#M - capacity of knapsack
#N - number of elements
#table_of_elements - list with value and weight of a single element
#l - table with results

def knapsack_problem(M, N, table_of_elements):
    l=[[0 for j in range (M+1)] for i in range(N+1)]
    for i in range(1, N+1):
        for j in range(M+1):
            vi=table_of_elements[i-1][0]
            wi=table_of_elements[i-1][1]
            if (wi>j):
                l[i][j]=l[i-1][j]
            else:
                l[i][j]=max(l[i-1][j], vi+l[i-1][j-wi])
    return l[N][M]

def plot_graph(listt, times, number):
    if (number==1):
        xaxis="Size of the input"
        titlee='Time of performing knapsack problem algorithm depending on size of the input'
        name="diff_sizes.png"
    else:
        xaxis="Capacity of the knapsack"
        titlee='Time of performing knapsack problem algorithm depending on capacity of the knapsack'
        name="diff_capacities.png"
    data_plot=pd.DataFrame({xaxis:listt, "Time [s]":times})
    chart = sns.lineplot(x=xaxis, y="Time [s]", data=data_plot, marker='o')
    chart.set_title(titlee, fontdict={'size': 15}, wrap=True)
    plt.yscale('log')
    plt.xscale('log')
    plt.savefig(name)
    plt.show()

list_of_capacities=[5, 10, 20, 100, 500, 2000, 5000, 10000]
list_of_elements=[5, 10, 20, 100, 500, 2000, 5000, 10000]
times_diff_capacities=[]
times_diff_nr_of_elements=[]
times_combined=[]
for i in list_of_elements:
    M=100
    table_of_elements=generate_random_elements(i, M)
    start=timer()
    print(knapsack_problem(M, i, table_of_elements))
    end=timer()
    times_diff_nr_of_elements.append(end-start)

for i in list_of_capacities:
    N=100
    table_of_elements=generate_random_elements(N, i)
    start=timer()
    print(knapsack_problem(i, N, table_of_elements))
    end=timer()
    times_diff_capacities.append(end - start)

for i in range(7):
    M=list_of_capacities[i]
    N=list_of_elements[i]
    table_of_elements=generate_random_elements(N, M)
    start=timer()
    #print(knapsack_problem(M, N, table_of_elements))
    end=timer()
    times_combined.append(end-start)

print(times_diff_nr_of_elements)
print(times_diff_capacities)
#print(times_combined)
plot_graph(list_of_elements, times_diff_nr_of_elements, 1)
plot_graph(list_of_capacities, times_diff_capacities, 2)
