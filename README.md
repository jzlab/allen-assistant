# allen-assistant

python command line utility that encapsulates the Allen Brain Observatory allensdk for streamlining querying, downloading, and exporting allen brain observatory data.

## Example Usage

Test out set of criteria to see what you get

```

$ python aa.py search -t VISp -c Cux2-CreERT2 -d 175 -d 250 -s static_gratings

RESULTS

Query parameters:
===============================

{'cache_dir': 'boc/',
'cre_lines': ['Cux2-CreERT2'],
'detailed': False,
'imaging_depths': [175, 250],
'outfile': None,
'stimuli': ['static_gratings'],
'targeted_structures': ['VISp']}
===============================


Number of Experiment Containers: 11

Number of Experiments returned: 8

```

When you are happy with the query use the same args to download

```
$ ./aa.py download -t VISp -c Cux2-CreERT2 -d 175 -d 250 -s static_gratings --output_dir boc/ophys_matfiles/

```

## Overview
The utility is split (possibly unnecessarily) into 2 subcommands which allow you to test your queries
before committing to long wait till they finish downloading

```
$ ./aa.py --help

usage: aa.py [-h] [-r] {download,search} ...
positional arguments:
{download,search}
download         Used for downloading files
search           Used for testing search queries

```

The Experiment Container and Other Experiment Params consistent across download/search, but search is shown below as an example

```

$ ./aa.py search --help
usage: aa.py search [-h] [-o] [--detailed] [-t] [-c] [-d] [-s]

optional arguments:
    -h, --help            show this help message and exit
    -o , --outfile        Filepath to save text report
    --detailed            Show a far more detailed report

Experiment Container Params:

    -t , --targeted_structures
                            Target Visual Cortex Structure. Allowed values are:
                            VISal VISl VISp VISpm


    -c , --cre_lines        Transgenic mouse line. Allowed values are
                            Cux2-CreERT2, Emx1-IRES-Cre, Nr5a1-Cre,
                            Rbp4-Cre_KL100, Rorb-IRES2-Cre, Scnn1a-Tg3-Cre

    -d , --imaging_depths
                            Imaging depths. Allowed values are 175, 250, 275, 335,
                            350, 375

Other Experiment Params:

    -s , --stimuli          Visual stimuli type. Allowed values are
                            drifting_gratings, locally_sparse_noise,
                            locally_sparse_noise_4deg, locally_sparse_noise_8deg,
                            natural_movie_one, natural_movie_three,
                            natural_movie_two, natural_scenes, spontaneous,
                            static_gratings

```

### Installing

Works on linux but I have also gotten it to work on macos

#### Linux


```
$ git clone https://github.com/jzlab/allen-assistant


```

### Prerequisites

This project was built on Python 2.7.10, the allensdk requires 2.7x and is not python3 compatible
You can use pip to install all dependencies

I recommend using a virtual environment so as to keep everything clean.

If you don't have virtualenv installed already

```
$ pip install virtualenv
```

then create and/or load the virtual environment

```
$ cd allen-assistant

$ virtualenv allen

$ source allen/bin/activate

$ pip install -r requirements.txt

```

If everything installs without a hitch it should run!

```
$ python aa.py --help


usage: aa.py [-h] [-r] {download,search} ...

positional arguments:
{download,search}
    download         Used for downloading files
    search           Used for testing search queries

optional arguments:
    -h, --help         show this help message and exit
    -r , --cache_dir   Default: ./boc/
```

## Built With

* [AllenSDK](http://alleninstitute.github.io/AllenSDK/) - The Allen SDK

## Authors

* **Elijah Christensen** - [Github](https://github.com/elijahc)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Original [Jupyter notebook] provided by the Allen Institute for examples
