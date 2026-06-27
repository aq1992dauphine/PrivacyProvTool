import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def build_timing_dataframe() -> pd.DataFrame:
    """
    Build the Cypher query timing table.

    Values are runtimes in milliseconds.
    Missing German graph-summary timing is represented as NaN.
    """

    data = {
        "Query": [
            "Graph summary",
            "Manual-gold comparison",
            "Erasure impact",
            "Sensitivity exposure",
            "Transformation responsibility",
            "Consent / purpose-compliance",
            "Data minimisation",
            "Role-aware visibility",
            "Role-aware visible subgraph",
            "Propagation coverage",
            "Operator coverage",
        ],
        "ASD": [
            7, 2, 4, 3, 3, 3, 3, 4, 4, 4, 2
        ],
        "Census": [
            30, 3, 4, 2, 6, 7, 3, 7, 20, 6, 2
        ],
        "COMPAS": [
            30, 4, 3, 2, 3, 5, 2, 5, 8, 3, 1
        ],
        "German": [
            np.nan, 3, 5, 2, 8, 7, 3, 7, 20, 7, 1
        ],
    }

    df = pd.DataFrame(data)
    df["Mean"] = df[["ASD", "Census", "COMPAS", "German"]].mean(axis=1, skipna=True)
    return df


def create_heatmap(df: pd.DataFrame, output_dir: Path) -> None:
    """
    Create a compact annotated heatmap.

    This is the most suitable version for an LNCS paper because it is dense,
    readable, and directly compares query types across pipelines.
    """

    pipelines = ["ASD", "Census", "COMPAS", "German"]
    values = df[pipelines].to_numpy(dtype=float)

    fig, ax = plt.subplots(figsize=(9.2, 5.6))

    # Mask missing values for display.
    masked_values = np.ma.masked_invalid(values)
    im = ax.imshow(masked_values, aspect="auto")

    ax.set_xticks(np.arange(len(pipelines)))
    ax.set_xticklabels(pipelines)

    ax.set_yticks(np.arange(len(df)))
    ax.set_yticklabels(df["Query"])

    ax.set_xlabel("Pipeline")
    ax.set_title("Cypher Query Runtime over Privacy-Aware Provenance Graphs")

    # Annotate every cell.
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            if np.isnan(values[i, j]):
                text = "n/a"
            else:
                text = f"{int(values[i, j])} ms"
            ax.text(j, i, text, ha="center", va="center", fontsize=8)

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Runtime (ms)")

    ax.text(
        0.99,
        -0.12,
        "Note: German graph-summary timing was not provided.",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=8,
    )

    fig.tight_layout()

    fig.savefig(output_dir / "cypher_query_timings_heatmap.png", dpi=300, bbox_inches="tight")
    fig.savefig(output_dir / "cypher_query_timings_heatmap.pdf", bbox_inches="tight")
    plt.close(fig)


def create_grouped_bar_chart(df: pd.DataFrame, output_dir: Path) -> None:
    """
    Create a grouped horizontal bar chart.

    This is useful as a presentation figure, because it clearly shows
    which query types are more expensive.
    """

    pipelines = ["ASD", "Census", "COMPAS", "German"]

    # Sort by mean runtime so the most expensive query groups appear first.
    plot_df = df.sort_values("Mean", ascending=False).reset_index(drop=True)

    y = np.arange(len(plot_df))
    bar_height = 0.18
    offsets = np.array([-1.5, -0.5, 0.5, 1.5]) * bar_height

    fig, ax = plt.subplots(figsize=(9.5, 6.2))

    for idx, pipeline in enumerate(pipelines):
        values = plot_df[pipeline].to_numpy(dtype=float)
        bars = ax.barh(y + offsets[idx], values, height=bar_height, label=pipeline)

        for bar, value in zip(bars, values):
            if not np.isnan(value):
                ax.text(
                    bar.get_width() + 0.4,
                    bar.get_y() + bar.get_height() / 2,
                    f"{int(value)}",
                    va="center",
                    fontsize=7,
                )

    ax.set_yticks(y)
    ax.set_yticklabels(plot_df["Query"])
    ax.invert_yaxis()

    ax.set_xlabel("Runtime (ms)")
    ax.set_title("Cypher Query Runtime by Query Type and Pipeline")
    ax.legend(title="Pipeline", loc="lower right")
    ax.grid(axis="x", alpha=0.3)

    ax.text(
        0.99,
        -0.10,
        "Note: German graph-summary timing was not provided.",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=8,
    )

    fig.tight_layout()

    fig.savefig(output_dir / "cypher_query_timings_grouped_bar.png", dpi=300, bbox_inches="tight")
    fig.savefig(output_dir / "cypher_query_timings_grouped_bar.pdf", bbox_inches="tight")
    plt.close(fig)


def create_summary_table(df: pd.DataFrame, output_dir: Path) -> None:
    """
    Export the timing table and a compact summary.

    The summary is useful for reporting in the evaluation section.
    """

    timing_csv = output_dir / "cypher_query_timings.csv"
    df.to_csv(timing_csv, index=False)

    pipelines = ["ASD", "Census", "COMPAS", "German"]

    summary = pd.DataFrame({
        "Pipeline": pipelines,
        "Mean runtime (ms)": [df[p].mean(skipna=True) for p in pipelines],
        "Median runtime (ms)": [df[p].median(skipna=True) for p in pipelines],
        "Max runtime (ms)": [df[p].max(skipna=True) for p in pipelines],
    })

    summary.to_csv(output_dir / "cypher_query_timing_summary.csv", index=False)


def main() -> None:
    output_dir = Path("query_timing_figures")
    output_dir.mkdir(parents=True, exist_ok=True)

    df = build_timing_dataframe()

    create_heatmap(df, output_dir)
    create_grouped_bar_chart(df, output_dir)
    create_summary_table(df, output_dir)

    print("Generated files:")
    print(f"- {output_dir / 'cypher_query_timings_heatmap.png'}")
    print(f"- {output_dir / 'cypher_query_timings_heatmap.pdf'}")
    print(f"- {output_dir / 'cypher_query_timings_grouped_bar.png'}")
    print(f"- {output_dir / 'cypher_query_timings_grouped_bar.pdf'}")
    print(f"- {output_dir / 'cypher_query_timings.csv'}")
    print(f"- {output_dir / 'cypher_query_timing_summary.csv'}")


if __name__ == "__main__":
    main()