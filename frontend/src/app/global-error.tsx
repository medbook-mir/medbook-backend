'use client'

import './globals.css'

const GlobalError = () => {
  return (
    <html>
      <body>
        <div className="flex min-h-screen flex-col items-center justify-center">
          <h2 className="mb-4 text-2xl font-bold">Something went wrong</h2>
          <button
            onClick={() => window.location.reload()}
            className="rounded bg-green-500 px-4 py-2 font-bold text-white hover:bg-green-700"
          >
            Refresh
          </button>
        </div>
      </body>
    </html>
  )
}
export default GlobalError
