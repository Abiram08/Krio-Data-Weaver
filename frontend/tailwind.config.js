/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    50: '#FFF5F0',
                    100: '#FFE7DC',
                    200: '#FFCEB9',
                    300: '#FFB696',
                    400: '#E07A47',
                    500: '#C15F3C',
                    600: '#A34F31',
                    700: '#853F26',
                    800: '#672F1C',
                    900: '#4A2014',
                },
                secondary: {
                    50: '#FBF9F6',
                    100: '#F4F3EE',
                    200: '#F5E6D3',
                    300: '#E0D8C6',
                    400: '#CBCAB9',
                    500: '#B1ADA1',
                    600: '#8F8A7D',
                    700: '#6D6959',
                    800: '#4B4735',
                    900: '#2D2A26',
                }
            },
            animation: {
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            }
        },
    },
    plugins: [],
}
