import axios from '@/api/client';
import type { RequestData, RequestStatus } from '@/types/requests';

export const fetchRequests = async () => {
  return axios.get('/requests');
};

export const createRequest = async (data: RequestData) => {
  return axios.post('/requests', data);
};

export const assignRequest = async (requestId: string, managerId: string) => {
  return axios.patch(`/requests/${requestId}/assign`, { managerId });
};

export const updateRequestStatus = async (requestId: string, status: RequestStatus) => {
  return axios.patch(`/requests/${requestId}/status`, { status });
};

export const getRequestDetails = async (requestId: string) => {
  return axios.get(`/requests/${requestId}`);
};
