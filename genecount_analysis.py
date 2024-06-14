from statistics import mean

summary_file = "genecount_test_summary.txt"
gene_counts_data = {}

with open(summary_file, "r") as f:
    for line in f:
        # getting the respective data
        entries = line.split()
        run = int(entries[1])
        gene_count = int(entries[3])
        avg_dist = float(entries[5])

        # appending data in
        if gene_count not in gene_counts_data:
            gene_counts_data[gene_count] = []
        gene_counts_data[gene_count].append(avg_dist)

# getting mean distances for each gene_count
mean_distances = {gene_count: mean(dists) for gene_count, dists in gene_counts_data.items()}
print("average distance for each gene_count:")
for gene_count, avg_dist in mean_distances.items():
    print(f"gene_count: {gene_count}, avg_dist: {avg_dist}")

# determine best gene_count
best_gene_count = max(mean_distances, key = mean_distances.get)
print(f"\nbest gene_count {best_gene_count} has average distance of {mean_distances[best_gene_count]}")