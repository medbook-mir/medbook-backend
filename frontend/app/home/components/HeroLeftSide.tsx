import { LocationIcon } from "@/app/_assets/icons/LocationIcon";
import { SearchIcon } from "@/app/_assets/icons/SearchIcon";

const title = "Online booking — the first step towards your health";
const description =
  "Hold incredible events, share knowledge, build and grow your product, create opportunity";

export const HeroLeftSide = () => {
  return (
    <div className="flex flex-col items-start justify-center w-full h-full gap-4">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white md:text-4xl">
        {title}
      </h1>
      <p className="text-lg text-gray-600 dark:text-gray-400">{description}</p>
      <div className="flex items-center w-full max-w-md gap-2 p-2 border border-gray-300 rounded-lg dark:border-gray-700">
        <SearchIcon />
        <input
          type="text"
          placeholder="Search for a doctor, clinic, or service"
          className="w-full bg-transparent outline-none"
        />
      </div>
      <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
        <LocationIcon />
        <span>Location</span>
      </div>
    </div>
  );
};
