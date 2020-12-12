# PylogPlot

The python code for logging and plotting data as part of [ErgPower][https://moralcode.github.io/ErgPower] experiments.


## Dependencies

In addition to the dependencies required in `pipenv`, the python scripts that interface with the Concept2 Ergometer's directly will need to have [Py3Row](https://github.com/droogmic/Py3Row) installed using the following command (which is also in their readme).

```
pip install -e git+https://github.com/droogmic/Py3Row.git#egg=pyrow
```
This is a temporary workaround until, according to the Py3Row documentation, the code becomes stable and has been packaged as a module. Once this happens, please submit a pull request to include this module in pipenv and update this part of the README.
