"use client";

import { useState } from "react";

const ErrorSimulator = ({
  message = "An error occurred",
}: {
  message?: string;
}) => {
  const [error, setError] = useState(false);

  if (error) {
    throw new Error(message);
  }

  return (
    <button
      title="Simulate an error"
      className="bg-red-950 p-1 text-sm font-semibold leading-none text-red-500"
      onClick={() => setError(true)}
    >
      Simulate Error
    </button>
  );
};

type WrapperProps = {
  children: React.ReactNode;
};

const ErrorWrapper = ({ children }: WrapperProps) => {
  return (
    <div className="border-gray-300 relative mt-8 flex flex-col rounded-lg border p-4">
      <div className="absolute left-4 top-0 -translate-y-1/2">
        <ErrorSimulator message="Simulated error in root layout" />
      </div>
      {children}
    </div>
  );
};

export default ErrorWrapper;
