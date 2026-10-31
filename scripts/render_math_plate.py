from pathlib import Path

START = (1, 1)
PAPER = "#f6f1e9"
INK = "#1b1b18"
RED = "#b73524"
MUTED = "#8c8274"


def rotate(point):
    x, y = point
    return -y, x


def reflect(point):
    x, y = point
    return x, -y


OPERATIONS = {"R": rotate, "S": reflect}
ROUTES = (("Rotate, then reflect", "RS"), ("Reflect, then rotate", "SR"))


def route_points(route):
    points = [START]
    for operation in route:
        points.append(OPERATIONS[operation](points[-1]))
    return points


def render(mobile=False):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch

    plt.rcParams.update({"font.family": "DejaVu Serif", "text.color": INK})
    fig = plt.figure(figsize=(9, 9) if mobile else (16, 6), dpi=100, facecolor=PAPER)
    if mobile:
        fig.text(0.07, 0.91, "Order matters.", fontsize=43)
        fig.text(0.07, 0.81, "Start at the ringed corner (1, 1).", fontsize=22)
        slots = ((0.07, 0.22, 0.37, 0.41), (0.56, 0.22, 0.37, 0.41))
        fig.text(0.07, 0.11, "R = quarter-turn anticlockwise", fontsize=20)
        fig.text(0.07, 0.06, "S = reflect across the horizontal axis", fontsize=20)
    else:
        fig.text(0.045, 0.75, "Same moves.", fontsize=41)
        fig.text(0.045, 0.60, "Different result.", fontsize=41)
        fig.text(0.045, 0.35, "R = quarter-turn anticlockwise", fontsize=17)
        fig.text(0.045, 0.27, "S = reflect across the horizontal axis", fontsize=17)
        fig.text(
            0.045, 0.12, "Start at the ringed corner (1, 1).", fontsize=16, color=MUTED
        )
        slots = ((0.44, 0.19, 0.23, 0.60), (0.73, 0.19, 0.23, 0.60))

    for (heading, route), slot in zip(ROUTES, slots):
        ax = fig.add_axes(slot, facecolor=PAPER)
        ax.set_aspect("equal")
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.6, 1.6)
        ax.axis("off")
        ax.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], color=INK, linewidth=1.6)
        ax.plot([-1.4, 1.4], [0, 0], color="#d3c8b8", linewidth=0.8)
        ax.plot([0, 0], [-1.4, 1.4], color="#d3c8b8", linewidth=0.8)
        points = route_points(route)
        ax.scatter(*zip(*points), s=35, color=MUTED, zorder=3)
        ax.scatter(
            *START, s=220, facecolors="none", edgecolors=MUTED, linewidths=1.5, zorder=6
        )
        for operation, start, end in zip(route, points, points[1:]):
            color = INK if operation == "R" else RED
            ax.add_patch(
                FancyArrowPatch(
                    start,
                    end,
                    connectionstyle="arc3,rad=0.28"
                    if operation == "R"
                    else "arc3,rad=0",
                    arrowstyle="-|>",
                    mutation_scale=18,
                    linewidth=2.0,
                    color=color,
                    shrinkA=9,
                    shrinkB=9,
                    zorder=4,
                )
            )
            midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
            dx, dy = end[0] - start[0], end[1] - start[1]
            offset = (
                (0.2 * dy, -0.2 * dx) if operation == "R" else (-0.22 * start[0], 0)
            )
            ax.text(
                midpoint[0] + offset[0],
                midpoint[1] + offset[1],
                operation,
                fontsize=22,
                color=color,
                ha="center",
                va="center",
            )
        ax.scatter(
            *points[-1], s=145, color=RED, edgecolors=PAPER, linewidths=1.5, zorder=5
        )
        title = heading.replace(", then ", "\nthen ") if mobile else heading
        ax.set_title(title, fontsize=23 if mobile else 19, pad=14)
        fig.text(
            slot[0] + slot[2] / 2,
            slot[1] - 0.035,
            f"Ends at {points[-1]}",
            ha="center",
            fontsize=22 if mobile else 18,
            color=RED,
        )

    name = "order-matters-mobile.png" if mobile else "order-matters.png"
    fig.savefig(Path(__file__).parents[1] / "assets" / name, facecolor=PAPER)
    plt.close(fig)


if __name__ == "__main__":
    render()
    render(mobile=True)
