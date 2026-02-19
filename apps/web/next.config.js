/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@dato/shared', '@dato/types', '@dato/ui', '@dato/agents', '@dato/database'],
  experimental: {
    typedRoutes: true,
  },
};

module.exports = nextConfig;
