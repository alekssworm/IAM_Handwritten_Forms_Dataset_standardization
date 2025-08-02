
# IAM Handwritten Forms Dataset – Standardization Scripts

## Overview

This repository contains two scripts for preprocessing and standardizing the [IAM Handwritten Forms Dataset](https://www.kaggle.com/datasets/naderabdalghani/iam-handwritten-forms-dataset/data).

### 1. `cut.py`

Splits each image into two parts:

* **Handwritten text**
* **Machine-printed text**

### 2. `png_to_text.py`

Converts the machine-printed part of the image into `.txt` format using OCR (Tesseract).

---

## Dataset

The scripts are designed to work with the **IAM Handwritten Forms Dataset**, available here:
[https://www.kaggle.com/datasets/naderabdalghani/iam-handwritten-forms-dataset/data](https://www.kaggle.com/datasets/naderabdalghani/iam-handwritten-forms-dataset/data)

---

## Dependencies

### For `cut.py`

```python
import cv2
import numpy as np
from pathlib import Path
import os
from tqdm import tqdm
```

### For `png_to_text.py`

```python
from PIL import Image
from pytesseract import pytesseract
from pathlib import Path
import os
from tqdm import tqdm
```

---

## Notes

When using **pytesseract**, make sure to install **Tesseract OCR** from the official repository:
[https://github.com/tesseract-ocr/tesseract#running-tesseract](https://github.com/tesseract-ocr/tesseract#running-tesseract)


