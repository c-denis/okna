// В users.d.ts
declare interface User {
  id: string;
  name: string;
  role: string;
  // другие свойства пользователя
}

// Делаем файл модулем
export { User };
