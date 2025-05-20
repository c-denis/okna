import type { Manager } from './users.d';

export enum RequestStatus {
  UNASSIGNED = 'unassigned',
  ASSIGNED = 'assigned',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  REJECTED = 'rejected'
}

export interface RequestCreateData {
  client_name: string;
  phone: string;
  address: string;
  city?: string;
  comment?: string;
  priority?: 'low' | 'medium' | 'high';
}

export interface Request extends RequestCreateData {
  id: number;
  status: RequestStatus;
  created_at: string;
  updated_at?: string;
  assigned_to?: Manager;
  is_blacklisted: boolean;
  status_history?: StatusHistoryItem[];
}

export interface StatusHistoryItem {
  status: RequestStatus;
  changed_at: string;
  changed_by: string;
  comment?: string;
}

export interface RequestFilterParams {
  status?: RequestStatus;
  manager_id?: number;
  city?: string;
  date_from?: string;
  date_to?: string;
  is_blacklisted?: boolean;
  search?: string;
}

export interface AssignRequestData {
  manager_id: number;
}

export interface UpdateStatusData {
  status: RequestStatus;
  comment?: string;
}

export interface BlacklistRequestData {
  reason: string;
}
