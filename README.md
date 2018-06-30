# Automated Data Entry Tool
Using a multilayer perceptron (MLP) trained on the MNIST database, digits are read off a pre-set invoice sheet. Identified digits are then processed downstreamed and entered directly into an Excel file.

## Introduction
This project aims to alleviate a key bottleneck of companies - manual data entry. Human-based data entry is slow, expensive, and prone to mistakes; here an MLP is used to overcome these weaknesses. 

## Features
### Error detection
As the invoice contains price, quantity, and total price, the tool also has an error-checking feature. If the numbers processed do not align, the offending excel cells are highlighted in red to flag potential errors. These errors can either be the result of handwriting error, or misidentification of digits by the MLP. A human operator can then manually inspect the problematic fields and correct any potential errors.
### Excel interfacing
Relevant information from processed invoices are automatically entered into Excel, allowing for ease of integration into existing company practices with minimal workflow disruption.

## Prerequisites
Before beginning, ensure that your installed version of Python is at least 3.6 and above. If not, a fresh install of Python can be obtained from [here](https://www.python.org/downloads/).

Usage of this tool requires the installation of a few dependencies in Python. 
- [Keras (for building the MLP)](https://keras.io/)
- [Tensorflow (for backend)](https://www.tensorflow.org/)
- [NumPy](http://www.numpy.org/)
- [SciPy](https://www.scipy.org/)
- [OpenCV](https://opencv.org/)
- [PIL](http://www.pythonware.com/products/pil/)

These dependencies can all be installed using `pip`

## Using the tool
To use the tool, simply scan your filled invoices in at 300 dpi and move the scanned `.jpg` files into the `inputs` directory. Run `main.py`.

## Further improvements
1. An MLP is far from state of the art in machine vision. A clear step up would be to switch to a Convolutional Neural Network.
2. Regardless of model, hyperparameters can be better tuned. As the current goal is to achieve a minimum viable product, hyperparameters have been left at whatever works good enough (~80% successful detection rate).
3. Porting to Tensorflow for finer control of model. At this first step, Keras is being used as a crutch to abstract away certain implementation details.
4. Cleaner code. While the current codebase is significantly cleaner than that of the first prototype, there is certainly room for improvement. Good general software engineering practices were likely overlooked at certain points in time, due to the author's lack of actual experience with real-world coding.
5. Reducing dependencies. There are likely significant overlaps within the slew of dependencies of this tool. As a greenhorn, the author is hesitant to mess with code that is currently working, but certainly sees the value of halving the number of dependencies.

## Acknowledgements
As a starter project, references were taken from a multitude of sources. These include:
- [opensourc.es](http://opensourc.es/blog/tensorflow-mnist) and [this reddit thread](https://www.reddit.com/r/MachineLearning/comments/4u29y8/understanding_the_preprocessing_steps_in_the/) for guidance on preprocessing scanned digits as per the MNIST database's requirements
- [machinelearningmastery.com](https://machinelearningmastery.com/handwritten-digit-recognition-using-convolutional-neural-networks-python-keras/) for the boilerplate code to set up the MLP model
- [cs231n](http://cs231n.github.io/) for the machine vision intuition needed
