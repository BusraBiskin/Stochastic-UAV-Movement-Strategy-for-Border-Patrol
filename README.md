# Stochastic UAV Movement Strategy for Border Patrol

This repository contains the implementation of a novel stochastic movement strategy for UAV border patrol operations, developed as part of a PhD thesis at the University of Southampton.

## Overview

This project introduces a probabilistic approach to UAV navigation for border surveillance, where UAV movements are governed by optimized probability vectors rather than deterministic paths. The framework includes:
- Simulation of UAV and target movements
- Implementation of three optimization methods (SA, SNM, RBF)
- Integration with ground sensors
- Multiple mission scenario implementations

## Key Features

- Stochastic movement strategy for unpredictable UAV patrolling
- Multiple optimization algorithms:
  - Simulated Annealing (SA)
  - Stochastic Nelder-Mead (SNM)
  - Radial Basis Function (RBF)
- Ground sensor integration
- Multi-UAV coordination capabilities
- Various mission scenario implementations

## Requirements

- Python 3.9
- Required packages:
  numpy>=1.21.0
  scipy>=1.7.0  # For optimize module
  pandas>=1.3.0
  matplotlib>=3.4.0
  time  # Built-in Python module
  math  # Built-in Python module
  random  # Built-in Python module 
  sys  # Built-in Python module
  functools  # Built-in Python module
