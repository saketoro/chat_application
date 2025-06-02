import { useState } from 'react';
import axios from 'axios';

const url = "http://127.0.0.1:8000";

export const App = () => {
  const [userMessage, setUserMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [uploadMessage, setUploadMessage] = useState("");
  const allowedFileTypes = ["text/plain"];

  const sendMessage = async () => {
    if (!userMessage.trim()) return;

    const newHistory = [...chatHistory, { role: "user", content: userMessage }];
    setChatHistory(newHistory);
    setUserMessage("");

    try {
      const response = await axios.post(`${url}/chat`, {
        user_message: userMessage,
        history: newHistory,
      });

      setChatHistory([...newHistory, { role: "bot", content: response.data.bot_message }]);
    } catch (error) {
      console.error("Error fetching chat response:", error);
      alert("エラーが発生しました。もう一度お試しください。");
    }
  };

  const uploadFile = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    if (!allowedFileTypes.includes(file.type)) {
      setUploadMessage("アップロードできるのは.txt形式のファイルのみです。");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(`${url}/upload_files`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setUploadMessage("アップロード成功: " + response.data.message + " " + response.data.db_id)
    } catch (error) {
      console.error("Error uploading file:", error);
      setUploadMessage("ファイルのアップロード中にエラーが発生しました。");
    }
  };

  return (
    <>
      <div>
        <h1>チャットアプリ</h1>
        <div style={{ border: "1px solid #ccc", padding: "10px", marginBottom: "10px", height: "300px", overflowY: "scroll" }}>
          {chatHistory.map((message, index) => (
            <div key={index} style={{ margin: "5px 0" }}>
              <strong>{message.role === "user" ? "あなた" : "AI"}:</strong> {message.content}
            </div>
          ))}
        </div>
        <input
          type="text"
          value={userMessage}
          onChange={(e) => setUserMessage(e.target.value)}
          placeholder="メッセージを入力してください"
          style={{ width: "80%", marginRight: "10px" }}
        />
        <button onClick={sendMessage}>送信</button>

        <div style={{ marginTop: "20px" }}>
          <h2>ファイルアップロード</h2>
          <input type="file" onChange={uploadFile} />
          {uploadMessage && <p>{uploadMessage}</p>}
        </div>
      </div>
    </>
  );
};