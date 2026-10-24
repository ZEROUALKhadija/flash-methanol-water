from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def plot_process_diagram(output_path):
    """Schéma simplifié : chauffage puis séparateur flash."""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    def box(x, y, w, h, label):
        patch = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.08",
            edgecolor="black",
            facecolor="white",
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, label,
                ha="center", va="center", fontsize=10)

    def arrow(start, end):
        ax.add_patch(FancyArrowPatch(
            start, end, arrowstyle="->",
            mutation_scale=15, color="black",
        ))

    box(0.3, 1.5, 1.5, 0.8, "Alimentation\n25 °C")
    box(3.0, 1.5, 1.5, 0.8, "Chauffage\n80 °C")
    box(5.8, 1.3, 1.5, 1.2, "Séparateur\nflash")

    arrow((1.8, 1.9), (3.0, 1.9))
    arrow((4.5, 1.9), (5.8, 1.9))
    arrow((7.3, 2.1), (8.7, 3.0))
    arrow((7.3, 1.6), (8.7, 0.8))

    ax.text(8.8, 3.1, "Vapeur", ha="center")
    ax.text(8.8, 0.6, "Liquide", ha="center")

    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_binary_diagram(result, output_path):
    """
    Représente les compositions calculées à la condition opératoire.
    Ce graphique n'est pas une enveloppe complète T-x-y.
    """
    labels = ["Eau", "Méthanol"]
    x = result["x_liquid"]
    y = result["y_vapor"]

    fig, ax = plt.subplots(figsize=(7, 5))
    pos = range(2)
    width = 0.35

    ax.bar([p - width / 2 for p in pos], x, width,
           label="Phase liquide")
    ax.bar([p + width / 2 for p in pos], y, width,
           label="Phase vapeur")

    ax.set_xticks(list(pos))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Fraction molaire")
    ax.set_ylim(0, 1)
    ax.set_title("Compositions liquide et vapeur à 80 °C")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)

    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)