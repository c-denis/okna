import { ref } from 'vue'

interface ValidationRules {
  [key: string]: {
    required?: boolean
    minLength?: number
    pattern?: RegExp
    validator?: (value: any) => boolean | string
  }
}

export function useValidation<T extends Record<string, any>>(
  formData: T,
  rules: ValidationRules
) {
  const errors = ref<Record<string, string>>(
    Object.keys(rules).reduce((acc, key) => ({ ...acc, [key]: '' }), {})
  )

  const validateField = (field: string): boolean => {
    if (!rules[field]) return true

    const value = formData[field]
    const rule = rules[field]
    let isValid = true

    if (rule.required && !value) {
      errors.value[field] = 'Field is required'
      return false
    }

    if (rule.minLength && value && value.length < rule.minLength) {
      errors.value[field] = `Minimum length is ${rule.minLength}`
      isValid = false
    }

    if (rule.pattern && value && !rule.pattern.test(value)) {
      errors.value[field] = 'Invalid format'
      isValid = false
    }

    if (rule.validator) {
      const customValidation = rule.validator(value)
      if (typeof customValidation === 'string') {
        errors.value[field] = customValidation
        isValid = false
      } else if (!customValidation) {
        errors.value[field] = 'Invalid value'
        isValid = false
      }
    }

    if (isValid) {
      errors.value[field] = ''
    }

    return isValid
  }

  const validateForm = (): boolean => {
    return Object.keys(rules)
      .map(field => validateField(field))
      .every(result => result)
  }

  const resetValidation = () => {
    errors.value = Object.keys(rules).reduce((acc, key) => ({ ...acc, [key]: '' }), {})
  }

  return {
    errors,
    validateField,
    validateForm,
    resetValidation
  }
}
