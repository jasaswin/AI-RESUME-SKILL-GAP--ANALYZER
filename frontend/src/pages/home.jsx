
import UploadResume from "../components/UploadResume";

const Home = () => {
  return (
    <div className="container">
      <div className="card">
        <h1>AI Resume Analyzer</h1>
        <p>Find your skill gaps instantly 🚀</p>
        <UploadResume />
      </div>
    </div>
  );
};

export default Home;