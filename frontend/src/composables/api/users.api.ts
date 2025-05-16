import axios from '@/api/client';

export const fetchManagersApi = async () => {
  return axios.get('/users/managers');
};

export const fetchUserRolesApi = async () => {
  return axios.get('/users/roles');
};

export const updateManagerStatus = async (managerId: string, status: string) => {
  return axios.patch(`/users/managers/${managerId}/status`, { status });
};
