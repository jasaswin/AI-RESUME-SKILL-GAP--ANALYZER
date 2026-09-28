
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
  baseURL: "https://ai-resume-skill-gap-analyzer-api.onrender.com",
});

export const analyzeResume = (formData) =>
  API.post("/analyze/", formData);

export const chatWithBot = (data) =>
  API.post("/chat", data);