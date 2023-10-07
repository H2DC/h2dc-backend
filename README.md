# Node Detection in Hand-Drawn Circuit using Hough Transform

## Introduction

This project focuses on detecting nodes in hand-drawn circuit diagrams using the Hough Transform algorithm implemented in Python. Nodes are essential components in circuit analysis, and automating their detection can be valuable in various applications.

## Prerequisites

Before running the code, ensure you have the following prerequisites installed:

- Python 3.x
- OpenCV (Open Source Computer Vision Library)
- NumPy

You can install these dependencies using `pip`:

```shell
pip install opencv-python numpy scikit-learn
```

## Installation

1. Clone the repository

```shell
git clone https://github.com/H2DC/node-detection
cd node-detection
```

2. Ensure you have OpenCV, NumPy and scikit-learn installed as mentioned in the prerequisites.


## Usage

1. Place your hand-drawn circuit images in the input of part of the code.
2. Run the node detection script:
```shell
python detect_nodes.py
```
3. The image with detected nodes will be displayed on the screen.
