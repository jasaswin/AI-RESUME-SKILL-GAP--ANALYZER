
// const SkillMatchCard = ({ percentage }) => {
//   return (
//     <div>
//       <h3>Skill Match</h3>
//       <h1 style={{ color: "#8b5cf6" }}>{percentage}%</h1>
//     </div>
//   );
// };

// export default SkillMatchCard;


const SkillMatchCard = ({ percentage }) => {
  const radius = 60;
  const stroke = 10;
  const normalizedRadius = radius - stroke * 2;
  const circumference = normalizedRadius * 2 * Math.PI;

  const strokeDashoffset =
    circumference - (percentage / 100) * circumference;

  return (
    <div style={{ textAlign: "center", marginTop: "20px" }}>
      <svg height={radius * 2} width={radius * 2}>
        <circle
          stroke="#333"
          fill="transparent"
          strokeWidth={stroke}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
        <circle
          stroke="#8b5cf6"
          fill="transparent"
          strokeWidth={stroke}
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          r={normalizedRadius}
          cx={radius}
          cy={radius}
          style={{ transition: "0.5s" }}
        />
      </svg>

      <h2 style={{ marginTop: "-90px", color: "#8b5cf6" }}>
        {percentage}%
      </h2>

      <p>Skill Match</p>
    </div>
  );
};

export default SkillMatchCard;