# allen-assistant

python command line utility for querying, downloading, and exporting allen brain observatory data

## Usage

```
$ ./aa.py --help

usage: aa.py [-h] [-r] {download,search} ...
positional arguments:
{download,search}
download         Used for downloading files
search           Used for testing search queries

```

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

#### Linux

```
$ git clone https://github.com/jzlab/allen-assistant
$ cd allen-assistant
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

### Prerequisites

This project was built on Python 2.7.10, the allensdk requires 2.7x and is not python3 compatible

```
$ pip install -r requirements.txt

```

If everything installs without a hitch it should run

## Built With

* [AllenSDK](http://alleninstitute.github.io/AllenSDK/) - The Allen SDK
*
* ## Contributing
*
* Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.
*
* ## Versioning
*
* We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).
*
* ## Authors
*
* * **Elijah Christensen** - *Initial work* - [Github](https://github.com/elijahc)
*
* See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.
*
* ## License
*
* This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
*
* ## Acknowledgments
*
* * Hat tip to anyone who's code was used
* * Inspiration
* * etc
*
