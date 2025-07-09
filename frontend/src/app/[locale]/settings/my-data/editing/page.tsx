'use client'

import Image from 'next/image'
import { CameraIcon, ProfileAvatarIcon } from '@/utils/icons'
import { FilledButton } from '@/components/ui/filled-button'
import { Form, message, Upload } from 'antd'
import { Controller, SubmitHandler, useForm } from 'react-hook-form'
import DefaultInput from '@/components/ui/default-input'
import { useTranslations } from 'next-intl'
import { yupResolver } from '@hookform/resolvers/yup'
import myDataSchema, { MyDataType } from '@/schema/mydata-schema'
import { useRouter } from '@/i18n/navigation'
import { useState } from 'react'
import { RcFile, UploadChangeParam } from 'antd/es/upload'
import DatepickerInput from '@/components/ui/date-picker'
import dayjs from 'dayjs'

const mockMyData = {
  name: 'Shohrux Rahmatov',
  birthday: '27/08/2000',
  email: 'shohrux.rahmatov@gmail.com',
  phone: '+99890 002 6655',
  username: 'shohrux.rahmatov@gmail.com',
  photo: ''
}

const MyDataEditing = () => {
  const router = useRouter()
  const t = useTranslations('settingsLayout.myDataEditingPage')
  const { control, handleSubmit } = useForm<MyDataType>({
    resolver: yupResolver(myDataSchema),
    defaultValues: mockMyData,
    mode: 'onBlur'
  })

  const onSubmit: SubmitHandler<MyDataType> = (data) => {
    console.log(data)
    router.back()
  }

  const [imageUrl, setImageUrl] = useState<string | undefined>()
  const [loading, setLoading] = useState(false)

  const getBase64 = (file: RcFile): Promise<string> =>
    new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => resolve(reader.result as string)
      reader.onerror = (error) => reject(error)
    })

  const beforeUpload = (file: RcFile) => {
    const isImage = file.type.startsWith('image/')
    if (!isImage) {
      message.error('You can only upload image files!')
    }
    const isLt10M = file.size / 1024 / 1024 < 10
    if (!isLt10M) {
      message.error('Image must be smaller than 10MB!')
    }
    return isImage && isLt10M
  }

  const handleChange = async (info: UploadChangeParam) => {
    if (info.file.status === 'uploading') {
      setLoading(true)
      return
    }
    if (info.file.status === 'done') {
      const base64 = await getBase64(info.file.originFileObj as RcFile)
      setImageUrl(base64)
      setLoading(false)
      message.success('Avatar updated!')
    }
  }

  return (
    <Form layout="vertical" onFinish={handleSubmit(onSubmit)}>
      <div className="flex flex-col p-10">
        <div className="flex items-center justify-between border-b-2 border-[#E9ECF4] pb-5">
          <div className="flex items-center gap-8">
            <Upload
              name="avatar"
              showUploadList={false}
              customRequest={({ file, onSuccess }) => setTimeout(() => onSuccess && onSuccess('ok'), 500)}
              beforeUpload={beforeUpload}
              onChange={handleChange}
            >
              <button
                type="button"
                aria-label="Change profile picture"
                style={{ position: 'relative', cursor: 'pointer' }}
                disabled={loading}
              >
                {imageUrl || mockMyData?.photo ? (
                  <Image
                    src={imageUrl || mockMyData?.photo}
                    alt="profile photo"
                    width={120}
                    height={120}
                    className="!h-[120px] !w-[120px] rounded-full object-contain"
                  />
                ) : (
                  <ProfileAvatarIcon />
                )}
                <div className="absolute inset-0 right-0 bottom-0 flex h-full w-full items-center justify-center rounded-full bg-black/40 transition-all duration-300 hover:bg-black/60">
                  {loading ? (
                    <div className="h-6 w-6 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                  ) : (
                    <CameraIcon />
                  )}
                </div>
                {loading && (
                  <div className="absolute inset-0 flex items-center justify-center rounded-full bg-black/60">
                    <div className="h-8 w-8 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                  </div>
                )}
              </button>
            </Upload>

            <div className="flex flex-col gap-1">
              <h1 className="text-[24px] leading-8 font-semibold">{mockMyData?.name}</h1>
              <p className="text-[16px] leading-[18px] font-normal text-[#797979]">{t('customer')}</p>
            </div>
          </div>
          <FilledButton
            className="!w-auto !rounded-2xl !bg-[#F4F6F9] !px-16 !py-6 !leading-[18px] font-normal !text-[#264796]"
            onClick={() => router.back()}
          >
            {t('cancel')}
          </FilledButton>
        </div>
        <div className="grid grid-cols-2 items-center gap-x-16 gap-y-2 pt-6">
          <Controller
            name="name"
            control={control}
            render={({ field, fieldState: { error } }) => (
              <Form.Item label={t('name')} required validateStatus={error ? 'error' : ''} help={error?.message}>
                <DefaultInput {...field} autoComplete="name" placeholder={t('namePlaceholder')} />
              </Form.Item>
            )}
          />

          <Controller
            name="birthday"
            control={control}
            render={({ field, fieldState: { error } }) => (
              <Form.Item label={t('birthday')} required validateStatus={error ? 'error' : ''} help={error?.message}>
                <DatepickerInput
                  placeholder={t('birthdayPlaceholder')}
                  className="w-full"
                  format="DD/MM/YYYY"
                  value={field.value ? dayjs(field.value, 'DD/MM/YYYY') : null}
                  onChange={(date) => field.onChange(date?.format('DD/MM/YYYY'))}
                  status={error ? 'error' : ''}
                  required
                />
              </Form.Item>
            )}
          />

          <Controller
            name="phone"
            control={control}
            render={({ field, fieldState: { error } }) => (
              <Form.Item label={t('phone')} required validateStatus={error ? 'error' : ''} help={error?.message}>
                <DefaultInput {...field} autoComplete="phone" placeholder={t('phonePlaceholder')} />
              </Form.Item>
            )}
          />

          <Controller
            name="username"
            control={control}
            render={({ field, fieldState: { error } }) => (
              <Form.Item label={t('login')} required help={error?.message}>
                <DefaultInput
                  {...field}
                  autoComplete="username"
                  status={error ? 'error' : ''}
                  placeholder={t('usernamePlaceholder')}
                />
              </Form.Item>
            )}
          />

          <Controller
            name="email"
            control={control}
            render={({ field, fieldState: { error } }) => (
              <Form.Item label={t('email')} required validateStatus={error ? 'error' : ''} help={error?.message}>
                <DefaultInput {...field} autoComplete="email" placeholder={t('emailPlaceholder')} />
              </Form.Item>
            )}
          />

          <FilledButton className="!py-5" htmlType="submit">
            {t('save')}
          </FilledButton>
        </div>
      </div>
    </Form>
  )
}
export default MyDataEditing
