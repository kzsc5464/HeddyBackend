import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const PetHealthChart = () => {
  const [healthData, setHealthData] = useState([]);

  useEffect(() => {
    const mockData = [
      {
        _id: '676d428cf344936d774dca25',
        pet_id: '65b97def28b77c2230b2c997',
        heart_rate: 222,
        steps: 13,
        calories: 35,
        distance: 353,
        recorded_at: '2024-12-26T11:48:28.344+00:00',
      },
      // Add more mock data points here for testing
    ];

    // Format the date for better display
    const formattedData = mockData.map(item => ({
      ...item,
      recorded_at: new Date(item.recorded_at).toLocaleTimeString(),
    }));

    setHealthData(formattedData);
  }, []);

  return (
    <div className="w-full h-96 p-4 bg-white rounded-lg shadow">
      <h2 className="text-xl font-bold mb-4">Pet Health Metrics</h2>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={healthData}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="recorded_at"
            label={{ value: 'Time', position: 'bottom' }}
          />
          <YAxis 
            yAxisId="left"
            label={{ value: 'Heart Rate / Steps', angle: -90, position: 'insideLeft' }}
          />
          <YAxis 
            yAxisId="right" 
            orientation="right"
            label={{ value: 'Calories / Distance', angle: 90, position: 'insideRight' }}
          />
          <Tooltip />
          <Legend />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="heart_rate"
            stroke="#8884d8"
            name="Heart Rate"
            dot={false}
          />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="steps"
            stroke="#82ca9d"
            name="Steps"
            dot={false}
          />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="calories"
            stroke="#ffc658"
            name="Calories"
            dot={false}
          />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="distance"
            stroke="#ff7300"
            name="Distance"
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PetHealthChart;