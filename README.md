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
   - Download the pretrained model from Google Drive:  
     [molscribe+ocsaug.pth](https://drive.google.com/file/d/1glGsZFxN3w-FEYY_mevLZgyh-Jrh0JqY/view?usp=sharing)  
   - Place the file into the `ckpt` folder:
     ```
     HAPC-OCSR/
     ├── main.py
     ├── environment.yml
     ├── ckpt/
     │   └── molscribe+ocsaug.pth
     ```

---

## Usage

Run the application with:
```bash
python main.py
```

**Workflow**  
- Choose an image file → Run prediction → View original and RDKit-rendered structures side by side.  
- Copy predicted SMILES with the **Copy** button.  
- Use **Back** to return to the input screen.  

---

## Acknowledgements
- **MolScribe** for OCSR backbone.  
- **RDKit**, **Pillow**, and **Tkinter** for visualization and GUI.  

---

## Contact
```bash
jonghwanc@hallym.ac.kr
```