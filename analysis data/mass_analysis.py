from statistics import mean

summary_file = "analysis data/weight_test_summary.txt"
weights_data = {}

with open(summary_file, "r") as f:
    for line in f:
        # getting the respective data
        entries = line.split()
        print(entries)
        weight = float(entries[3])
        avg_dist = float(entries[5])

        # appending data in
        if weight not in weights_data:
            weights_data[weight] = []
        weights_data[weight].append(avg_dist)

# getting mean distances for each weight
mean_distances = {weight: mean(dists) for weight, dists in weights_data.items()}
print("average distance for each weight:")
for weight, avg_dist in mean_distances.items():
    print(f"weight: {weight}, avg_dist: {avg_dist}")

# determine best weight
best_weight = max(mean_distances, key = mean_distances.get)
print(f"\nbest weight {best_weight} has average distance of {mean_distances[best_weight]}")