# PrototypeYoloInferencing
Prototype for my thesis in

Before Installation: 
Make sure you have Python 3.10 installed and have the path added to environment variables. 

check by running py --version or python --version, result should be Python 3.10.x

Check your CUDA version with.

nvidia-smi


Installation Instruction
1.  In the project folder, clone Allan's Yolov10 fork
	git clone https://github.com/allansdefreitas/yolov10.git .
2. Inside the yolov10 folder, create venv
	py -3.10 -m venv venv
	this should make yolov10\venv
3. Activate Virtual Enviroment
	venv\Scripts\activate
4. Inside venv, Install required tools
	pip install --upgrade pip setuptools wheel
	pip install ultralytics
	pip install -r requirements.txt
5. install Pytorch with GPU support
	pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

