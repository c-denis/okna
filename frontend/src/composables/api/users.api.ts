import httpClient from '@/utils/httpClient';

export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  status: 'active' | 'inactive' | 'suspended';
  createdAt: string;
}

export interface Manager extends User {
  assignedRequestsCount: number;
}

export interface Role {
  id: string;
  name: string;
  permissions: string[];
}

export const fetchManagers = async (): Promise<Manager[]> => {
  try {
    const response = await httpClient.get<Manager[]>('/users/managers');
    return response.data;
  } catch (error) {
    console.error('Error fetching managers:', error);
    throw error;
  }
};

export const fetchUserRoles = async (): Promise<Role[]> => {
  try {
    const response = await httpClient.get<Role[]>('/users/roles');
    return response.data;
  } catch (error) {
    console.error('Error fetching user roles:', error);
    throw error;
  }
};

export const updateManagerStatus = async (
  managerId: string,
  status: 'active' | 'inactive'
): Promise<Manager> => {
  try {
    const response = await httpClient.patch<Manager>(
      `/users/managers/${managerId}/status`,
      { status }
    );
    return response.data;
  } catch (error) {
    console.error(`Error updating manager ${managerId} status:`, error);
    throw error;
  }
};
