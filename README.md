[![Lint Format Test Install](https://github.com/johncoogan53/DataPipeline/actions/workflows/CICD.yaml/badge.svg)](https://github.com/johncoogan53/DataPipeline/actions/workflows/CICD.yaml)
# Azure Databricks ETL Pipeline

## Overview
This project is an end to end data pipeline which takes raw, web scraped, data for video game reviews on the Steam platform, processes them through a scheduled ETL Databricks pipeline and produces useful visualizations about the data. This workflow pulls the first n number of positive and negative reviews of a specific video game and processes that data. This can be used to continuously update business intelligence for game developers. This project also leverages the value of Delta Lake storage by
