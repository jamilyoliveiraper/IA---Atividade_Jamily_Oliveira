import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Ellipse

pos = {"Str": (1, 4), "Flw": (4, 4), "R": (2.5, 2.7), "V": (2.5, 1.4),
       "B": (5.2, 1.4), "K": (7.2, 1.4), "Li": (4.8, 0)}
edges = [("Str","R"),("Flw","R"),("R","V"),("V","Li"),("B","Li"),("K","Li")]
fig, ax = plt.subplots(figsize=(7, 4.6)); ax.axis("off"); ax.set_xlim(0, 8.2); ax.set_ylim(-0.8, 4.8)
for n,(x,y) in pos.items():
    ax.add_patch(Ellipse((x,y),1.2,0.7,fc="#dbe9ff",ec="#1f4e99",lw=1.5,zorder=2))
    ax.text(x,y,n,ha="center",va="center",fontsize=13,fontweight="bold",zorder=3)
for a,b in edges:
    ax.add_patch(FancyArrowPatch(pos[a],pos[b],arrowstyle="-|>",mutation_scale=16,
        shrinkA=22,shrinkB=22,lw=1.5,color="#333",zorder=1))
plt.savefig("rede_bayesiana.png", dpi=200, bbox_inches="tight")
