from statistics import mean

summary_file = "analysis data/len_rad_test_summary.txt"
link_data = {}

with open(summary_file, "r") as f:
    for line in f:
        # getting the respective data
        entries = line.split()
        l_length = float(entries[1])
        l_radius = float(entries[3])
        avg_dist = float(entries[5])

        # appending data in
        if l_length not in link_data:
            link_data[l_length] = {}
        if l_radius not in link_data[l_length]:
            link_data[l_length][l_radius] = []

        link_data[l_length][l_radius].append(avg_dist)

# getting mean distances for each link_length + link_radius
mean_distances = {
    l_length: {
        l_radius: mean(dists) for l_radius, dists in link_data[l_length].items()
    }
    for l_length in link_data
}
print("average distance for each link_length and link_radius combinations:")
for l_length, radii in mean_distances.items():
    for l_radius, avg_dist in radii.items():
        print(f"link_length: {l_length}, link_radius: {l_radius}, avg_dist: {avg_dist}")

# determine best link_length + link_radius combination
best_combi = max(
    ((l_length, l_radius, avg_dist) 
     for l_length, radii in mean_distances.items() 
     for l_radius, avg_dist in radii.items()),
     key = lambda x: x[2]
)

best_l_length, best_l_radius, best_avg_dist = best_combi
print(f"\nbest combination: link_length = {best_l_length}, link_radius = {best_l_radius}\naverage distance: {best_avg_dist}")