# 開発環境
- OS : Windows11
- Shell : Powershell

# 開発環境の準備手順
開発環境の準備手順です
1. 下記コマンドをPowerShellで実行してUVをインストールする
   ```
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
2. 下記コマンドを実行し、backendディレクトリに移動する
   ```
   cd backend
   ```
3. 下記コマンドを実行し、UVのプロジェクトを作成する
    ```
    uv init my-project --no-readme --app
    ```
4. 下記のコマンドを実行し、仮想環境を作成する
    ```
    cd my-project
    ```
5. 下記のコマンドを実行し、仮想環境を作成する
    ```
    uv venv
    ```
6. 仮想環境を有効にする  
    ```
    venv\Scripts\activate
    ```
7. 下記コマンドを実行し、依存パッケージをインストールする
    ```
    uv add -r ../requirements.txt
    ```

# FastAPIアプリケーションの起動方法 
- 下記コマンドを実行し、APIを起動する
      
    ```
    python api_app.py
    ```
# MCPサーバーの起動方法
- 下記コマンドを実行し、APIを起動する
      
    ```
    python mcp_app.py
    ```

# Dockerの起動方法
## Dockerイメージの作成
`docker build -t chat_application .`

## コンテナの起動
`docker run -p 8000:8000 -p 8001:8001 chat_application`


# 参考リンク
## UV
- [uvを使ってPython実行環境を整理してみた](https://dev.classmethod.jp/articles/i-like-uv/)
- [uv （pythonパッケージマネージャー）の使い方　簡易版](https://qiita.com/futakuchi0117/items/9ec8bd84797fed180647)
- [uvだけでPythonプロジェクトを管理する](https://zenn.dev/turing_motors/articles/594fbef42a36ee)

## FastAPI
- [【完全版】React + FastAPIで開発するモダンなwebアプリ](https://zenn.dev/sawao/articles/15a9cf0e3360a7)