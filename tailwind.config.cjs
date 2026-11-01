/* index.html'deki Tailwind sınıflarından assets/site.css üretilir: npm run build */
module.exports = {
  content: ['./index.html'],
  /* ürün etiket renkleri urunler.json'dan (yönetim paneli) gelir */
  safelist: ['bg-blush', 'bg-peach', 'bg-lavender', 'bg-sage'],
  theme: {
    extend: {
      colors: {
        cream: '#FAF7F0', ink: '#292D29', forest: '#254D3A', forestDeep: '#18392B', line: '#E8E3D9',
        ok: '#287A50', warn: '#A96B15', bad: '#B83B3B', forestLight: '#686C65',
        blush: '#F3DCDA', blushDark: '#D8A0A0', rose: '#A9505F', sage: '#C9D5C2', sageDark: '#7E9A82',
        sageText: '#4E6B54', sageLight: '#EDF2E8', lavender: '#DCD5EE', lavenderDark: '#B3A6D9',
        peach: '#F1C7AC', peachDark: '#DFA37E'
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        serif: ['Playfair Display', 'serif'],
        script: ['Dancing Script', 'cursive']
      },
      boxShadow: {
        'soft': '0 10px 30px -8px rgba(37, 77, 58, 0.10)',
        'soft-lg': '0 24px 48px -12px rgba(37, 77, 58, 0.16)'
      }
    }
  }
};
