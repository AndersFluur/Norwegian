Installation
============
Download package from Githup

cd Norwegian

python setup.py sdist
pip install --user dist/norwegian-1.0.tar.gz
/home/$USER/.local/bin/norwegian

Running
=======
python src/norwegian.py -h

Usage: norwegian.py [-h] --origin ORIGIN --destination DESTINATION --duration
                    DURATION --months-ahead MONTHS_AHEAD

Read flights and prices from Norwegians web and present a list of trips and
prices

optional arguments:
  -h, --help            show this help message and exit
  --origin ORIGIN, -a ORIGIN
                        The airport to travel from
  --destination DESTINATION, -z DESTINATION
                        The airport to travel to
  --duration DURATION, -u DURATION
                        Wanted duration of the trip
  --months-ahead MONTHS_AHEAD, -m MONTHS_AHEAD
                        Number of months in the future to fetch flights for

