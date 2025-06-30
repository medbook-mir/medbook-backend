const Location = () => {
  return (
    <section className="rounded-[12px] bg-[#F2F7F6] p-5">
      <h3 className="mb-4 text-[16px] leading-[100%] font-bold">Map</h3>
      <iframe
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1384.425623099472!2d69.25474741848696!3d41.3118066546201!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x38ae8b107b1753e3%3A0x9b6e23504f448e8c!2sInternational%20Press%20Club%20of%20Uzbekistan!5e0!3m2!1sen!2s!4v1751299163765!5m2!1sen!2s"
        width="310"
        height="622"
        style={{ border: 0 }}
        allowFullScreen
        loading="lazy"
        referrerPolicy="no-referrer-when-downgrade"
        className="rounded-[12px] border border-[#CECECE]"
      ></iframe>
    </section>
  )
}
export default Location
