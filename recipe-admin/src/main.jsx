import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import { BrowserRouter as Router } from 'react-router-dom'
import GlobalStyles from './components/GlobalStyles/GlobalStyles.jsx'

createRoot(document.getElementById('root')).render(
  <Router>
    <GlobalStyles >
      <App />
    </GlobalStyles>
  </Router>
)
