import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface EmotionData {
  date: string;
  emotions: {
    anger: number;
    disgust: number;
    fear: number;
    joy: number;
    neutral: number;
    sadness: number;
    surprise: number;
  };
}

interface SummaryData {
  date: string;
  description: string;
}

interface EmotionChartProps {
  data: EmotionData[];
  summaryData: SummaryData[];
}

const EmotionChart: React.FC<EmotionChartProps> = ({ data }) => {
  // Filter data to only include dates from 01/04/2025 to 10/04/2025
  const filteredData = data.filter(item => {
    const [day, month, year] = item.date.split('/').map(Number);
    const date = new Date(year, month - 1, day);
    const startDate = new Date(2025, 3, 1); // April 1, 2025
    const endDate = new Date(2025, 3, 10); // April 10, 2025
    return date >= startDate && date <= endDate;
  });

  // Sort data by date to ensure chronological order
  const sortedData = [...filteredData].sort((a, b) => {
    const [dayA, monthA, yearA] = a.date.split('/').map(Number);
    const [dayB, monthB, yearB] = b.date.split('/').map(Number);
    return new Date(yearA, monthA - 1, dayA).getTime() - new Date(yearB, monthB - 1, dayB).getTime();
  });

  const chartData = {
    labels: sortedData.map(item => item.date),
    datasets: [
      {
        label: 'Joy',
        data: sortedData.map(item => item.emotions.joy),
        borderColor: '#FFD700',
        backgroundColor: 'rgba(255, 215, 0, 0.5)',
        tension: 0.4
      },
      {
        label: 'Sadness',
        data: sortedData.map(item => item.emotions.sadness),
        borderColor: '#4169E1',
        backgroundColor: 'rgba(65, 105, 225, 0.5)',
        tension: 0.4
      },
      {
        label: 'Anger',
        data: sortedData.map(item => item.emotions.anger),
        borderColor: '#FF4500',
        backgroundColor: 'rgba(255, 69, 0, 0.5)',
        tension: 0.4
      },
      {
        label: 'Fear',
        data: sortedData.map(item => item.emotions.fear),
        borderColor: '#800080',
        backgroundColor: 'rgba(128, 0, 128, 0.5)',
        tension: 0.4
      },
      {
        label: 'Surprise',
        data: sortedData.map(item => item.emotions.surprise),
        borderColor: '#FF69B4',
        backgroundColor: 'rgba(255, 105, 180, 0.5)',
        tension: 0.4
      },
      {
        label: 'Neutral',
        data: sortedData.map(item => item.emotions.neutral),
        borderColor: '#808080',
        backgroundColor: 'rgba(128, 128, 128, 0.5)',
        tension: 0.4
      },
      {
        label: 'Disgust',
        data: sortedData.map(item => item.emotions.disgust),
        borderColor: '#006400',
        backgroundColor: 'rgba(0, 100, 0, 0.5)',
        tension: 0.4
      }
    ]
  };

  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Emotional Patterns Over Time',
        font: {
          size: 16
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 10,
        title: {
          display: true,
          text: 'Intensity (1-10)'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Date'
        }
      }
    }
  };

  return (
    <div className="chart-container">
      <Line data={chartData} options={options} />
    </div>
  );
};

export default EmotionChart; 