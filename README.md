# ONSLocal

## Installation

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

