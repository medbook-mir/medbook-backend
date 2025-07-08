import { setLocale } from 'yup'

setLocale({
  mixed: {
    required: 'This field is required',
    default: 'Invalid value',
    notType: 'Invalid value'
  }
})
