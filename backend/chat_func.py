from langchain_community.llms import LlamaCpp
from fastapi import HTTPException

def chat_with_llama(model_name: str, user_message: str):
    """
    Llamaモデルを使用してチャット応答を生成する関数。

    Args:
        model_name (str): 使用するモデルの名前。
        user_message (str): ユーザーからのメッセージ。

    Returns:
        str: モデルからの応答メッセージ。
    """
    # モデルの準備
    llm = LlamaCpp(model_path=model_name)

    # プロンプト編集
    prompt = "あなたは誠実で優秀な日本人のアシスタントです。特に指示が無い場合は、常に日本語で回答してください。{}。".format(user_message)

    # Llamaモデルを使用して応答を生成
    try:
        bot_message = llm.invoke(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Llamaモデルエラー: {str(e)}")

    return bot_message