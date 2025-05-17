interface ReportData {
  total: number;
  completed: number;
  rejected: number;
  averageTime: string;
  byStatus: Array<{
    status: string;
    count: number;
  }>;
  byCity: Array<{
    city: string;
    total: number;
    completed: number;
  }>;
}

interface ManagerStats {
  id: number;
  name: string;
  completed: number;
  rejected: number;
  efficiency: number;
  lastActivity?: string;
}
