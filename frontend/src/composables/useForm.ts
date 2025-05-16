import { ref } from 'vue'

type ValidationRule = (value: string) => string | boolean

interface FormField {
  value: string
  error: string
  rules?: ValidationRule[]
}

export function useForm<T extends Record<string, FormField>>(initialForm: T) {
  const form = ref<T>({ ...initialForm })

  const validateField = (fieldName: keyof T): boolean => {
    const field = form.value[fieldName]
    if (!field.rules) return true

    for (const rule of field.rules) {
      const result = rule(field.value)
      if (typeof result === 'string') {
        field.error = result
        return false
      }
    }

    field.error = ''
    return true
  }

  const validateForm = (): boolean => {
    return Object.keys(form.value)
      .map(key => validateField(key as keyof T))
      .every(result => result)
  }

  const resetForm = () => {
    Object.keys(form.value).forEach(key => {
      form.value[key as keyof T].value = initialForm[key as keyof T].value
      form.value[key as keyof T].error = ''
    })
  }

  return { form, validateField, validateForm, resetForm }
}
