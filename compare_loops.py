with open('trace_bug2.for') as f1, open('msh_combined.for') as f2:
    t1 = "".join(f1.readlines()[:180])
    t2 = "".join(f2.readlines()[:259])

with open('loop1.txt', 'w') as f:
    f.write(t1)
with open('loop2.txt', 'w') as f:
    f.write(t2)
print("Wrote loop1.txt and loop2.txt")
