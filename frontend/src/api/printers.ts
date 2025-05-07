import axios from 'axios';

// Printer data type
export interface Printer {
  name: string;
  web_name: string;
  x: number;
  y: number;
  w: number;
  h: number;
  d_x: number;
  d_y: number;
}

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Load printers list
export async function fetchPrinters(): Promise<Record<string, Printer>> {
  const response = await axios.get<Record<string, Printer>>(`${API_URL}/api/printers`);
  return response.data;
}
