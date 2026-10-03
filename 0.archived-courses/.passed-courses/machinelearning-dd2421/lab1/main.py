import monkdata as m
import dtree as d
import random
import matplotlib.pyplot as plt
import numpy as np
import drawtree_qt5 as qt5
# Set seed for reproducibility (optional, but good for debugging)
random.seed(42)

def partition(data, fraction):
    """
    Partitions the data into training and validation sets.
    """
    ldata = list(data)
    random.shuffle(ldata)
    breakPoint = int(len(ldata) * fraction)
    return ldata[:breakPoint], ldata[breakPoint:]

def prune_tree(tree, validation_data):
    """
    Iteratively prunes the tree to maximize accuracy on validation_data.
    """
    current_tree = tree
    best_acc = d.check(current_tree, validation_data)
    
    while True:
        alternatives = d.allPruned(current_tree)
        if not alternatives:
            break
            
        # Find the best pruned candidate
        best_candidate = max(alternatives, key=lambda t: d.check(t, validation_data))
        candidate_acc = d.check(best_candidate, validation_data)
        
        if candidate_acc >= best_acc:
            current_tree = best_candidate
            best_acc = candidate_acc
        else:
            break # Stop if no improvement
            
    return current_tree

def assignment_1():
    print("=== Assignment 1: Entropy ===")
    print(f"Entropy Monk-1: {d.entropy(m.monk1):.6f}")
    print(f"Entropy Monk-2: {d.entropy(m.monk2):.6f}")
    print(f"Entropy Monk-3: {d.entropy(m.monk3):.6f}")
    print()

def assignment_3():
    print("=== Assignment 3: Information Gain ===")
    datasets = [("Monk-1", m.monk1), ("Monk-2", m.monk2), ("Monk-3", m.monk3)]
    
    print(f"{'Dataset':<10} {'A1':<10} {'A2':<10} {'A3':<10} {'A4':<10} {'A5':<10} {'A6':<10}")
    for name, data in datasets:
        gains = [d.averageGain(data, attr) for attr in m.attributes]
        row = f"{name:<10} " + " ".join(f"{g:.6f}  " for g in gains)
        print(row)
    print()

def assignment_5():
    print("=== Assignment 5: Full Tree Performance ===")
    datasets = [
        ("Monk-1", m.monk1, m.monk1test),
        ("Monk-2", m.monk2, m.monk2test),
        ("Monk-3", m.monk3, m.monk3test)
    ]
    
    print(f"{'Dataset':<10} {'E_train':<10} {'E_test':<10}")
    for name, train, test in datasets:
        t = d.buildTree(train, m.attributes)
        e_train = 1 - d.check(t, train)
        e_test = 1 - d.check(t, test)
        print(f"{name:<10} {e_train:<10.6f} {e_test:<10.6f}")
    print()

def assignment_7():
    print("=== Assignment 7: Pruning Analysis ===")
    fractions = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    iterations = 5000  # Number of runs per fraction
    
    results_m1 = {'mean': [], 'std': []}
    results_m3 = {'mean': [], 'std': []}
    
    print(f"Running {iterations} iterations per fraction. This may take a moment...")
    
    for frac in fractions:
        errors_m1 = []
        errors_m3 = []
        
        for _ in range(iterations):
            # Monk 1
            train_m1, val_m1 = partition(m.monk1, frac)
            t1 = d.buildTree(train_m1, m.attributes)
            pruned_t1 = prune_tree(t1, val_m1)
            errors_m1.append(1 - d.check(pruned_t1, m.monk1test))
            
            # Monk 3
            train_m3, val_m3 = partition(m.monk3, frac)
            t3 = d.buildTree(train_m3, m.attributes)
            pruned_t3 = prune_tree(t3, val_m3)
            errors_m3.append(1 - d.check(pruned_t3, m.monk3test))
            
        # Store stats
        results_m1['mean'].append(np.mean(errors_m1))
        results_m1['std'].append(np.std(errors_m1))
        results_m3['mean'].append(np.mean(errors_m3))
        results_m3['std'].append(np.std(errors_m3))
        
        print(f"Fraction {frac}: M1_Err={results_m1['mean'][-1]:.4f}, M3_Err={results_m3['mean'][-1]:.4f}")

    # --- NEW: Plotting with 2 subplots ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Subplot 1: Mean Error
    ax1.errorbar(fractions, results_m1['mean'], yerr=results_m1['std'], label='Monk-1', marker='o', capsize=5)
    ax1.errorbar(fractions, results_m3['mean'], yerr=results_m3['std'], label='Monk-3', marker='^', capsize=5)
    ax1.set_title(f'Mean Test Error (n={iterations})')
    ax1.set_xlabel('Training Fraction')
    ax1.set_ylabel('Mean Test Error')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Subplot 2: Standard Deviation
    ax2.plot(fractions, results_m1['std'], label='Monk-1', marker='o', color='C0')
    ax2.plot(fractions, results_m3['std'], label='Monk-3', marker='^', color='C1')
    ax2.set_title(f'Standard Deviation of Error (n={iterations})')
    ax2.set_xlabel('Training Fraction')
    ax2.set_ylabel('Standard Deviation')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('image1.png')
    print("\nPlot saved as 'image1.png'\n")

def visualize_pruned_tree():
    print("=== Visualizing Pruned Tree for MONK-1 (Fraction 0.6) ===")
    
    # 1. Partition the data (60% training, 40% validation)
    train_m1, val_m1 = partition(m.monk3, 0.7)
    
    # 2. Build the initial full tree
    t1 = d.buildTree(train_m1, m.attributes)
    
    # 3. Prune the tree using your pruning logic
    pruned_t1 = prune_tree(t1, val_m1)
    
    # 4. Draw the pruned tree
    print("Opening UI window to display the tree. Close the window to continue...")
    qt5.drawTree(pruned_t1)
if __name__ == "__main__":
    assignment_1()
    assignment_3()
    assignment_5()
    assignment_7()
    # visualize_pruned_tree()
