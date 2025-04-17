# Postcode lookup

## Overview

This script produces a demographic breakdown for each supplied postcode, at the level of output area (OA), which is the 
smallest geographical unit that the census uses.

As there can be multiple postcodes in each OA, if there is overlap between the supplied postcodes, this will be shown in
the produced tables. 

## Usage

### Setup Instructions

1. Follow the installation instructions [here](../README.md#installation)
2. Rename `.env-example` to `.env`.
3. Ensure the `.env` file contains the correct file names for the required data.

### Data requirements

The user needs to provide the following data files, with links specified in a `.env` file:

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