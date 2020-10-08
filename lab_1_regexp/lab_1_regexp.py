import re
import os
from collections import defaultdict
import numpy as np
import matplotlib.ticker as mtick
from matplotlib import pyplot as plt

def get_texts_dataset(dataset_path):
    filenames = os.listdir(dataset_path)
    texts = []
    text_names = []
    for filename in filenames:
        file_path = os.path.join(dataset_path, filename)
        with open(file_path) as current_file:
            texts.append(current_file.read())
            text_names.append(filename)
    return text_names, texts

def count_by_year(file_labels,counts_by_document):
    counts_by_year = defaultdict(lambda: 0)
    for fname, count in zip(file_labels, counts_by_document):
        key = fname.split("_")[0]
        counts_by_year[key] += count
    return counts_by_year


data_dir = os.path.join("..", "data", "ustawy")
file_labels, dataset = get_texts_dataset(data_dir)

dodaje_sie = r"(dodaje[\s\n]*si[eę][\s\n]*(art[\.\n\s]|ust[\.\n\s]|pkt[\.\n\s]|lit|zdanie|§|rozdzia[lł]|dzia[lł]))"
out_dodaje_sie = map(lambda x: re.findall(dodaje_sie, x, re.IGNORECASE), dataset)
counts_dodaje_sie = list(map(lambda x: len(x), out_dodaje_sie))
counts_by_year_dodaje_sie = count_by_year(file_labels, counts_dodaje_sie)
print(counts_by_year_dodaje_sie)
print(sum(counts_by_year_dodaje_sie.values()))

skresla_sie = r"((art[\.\n\s]|ust[\.\n\s]|pkt[\.\n\s]|lit|zdanie|§|rozdzia[lł]|dzia[lł])([\s\n]*[\w-]*[\s\n]*)skre[sś]la[\s\n]*si[eę]|skre[sś]la[\s\n]*si[eę][\s\n]*(art[\.\n\s]|ust[\.\n\s]|pkt[\.\n\s]|lit|zdanie|§|rozdzia[lł]|dzia[lł]))"
out_skresla_sie = map(lambda x: re.findall(skresla_sie, x, re.IGNORECASE), dataset)
counts_skresla_sie = list(map(lambda x: len(x), out_skresla_sie))
counts_by_year_skresla_sie = count_by_year(file_labels, counts_skresla_sie)
print(counts_by_year_skresla_sie)
print(sum(counts_skresla_sie))

otrzymuje = r"(art[\.\n\s]|ust[\.\n\s]|pkt[\.\n\s]|lit|zdanie|§|rozdzia[lł]|dzia[lł])([\s\n]*[\w-]*[\s\n]*)otrzymuje[\s\n]*brzmienie"
out_otrzymuje = map(lambda x: re.findall(otrzymuje, x, re.IGNORECASE), dataset)
counts_otrzymuje = list(map(lambda x: len(x), out_otrzymuje))
counts_by_year_otrzymuje = count_by_year(file_labels, counts_otrzymuje)
print(counts_by_year_otrzymuje)
print(sum(counts_otrzymuje))

# plotting
years = np.array(list(counts_by_year_dodaje_sie.keys()))
order = [x[0] for x in sorted(list(enumerate(years)), key=lambda x: x[1])]
c_d = np.array(list(counts_by_year_dodaje_sie.values()))
c_s = np.array(list(counts_by_year_skresla_sie.values()))
c_o = np.array(list(counts_by_year_otrzymuje.values()))
totals = np.array(c_d+c_s+c_o)
s_c_d = c_d / totals
s_c_s = c_s / totals
s_c_o = c_o / totals

fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.bar(years[order], s_c_d[order], label="percent added")
ax.bar(years[order], s_c_s[order], bottom=s_c_d[order], label="percent removed")
ax.bar(years[order], s_c_o[order], bottom=s_c_d[order] + s_c_s[order], label="percent changed")
plt.ylabel('Bill amendments percentage')
plt.xlabel('Year')
plt.title('Bill amendment percentage change by years')
plt.legend()
plt.show()

ustawa = r"(ustaw([aoyeęą]|a(mi|ch)|om|ie)?\W)"
ustawa_z = r"(ustaw([aoyeęą]|a(mi|ch)|om|ie)?\W(?=z[\n\s]dnia))"
ustawa_n = r"(ustaw([aoyeęą]|a(mi|ch)|om|ie)?\W(?!z[\n\s]dnia))"
o_ustawa = r"((?<!o[\n\s]zmianie[\n\s])(ustaw([aoyeęą]|a(mi|ch)|om|ie)?\W))"
out_ustawa = map(lambda x: re.findall(ustawa, x, re.IGNORECASE), dataset)
out_ustawa_z = map(lambda x: re.findall(ustawa_z, x, re.IGNORECASE), dataset)
out_ustawa_n = map(lambda x: re.findall(ustawa_n, x, re.IGNORECASE), dataset)
out_o_ustawa = map(lambda x: re.findall(o_ustawa, x, re.IGNORECASE), dataset)
counts_ustawa = sum(map(lambda x: len(x), out_ustawa))
counts_ustawa_z = sum(map(lambda x: len(x), out_ustawa_z))
counts_ustawa_n = sum(map(lambda x: len(x), out_ustawa_n))
counts_o_ustawa = sum(map(lambda x: len(x), out_o_ustawa))
print("liczba wystąpień:\n"
      "\tustawa:\t{0}\n"
      "\tustawa+\"z dnia\": {1}\n"
      "\tustawa-\"z dnia\": {2}\n"
      "\tsuma:\t{3}\n"
      "\t-\"o zmianie\"ustawa: {4}".format(counts_ustawa,
                             counts_ustawa_z,
                             counts_ustawa_n,
                             counts_ustawa_z + counts_ustawa_n,
                             counts_o_ustawa))

fig, ax = plt.subplots()
ax.bar(["ustawa"],
       [counts_ustawa])
ax.bar(["ustawa+\"z dnia\""],
       [counts_ustawa_z])
ax.bar(["ustawa-\"z dnia\""],
       [counts_ustawa_n])
ax.bar(["-\"o zmianie\"ustawa"],
       [counts_o_ustawa])
plt.ylabel('Number of occurrences')
plt.xlabel('Pattern type')
plt.title('Number of occurrences of given patterns')
plt.show()