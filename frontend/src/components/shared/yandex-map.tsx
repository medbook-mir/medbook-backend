'use client'

import { useEffect, useRef } from 'react'
import locationIcon from '@/assets/icons/location.svg'

interface Location {
  id: number
  name: string
  latitude: number
  longitude: number
}

const YandexMap = ({ locations, width, height }: { locations: Location[]; width: string; height: string }) => {
  const mapRef = useRef(null)

  useEffect(() => {
    const script = document.createElement('script')
    script.src = 'https://api-maps.yandex.ru/2.1/?apikey=YOUR_API_KEY&lang=ru_RU'
    script.type = 'text/javascript'
    script.onload = () => {
      window.ymaps.ready(() => {
        const map = new window.ymaps.Map(mapRef.current, {
          center: [41.311041, 69.254568],
          zoom: 16
        })

        locations.forEach((loc) => {
          const placemark = new window.ymaps.Placemark(
            [loc.latitude, loc.longitude],
            {
              balloonContent: `<strong>${loc.name}</strong>`
            },
            {
              iconLayout: 'default#image',
              iconImageHref: locationIcon,
              iconImageSize: [32, 32],
              iconImageOffset: [-16, -32]
            }
          )
          map.geoObjects.add(placemark)
        })
      })
    }
    document.body.appendChild(script)
  }, [locations])

  return <div ref={mapRef} style={{ width, height, borderRadius: '12px', border: '1px solid #CECECE' }} />
}

export default YandexMap
