export interface Observation {
  id: string;
  date: string;
  message: string;
}

export interface ParentInputState {
  observations: Observation[];
  currentMessage: string;
  isLoading: boolean;
  error: string | null;
} 