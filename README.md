Introduction
============

Norwegian is software that reads flights and prices from the Airline Norwegians web site.
By enterring origin and destination and the duration of the trip, a sorted list of trips with round trip prices is printed.

Origin and destination is enterred as an [IATA three letter city code](http://www.iata.org/publications/Pages/code-search.aspx)


Installation
============
Download package from Githup:

wget https://github.com/AndersFluur/Norwegian/archive/master.zip

unzip  Norwegian-master.zip

cd Norwegian-master

python setup.py sdist

pip install --user dist/norwegian-1.0.1.tar.gz

The program is now installed in: /home/$USER/.local/bin

Running
=======

```
norwegian -h

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
```
