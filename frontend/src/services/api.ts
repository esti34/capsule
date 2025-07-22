import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export interface Item {
  id: number;
  name: string;
  description: string | null;
  owner_id: number;
  is_active: boolean;
}

export interface User {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
  items: Item[];
}

export interface CreateUserData {
  email: string;
  username: string;
  password: string;
}

export interface CreateItemData {
  name: string;
  description?: string;
}

const api = {
  // User endpoints
  getUsers: async () => {
    const response = await axios.get<User[]>(`${API_URL}/api/users/`);
    return response.data;
  },
  
  getUser: async (id: number) => {
    const response = await axios.get<User>(`${API_URL}/api/users/${id}`);
    return response.data;
  },
  
  createUser: async (userData: CreateUserData) => {
    const response = await axios.post<User>(`${API_URL}/api/users/`, userData);
    return response.data;
  },
  
  // Item endpoints
  getItems: async () => {
    const response = await axios.get<Item[]>(`${API_URL}/api/items/`);
    return response.data;
  },
  
  createItem: async (userId: number, itemData: CreateItemData) => {
    const response = await axios.post<Item>(
      `${API_URL}/api/users/${userId}/items/`, 
      itemData
    );
    return response.data;
  },
};

export default api; 