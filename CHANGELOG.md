# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Dates formatted as YYYY-MM-DD as per [ISO standard](https://www.iso.org/iso-8601-date-and-time-format.html).

## v0.2.0 - 2024-10-02

Conducted reproduction, evaluated code and article, organised research compendium, and test run by second STARS team member.

### Added

* Reproduction of the model in `reproduction/`
* Evaluation of the code and article against guidelines (in `evaluation/`)
* Summary report and reflections from reproduction
* Organised and documented reproduction to form a `research compendium`
* Test-run of model by Tom Monks, attempting to run code from `reproduction/`

### Changed

* Removed one item from the scope - in-text result 1: "The strongest protective effect is seen with the N95 masks (nearly equivalent to a FFP2 mask), which has the effect of reducing the odds of transmission by 0.09". This was because I realised that this was not in fact a result, but just a statement of the parameter used in the model (to simulate the effect of wearing masks, you reduce the odds of transmission (p=0.15) by 0.09 (p=0.15*0.09) when you run the model).

## v0.1.0 - 2024-07-22

Set up repository and defined scope of reproduction.

### Added

* Code from original study
* Article and supplementary materials
* Reformatted csv tables from the supplementary materials
* Planned scope for reproduction

### Changed

* Modified template to be about Lim et al. 2020