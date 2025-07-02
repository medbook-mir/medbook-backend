import YandexMap from '@/components/shared/yandex-map'

const location = {
  id: 1,
  name: 'International Press Club of Uzbekistan',
  latitude: 41.3118066546201,
  longitude: 69.25474741848696
}

const Location = () => {
  return (
    <section className="rounded-[12px] bg-[#F2F7F6] p-5">
      <h3 className="mb-4 text-[16px] leading-[100%] font-bold">Map</h3>
      <YandexMap locations={[location]} width="310px" height="622px" />
    </section>
  )
}
export default Location
