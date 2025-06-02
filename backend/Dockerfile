# ベースイメージを指定
FROM python:3.13-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なビルドツールをインストール
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    cmake \
    git \
    && apt-get clean

# 必要なファイルをコンテナにコピー
COPY ./requirements.txt /app/requirements.txt
COPY ./ /app/

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install llama-cpp-python>=0.1.50 --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

# ポートを公開
EXPOSE 8000
EXPOSE 8001

# 起動前にファイル構造を確認
RUN ls -la /app/

# デフォルトのコマンドを設定
CMD ["sh", "-c", "python /app/api_app.py & python /app/mcp_app.py"]