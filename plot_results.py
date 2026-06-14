import pickle, matplotlib.pyplot as plt, seaborn as sns

with open("eval_results.pkl", "rb") as f:
    res = pickle.load(f)

if "decentralised_latencies" in res:
    plt.figure()
    sns.histplot(res["decentralised_latencies"], bins=15, kde=True)
    plt.title("Decentralised Authentication Latency (ms)")
    plt.xlabel("Latency (ms)")
    plt.savefig("latency_hist.png")
    print("Saved latency_hist.png")

print(f"Replay resistant: {res.get('replay_resistant')}")
print(f"Fault tolerant: {res.get('fault_tolerant')}")