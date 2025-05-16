type ValidationResult = string | boolean
type ValidationRule = (value: string) => ValidationResult

/**
 * Проверка на обязательное поле
 */
export const required: ValidationRule = (value) => {
  return !!value.trim() || 'Поле обязательно для заполнения'
}

/**
 * Проверка email
 */
export const email: ValidationRule = (value) => {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return pattern.test(value) || 'Введите корректный email'
}

/**
 * Проверка номера телефона
 */
export const phone: ValidationRule = (value) => {
  const pattern = /^\+?[\d\s\-()]{10,}$/
  return pattern.test(value) || 'Введите корректный номер телефона'
}

/**
 * Проверка минимальной длины
 * @param min Минимальная длина
 */
export const minLength = (min: number): ValidationRule => {
  return (value) => {
    return value.length >= min || `Минимальная длина - ${min} символов`
  }
}

/**
 * Проверка совпадения паролей
 * @param compareWith Поле для сравнения (Ref)
 */
export const matchPassword = (compareWith: Ref<string>): ValidationRule => {
  return (value) => {
    return value === compareWith.value || 'Пароли не совпадают'
  }
}

/**
 * Создание составного валидатора
 * @param rules Массив правил валидации
 */
export const createValidator = (rules: ValidationRule[]) => {
  return (value: string): ValidationResult => {
    for (const rule of rules) {
      const result = rule(value)
      if (typeof result === 'string') return result
    }
    return true
  }
}
