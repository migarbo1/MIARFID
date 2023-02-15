import matplotlib.pyplot as plt
import numpy as np

ppl_3 = [83.18104,80.58081,78.99527]
ppl_4 = [75.52358,73.14549,71.70051]
models = [ppl_3, ppl_4]
names = ['N=3','N=4']
freq = [1,5,9]
plt.xlabel('Freq. of removed words')
plt.ylabel('Perplexity')

for i in range(len(models)):
    ppl = models[i]
    plt.plot(freq, ppl, label=names[i])

plt.title('Perplexity over EuroParl modifying vocabulary size')
plt.legend()
plt.show()





#plot task 2
#ppl_KN = [8.323726,7.95679]
#ppl_WB = [7.831292,7.151701]
#ppl_UKN = [7.65308,7.039372]
#ppl_GT = [7.677726, 7.226808]
#models = [ppl_KN, ppl_WB, ppl_GT, ppl_UKN]
#names = ['Kneser-Ney','Witten-Bell', 'Good-Turing', 'Unmod Kneser-Ney']
#axis = np.arange(2)
#width = 0.2
#ngram = [3,4]
#plt.xlabel('n-grams')
#plt.ylabel('perplexity')
#plt.xticks(axis+width, ngram)

#for i in range(len(models)):
#    ppl = models[i]
#    plt.bar(axis+width*i, ppl, width, label=names[i])

#plt.title('Perplexity over Dihana with diffent discount methods')
#plt.legend()
#plt.show()


#plot task 3
#ppl_KN = [8.323726,7.95679]
#ppl_WB = [7.831292,7.151701]
#ppl_KN_inter = [7.704635,7.015106]
#ppl_WB_inter = [7.364972, 6.576761]
#models = [ppl_KN, ppl_KN_inter, ppl_WB, ppl_WB_inter]
#colors = ['tan', 'teal', 'wheat', 'lightblue']
#names = ['K-N Backoff','K-N interpolated', 'W-B Backoff', 'W-B interpolated']
#axis = np.arange(2)
#width = 0.2
#ngram = [3,4]
#plt.xlabel('n-grams')
#plt.ylabel('perplexity')
#plt.xticks(axis+width*3/2, ngram)
#inner_space = 0

#for i in range(len(models)):
#    ppl = models[i]
#    inner_space += 0.05 if i > 1 and i%2 == 0 else 0
#    plt.bar(axis+width*i+inner_space, ppl, width, label=names[i], color = colors[i])

#plt.title('Perplexity over Dihana with different smoothing methods')
#plt.legend()
#plt.show()


#plot task 4
#freq_1 = [445.9889,436.2709]
#freq_5 = [365.6272,357.5508]
#freq_9 = [358.49,350.5818]
#axis = np.arange(2) 
#width = 0.25
#ngram = [3,4]
#plt.xlabel('n-grams')
#plt.ylabel('perplexity')
#plt.xticks(axis+width, ngram)
#plt.bar(axis, freq_1, width, label='Words freq > 1')
#plt.bar(axis+width, freq_5, width, label='Words freq > 5')
#plt.bar(axis+width*2, freq_9, width, label = 'Words freq > 9')
#plt.title('Perplexity over Europarl with modified vocabulary')
#plt.legend()
#plt.show()
