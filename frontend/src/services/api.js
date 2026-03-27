
// import axios from "axios";

// const API = axios.create({
//   baseURL: "http://127.0.0.1:8000",
// });

// export const analyzeResume = (formData) =>
//   API.post("/analyze", formData, {
//     headers: {
//       "Content-Type": "multipart/form-data",
//     },
//   });

import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const analyzeResume = (formData) =>
  API.post("/analyze/", formData); // ✅ match backend + no manual headers

export const chatWithBot = (data) =>
  API.post("/chat", data);