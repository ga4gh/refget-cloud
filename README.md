[![Logo](https://www.ga4gh.org/wp-content/themes/ga4gh-theme/gfx/GA-logo-horizontal-tag-RGB.svg)](https://ga4gh.org)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=flat-square)](https://opensource.org/licenses/Apache-2.0)
[![Travis (.org) branch](https://img.shields.io/travis/ga4gh/refget-cloud/master.svg?style=flat-square)](https://travis-ci.org/ga4gh/refget-cloud)
[![Coverage Status](https://img.shields.io/coveralls/github/ga4gh/refget-cloud.svg?style=flat-square)](https://coveralls.io/github/ga4gh/refget-cloud?branch=master)

# Refget Cloud

Configurable, python-based Refget web service. Can be configured to run in multiple deployment contexts (e.g. containerized server, serverless) and serve data from multiple cloud-based sources.

Refget Cloud is an implementation of the [Refget API Specification v1.0.0](https://samtools.github.io/hts-specs/refget.html), developed by the [Global Alliance for Genomics and Health](https://www.ga4gh.org/).

Currently, this codebase has been deployed to serve reference sequences from the [International Nucleotide Sequence Database Collaboration (INSDC)](http://www.insdc.org/). Click [here](https://refget-insdc.jeremy-codes.com/index.html) to view its OpenAPI documentation and begin accessing sequences.

If you are interested in setting up your own serverless implementation of refget using a cloud-based object store, please review the [documention](docs/INDEX.md) to get started.

## Supported Deployment Contexts

* [AWS ECS + Fargate](docs/guides/DeployAwsEcsFargate.md)
* [AWS Serverless / Lambda](docs/guides/DeployAwsLambda.md)

## Supported Data Sources

* [AWS S3 ](docs/guides/DataSourceAwsS3.md)

# Issues

If you encounter any issues when running your own refget web service, or would like this service to be configured for another deployment context or data source, please send an email to the tool maintainer:

* Jeremy Adams (jeremy.adams@ga4gh.org)