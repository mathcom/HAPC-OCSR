import os
import tkinter as tk
from rdkit.Chem import Draw, MolFromSmiles, rdDepictor
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

import torch
from MolNexTR import molnextr
from MolScribe import molscribe


## PyTorch 모델 클래스
class MyModel:
    def __init__(self, name="molscribe"):
        self.name = name
        if self.name == "molnextr":
            self.model = molnextr(os.path.join('.', 'ckpt', 'molnextr+ocsaug.pth'), torch.device('cpu'))
            self._predict = self._predict_molnextr
        else:
            self.model = molscribe(os.path.join('.', 'ckpt', 'molscribe+ocsaug.pth'), torch.device('cpu'))
            self._predict = self._predict_molscribe
            
    def predict(self, filepath_image):
        return self._predict(filepath_image)
        
    def _predict_molscribe(self, filepath_image):
        res = self.model.predict_image_file(filepath_image)
        smi = res['smiles']
        return smi
        
    def _predict_molnextr(self, filepath_image):
        with torch.no_grad():
            res = self.model.predict_final_results(filepath_image, return_atoms_bonds=True)
        smi = res['predicted_smiles']
        return smi


## GUI 클래스
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Hallym-APCLab-OCSAug")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # 환경 변수
        self.output_size_width = 300
        self.output_size_height = 300
        
        # 모델 로드
        self.model = MyModel()

        # 상태 변수
        self.current_image_path = None
        self.current_photo_image = None

        # 프레임 정의
        self.frame_input = tk.Frame(self.root)
        self.frame_result = tk.Frame(self.root)

        # UI 구성
        self._build_input_frame()
        self._build_result_frame()

        # 초기에는 입력 프레임 표시
        self.frame_input.pack(fill="both", expand=True)


    def _build_input_frame(self):
        """입력 프레임 UI 구성"""
        self.label_image_preview = tk.Canvas(self.frame_input, width=400, height=400, bg="gray")
        self.label_image_preview.pack(pady=10)

        ## Canvas 초기화
        self.init_preview()

        # 버튼: 이미지 불러오기
        self.btn_load = tk.Button(self.frame_input, text="Choose an image file", command=self.load_image)
        self.btn_load.pack(pady=5)

        # 버튼: 시작
        self.btn_start = tk.Button(self.frame_input, text="Run", command=self.start_prediction)
        self.btn_start.config(state=tk.DISABLED)
        self.btn_start.pack(pady=5)


    def _build_result_frame(self):
        """결과 프레임 UI 구성"""
        frame_images = tk.Frame(self.frame_result)
        frame_images.pack(pady=10)

        self.label_result_input = tk.Canvas(
            frame_images,
            width=self.output_size_width,
            height=self.output_size_height,
            bg="lightgray"
        )
        self.label_result_input.pack(side="left", padx=5)

        self.label_result_mol = tk.Canvas(
            frame_images,
            width=self.output_size_width,
            height=self.output_size_height,
            bg="lightgray"
        )
        self.label_result_mol.pack(side="right", padx=5)

        # SMILES 결과 표시 (Entry + Copy 버튼)
        frame_smiles = tk.Frame(self.frame_result)
        frame_smiles.pack(pady=10)

        tk.Label(frame_smiles, text="SMILES:").pack(side="left")

        self.entry_result = tk.Entry(frame_smiles, width=50)
        self.entry_result.pack(side="left", padx=5)
        self.entry_result.config(state="readonly")

        self.btn_copy = tk.Button(frame_smiles, text="Copy", command=self.copy_smiles)
        self.btn_copy.pack(side="left")

        self.btn_back = tk.Button(self.frame_result, text="Back", command=self.go_back)
        self.btn_back.pack(pady=5)


    def load_image(self):
        """이미지 파일 불러오기"""
        file_types = [("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        path = filedialog.askopenfilename(title="Select an image", filetypes=file_types)
        if not path:
            return
        self.current_image_path = path
        try:
            img = Image.open(path)
            img.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(img)
        except Exception as e:
            messagebox.showerror("Error", f"이미지를 열 수 없습니다:\n{e}")
            return

        self.label_image_preview.create_image(200, 200, image=photo)
        self.label_image_preview.image = photo  # reference 유지
        self.current_photo_image = photo
        self.btn_start.config(state=tk.NORMAL)


    def start_prediction(self):
        """모델 예측 실행"""
        if self.current_image_path is None:
            return
        
        try:
            # SMILES 예측
            result_text = self.model.predict(self.current_image_path)
            # RDKit 이미지 생성
            result_img = Draw.MolToImage(
                MolFromSmiles(result_text),
                size=(self.output_size_width, self.output_size_height),
                kekulize=True,
                wedgeBonds=True,
                fitImage=True
            )
        except Exception as e:
            messagebox.showerror("ERROR", f"예측 실패:\n{e}")
            return

        # 결과 텍스트 → Entry에 삽입
        self.entry_result.config(state="normal")
        self.entry_result.delete(0, tk.END)
        self.entry_result.insert(0, result_text)
        self.entry_result.config(state="readonly")

        # 원본 입력 이미지 표시
        img = Image.open(self.current_image_path)
        img.thumbnail((self.output_size_width, self.output_size_height))
        input_photo = ImageTk.PhotoImage(img)
        self.label_result_input.delete("all")
        cx, cy = self.output_size_width // 2, self.output_size_height // 2
        self.label_result_input.create_image(cx, cy, image=input_photo)
        self.label_result_input.image = input_photo

        # RDKit 이미지 표시
        mol_photo = ImageTk.PhotoImage(result_img)
        self.label_result_mol.delete("all")
        self.label_result_mol.create_image(cx, cy, image=mol_photo)
        self.label_result_mol.image = mol_photo

        # 화면 전환
        self.frame_input.pack_forget()
        self.frame_result.pack(fill="both", expand=True)


    def go_back(self):
        """결과 화면에서 입력 화면으로 돌아가기"""
        self.frame_result.pack_forget()
        self.frame_input.pack(fill="both", expand=True)

        ## 상태 초기화
        self.current_image_path = None
        self.current_photo_image = None
        self.btn_start.config(state=tk.DISABLED)
        
        ## Canvas 초기화
        self.init_preview()


    def init_preview(self):
        """미리보기 화면 초기화"""
        self.label_image_preview.delete("all")
        self.label_image_preview.create_rectangle(0, 0, 400, 400, fill="gray")
        self.label_image_preview.create_text(200, 200, text="Select an image", fill="black")


    def copy_smiles(self):
        """SMILES 문자열을 클립보드에 복사"""
        smiles = self.entry_result.get()
        if smiles:
            self.root.clipboard_clear()
            self.root.clipboard_append(smiles)
            messagebox.showinfo("Copied", "SMILES copied to clipboard!")


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()