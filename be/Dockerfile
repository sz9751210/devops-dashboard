# 使用官方的 Python 基礎映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝 Python 依賴
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# 複製應用程式碼到工作目錄
COPY . .

# 設定環境變數
# ENV FLASK_APP=main.py
# ENV FLASK_RUN_HOST=0.0.0.0

# 暴露應用的運行端口
EXPOSE 9090

# 啟動應用
CMD ["python", "main.py"]
