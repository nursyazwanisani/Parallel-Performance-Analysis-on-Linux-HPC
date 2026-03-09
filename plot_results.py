import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

processors = [1, 2, 4]
times_strong = [0.422, 0.230, 0.122]

speedup = [times_strong[0]/t for t in times_strong]
efficiency = [s/p for s, p in zip(speedup, processors)]
ideal = processors

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].plot(processors, speedup, 'bo-', label='Actual')
axes[0].plot(processors, ideal, 'r--', label='Ideal')
axes[0].set_xlabel('Number of Processors')
axes[0].set_ylabel('Speedup')
axes[0].set_title('Strong Scaling: Speedup')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].bar(processors, efficiency, color='steelblue')
axes[1].axhline(y=1.0, color='r', linestyle='--')
axes[1].set_xlabel('Number of Processors')
axes[1].set_ylabel('Efficiency')
axes[1].set_title('Strong Scaling: Efficiency')
axes[1].set_ylim(0, 1.2)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('plots/strong_scaling.png', dpi=150)
print('Saved plots/strong_scaling.png')

processors_w = [1, 2, 4]
times_weak = [0.432, 0.445, 0.476]
efficiency_w = [times_weak[0]/t for t in times_weak]

fig2, ax = plt.subplots(figsize=(8, 5))
ax.plot(processors_w, efficiency_w, 'go-', label='Actual', linewidth=2)
ax.axhline(y=1.0, color='r', linestyle='--', label='Ideal')
ax.set_xlabel('Number of Processors')
ax.set_ylabel('Efficiency')
ax.set_title('Weak Scaling: Efficiency')
ax.set_ylim(0, 1.2)
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('plots/weak_scaling.png', dpi=150)
print('Saved plots/weak_scaling.png')
