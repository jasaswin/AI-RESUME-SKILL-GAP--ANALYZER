
const GapList = ({ gaps, title }) => {
  if (!Array.isArray(gaps)) return null;

  return (
    <div className="section">
      <h3>{title}</h3>

      <div>
        {gaps.map((skill, index) => (
          <span key={index} className="tag">
            {typeof skill === "object" ? skill.skill : skill}
          </span>
        ))}
      </div>
    </div>
  );
};

export default GapList;
