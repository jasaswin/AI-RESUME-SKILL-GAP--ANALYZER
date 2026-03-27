
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const SkillChart = ({ matched, missing }) => {
  const data = [
    { name: "Matched", value: matched?.length || 0 },
    { name: "Missing", value: missing?.length || 0 },
  ];

  return (
    <div style={{ height: 250 }}>
      <ResponsiveContainer>
        <BarChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SkillChart;