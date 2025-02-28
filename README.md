# TransPrint

TransPrint, a covert and passive continuous authentication scheme that leverages the temporal characteristics of USB transactions during device enumeration and file system operations.

## Features

- Detects and prevents malicious USB storage devices at a much earlier stage
- CSV file splitting based on configurable filters
- USB timestamp data extraction
- Time series visualization
- DTW (Dynamic Time Warping) similarity analysis
- Configurable via YAML files

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Install dependencies using Poetry:
```bash
poetry install
```

## Configuration
Create a config.yaml file in the project root or use the template in config.yaml:
```yaml
register:
    # Data splitting settings
    divide_input_path: "input.csv"  # you can get csv file from wireshark using usbmon
    divide_output_prefix: "output/"
    divide_filter: ["host", "USBMS"]

    # Data loading settings
    load_base_path: "/path/to/data/"
    load_start_idx: 2
    load_end_idx: 102
    load_file_pattern: "output_{}.csv"

    # Drawing settings
    draw_title: "USB Time Series"
    draw_xlabel: "Sequence"
    draw_ylabel: "Value"
    draw_save_path: "./output.pdf"
```

## Usage

```bash
# Run analysis with default config
python -m src.cli analyze

# Run with custom config file
python -m src.cli -c custom_config.yaml analyze
```

## Project Structure

```
src
├── cli.py
└── core
    ├── config.py
    ├── data_load.py
    ├── divide.py
    ├── draw.py
    ├── __init__.py
    ├── similarity.py
    ├── statistics.py
    └── timestamp_get.py
```
## Dependencies
- Python ≥ 3.11
- pandas
- matplotlib
- click
- pyyaml

## License
MIT License

Copyright (c) 2025 TransPrint Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.