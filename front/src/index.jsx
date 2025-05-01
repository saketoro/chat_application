import React from 'react';
import ReactDOM from 'react-dom/client';
// import './index.css';
import {App} from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// パフォーマンス測定のための関数
// 詳細は https://bit.ly/CRA-vitals を参照
reportWebVitals();
