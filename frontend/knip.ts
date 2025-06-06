type KnipConfigType = {
  rules: Record<string, "warn" | "error" | "off">;
  ignoreDependencies?: string[];
};

const config: KnipConfigType = {
  rules: {
    dependencies: "warn",
    unlisted: "warn",
    binaries: "warn",
    unresolved: "warn",
    exports: "warn",
    nsExports: "warn",
    types: "warn",
    nsTypes: "warn",
    enumMembers: "warn",
    classMembers: "warn",
    duplicates: "warn",
    files: "warn",
  },
  ignoreDependencies: ["lint-staged"],
};

export default config;
