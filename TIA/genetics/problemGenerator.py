import json
import random

n_tasks = 85
alpha = 0.65

roles = ["J", "S", "C"]
prices_hour = {"J": 19000/8760.0, "S":29615/8760.0, "C":37953/8760.0}
gen_tasks = []
total_hours = 0
total_cost = 0
for i in range(n_tasks):
    role_index =  random.randint(0,len(roles)-1)
    hours = random.randint(3,15)
    role = roles[role_index]
    total_hours += hours
    total_cost += hours*prices_hour[role]
    task={"t":hours,'r':role}
    gen_tasks.append(task)

jsonString = json.dumps(gen_tasks)
jsonFile = open("problem{}.json".format(n_tasks), "w")
jsonFile.write(jsonString)
jsonFile.close()
print("hours:", total_hours)
print("cost:", total_cost)
print("fitness:",alpha * total_hours + (1-alpha) * total_cost)