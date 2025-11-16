# FOSSEE TASK

## Project Requirements

The project requirement is listed [here](./PyLaTex%20report%20Screening%20task.pdf).

## Setup

1. Install the required LaTeX distribution:
  ```sh
  sudo apt-get install texlive-full
  ```

2. Install Python dependencies:
  - using uv:
  ```sh
  uv sync
  ```
   
  - using pip:
  ```sh
  pip install -r requirements.txt
  ```

## How to use the script

```sh
python script.py --help
```

```sh
usage: script.py [-h] [--excel EXCEL] [--image IMAGE] [--output OUTPUT]

Generate an engineering report using PyLaTeX.

options:
  -h, --help            show this help message and exit
  --excel EXCEL, -e EXCEL
                        Path to the Excel file containing force data.
  --image IMAGE, -i IMAGE
                        Path to the beam image.
  --output OUTPUT, -o OUTPUT
                        Output PDF file name (without extension).
```
