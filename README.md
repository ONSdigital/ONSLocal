# ONSLocal

## Contact
This repository was developed and is maintained by the ONS Local team.

> To contact us raise an issue on Github or via email at [ons.local@ons.gov.uk](mailto:ons.local@ons.gov.uk) with the subject GITHUB.

## Scripts

* [Postcode lookup](Postcode_lookup/README.md) - This script produces a demographic breakdown for each supplied postcode,
at the level of output area.

## Project structure

```text
ONSLocal/
├── Development/ <- Folder containing code for development
├── Shared/ <- Folder containing code used across scripts
├── LICENSE <- License for the project
├── .github/ <- Folder containing files to automate github processes
├── .gitignore <- Contains a list of file types that git will ignore
├── README.md
├── requirements.txt <- File containing project dependencies
```

All other folders, such as `Postcode_lookup` are folders containing scripts to be ran, and are detailed 
[here](README.md#scripts).

## Setup

* This project was developed using Python 3.12.3
* Required Python libraries are listed in `requirements.txt`

### Installation

Navigate to the folder where you wish to clone this git repository and run:

```
git clone https://github.com/ONSdigital/ONSLocal.git
```

IDEs such as Pycharm can make virtual environment set up easier, however, to manually set up a virtual environment, 
enter the cloned folder and initialise a virtual environment using:

```
cd ONSLocal
python -m venv venv
```

To activate the virtual environment:

* On Windows

```
venv\Scripts\activate
```

* On MacOS/Linux

```
source venv/bin/activate
```

Then download the requirements in the virtual environment using
To install it with `pip`, use:
```
pip install -r requirements.txt
```

The desired script can then be ran using:

```
python <script-name>/main.py
```

## Useful external links

* [Explore local statistics](https://www.ons.gov.uk/explore-local-statistics/) - Find, compare and visualise statistics 
about places in the United Kingdom.
