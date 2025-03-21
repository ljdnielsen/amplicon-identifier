import sys
import glob
import dendropy
from dendropy.calculate.treecompare import symmetric_difference

# Check command-line arguments
if len(sys.argv) != 3:
    print("Usage: python compare_rf.py <mitogenome_tree> <amplicon_tree_folder>")
    sys.exit(1)

# Assign input variables
mitogenome_tree_file = sys.argv[1]
amplicon_tree_folder = sys.argv[2]

def compute_rf_distance(tree1_file, tree2_file):
    """Computes Robinson-Foulds distance between two Newick trees with a shared taxon namespace."""
    taxon_namespace = dendropy.TaxonNamespace()  # Shared namespace

    # Load both trees with the same namespace
    tree1 = dendropy.Tree.get(path=tree1_file, schema="newick", taxon_namespace=taxon_namespace)
    tree2 = dendropy.Tree.get(path=tree2_file, schema="newick", taxon_namespace=taxon_namespace)

    return symmetric_difference(tree1, tree2)

# Find all amplicon trees
amplicon_trees = glob.glob(f"{amplicon_tree_folder}/*.nwk")

# Compute RF distances
results = []
for amplicon_tree in amplicon_trees:
    rf_distance = compute_rf_distance(mitogenome_tree_file, amplicon_tree)
    results.append((amplicon_tree, rf_distance))

# Sort by lowest RF distance (best match)
results.sort(key=lambda x: x[1])

# Print results
print("\nPrimer Pair Rankings (Robinson-Foulds Distance to Full Mitogenome):")
for primer, rf in results:
    print(f"{primer}: RF Distance={rf}")

# Best primer pair
best_primer = results[0]
print(f"\nBest primer pair: {best_primer[0]} (RF Distance={best_primer[1]})")
