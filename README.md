# CARMENES input catalogue of M dwarfs VIII. Multiplicity from close spectroscopic binaries to ultrawide systems
  
> This repository contains the pieces of code necessary to produce all figures, tables and models in this volume of the series.

The *CARMENES input catalogue of M dwarfs* series contains:

- <a href="#" target="_blank">**VIII. Multiplicity from close spectroscopic binaries to ultrawide systems**</a>  **Cifuentes et al 2023, in prep** (this work).
- <a href="#" target="_blank">VII. To be defined</a>  In prep.
- <a href="https://ui.adsabs.harvard.edu/abs/2021A%26A...652A.116P/abstract" target="_blank">VI. A time-resolved Ca II H&K catalog from archival data</a>  Perdelwitz et al 2021.
- <a href="https://ui.adsabs.harvard.edu/abs/2020A%26A...642A.115C/abstract" target="_blank">V. Luminosities, colours, and spectral energy distributions</a>  Cifuentes et al 2020.
- <a href="https://ui.adsabs.harvard.edu/abs/2019A%26A...621A.126D/abstract" target="_blank">IV. New rotation periods from photometric time series </a> Díez Alonso et al. 2019.
- <a href="https://ui.adsabs.harvard.edu/abs/2018A%26A...614A..76J/abstract" target="_blank">III. Rotation and activity from high-resolution spectroscopic observations </a> Jeffers et al. 2018.
- <a href="https://ui.adsabs.harvard.edu/abs/2017A%26A...597A..47C/abstract" target="_blank">II. High-resolution imaging with FastCam</a> Cortés-Contreras et al. 2017.
- <a href="https://ui.adsabs.harvard.edu/abs/2015A%26A...577A.128A/abstract" target="_blank">I. Low-resolution spectroscopy with CAFOS</a> Alonso-Floriano et al. 2015.

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![Publication](https://img.shields.io/badge/Published%3F-soon-orange.svg)](https://www.aanda.org/articles/aa/abs/2020/10/aa38295-20/aa38295-20.html)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://GitHub.com/ccifuentesr)

## Table of Contents

- [Installation](#installation)
- [Structure](#structure)
- [Support](#support)
- [License](#license)
- [Suggested Resources](#resources)

---

## Installation

> The files are self-contained, self-consistent, homogenoeusly formatted, fairly self-explanatory.

- Clone this repo to your local machine using `git clone https://github.com/ccifuentesr/CARMENES-VIII`, or
- Download this repo as a .zip and run the scripts in your local machine.
- The installation of some basic libraries is a prerequisite: `numpy`, `scipy`, `astropy`, `matplotlib` or `emcee`, mainly.
- The font Adobe's Minion Pro is sometimes invoked at the beginning of some scripts to format labels and legends. This line (```fpath = ...```) can be safely commented if unwanted.  

## Structure

The following directories:

- Directory ./: Includes all the code files named as `cif03.xxx_***.py`, where `xxx` defines the usage for the particular code ('plot', 'utilities', 'calculator', 'model').
- Directory ./Data: Includes all necessary auxiliary files.

The **main table** (`cif03.full_table.csv`) [190 rows, 2642 columns, 3.3 MB] contains astrometric and photometric data, fundamental parameters, and multiplicity information of all the stars in the sample and their physically bound components.


---

## Support

Reach out to me at <a href="mailto:ccifuentes@cab.inta-csic.es">`ccifuentes@cab.inta-csic.es`</a>.

---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**

---

## Suggested Resources

- <a href="https://www.python.org/dev/peps/pep-0008/" target="_blank">Style Guide for Python Code (PEP 8)</a>
- <a href="https://carmenes.caha.es" target="_blank">CARMENES Website</a>
