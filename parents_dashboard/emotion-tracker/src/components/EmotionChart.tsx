import React, { useMemo } from 'react';
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
    [key: string]: number;
  };
}

interface EmotionChartProps {
  data: EmotionData[];
  summaryData: Array<{
    date: string;
    description: string;
  }>;
}

const EmotionChart: React.FC<EmotionChartProps> = ({ data, summaryData }) => {
  console.log('EmotionChart rendering with data:', data);
  
  if (!data || data.length === 0) {
    console.log('No data available for chart');
    return <div>No data available for chart</div>;
  }
  
  // Get all unique emotion keys from the data
  const emotionKeys = useMemo(() => {
    const keys = new Set<string>();
    data.forEach(item => {
      Object.keys(item.emotions).forEach(key => keys.add(key));
    });
    return Array.from(keys);
  }, [data]);
  
  console.log('Emotion keys found:', emotionKeys);
  
  // Generate colors for each emotion
  const getEmotionColor = (emotion: string, index: number) => {
    const colors = [
      'rgb(75, 192, 192)',   // teal
      'rgb(255, 99, 132)',   // pink
      'rgb(255, 159, 64)',   // orange
      'rgb(153, 102, 255)',  // purple
      'rgb(54, 162, 235)',   // blue
      'rgb(255, 205, 86)',   // yellow
      'rgb(201, 203, 207)',  // gray
      'rgb(255, 99, 71)',    // tomato
      'rgb(50, 205, 50)',    // lime
      'rgb(147, 112, 219)'   // medium purple
    ];
    return colors[index % colors.length];
  };
  
  // Generate background colors for each emotion
  const getEmotionBackgroundColor = (emotion: string, index: number) => {
    const color = getEmotionColor(emotion, index);
    return color.replace('rgb', 'rgba').replace(')', ', 0.5)');
  };
  
  // Get emotion emoji based on the exact emotion name from the file
  const getEmotionEmoji = (emotion: string) => {
    const emojis: { [key: string]: string } = {
      // Emotions from the file
      "happiness": "😊",
      "sadness": "😢",
      "anger": "😠",
      "fear": "😨",
      "excitement": "🤩",
      "calm": "😌",
      "frustration": "😤",
      "satisfaction": "😊",
      "worry": "😟",
      "contentment": "😌",
      
      // Additional emotions that might be in the file
      "joy": "😄",
      "surprise": "😲",
      "disgust": "🤢",
      "neutral": "😐",
      "embarrassment": "😳",
      "anxiety": "😰",
      "confusion": "😕",
      "disappointment": "😞",
      "pride": "😊",
      "relief": "😌"
    };
    return emojis[emotion.toLowerCase()] || "😐";
  };
  
  // Create datasets dynamically based on available emotions
  const chartData = useMemo(() => {
    return {
      labels: data.map(item => item.date),
      datasets: emotionKeys.map((emotion, index) => ({
        label: emotion.charAt(0).toUpperCase() + emotion.slice(1),
        data: data.map(item => item.emotions[emotion] || 0),
        borderColor: getEmotionColor(emotion, index),
        backgroundColor: getEmotionBackgroundColor(emotion, index),
        tension: 0.3,
      }))
    };
  }, [data, emotionKeys]);
  
  console.log('Chart data prepared:', chartData);

  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          padding: 20,
          font: {
            size: 14,
            weight: 'bold'
          },
          boxWidth: 15,
          boxHeight: 15,
          usePointStyle: true
        }
      },
      title: {
        display: true,
        text: 'Emotional Patterns Over Time',
        font: {
          size: 24,
          weight: 'bold'
        },
        padding: {
          top: 20,
          bottom: 30
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        padding: 12,
        titleFont: {
          size: 16,
          weight: 'bold'
        },
        bodyFont: {
          size: 14
        },
        boxPadding: 6
      }
    },
    scales: {
      x: {
        grid: {
          display: false
        },
        ticks: {
          font: {
            size: 12
          },
          maxRotation: 45,
          minRotation: 45
        }
      },
      y: {
        beginAtZero: true,
        max: 10,
        grid: {
          color: 'rgba(0, 0, 0, 0.1)'
        },
        ticks: {
          font: {
            size: 12
          },
          stepSize: 2
        }
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    }
  };
  
  return (
    <div className="card">
      <h2 className="section-title">Emotion Tracker</h2>
      
      <div style={{ height: '600px', width: '100%', padding: '20px' }}>
        <Line data={chartData} options={options} />
      </div>
      
      <div className="emotion-legend">
        {emotionKeys.map((emotion, index) => (
          <div key={emotion} className="emotion-item">
            <div 
              className="emotion-color" 
              style={{ backgroundColor: getEmotionColor(emotion, index) }}
            />
            <span>{getEmotionEmoji(emotion)} {emotion.charAt(0).toUpperCase() + emotion.slice(1)}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EmotionChart; 