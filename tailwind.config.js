module.exports = {
  content: ['./index.html', './archivio.html', './opere.html', './privacy.html', './src/**/*.js'],
  safelist: [
    'bg-terracotta-600','text-white','shadow-sm',
    'bg-stone-100','text-stone-600',
  ],
  theme: {
    extend: {
      colors: {
        terracotta: { 50:'#fdf8f6',100:'#fbeee9',500:'#c85a32',600:'#b2441d',700:'#943314',800:'#7a2b13' },
        sage: { 100:'#eef2ee',500:'#607d61',700:'#3a523b' },
        ambergold: { 400:'#fbbf24',500:'#f59e0b',600:'#d97706' },
        stonebg: '#fcfaf7',
      },
      fontFamily: { serif:['Playfair Display','serif'], sans:['Plus Jakarta Sans','sans-serif'] },
    },
  },
  plugins: [],
};
