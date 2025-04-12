# Child Emotion Tracker

A React-based web application for tracking and visualizing children's emotional patterns over time. This application helps parents and caregivers monitor and understand their child's emotional well-being through an intuitive interface.

## Features

- Interactive emotion tracking chart
- Daily emotion summaries
- Visual representation of emotional patterns
- Responsive design for all devices
- Easy-to-use interface

## Prerequisites

- Node.js (v14.0.0 or higher)
- npm (v6.0.0 or higher)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd emotion-tracker
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will be available at `http://localhost:3000`

## Project Structure

```
emotion-tracker/
├── src/
│   ├── components/
│   │   ├── EmotionChart.tsx
│   │   └── SummaryList.tsx
│   ├── utils/
│   │   └── dataLoader.ts
│   ├── styles/
│   │   └── global.css
│   ├── App.tsx
│   └── index.tsx
├── public/
├── package.json
└── README.md
```

## Usage

1. The application automatically loads and displays emotion data
2. The chart section shows the emotional patterns over time
3. The summary section provides daily breakdowns of emotions
4. Hover over data points to see detailed information

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
