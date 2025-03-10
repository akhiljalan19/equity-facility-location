# Equity across Demographic Groups for the Facility Location Problem

This repository contains instructions on how to reproduce our experiments and figures. 

## Reproducing each figure

This table describes where the code that was used to generate each figure came from. By running the appropriate iPython notebook. The "Block of cells" column describes the heading where functions used to generate the figure in question begin. Notebooks with multiple figures are split up into multiple blocks of cells. 

**NOTE**: In general, when running code it a notebook, *every cell will rely on cells before it*, which are used for package imports and custom functions. If you want to run cell N, you must run cells 1, 2, ..., N-1 first.

| Figure Number | Notebook Which Generates It        | Block of cells                                    |
|---------------|------------------------------------|---------------------------------------------------|
| 1             | `fac-overlay.ipynb`                | All                                               |
| 2             | `dataset-characteristics.ipynb`    | "Compute Correlations"                            |
| 3             | `dataset-characteristics.ipynb`    | "Scatterplots"                                    |
| 4             | `alta-bates-closure.ipynb`         | "Load Increases"                                  |
| 5             | `alta-bates-closure.ipynb`         | "Load Increases"                                  |
| 6             | `approx-optimality-analysis.ipynb` | "Optimal Replacement to Alta Bates"               |
| 7             | `approx-optimality-analysis.ipynb` | "Scale Factor Heatmap"                            |
| 8             | `approx-optimality-analysis.ipynb` | "Scale Factor Heatmap"                            |
| 9             | `approx-optimality-analysis.ipynb` | "Scale Factor Heatmap"                            |
| 10            | `alta-bates-closure.ipynb`         | "Travel Distance Increase for Displaced Users"    |
| 11            | `alta-bates-closure.ipynb`         | "Travel Distance Increase for Displaced Users"    |
| 12            | `approx-optimality-analysis.ipynb` | "Worst Scale Factor vs Lambda"                    |

## Organization of the notebooks

Our analysis is split up into various Jupyter notebooks. Each notebook contains text to explain the different sections of code, and function documentation with input/output behavior. Here is a high-level summary of each notebook.

`fac-overlay.ipynb`: Contains the code to generate Figure 1. Using screenshots of Google Maps, as well as Latitude/Longitude coordinates for the hospitals in our dataset, we overlay the facilities as a scatterplot on the raw Google Maps image.

`dataset-characteristics.ipynb`: Contains the code for section 4.1, describing characteristics of Alameda and Contra Costa county. Contains the code used to generate demographic scatterplots (Figure 2). Computes the correlations of different groups (Figure 3). 

`allocation-df-prepare.ipynb`: Prepares CSV files that are used in 4.2 and 4.3 - see the files in `all-data/allocation-dfs`. We call these *allocation DataFrames* because we generates DataFrames (essentially, spreadsheets or tables) whose rows are unique allocations (sets of facilities to open) and columns are various statisics of each allocation we are interested in (e.g. average travel distance, capacity deviation, etc). In particular, we generate a DataFrame for opening 3 facilities from scratch, which is used in 4.3 - see `all-data/allocation-dfs/three_facs_to_open_from_scratch.csv`. Further, we generate DataFrames which encode results for the Alta Bates replacement problem in section 4.2 - see `all-data/allocation-dfs/alta-bates-replacements-rescaled-beds`.

`approx-optimality-analysis.ipynb`: Contains the code for section 4.3. Generate the heatmaps of scale factors for various allocations (Figures 7 - 9), as well as growth of the worst scale factor for the approximately optimal allocation as a function of lambda (Figure 12 in the appendix). This also contains the code to find the optimal replacement for Alta Bates under various lambda, eta values (Figure 6). 

`alta-bates-closure.ipynb`: Contains some of the code for section 4.2 on Alta Bates' closure. Contains the code analyzing the load increases for nearby hospitals (Figures 4-5), and increases in travel distance for the displaced Alta Bates users (Figures 10-11). Computes some statistics about facility 16 - such as the number of users it has when opened, and what their average travel distance is before/after it is opened. 

## Software requirements

All code was written in Python 3.7.3. In addition to installing Jupyter and Python, you will need the following packages: 

* Pandas
* Numpy
* Matplotlib
* Seaborn 
* Scipy

We recommend you use either Pip or Anaconda as a package manager. 