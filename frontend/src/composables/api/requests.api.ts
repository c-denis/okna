import httpClient from '@/utils/httpClient';

export enum RequestStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  REJECTED = 'rejected'
}

export interface RequestData {
  title: string;
  description: string;
  priority?: 'low' | 'medium' | 'high';
  category: string;
}

export interface Request extends RequestData {
  id: string;
  status: RequestStatus;
  createdAt: string;
  updatedAt?: string;
  assignedManagerId?: string;
}

export const fetchRequests = async (): Promise<Request[]> => {
  try {
    const response = await httpClient.get<Request[]>('/requests');
    return response.data;
  } catch (error) {
    console.error('Error fetching requests:', error);
    throw error;
  }
};

export const createRequest = async (data: RequestData): Promise<Request> => {
  try {
    const response = await httpClient.post<Request>('/requests', data);
    return response.data;
  } catch (error) {
    console.error('Error creating request:', error);
    throw error;
  }
};

export const assignRequest = async (requestId: string, managerId: string): Promise<Request> => {
  try {
    const response = await httpClient.patch<Request>(`/requests/${requestId}/assign`, { managerId });
    return response.data;
  } catch (error) {
    console.error(`Error assigning request ${requestId}:`, error);
    throw error;
  }
};

export const updateRequestStatus = async (
  requestId: string,
  status: RequestStatus
): Promise<Request> => {
  try {
    const response = await httpClient.patch<Request>(`/requests/${requestId}/status`, { status });
    return response.data;
  } catch (error) {
    console.error(`Error updating status for request ${requestId}:`, error);
    throw error;
  }
};

export const getRequestDetails = async (requestId: string): Promise<Request> => {
  try {
    const response = await httpClient.get<Request>(`/requests/${requestId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching details for request ${requestId}:`, error);
    throw error;
  }
};
