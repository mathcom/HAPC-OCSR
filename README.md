# HAPC-OCSR
OCSR implemented by Hallym APCLab

## Overview
HAPC-OCSR is an Optical Chemical Structure Recognition (OCSR) system developed by the **AI-Powered Cheminformatics Laboratory (APCLab), Hallym University**.  
The tool provides a Tkinter-based GUI to:
- Upload a chemical structure image.
- Predict the corresponding SMILES string using a PyTorch model.
- Visualize both the uploaded image and the RDKit-rendered molecular structure.
- Copy the predicted SMILES string with a single click.

---

## Installation

> **Note for Windows users**  
> Since this repository provides a Windows-specific launcher (`run_app.bat`), please place the `HAPC-OCSR-master` directory under your Documents folder:  
> ```
> C:\Users\%USERNAME%\Documents\HAPC-OCSR-master
> ```

1. **Clone the repository**
   ```bash
   git clone https://github.com/mathcom/HAPC-OCSR.git
   cd HAPC-OCSR
   ```

2. **Create and activate conda environment**
   ```bash
   conda env create -f environment.yml
   conda activate hapc-ocsr
   ```

3. **Download model checkpoint**
   - Create a folder named `ckpt` in the project root:
     ```bash
     mkdir ckpt
     ```
   - Download the pretrained models from Google Drive:  
     [molscribe+ocsaug.pth](https://drive.google.com/file/d/1glGsZFxN3w-FEYY_mevLZgyh-Jrh0JqY/view?usp=sharing)  
     [molnextr+ocsaug.pth](https://drive.google.com/file/d/1hn9XGyBEQPwc8jgbixYgHlqIK9IMSt7q/view?usp=sharing)  
   - Place the files into the `ckpt` folder:
     ```
     HAPC-OCSR-master/
     ├── main.py
     ├── run_app.bat
     ├── environment.yml
     ├── ckpt/
     │   └── molscribe+ocsaug.pth
     │   └── molnextr+ocsaug.pth
     ```

---

## Usage

### Option 1: Run with Conda
```bash
python main.py
```

### Option 2: Run with Batch file (Windows only)
Simply double-click:
```
run_app.bat
```
This script will automatically launch the program using:
```
%USERPROFILE%\miniconda3\envs\hapc-ocsr\python.exe %USERPROFILE%\Documents\HAPC-OCSR-master\main.py
```

---

## Acknowledgements
- **MolScribe** and **MolNexTR** for OCSR backbone.  
- **RDKit**, **Pillow**, and **Tkinter** for visualization and GUI.  

---

## Contact
```bash
jonghwanc@hallym.ac.kr
```
