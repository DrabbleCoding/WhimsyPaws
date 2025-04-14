declare module '*/emotions.json' {
  const value: Array<{
    date: string;
    emotions: {
      [key: string]: number;
    };
  }>;
  export default value;
} 