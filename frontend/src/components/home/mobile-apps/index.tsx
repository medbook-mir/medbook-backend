import { icons, images } from '@/assets'
import { Link } from '@/i18n/navigation'
import { Container } from '@/theme/container'
import Image from 'next/image'

const MobileApps = () => {
  return (
    <section className="bg-[#046D5F] py-20 text-white">
      <Container>
        <div className="flex flex-wrap items-center justify-between gap-12">
          <div data-aos="fade-right" className="flex max-w-[570px] flex-col gap-14">
            <div className="flex flex-col gap-5">
              <h2 className="text-[46px] leading-[60px] font-bold">Download App Now</h2>
              <p className="text-[16px] leading-6 font-normal">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Viverra nunc ante velit vitae. Est tellus
                vitae, nullam lobortis enim. Faucibus amet etiam tincidunt rhoncus, ullamcorper velit. Ullamcorper risus
                tempor, ac nunc libero urna, feugiat.
              </p>
            </div>
            <div className="flex gap-2">
              <Link href="https://play.google.com/store/" target="_blank" rel="noopener noreferrer">
                <Image src={icons.googlePlay} width={164} height={48} alt="Google play" />
              </Link>
              <Link href="https://apple.com/app-store/" target="_blank" rel="noopener noreferrer">
                <Image src={icons.appStore} width={164} height={48} alt="App store" />
              </Link>
            </div>
          </div>
          <div data-aos="fade-left" className="flex gap-6">
            <Image src={images.mobileScreenshot1} width={207} height={450} alt="Mobile screenshot 1" />
            <Image src={images.mobileScreenshot2} width={207} height={450} alt="Mobile screenshot 2" />
          </div>
        </div>
      </Container>
    </section>
  )
}
export default MobileApps
