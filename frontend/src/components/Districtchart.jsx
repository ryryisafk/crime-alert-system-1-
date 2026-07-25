import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";


function DistrictChart({ data }) {

  return (

    <div className="chart-card">

      <h2>Crime by District</h2>

      <ResponsiveContainer width="100%" height={400}>

        <BarChart
          data={data}
          layout="vertical"
          margin={{
            left: 30,
          }}
        >

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis type="number" />

          <YAxis
            dataKey="district"
            type="category"
            width={100}
          />

          <Tooltip />

          <Bar
            dataKey="count"
            fill="#ef4444"
            radius={[0,8,8,0]}
          />

        </BarChart>

      </ResponsiveContainer>

    </div>

  );

}


export default DistrictChart;