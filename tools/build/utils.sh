#!/bin/bash

function create_env() {
  conda env create -f environment.yml
  conda activate datum
}
