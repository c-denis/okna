// src/types/requests.d.ts
declare interface Request {
  id: string;
  // другие поля запроса
}

declare interface RequestData {
    data: Date; // структура данных запроса
}

declare interface RequestStatus {
  // возможные статусы
}

// Делаем файл модулем
export { Request, RequestData, RequestStatus };
