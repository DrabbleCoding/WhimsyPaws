import { EmotionData, SummaryData, ProcessedData } from '../types';

// This would normally fetch from an API or file
// For this demo, we'll use mock data
export const loadEmotionsData = (): EmotionData => {
  return {
    "01/04/2025": {
      "anger": 2,
      "disgust": 1,
      "fear": 6,
      "joy": 2,
      "neutral": 3,
      "sadness": 5,
      "surprise": 3
    },
    "02/04/2025": {
      "anger": 3,
      "disgust": 1,
      "fear": 4,
      "joy": 2,
      "neutral": 2,
      "sadness": 8,
      "surprise": 5
    },
    "03/04/2025": {
      "anger": 1,
      "disgust": 0,
      "fear": 2,
      "joy": 9,
      "neutral": 3,
      "sadness": 1,
      "surprise": 4
    },
    "04/04/2025": {
      "anger": 1,
      "disgust": 0,
      "fear": 3,
      "joy": 5,
      "neutral": 6,
      "sadness": 2,
      "surprise": 3
    },
    "05/04/2025": {
      "anger": 2,
      "disgust": 1,
      "fear": 4,
      "joy": 3,
      "neutral": 5,
      "sadness": 4,
      "surprise": 2
    },
    "06/04/2025": {
      "anger": 1,
      "disgust": 0,
      "fear": 2,
      "joy": 7,
      "neutral": 4,
      "sadness": 2,
      "surprise": 3
    },
    "07/04/2025": {
      "anger": 1,
      "disgust": 0,
      "fear": 1,
      "joy": 8,
      "neutral": 3,
      "sadness": 1,
      "surprise": 2
    },
    "08/04/2025": {
      "anger": 1,
      "disgust": 0,
      "fear": 1,
      "joy": 9,
      "neutral": 2,
      "sadness": 1,
      "surprise": 3
    },
    "09/04/2025": {
      "anger": 3,
      "disgust": 1,
      "fear": 4,
      "joy": 2,
      "neutral": 2,
      "sadness": 7,
      "surprise": 2
    },
    "10/04/2025": {
      "anger": 1,
      "disgust": 0,
      "fear": 2,
      "joy": 7,
      "neutral": 3,
      "sadness": 2,
      "surprise": 3
    }
  };
};

export const loadSummaryData = (): SummaryData[] => {
  return [
    {
      date: "2025-04-01",
      description: "User felt anxious and discouraged after the math test, dwelling on a mistake despite having prepared."
    },
    {
      date: "2025-04-02",
      description: "User was deeply disappointed about not making the soccer team and felt emotionally low, but comforted by a supportive friend."
    },
    {
      date: "2025-04-03",
      description: "User was in high spirits, enjoying a fun birthday party and socializing with new friends."
    },
    {
      date: "2025-04-04",
      description: "User was thoughtful and calm during the hospital visit, showing curiosity and emotional maturity."
    },
    {
      date: "2025-04-05",
      description: "User felt physically unwell and emotionally subdued, mostly resting and staying quiet."
    },
    {
      date: "2025-04-06",
      description: "User felt more energetic and creatively engaged as they recovered, showing signs of returning joy."
    },
    {
      date: "2025-04-07",
      description: "User was confident and proud, happy to share their art and be back in their normal routine."
    },
    {
      date: "2025-04-08",
      description: "User was cheerful and playful, enjoying quality time with a friend and feeling lighthearted."
    },
    {
      date: "2025-04-09",
      description: "User came home feeling hurt and sad after being teased, needing extra emotional support."
    },
    {
      date: "2025-04-10",
      description: "User seemed much more upbeat and hopeful, talking openly and showing interest in new activities."
    }
  ];
};

export const processEmotionData = (emotionsData: EmotionData): ProcessedData => {
  // Convert dates to YYYY-MM-DD format
  const formattedDates = Object.keys(emotionsData).map(date => {
    const [day, month, year] = date.split('/');
    return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
  });
  
  // Sort dates
  const dates = formattedDates.sort();
  
  // Get all emotions
  const emotions = Object.keys(emotionsData[Object.keys(emotionsData)[0]]);
  
  // Create emotion values object
  const emotionValues: { [emotion: string]: number[] } = {};
  
  // Initialize emotion values arrays
  emotions.forEach(emotion => {
    emotionValues[emotion] = [];
  });
  
  // Fill emotion values arrays
  dates.forEach(date => {
    const originalDate = date.split('-').reverse().join('/');
    emotions.forEach(emotion => {
      emotionValues[emotion].push(emotionsData[originalDate][emotion]);
    });
  });
  
  return {
    dates,
    emotionValues
  };
}; 