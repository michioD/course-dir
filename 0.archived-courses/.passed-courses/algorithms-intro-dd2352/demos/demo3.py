import itertools
import heapq

def can_schedule(tasks, f):
    """
    Checks if a given list of tasks can be scheduled.
    tasks: list of tuples (start_day, deadline)
    f: max homeworks per day
    """
    # Sort tasks primarily by start day
    tasks.sort(key=lambda x: x[0])
    
    pq = [] # Min-heap to store deadlines of available tasks
    task_idx = 0
    n = len(tasks)
    
    current_day = -1
    slots_used = 0
    
    # Process until all tasks are pushed to PQ and the PQ is empty
    while task_idx < n or pq:
        # If no tasks are currently available, jump time forward to the next task's start day
        if not pq:
            next_s = tasks[task_idx][0]
            if current_day < next_s:
                current_day = next_s
                slots_used = 0 # New day, reset capacity
        
        # Push all tasks that have started by 'current_day' into the priority queue
        while task_idx < n and tasks[task_idx][0] <= current_day:
            heapq.heappush(pq, tasks[task_idx][1]) # Push the deadline
            task_idx += 1
            
        # Process the available task with the earliest deadline (Greedy EDF)
        if pq:
            d = heapq.heappop(pq)
            
            # If the earliest deadline has already passed, scheduling is impossible
            if d < current_day:
                return False
                
            slots_used += 1
            
            # If we've hit our daily capacity, advance to the next day
            if slots_used == f:
                current_day += 1
                slots_used = 0
                
    return True

def plan_courses(n, s, d, c, f):
    """
    Finds the smallest set of courses to fail.
    n: total number of homeworks
    s: list of start days
    d: list of deadlines
    c: list of course IDs (1 to 5)
    f: max homeworks per day
    """
    courses = [1, 2, 3, 4, 5]
    min_failed_count = 6
    best_failed_set = []
    
    # Test all combinations of courses to pass, from size 5 down to 0
    for r in range(5, -1, -1):
        # Optimization: skip if we've already found a valid set with fewer or equal failures
        if 5 - r >= min_failed_count:
            continue
            
        for passed_subset in itertools.combinations(courses, r):
            passed_set = set(passed_subset)
            
            # Extract all homeworks for the courses we are trying to pass
            tasks = []
            for i in range(n):
                if c[i] in passed_set:
                    tasks.append((s[i], d[i]))
                    
            # Check if this subset of homeworks is schedulable
            if can_schedule(tasks, f):
                failed_set = [course for course in courses if course not in passed_set]
                if len(failed_set) < min_failed_count:
                    min_failed_count = len(failed_set)
                    best_failed_set = failed_set
                    
    return best_failed_set

# --- Testing with the provided example ---
f_example = 2
n_example = 7
s_example = [10, 12, 10, 12, 11, 11, 11]
d_example = [11, 12, 11, 12, 12, 12, 12]
c_example = [1, 1, 2, 2, 3, 3, 4]

failed_courses = plan_courses(n_example, s_example, d_example, c_example, f_example)
print(f"Smallest set of courses to fail: {failed_courses}") 
# Expected Output: [3] (meaning he passes {1, 2, 4, 5})
