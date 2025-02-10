import { Routes, Route } from 'react-router-dom'
import AdminPanel from './pages/AdminPanel'
// import Home from './Pages/Home/Home'
const theme = 'light-theme'
function App() {
  return (
    <div className={`App ${theme}`}>
      <Routes>
        <Route path='/' element={<AdminPanel />} />
      </Routes>
    </div>
  )
}

export default App
