import { useState } from 'react';
import axios from 'axios';

const url = "http://127.0.0.1:8000";

export const App = () => {
  const [data, setData] = useState({ message: '' });

  const getHello = async () => {
    try {
      const response = await axios.get(url);
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <>
      <p>ここにアプリの内容を記述します。</p>
      <div>
        {data.message}
      </div>
      <button onClick={getHello}>APIにリクエストを送信</button>
    </>
  );
}