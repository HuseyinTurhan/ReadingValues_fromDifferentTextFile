import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import re
import os
import itertools
import argparse 

dict_run = {}
dict_load = {}
def Threadsing(filename):
    for i in ["t1", "t2", "t4", "t8"]:
        if i in filename:
            return i[1]

def versioning(filename):
    for i in ["sdrob", "native", "tlsf"]:
        if i in filename:
            return i

def percentage(df):
    dict_vals = {}
    for Threads in ["1","2","4","8"]:
        native_over_tlsf = 100- ((float((df[(df["Threads"] == Threads) & (df["version"] == "tlsf")]["Throughput (ops/sec)"]).mean()) *100) / float((df[(df["Threads"] == Threads) & (df["version"] == "native")]["Throughput (ops/sec)"]).mean()))
        tlsf_over_sdrob =  100- ((float((df[(df["Threads"] == Threads) & (df["version"] == "sdrob")]["Throughput (ops/sec)"]).mean())*100) / float((df[(df["Threads"] == Threads) & (df["version"] == "tlsf")]["Throughput (ops/sec)"]).mean()))     
        native_over_sdrob = 100- ((float((df[(df["Threads"] == Threads) & (df["version"] == "sdrob")]["Throughput (ops/sec)"]).mean())*100) / float((df[(df["Threads"] == Threads) & (df["version"] == "native")]["Throughput (ops/sec)"]).mean()))    
        dict_vals[Threads] = {"native/tlsf" : native_over_tlsf,
                            "tlsf/sdrob" : tlsf_over_sdrob,
                            "native/sdrob" : native_over_sdrob}
        return dict_vals

def main():
    list_run = []
    list_load = []
    g,h,x = 0,0,0
    path2 = os.getcwd() 
    path2 = path2 #+ path 
    os.chdir(path2)
    for filename in os.listdir(path2):
        if filename.endswith(".txt"):
            with open(filename, 'r') as fp:
                x = fp.readlines()[1]
                print(fp)
                print(x)
                temp = float(re.findall("\d+\.\d+", x)[0])
            if "load" in filename:
                version = versioning(filename)
                Threads = Threadsing(filename)
                dict_load[h] = {'Throughput (ops/sec)': temp,
                                'version':version,
                                'Threads':Threads}
                h+=1
            elif "run" in filename:
                version = versioning(filename)
                Threads = Threadsing(filename)
                dict_run[g] = {"Throughput (ops/sec)": temp,
                                "version":version,
                                "Threads":Threads}
                g+=1
            else:
                    print("You must check the txt filename!! It doesn't contain LOAD or RUN words.")
        else:
            continue

    df_run = pd.DataFrame(dict_run).T
    df_load = pd.DataFrame(dict_load).T
    dict_to_excel = {}
    dict_to_excel["run"] = percentage(df_run)
    dict_to_excel["load"] = percentage(df_load)
    df_to_excel = pd.concat({k: pd.DataFrame.from_dict(v, 'index') for k, v in dict_to_excel.items()}, axis=0)
    df_to_excel.to_excel("output.xlsx")


    fig, (ax0, ax1) = plt.subplots(
    nrows=1, ncols=2, sharex=False, sharey=True, figsize=(12,6))
    sns.set(style = 'whitegrid', palette="colorblind")

    sns.barplot(x='Threads', y='Throughput (ops/sec)', hue='version', 
            data=df_load, ax=ax0, order=["1", "2", "4", "8"], hue_order=["native", "tlsf", "sdrob"])
    sns.barplot(x='Threads', y='Throughput (ops/sec)', hue='version', 
            data=df_run, ax=ax1, order=["1", "2", "4", "8"], hue_order=["native", "tlsf", "sdrob"])


    num_locations = len(df_run.Threads.unique())
    hatches = itertools.cycle(['//', 'xx', '++'])
    for i, bar in enumerate(ax0.patches):
        if i % num_locations == 0:
            hatch = next(hatches)
        bar.set_hatch(hatch)
    for i, bar in enumerate(ax1.patches):
        if i % num_locations == 0:
            hatch = next(hatches)
        bar.set_hatch(hatch)
    ax0.set(xlabel="LOADING PHASE")
    ax1.set(xlabel="RUNNING PHASE")
    ax0.legend(title= "version")
    ax1.legend(title= "version")
    plt.savefig('figure.png')
    plt.show()

if __name__ == "__main__":
    main()
