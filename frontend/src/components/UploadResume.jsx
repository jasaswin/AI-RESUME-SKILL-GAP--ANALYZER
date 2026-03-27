import { useState } from "react";
import { analyzeResume } from "../services/api";
import { useNavigate } from "react-router-dom";

const UploadResume = () => {
  const [file, setFile] = useState(null);
  const [jd, setJd] = useState("");
  const [loading, setLoading] = useState(false); // ✅ NEW
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file || !jd) {
      return alert("Upload resume and enter job description");
    }

    const formData = new FormData();
    formData.append("resume_file", file);
    formData.append("job_description", jd);

    try {
      setLoading(true); // ✅ start loading
      const res = await analyzeResume(formData);
      navigate("/result", { state: res.data });
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false); // ✅ stop loading
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />

      <textarea
        placeholder="Paste Job Description..."
        value={jd}
        onChange={(e) => setJd(e.target.value)}
      />

      <button type="submit">
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>
    </form>
  );
};

export default UploadResume;
