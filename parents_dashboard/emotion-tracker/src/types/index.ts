export interface EmotionData {
  [date: string]: {
    [emotion: string]: number;
  };
}

export interface SummaryData {
  date: string;
  description: string;
}

export interface EmotionValue {
  date: string;
  [emotion: string]: string | number;
}

export interface ProcessedData {
  dates: string[];
  emotionValues: { [emotion: string]: number[] };
} 