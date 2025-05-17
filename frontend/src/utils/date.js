import { format, startOfWeek, startOfMonth } from 'date-fns';

export const formatDate = (date) => format(new Date(date), 'dd.MM.yyyy');

export const getPeriodDates = (period) => {
  const today = new Date();

  switch (period) {
    case 'today':
      return {
        start: today,
        end: today
      };
    case 'week':
      return {
        start: startOfWeek(today),
        end: today
      };
    case 'month':
      return {
        start: startOfMonth(today),
        end: today
      };
    default:
      return {
        start: today,
        end: today
      };
  }
};
