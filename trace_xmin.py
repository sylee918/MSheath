import subprocess

for xmin in [-10.0, -5.0, -2.0, -1.0, 0.0]:
    cmd = f"""1
400.0 5.0 10.0 0.0 0.0 5.0 0.0
{xmin} 0.0 1.0 -15.0 -15.0 1.0
test_trace.dat
"""
    p = subprocess.run(
        ["wsl", "-d", "Ubuntu-22.04", "--", "bash", "-c",
         f"cd '/mnt/c/Users/slee122/OneDrive - NASA/Desktop/Work/JSokol/MSheath' && printf '{cmd}' | ./msh_calc_grid"],
        capture_output=True, text=True
    )
    with open('test_trace.dat') as f:
        lines = [l for l in f if not l.startswith('#')]
    last_line = lines[-1].split()
    print(f"xmin={xmin:5.1f} -> X={last_line[0]}, Z={last_line[2]}, DEN={last_line[3]}")
