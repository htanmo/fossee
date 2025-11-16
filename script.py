import argparse
import pandas as pd
from pylatex import (
    Document,
    Section,
    Subsection,
    TikZ,
    Axis,
    Plot,
    Command,
    Figure,
    Center,
    NoEscape,
    NewPage,
    LongTabu,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate an engineering report using PyLaTeX."
    )

    parser.add_argument(
        "--excel",
        "-e",
        default="Force Table.xlsx",
        help="Path to the Excel file containing force data.",
    )

    parser.add_argument(
        "--image",
        "-i",
        default="Simply Supported Beam.png",
        help="Path to the beam image.",
    )

    parser.add_argument(
        "--output",
        "-o",
        default="Report",
        help="Output PDF file name (without extension).",
    )

    return parser.parse_args()


def generate_report(excel_file, beam_image, output_pdf):
    df = pd.read_excel(excel_file)

    geometry_options = {"margin": "1in"}
    doc = Document(geometry_options=geometry_options)
    doc.preamble.append(Command("title", "Structural Analysis Report"))
    doc.preamble.append(Command("author", "Auto-generated"))
    doc.preamble.append(Command("date", NoEscape(r"\today")))
    doc.append(NoEscape(r"\maketitle"))
    doc.append(NewPage())

    doc.append(Command("tableofcontents"))
    doc.append(NewPage())

    with doc.create(Section("Introduction")):
        doc.append(
            "This report presents the shear force and bending moment diagrams for a simply supported beam based on the provided data. "
            "The objective is to visualize the internal forces acting on the member."
        )
        with doc.create(Subsection("Beam Description")):
            doc.append(
                "Below is the schematic representation of the simply supported beam used in this analysis."
            )
            with doc.create(Figure(position="h!")) as fig:
                fig.add_image(beam_image, width=NoEscape(r"0.8\textwidth"))
                fig.add_caption("Simply Supported Beam Configuration")
        with doc.create(Subsection("Data Source")):
            doc.append(
                "The internal force data used in this report is extracted from the provided Excel sheet."
            )

    doc.append(NewPage())
    with doc.create(Section("Input Data Table")):
        doc.append("The force table extracted from the Excel sheet is shown below:")
        with doc.create(LongTabu("|l|l|l|")) as table:
            table.add_hline()
            table.add_row(df.columns.tolist())
            table.add_hline()

            for _, row in df.iterrows():
                table.add_row(row.tolist())
                table.add_hline()

    doc.append(NewPage())
    with doc.create(Section("Analysis")):
        doc.append(
            "The diagrams below visually represent the variations in internal forces along the length of the beam."
        )
        with doc.create(Subsection("Shear Force Diagram (SFD)")):
            with doc.create(Center()):
                with doc.create(TikZ()) as tikz:
                    plot_options = NoEscape(
                        r"height=6cm, width=12cm, grid=major, xlabel={Span (m)}, ylabel={Shear Force (kN)}"
                    )
                    with tikz.create(Axis(options=plot_options)) as plot:
                        coordinates = list(zip(df["x"], df["Shear force"]))
                        plot.append(Plot(name="SFD", coordinates=coordinates))

        with doc.create(Subsection("Bending Moment Diagram (BMD)")):
            with doc.create(Center()):
                with doc.create(TikZ()) as tikz:
                    plot_options = NoEscape(
                        r"height=6cm, width=12cm, grid=major, xlabel={Span (m)}, ylabel={Bending Moment (kN·m)}"
                    )
                    with tikz.create(Axis(options=plot_options)) as plot:
                        coordinates = list(zip(df["x"], df["Bending Moment"]))
                        plot.append(
                            Plot(
                                name="BMD",
                                coordinates=coordinates,
                                options=NoEscape("mark=*, color=red"),
                            )
                        )

    doc.generate_pdf(output_pdf, clean_tex=False)


if __name__ == "__main__":
    args = parse_args()
    generate_report(args.excel, args.image, args.output)
