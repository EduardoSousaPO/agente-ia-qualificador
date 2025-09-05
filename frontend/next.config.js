/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configurações básicas e estáveis
  reactStrictMode: true,
  
  // Compilação otimizada apenas para produção
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
  
  // Webpack simplificado
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
      }
    }
    return config
  },
  
  // Compressão
  compress: true,
  
  // Otimizar imagens
  images: {
    formats: ['image/webp'],
    minimumCacheTTL: 60,
  },
}

module.exports = nextConfig