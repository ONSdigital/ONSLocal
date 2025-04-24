# Postcode lookup

## Overview

This script produces a demographic breakdown for each supplied postcode, at the level of output area (OA), which is the 
smallest geographical unit that the census uses. The output of this script will be:

* A `.csv` and `.png` file that gives demographic information for each supplied postcode, at output area level.
* A `.csv` file showing the postcode-output area mapping.

Note: as there can be multiple postcodes in each OA, if there is overlap between the supplied postcodes, this will be shown in
the produced tables. 

## Usage

### Setup Instructions

1. Follow the installation instructions [here](../README.md#installation).
2. Create the `data` and `output` folders.
3. Make sure the `data` folder contains the required files as specified [here](README.md#data-requirements).
4. Rename `.env-example` to `.env`.
5. Ensure the `.env` file contains the correct file names for the files in the `data` folder.

### Data requirements

The user needs to provide the following data files:

* `postcode_output_area_mapping` should be a National Statistics Postcode Lookup file, such as 
[found here](https://geoportal.statistics.gov.uk/datasets/ec30de8df7cb4e8b8f6158e4337f46d2/about).
* `postcode_list`: A file that contains a list of postcodes in a column called `Postcode`.
* `variable_files`: A list variable files from the census. This data can be downloaded from 
[here](https://www.ons.gov.uk/datasets/create). When creating a custom dataset, each variable of interest should be 
downloaded separately.


### File Format and Location

- All data should be in `.csv` format.
- Save all files in a `data` folder.
- In the `.env` file, specify only the file name and extension (e.g., `postcodes.csv`).

As seen in the `.env-example`, the final `.env` file for this script should look similar to:

```text
postcode_output_area_mapping = "postcode-output_area_mapping.csv"
postcode_list = "postcode_list.csv"
variable_files = ["age.csv", "ethnicity.csv"]
```

### Project structure

After following the setup instructions, the final project structure should look similar to:

```text
Postcode_lookup/
├── data/ <- Folder containing data
├── ├── age_oa_census.csv <- Age variable data
├── ├── COB_oa_census.csv <- Country of birth variable data
├── ├── NSPL_FEB_2025_UK.csv <- Postcode to output area mapping
├── ├── postcode_list.csv <- Postcode list
├── output/ <- Folder containing script output
├── tests/ <- Folder containing code tests
├── .env <- File that contains data paths
├── .env-example <- Example of data paths
├── __init__.py
├── main.py <- File to run
├── README.md
```